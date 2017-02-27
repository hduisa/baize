#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    core.spider_loader
    ~~~~~~~~~~~~~~~~~~

    spider loader.
    For load spider dynamically.

    :author:    lightless <root@lightless.me>
    :homepage:  https://github.com/LiGhT1EsS/baize
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

import os

from utils import logger


class SpiderLoader(object):
    """
    爬虫加载类
    """
    # todo: 动态加载爬虫，当爬虫发生修改时，reload it!

    def __init__(self):
        super(SpiderLoader, self).__init__()

        # 存储所有的爬虫类
        # {'spider_filename': Class}
        self.spider_dict = dict()

        # 获取存储爬虫的目录
        self.spiders_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spiders")

    def load_all(self):
        logger.debug(self.spiders_path)
        all_spider_files = os.listdir(self.spiders_path)
        for spider_file in all_spider_files:
            logger.debug("Find file {0}".format(spider_file))

            # 略过所有以双下划线开头的文件
            if spider_file.startswith("__"):
                logger.debug("Jumping file {0}".format(spider_file))
                continue

            # spider_name = spider_file.split(".")[0].replace("_", " ").title().replace(" ", "")
            name = spider_file.split(".")[0]
            logger.info("Try to load spider in {0}".format(spider_file))

            # from core.spiders import rss_spider
            # rss_spider.get_class()
            spider_class = __import__("core.spiders", fromlist=[name])
            spider_real_class = getattr(spider_class, str(name)).get_class()
            logger.debug("Get spider class: {0}".format(spider_real_class))
            self.spider_dict[spider_file] = spider_real_class

    def load_one(self, spider_filename):
        """
        根据文件名加载一个爬虫
        :param spider_filename: String
        :return:
        """
        logger.info("Start Loading Spider {0}".format(spider_filename))

        # 如果已经加载过了，直接返回
        if spider_filename in self.spider_dict.keys():
            return self.spider_dict[spider_filename]

        try:
            name = spider_filename.split(".")[0]
            temp_package = __import__("core.spiders", fromlist=[name])
            spider_real_class = getattr(temp_package, str(name)).get_class()
            self.spider_dict[spider_filename] = spider_real_class
            return self.spider_dict[spider_filename]
        except Exception as e:
            # todo: 把Exception换掉
            logger.warning("Error when loading spider: {0}".format(spider_filename))
            logger.warning(e)
