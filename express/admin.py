# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.http import HttpResponse
from django.http import StreamingHttpResponse

import os
import csv
from datetime import datetime
from django.contrib.auth.models import User
from express.utils import file_iter, data_iter
from express.models import Express, ExpressArchive


class Echo(object):
    def write(self, value):
        return value


class ExpressAdmin(admin.ModelAdmin):
    search_fields = ('=number', '=status', '=follower__username')
    show_full_result_count = False
    list_display = (
        'number', 'orig', 'start_time', 'status',
        'follower', 'detail', 'detail_time',
        'error_type', 'progess', 'progess_time', 'resaon'
    )
    list_display_links = (
        'number', 'orig', 'status', 'detail', 'follower',
        'error_type', 'progess', 'resaon'
    )
    list_per_page = 100
    list_filter = (
        'follower', 'status', 'orig', 'detail_time', 'progess_time'
    )
    fieldsets = [
        ('基本信息', {'fields': ['number', 'orig', 'status']}),
        ('业务信息', {'fields': ['follower', 'detail']}),
        ('业务详情', {'fields': ['error_type', 'progess', 'resaon']}),
        (None, {'fields': ['end_time']}),
    ]
    exclude = ['priority']
    actions = ['export_data']
    date_hierarchy = 'start_time'

    def save_model(self, request, obj, form, change):
        post_dic = form.cleaned_data
        detail = post_dic.get('detail')
        for key,value in post_dic.iteritems():
            setattr(obj, key, value)
        if detail:
            setattr(obj, 'priority', 1)
        obj.save()

    def get_queryset(self, request):
        qs = super(ExpressAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.has_perm('express.change_detail'):
            orig = User.objects.get(username=request.user).first_name
            return Express.objects.filter(orig=orig)
        else:
            user = User.objects.get(username=request.user)
            return user.express_set.all()

    def get_readonly_fields(self, request, obj):
        permes = request.user.get_all_permissions()
        read_only_fields = ()
        if request.user.is_superuser:
            return ()
        if 'express.change_detail' in permes:
            read_only_fields = (
                'number', 'orig', 'start_time', 'status', 'end_time',
                'follower', 'error_type', 'progess', 'resaon'
            )
        if 'express.change_follower' in permes:
            read_only_fields = (
                'number', 'orig', 'follower', 'start_time', 'detail'
            )
        return read_only_fields

    def export_data(self, request, queryset):
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        response = StreamingHttpResponse(
            (writer.writerow(datas) for datas in data_iter(queryset)),
            content_type="text/csv"
        )
        response['Content-Type'] = 'application/octest-stream'
        response['Content-Disposition'] = 'attachment;filename="data.csv"' 
        return response
    export_data.short_description = '导出选中数据'


class ExpressArchiveAdmin(admin.ModelAdmin):
    search_fields = ('=number',)
    show_full_result_count = False
    fieldsets = [
        ('完结基本信息', {'fields':[
                                    'number', 'orig', 'start_time', 'status',
                                     'follower', 'detail', 'end_time'
                                   ]
                         }
        ),
        ('客户留言信息', {'fields':['message', 'msg_time']})
    ]
    list_display = (
        'number', 'orig', 'start_time', 'status',
        'follower', 'detail', 'end_time', 'message', 'msg_time'
    )
    list_filter = ('follower', 'status', 'orig')
    actions = ['export_data']

    def save_model(self, request, obj, form, change):
        user = request.user
        if change:
            if user.has_perm('express.change_msg'):
                obj.message = form.cleaned_data.get('message')
                obj.save()
            if user.has_perm('express.change_time'):
                obj.msg_time = form.cleaned_data.get('msg_time')
                obj.save()
        else:
            return None

    def get_readonly_fields(self, request, obj):
        reads = self.list_display
        if request.user.is_superuser:
            reads = ['number', 'orig', 'start_time', 'end_time']
        elif request.user.has_perm('express.change_time'):
            reads = [
              'number', 'orig', 'start_time', 'status', 
              'detail', 'error_type', 'progess', 'resaon',
              'end_time','follower', 'message'
            ]
        elif request.user.has_perm('express.change_msg'):
            reads = [
              'number', 'orig', 'start_time', 'status',
               'detail','error_type', 'progess', 'resaon', 
               'end_time', 'follower', 'msg_time'
            ]
        return reads

    def export_data(self, request, queryset):
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        response = StreamingHttpResponse(
            (writer.writerow(datas) for datas in data_iter(queryset)),
            content_type="text/csv"
        )
        response['Content-Type'] = 'application/octest-stream'
        response['Content-Disposition'] = 'attachment;filename="data.csv"' 
        return response
    export_data.short_description = '导出选中数据'


admin.site.register(Express, ExpressAdmin)
admin.site.register(ExpressArchive, ExpressArchiveAdmin)
admin.site.site_hader = 'ANE'
admin.site.site_title = 'ANE EXPRESS'
