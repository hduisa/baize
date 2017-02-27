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

import requests
import feedparser

from utils import logger


class RssSpider(object):

    def __init__(self, task):
        """
        Rss Spider
        :param task: namedtuple(title,url,source_type,source_id,spider_id)
        """
        self._task = task
        self.use_proxy = task.use_proxy
        self._default_proxy = {
            "http": "socks5://127.0.0.1:9050",
            "https": "socks5://127.0.0.1:9050",
        }

    def run(self):
        logger.debug(self._task)
        logger.debug("RssSpider Starting")
        url = self._task.url

        if self.use_proxy != 0:
            r = requests.get(url, proxies=self._default_proxy)
        else:
            r = requests.get(url)

        logger.debug(r.content)


def get_class():
    return RssSpider
