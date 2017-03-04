#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    apps.show.controller.show
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Main show controller.

    :author:    lightless <root@lightless.me>
    :homepage:  https://github.com/LiGhT1EsS/baize
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

from django.views import View
from django.shortcuts import render

from apps.db.models import BzArticles, BzSource


class ShowIndex(View):

    @staticmethod
    def get(request):

        articles = BzArticles.objects.filter(is_deleted=0).all()[:10]
        rss_source = BzSource.objects.filter(is_deleted=0).all()

        context = {
            "articles": articles,
            "rss_sources": rss_source,
        }
        return render(request, "shows/show.html", context=context)

