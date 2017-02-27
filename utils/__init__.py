#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    utils
    ~~~~~

    utils package.

    :author:    lightless <root@lightless.me>
    :homepage:  https://github.com/LiGhT1EsS/baize
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

from collections import namedtuple


from utils.log_helper import logger
from utils.validate_params import ValidateParams
from utils.random_string import make_random_string
from utils.share_memory import share_memory


SpiderTask = namedtuple("SpiderTask", "title url source_type source_id spider_id use_proxy")

__all__ = ["logger", "ValidateParams", "make_random_string", "share_memory", "SpiderTask"]
