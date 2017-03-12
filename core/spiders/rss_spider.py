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

import time
import datetime

import requests
import feedparser

from utils import logger
from core.base_spider import BaseSpider
from apps.db.models import BzArticles, BzSource


class RssSpider(BaseSpider):

    def __init__(self, task):
        super(RssSpider, self).__init__(task)

    def run(self):
        html = self.http_request()
        feed = self.parse_rss(html)
        for f in feed:
            self.save(f)
        self.update_refresh_time()


def get_class():
    return RssSpider

