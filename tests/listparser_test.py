#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    listparser_test
    ~~~~~~~~~~~~~~~

    Rss system models. Including RSS sources and RSS news.

    :author:    lightless <root@lightless.me>
    :homepage:  https://github.com/LiGhT1EsS/baize
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

from utils import parser_opml

f = open("feedly.opml", "r", encoding="utf-8")
raw_opml = f.read()
f.close()

x = parser_opml(raw_opml)
print(x["blog"])
