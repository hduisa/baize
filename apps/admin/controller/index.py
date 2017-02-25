#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    apps.admin.controller.index
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    admin index controller.

    :author:    lightless <root@lightless.me>
    :homepage:  https://github.com/LiGhT1EsS/baize
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

from django.views import View
from django.shortcuts import render


class IndexView(View):

    @staticmethod
    def get(request):
        return render(request, "admin/index.html")

