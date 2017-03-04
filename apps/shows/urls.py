#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    apps.shows.urls
    ~~~~~~~~~~~~~~~

    The shows app's router

    :author:    lightless <root@lightless.me>
    :homepage:  https://github.com/LiGhT1EsS/baize
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

from django.conf.urls import url

from apps.shows.controller import show, api

urlpatterns = [
    url(r"^index$", show.ShowIndex.as_view(), name="show_index"),
    url(r"^api/like$", api.LikeApiView.as_view(), name="show_api_like"),
]