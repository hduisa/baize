#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    core.spider_engine
    ~~~~~~~~~~~~~~~~~~

    The CORE spider engine.
    Threading Pool and RSS spider.

    :author:    lightless <root@lightless.me>
    :homepage:  https://github.com/LiGhT1EsS/baize
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

import queue
import threading
import time
import datetime

from utils import logger, SpiderTask
from apps.db.models import BzSource, BzSpiders
from core.spider_loader import SpiderLoader


class SpiderEngine(object):
    """
    Spider engine.
    主要的线程池分发和RSS爬虫
    """

    def __init__(self):

        # 存储任务的队列
        """
        任务的格式
        namedtuple(title, url, source_type, source_id)
        """
        self._task_queue = queue.Queue()

        # 存储当前正在运行的线程的列表
        self._working_thread_list = list()

        # 当前正在运行的任务数量
        # 不要使用len(self._working_thread_list)来取，因为里面会有死亡的线程
        self._working_thread_num = 0

        # 线程池大小
        self._max_pool_size = 10

        # 线程池退出标志
        self._exited = False

        # 分发线程
        self.main_loop_thread = threading.Thread(target=self._loop, name="SpiderEngineMainLoop")
        self.main_loop_thread.start()

        # 定期检查源是否需要刷新
        self.refresh_thread = threading.Thread(target=self._refresh, name="RefreshCheckLoop")
        self.refresh_thread.start()

        # 加载爬虫
        self.spider_loader = SpiderLoader()

    def stop(self):
        """
        结束spider engine
        :return: None
        """
        self._exited = True
        logger.info("停止任务已下发，等待线程池退出")

    def _update_thread_list(self):
        """
        更新线程计数，从列表中移除死亡线程
        :return: Integer, 最新的线程数量
        """
        working = 0
        for thread in self._working_thread_list:
            if thread.isAlive():
                working += 1
            else:
                self._working_thread_list.remove(thread)
                logger.debug("从列表中移除死亡线程: {0}".format(thread.name))
        self._working_thread_num = working
        return working

    def add_one_task(self, task):
        """
        向任务队列中添加任务
        :param task: tuple，任务信息
        :return: Boolean
        """
        if not isinstance(task, SpiderTask):
            logger.warning("错误的任务格式")
            return False
        self._task_queue.put(task)
        logger.debug("已添加任务'{0}', 等待任务轮询".format(task.title))

    def add_tasks(self, tasks=None):
        """
        添加多个任务，列表形式传递
        :param tasks: list，需要添加的多个任务
        :return: Boolean/Integer
        """
        success_count = 0

        if not isinstance(tasks, list):
            logger.warning("错误的任务格式")
            return False
        for t in tasks:
            if self.add_one_task(t):
                success_count += 1
        return success_count

    def _refresh(self):
        """
        循环检查RSS源是否需要刷新
        :return: None
        """

        while not self._exited:

            time.sleep(5)

            logger.debug("开始检查上次刷新时间")

            source_qs = BzSource.objects.filter(is_deleted=0).all()
            current_time = datetime.datetime.now()
            current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
            logger.debug("Current Time: {0}".format(current_time_str))
            for each_source in source_qs:
                last_time = each_source.last_refresh_time
                freq = each_source.refresh_freq
                logger.debug("{2}上次刷新时间为: {0}， 下次刷新时间为: {1}".format(
                    last_time, last_time + datetime.timedelta(minutes=freq), each_source.title
                ))

                if last_time + datetime.timedelta(minutes=freq) < current_time:
                    self.add_one_task(
                        SpiderTask(
                            title=each_source.title, url=each_source.url,
                            source_id=each_source.id, source_type=each_source.source_type,
                            spider_id=each_source.spider_id, use_proxy=each_source.proxy
                        )
                    )

        logger.info("SpiderEngine 刷新检查线程退出")

    def _loop(self):
        """
        线程池的死循环函数
        :return:
        """

        logger.info("SpiderEngine启动...")

        while not self._exited:
            # time.sleep(1)

            # 更新线程计数以及从列表中删除死亡线程
            self._update_thread_list()

            # 查看当前是否有任务
            if self._task_queue.empty():
                logger.debug("任务队列为空, 当前运行任务数: {0}".format(self._working_thread_num))
                time.sleep(1)
                continue

            # 查看是否有空闲的位置
            if self._working_thread_num >= self._max_pool_size:
                logger.debug("线程池已满")
                time.sleep(1)
                continue

            # 获取任务并运行
            task = self._task_queue.get_nowait()

            # 获取任务的爬虫信息
            spider_id = task.spider_id
            spider_qs = BzSpiders.objects.filter(id=spider_id).first()
            if not spider_qs:
                logger.error("Invalid SpiderTask, No such spider. Task info: {0}".format(task))
                time.sleep(1)
                continue

            # 根据爬虫信息，import进相应的爬虫并实例化
            spider_filename = spider_qs.spider_filename
            spider_class = self.spider_loader.load_one(spider_filename)
            spider_instance = spider_class(task)

            # 生成线程名称
            thread_name = spider_filename.split(".")[0] + "_" + task.title

            # 生成工作线程
            task_thread = threading.Thread(target=spider_instance.run, name=thread_name)
            task_thread.start()
            self._working_thread_list.append(task_thread)

            # 更新这个任务的最后一次刷新时间
            qs = BzSource.objects.filter(id=task.source_id).first()
            qs.last_refresh_time = datetime.datetime.now()
            qs.save()

        logger.info("SpiderEngine 主循环线程退出")



