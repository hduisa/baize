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

from django.views import View
from django.shortcuts import render

from utils import parser_opml, logger


class ImportOPMLView(View):

    @staticmethod
    def get(request):
        return render(request, "admin/import_from_opml.html")

    @staticmethod
    def post(request):
        opml_file = request.FILES.get("opml-file", None)
        logger.debug(opml_file)
        logger.debug(request.FILES)
        raw_opml = ""
        for chunk in opml_file.chunks():
            raw_opml += str(chunk)
        logger.debug(raw_opml)

