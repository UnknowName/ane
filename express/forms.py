#!/bin/env python
# coding:utf8

from django import forms
from django.forms import widgets


class FileForm(forms.Form):
    TYPES = (
      ('import', '导入数据'),
      ('follower', '批量修改跟单人员'),
      ('status', '批量修改状态'),
    )
    filename = forms.FileField(label='上传')
    op_type = forms.ChoiceField(choices=TYPES, label='操作类型')


class LoginForm(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(label='password', widget=widgets.PasswordInput())
