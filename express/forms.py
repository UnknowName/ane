#!/bin/env python
# coding:utf8

from django import forms


class ImportForm(forms.Form):
    filename = forms.FileField(lable='上传')
