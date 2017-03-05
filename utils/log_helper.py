#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    utils.log_helper
    ~~~~~~~~~~~~~~~~

    Log module.

    :author:    lightless <root@lightless.me>
    :homepage:  https://github.com/LiGhT1EsS/baize
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

import os
import logging
import logging.handlers

import colorlog


t = os.path.dirname(os.path.abspath(__file__))
t = os.path.join(t, "../logs/baize.log")
log_filename = t
handler = colorlog.StreamHandler()
handler.setFormatter(
    colorlog.ColoredFormatter(
        fmt='%(log_color)s[%(levelname)s] [%(threadName)s] [%(asctime)s] [%(filename)s:%(lineno)d] %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
    )
)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel("DEBUG")

file_handler = logging.handlers.TimedRotatingFileHandler(log_filename, when="midnight", backupCount=30)
file_formatter = logging.Formatter(
    fmt='[%(levelname)s] [%(threadName)s] [%(asctime)s] [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
