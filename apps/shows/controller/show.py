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

from apps.db.models import BzArticles, BzSource, BzSourceGroup


class ShowIndex(View):

    @staticmethod
    def get(request):

        articles = BzArticles.objects.filter(is_deleted=0).all()[:10]
        rss_source = BzSource.objects.filter(is_deleted=0).all()

        rss_result = dict()
        for each_rss in rss_source:

            # 获取group name
            gid = each_rss.group_id
            source_group_qs = BzSourceGroup.objects.filter(is_deleted=0, id=gid).first()
            if not source_group_qs:
                group_name = "NoGroup"
            else:
                group_name = source_group_qs.group_name

            # 添加到rss_result中
            if group_name in rss_result.keys():
                rss_result[group_name].append(each_rss)
            else:
                rss_result[group_name] = list()
                rss_result[group_name].append(each_rss)

        context = {
            "articles": articles,
            "rss_sources": rss_result,
        }
        return render(request, "shows/show.html", context=context)

