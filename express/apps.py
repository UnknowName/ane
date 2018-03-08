# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class ExpressConfig(AppConfig):
    name = 'express'
    verbose_name = '安能运单管理'


class AuthConfig(AppConfig):
    name = 'django.contrib.auth'
    verbose_name = '用户管理'
