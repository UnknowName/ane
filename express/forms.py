#!/bin/env python
# coding:utf8

from django import forms
from django.forms import widgets


class FileForm(forms.Form):
    filename = forms.FileField(label='上传')


class LoginForm(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(label='password', widget=widgets.PasswordInput())
