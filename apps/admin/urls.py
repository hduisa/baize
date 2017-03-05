#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    apps.admin.urls
    ~~~~~~~~~~~~~~~

    The admin app's router

    :author:    lightless <root@lightless.me>
    :homepage:  https://github.com/LiGhT1EsS/baize
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

from django.conf.urls import url

from apps.admin.controller import index, import_opml

urlpatterns = [
    url(r"^index$", index.IndexView.as_view(), name="admin_index"),

    # import from OPML file
    url(r"^import$", import_opml.ImportOPMLView.as_view(), name="admin_import"),
]