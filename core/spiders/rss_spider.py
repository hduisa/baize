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
from apps.db.models import BzArticles, BzSource


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

        # logger.debug(r.content)
        raw_feed = feedparser.parse(r.content)
        source_qs = BzSource.objects.filter(id=self._task.source_id).first()
        if not source_qs:
            logger.warning("Wrong source information.")

        for feed in raw_feed.get("entries"):
            title = feed.get("title")
            link = feed.get("link")
            try:
                content = feed.get("content", "")[0].get("value", "")
            except IndexError:
                content = feed.get("summary", "")
            if content == "":
                content = link
            summary = feed.get("summary", "")
            if summary == "":
                summary = content[:512]
            else:
                summary = summary[:512]
            publish_time = feed.get("published_parsed")

            # 检查是否存在该文章了
            temp_qs = BzArticles.objects.filter(url=link).first()
            if temp_qs:
                logger.info("文章[{0}]已经存在".format(title))
                continue

            new_article = BzArticles()
            new_article.title = title
            new_article.url = link
            new_article.contents = content
            new_article.summary = summary
            new_article.publish_time = datetime.datetime.fromtimestamp(time.mktime(publish_time))
            new_article.source = source_qs
            new_article.save()
            logger.info("存储文章[{0}]成功".format(title))


def get_class():
    return RssSpider

