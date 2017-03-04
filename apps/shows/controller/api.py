#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    apps.show.controller.api
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Show controller's API.

    :author:    lightless <root@lightless.me>
    :homepage:  https://github.com/LiGhT1EsS/baize
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

from django.views import View
from django.http import JsonResponse

from apps.db.models import BzArticles, BzLikeLog


class LikeApiView(View):
    """
    赞或踩功能的API接口
    """

    @staticmethod
    def post(request):
        act = request.POST.get("act", "like")
        aid = request.POST.get("aid", "")
        if aid == "":
            return JsonResponse(dict(code=1005, message="Error"))
        article_qs = BzArticles.objects.filter(is_deleted=0, id=aid).first()
        if not article_qs:
            return JsonResponse(dict(code=1006, message="Error"))

        # 检查用户是否操作过这个文章
        log_qs = BzLikeLog.objects.filter(
            is_deleted=0, user_id=request.session["user_id"], article_id=aid
        ).first()
        if log_qs:
            return JsonResponse(dict(code=1007, message="请勿重复操作"))

        if act == "like":
            article_qs.likes += 1
            article_qs.save()
            log_qs = BzLikeLog(user_id=request.session["user_id"], article_id=aid, operate=1)
            log_qs.save()
            return JsonResponse(dict(code=1001, message="success"))

        elif act == "dislike":
            article_qs.dislike += 1
            article_qs.save()
            log_qs = BzLikeLog(user_id=request.session["user_id"], article_id=aid, operate=2)
            log_qs.save()
            return JsonResponse(dict(code=1001, message="success"))

        else:
            return JsonResponse(dict(code=1004, message="Error!"))



