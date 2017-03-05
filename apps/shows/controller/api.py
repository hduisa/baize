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

        # 获取参数
        act = request.POST.get("act", "like")
        aid = request.POST.get("aid", "")
        if aid == "":
            return JsonResponse(dict(code=1005, message="Error"))
        article_qs = BzArticles.objects.filter(is_deleted=0, id=aid).first()
        if not article_qs:
            return JsonResponse(dict(code=1006, message="Error"))

        user_id = request.session.get("user_id")
        log_qs = BzLikeLog.objects.filter(
            is_deleted=0, user_id=user_id, article_id=aid
        ).first()

        # 根据act参数判断操作类型
        if act == "like":

            if not log_qs:
                # 直接加一
                article_qs.likes += 1
                article_qs.save()
                # 点赞log
                qs = BzLikeLog(article_id=aid, user_id=user_id, operate=1)
                qs.save()
                return JsonResponse(dict(code=1001, message="操作成功"))
            else:
                if log_qs.operate == 1:
                    # 已经点过赞了，取消赞
                    log_qs.delete()
                    article_qs.likes -= 1
                    article_qs.save()
                    return JsonResponse(dict(code=1001, message="操作成功"))
                else:
                    # 不能同时点赞和踩
                    return JsonResponse(dict(code=1004, message="不能同时赞和踩"))

        elif act == "dislike":
            if not log_qs:
                article_qs.dislike += 1
                article_qs.save()
                qs = BzLikeLog(article_id=aid, user_id=user_id, operate=2)
                qs.save()
                return JsonResponse(dict(code=1001, message="操作成功"))
            else:
                if log_qs.operate == 2:
                    log_qs.delete()
                    article_qs.dislike -= 1
                    article_qs.save()
                    return JsonResponse(dict(code=1001, message="操作成功"))
                else:
                    # 不能同时点赞和踩
                    return JsonResponse(dict(code=1004, message="不能同时赞和踩"))
        else:
            return JsonResponse(dict(code=1004, message="Error!"))





