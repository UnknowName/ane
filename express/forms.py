#!/bin/env python
# coding:utf8

from django import forms


class FileForm(forms.Form):
    filename = forms.FileField(label='上传')
