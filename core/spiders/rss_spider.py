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


class RssSpider(object):

    def __init__(self, task):
        self._task = task

    def run(self):
        pass
