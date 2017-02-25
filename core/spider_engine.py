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

from utils import logger


class SpiderEngine(object):
    """
    Spider engine.
    主要的线程池分发和RSS爬虫
    """

    def __init__(self):

        # 存储任务的队列
        """
        任务的格式
        tuple()
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
        self.main_loop_thread = threading.Thread(target=self._run, name="SpiderEngineMainLoop")
        self.main_loop_thread.start()

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
        self._task_queue.put(task)

    def add_tasks(self, tasks=None):
        """
        添加多个任务，列表形式传递
        :param tasks: list，需要添加的多个任务
        :return: Boolean/Integer
        """
        success_count = 0

        if not isinstance(tasks, list):
            return False
        for t in tasks:
            if self.add_one_task(t):
                success_count += 1
        return success_count

    def _run(self):
        """
        线程池的死循环函数
        :return:
        """

        while self._exited:
            time.sleep(1)

            # 更新线程计数以及从列表中删除死亡线程
            self._update_thread_list()

            # 查看当前是否有任务
            if self._task_queue.empty():
                logger.debug("任务队列为空, 当前运行任务数: {0}".format(self._working_thread_num))
                continue

            # 查看是否有空闲的位置
            if self._working_thread_num >= self._max_pool_size:
                logger.debug("线程池已满")
                continue

            # 获取任务并运行
            task = self._task_queue.get_nowait()




