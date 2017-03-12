#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    core.base_spider
    ~~~~~~~~~~~~~~~~

    The base class for the all spiders.

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
from apps.db.models import BzSource, BzArticles


class BaseSpider(object):
    """
    The base class for all spiders.
    """

    def __init__(self, task):
        """
        :param task: namedtuple(title,url,source_type,source_id,spider_id)
        """
        super(BaseSpider, self).__init__()

        # spider task
        self._task = task

        # default proxy setting
        # todo: move this to config file.
        self._default_proxy_setting = {
            "http": "socks5://127.0.0.1:9050",
            "https": "socks5://127.0.0.1:9050",
        }

        # default UA setting
        # todo: move this to config file.
        self._user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
                           "(KHTML, like Gecko) Chrome/58.0.3010.0 Safari/537.36"

    def http_request(self, target_url=None):
        """
        Make a HTTP request.
        :param target_url: 待请求的URL，如果为None，则从task中取URL
        :return: String，网页内容
        """
        url = target_url if target_url is not None else self._task.url
        use_proxy = self._task.use_proxy
        headers = {
            'User-agent': self._user_agent,
        }

        if use_proxy:
            r = requests.get(url, proxies=self._default_proxy_setting, headers=headers)
        else:
            r = requests.get(url, headers=headers)

        return r.content

    def parse_rss(self, raw_rss):
        """
        解析RSS文章
        :param raw_rss: 待解析的原文
        :return: dict
        """

        result = list()
        raw_feed = feedparser.parse(raw_rss)

        # 检查source
        source_qs = BzSource.objects.filter(is_deleted=0, id=self._task.source_id).first()
        if not source_qs:
            return None

        # 开始解析
        entries = raw_feed.get("entries", "")
        if not entries:
            return None

        for entry in entries:
            title = entry.get("title")
            link = entry.get("link")

            try:
                content = entry.get("content", "")[0].get("value", "")
            except IndexError:
                content = entry.get("summary", "")

            summary = entry.get("summary", "")
            if not summary:
                summary = content[:512]
            else:
                summary = summary[:512]

            publish_time = entry.get("published_parsed")
            if not publish_time:
                publish_time = datetime.datetime.now()
            else:
                publish_time = datetime.datetime.fromtimestamp(time.mktime(publish_time))

            temp_dict = {
                "title": title,
                "url": link,
                "summary": summary,
                "contents": content,
                "publish_time": publish_time,
            }
            result.append(temp_dict)
        return result

    def update_refresh_time(self):
        """
        Update source last refresh time.
        :return: Boolean, True/False.
        """
        source_id = self._task.source_id
        source_qs = BzSource.objects.filter(is_deleted=0, id=source_id).first()
        if not source_qs:
            return False
        else:
            source_qs.last_refresh_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            source_qs.save()
            return True

    def save(self, article_obj):
        # todo: change it to thread pool
        """
        Save data to database.
        Auto format the articles.
        :param article_obj: article dict
        obj = {
            "title": None,
            "url": None,
            "contents": contents,
            "summary": summary,
            "publish_time": "",
        }
        :rtype: bool
        :return: Boolean
        """

        # 检查title
        title = article_obj.get("title", "")
        if not title:
            title = "[{t}]No Title Article".format(t=str(int(time.time())))

        # 检查url
        url = article_obj.get("url")
        if not url:
            logger.warning("存储文章[{0}]失败，原因：文章URL不正确".format(title))
            return False

        # 检查contents
        contents = article_obj.get("contents", "")
        if not contents:
            contents = url

        # 检查summary
        summary = article_obj.get("summary", "")
        if not summary:
            summary = contents[:512]

        # 检查publish time
        publish_time = article_obj.get("publish_time", "")
        if not publish_time:
            publish_time = datetime.datetime.now()

        # 检查source
        sid = self._task.source_id
        if not sid:
            return False
        source_qs = BzSource.objects.filter(is_deleted=0, id=sid).first()
        if not source_qs:
            logger.warning("存储文章[{0}]失败，原因：RSS源不存在".format(title))
            return False

        # 检查是否已经存在了
        temp_qs = BzArticles.objects.filter(is_deleted=0, title=title).first()
        if temp_qs:
            return True

        new_article = BzArticles(
            title=title, url=url, contents=contents, summary=summary,
            publish_time=publish_time, source=source_qs
        )
        new_article.save()
        logger.info("存储文章[{0}]成功".format(title))
