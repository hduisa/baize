#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    tests
    ~~~~~

    Rss system models. Including RSS sources and RSS news.

    :author:    lightless <root@lightless.me>
    :homepage:  https://github.com/LiGhT1EsS/baize
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

import requests
import feedparser


if __name__ == '__main__':

    url = "https://lightless.me/feed"
    content = requests.get(url).content
    raw_feed = feedparser.parse(content)
    print(raw_feed)
    for feed in raw_feed.get("entries"):
        title = feed.get("title")
        link = feed.get("link")
        summary = feed.get("summary")
        content = feed.get("content")
        publish_time = feed.get("published_parsed")

