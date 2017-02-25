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


class ShowIndex(View):

    @staticmethod
    def get(request):
        return render(request, "shows/show.html")

