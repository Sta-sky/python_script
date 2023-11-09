#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/10/13 14:49
# @Author  : bruce@laien.io
# @File    : urls.py.py
# @Description
from django.urls import path, include

from user.views import get_user, create_user

urlpatterns = [
    path(r'get_user', get_user),
    path(r'create_user', create_user)
]
