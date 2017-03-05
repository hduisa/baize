#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    apps.db.models
    ~~~~~~~~~~~~~~

    The whole project's model.

    :author:    lightless <root@lightless.me>
    :homepage:  https://github.com/LiGhT1EsS/baize
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

import datetime

from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class BzUser(models.Model):
    """
    Store user's basic information.
    """

    class Meta:
        db_table = "bz_user"

    username = models.CharField(max_length=32, null=False, blank=False, unique=True)
    email = models.EmailField(null=False, blank=False, unique=True)
    password = models.CharField(max_length=256, null=False, blank=False)
    token = models.CharField(max_length=32, null=False, blank=False, unique=True)

    # user status
    # 1: not active, 2: normal user, 3: banned user
    status = models.PositiveSmallIntegerField(default=1, blank=False, null=False, db_index=True)

    # user's role
    # 1: guest: can only view all news.
    # 2: member: can like or unlike the news.
    # 3: shows manager: can view admin panel. can add/del/edit shows source or import opml file.
    # 4-9: Reserved.
    # 10: master: can do anything.
    role = models.PositiveSmallIntegerField(default=1, blank=False, null=False)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return "<BzUser {user_id} - {username} - {status} - {role}>".format(
            user_id=self.id, username=self.username, status=self.get_status(),
            role=self.role
        )

    def get_status(self):
        """
        get user status by status code.
        :return: unicode
        """
        status_dict = {
            1: "未激活",
            2: "正常",
            3: "禁止登陆",
        }
        try:
            return status_dict[self.status]
        except KeyError:
            return "未知状态"

    def set_password(self, password):
        self.password = make_password(password)

    def check_password(self, password):
        return check_password(password, self.password)


class BzUserLoginLog(models.Model):
    """
    Store user's login log.
    Include IP and Time
    """

    class Meta:
        db_table = "bz_user_login_log"

    ip = models.CharField(max_length=16, null=False, blank=True, default="0.0.0.0")
    login_time = models.DateTimeField(null=False, blank=True, default="")

    user = models.ForeignKey(BzUser, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return "<BzUserLoginLog {username} - {ip} - {login_time}>".format(
            username=self.user.username,
            ip=self.ip,
            login_time=self.login_time.strftime("%Y-%m-%d %H:%M:%S")
        )


class BzActiveCode(models.Model):
    """
    Store all active code, or invite code.
    """

    class Meta:
        db_table = "bz_active_code"

    user_id = models.BigIntegerField(null=False, blank=False, default=0)
    code = models.CharField(max_length=32, null=False, blank=True, default="")
    used_time = models.DateTimeField(auto_now_add=True)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def use_code(self, user_id=None):
        """
        Use this active code for user_id
        :param user_id: Integer
        :return: Boolean
        """
        if user_id:
            self.user_id = user_id
            self.used_time = datetime.datetime.now()
            return True
        else:
            return False

    def __str__(self):
        return "<BzActiveCode {code} - {status}>".format(
            code=self.code, status=self.get_status()
        )

    def get_status(self):
        """
        Get if this code already be used.
        :return: unicode
        """
        if self.user_id == 0:
            return "未使用"
        else:
            return "已使用"


class BzSourceGroup(models.Model):
    """
    存储RSS分组的信息
    """

    class Meta:
        db_table = "bz_source_group"

    group_name = models.CharField(max_length=64, db_index=True, default="")
    group_desc = models.CharField(max_length=256, default="")

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return "<BzSourceGroup {name}>".format(name=self.group_name)


class BzSource(models.Model):

    class Meta:
        db_table = "bz_source"

    title = models.CharField(max_length=128, unique=True)
    url = models.CharField(max_length=256)

    # Source type. default is RSS
    # Maybe it's will support more source like WEB spiders in the future.
    # 1: RSS
    source_type = models.SmallIntegerField(default=1)

    # spider id
    # indicate which spider to use
    spider_id = models.IntegerField(default=0)

    proxy = models.IntegerField(default=0)

    # the frequency of the source's refresh.
    # default 30 min.
    refresh_freq = models.IntegerField(default=30)
    last_refresh_time = models.DateTimeField(default=datetime.datetime.now)
    author = models.CharField(max_length=64, unique=True)
    group_id = models.IntegerField(default=0)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return "<BzSource - {title}>".format(title=self.title)

    def update_last_refresh_time(self, refresh_time):
        self.last_refresh_time = refresh_time


class BzArticles(models.Model):

    class Meta:
        db_table = "bz_articles"

    title = models.CharField(max_length=512)
    url = models.CharField(max_length=256)
    summary = models.CharField(max_length=512, default="")
    contents = models.TextField()
    likes = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    publish_time = models.DateTimeField(default=datetime.datetime.now)
    source = models.ForeignKey(BzSource, on_delete=models.CASCADE)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return "<BzArticle {title} - {likes}>".format(
            title=self.title, likes=self.likes,
        )

    def like(self):
        self.likes += 1

    def unlike(self):
        self.likes -= 1


class BzLikeLog(models.Model):

    class Meta:
        db_table = "bz_like_log"

    article_id = models.BigIntegerField(db_index=True)
    user_id = models.BigIntegerField(db_index=True)

    # like or unlike
    # 1: like
    # 2: unlike
    operate = models.SmallIntegerField()

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def get_operate(self):
        if self.operate == 1:
            return "like"
        elif self.operate == 2:
            return "unlike"
        else:
            return "unknown"

    def __str__(self):
        return "<BzLikeLog {aid} - {op}>".format(
            aid=self.article_id, op=self.get_operate()
        )


class BzSpiders(models.Model):

    class Meta:
        db_table = "bz_spiders"

    spider_name = models.CharField(max_length=64, db_index=True)
    spider_filename = models.CharField(max_length=255)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return "<BzSpiders {sn}>".format(sn=self.spider_name)
