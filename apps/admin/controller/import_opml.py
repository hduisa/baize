#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    apps.admin.controller.index
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Import RSS source from OPML file.

    :author:    lightless <root@lightless.me>
    :homepage:  https://github.com/LiGhT1EsS/baize
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

from tempfile import TemporaryFile

from django.views import View
from django.http import JsonResponse
from django.shortcuts import render

from utils import parser_opml, logger
from apps.db.models import BzSourceGroup, BzSource


class ImportOPMLView(View):

    @staticmethod
    def get(request):
        return render(request, "admin/import_from_opml.html")

    @staticmethod
    def post(request):
        opml_file = request.FILES.get("opml-file", None)

        raw_opml = ""
        for chunk in opml_file.chunks():
            raw_opml += chunk.decode("utf-8")

        with TemporaryFile("w+t") as ff:
            ff.write(raw_opml)
            ff.seek(0)
            result = parser_opml(ff)

        import_sum = 0
        exist_sum = 0

        # 导入所有的源
        for key, value in result.items():
            group_name = key

            # 检查分组是否已经存在
            qs = BzSourceGroup.objects.filter(group_name=group_name).first()
            if qs:
                # 存在，取出分组id
                group_id = qs.id
            else:
                # 不存在，插入新的分组并取出分组id
                source_group = BzSourceGroup(group_name=group_name, group_desc=group_name)
                source_group.save()
                group_id = source_group.id

            for s in value:
                # 检查这个RSS源是否存在
                qs = BzSource.objects.filter(url=s.get("url"))
                if qs:
                    exist_sum += 1
                    continue
                else:
                    source = BzSource(title=s.get("title"), url=s.get("url"), spider_id=1, group_id=group_id)
                    source.save()
                    import_sum += 1

        return JsonResponse(dict(code=1001, message="导入成功，已存在{0}个源，导入{1}个源".format(exist_sum, import_sum)))






