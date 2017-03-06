#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    utils.parser_opml
    ~~~~~~~~~~~~~~~~~

    Parser OPML file.

    :author:    lightless <root@lightless.me>
    :homepage:  https://github.com/LiGhT1EsS/baize
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

import listparser

from utils import logger


def parser_opml(handler):
    result = listparser.parse(handler)
    logger.debug(result)
    source = dict()

    for feed in result.feeds:
        group = feed.categories
        for g in group:
            if g[0].lower() == "must read":
                continue
            else:
                group = g[0]
        # print(group)
        if group not in source.keys():
            source[group] = list()

        source[group].append(dict(title=feed.title, url=feed.url))

    return source


