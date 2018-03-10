#!/bin/env python
# coding:utf8


from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger


def split_page(request, lst):
    paginator = Paginator(lst, 50)
    page = request.GET.get('page')
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_page)
    return numbers
