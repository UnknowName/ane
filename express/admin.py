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
    list_per_page = 50
    list_filter = (
        'follower', 'status', 'orig', 'start_time',
        'detail_time', 'progess_time'
    )
    fieldsets = [
        ('基本信息', {'fields': ['number', 'orig', 'status']}),
        ('业务信息', {'fields': ['follower', 'detail']}),
        ('业务详情', {'fields': ['error_type', 'progess', 'resaon']}),
        (None, {'fields': ['end_time']}),
    ]
    exclude = ['priority']
    actions = ['export_data']

    def save_model(self, request, obj, form, change):
        post_dic = form.cleaned_data
        post_number = post_dic.get('number')
        post_orig = post_dic.get('orig')
        post_start_time = post_dic.get('start_time')
        post_status = post_dic.get('status')
        post_follower = post_dic.get('follower')
        post_detail = post_dic.get('detail')
        post_error_type = post_dic.get('error_type')
        post_progess = post_dic.get('progess')
        post_resaon = post_dic.get('resaon')
        post_end_time = post_dic.get('end_time')
        # First Add the express
        if not change:
            Express.objects.create(
                number=long(post_number),
                orig=post_orig,
                start_time=post_start_time,
                status=post_status,
                follower=post_follower,
                detail = post_detail,
                error_type=post_error_type,
                progess=post_progess,
                resaon=post_resaon,
                end_time=post_end_time,
                priority=0
            )
            return None
        # Edit Something
        if change:
            if form.initial.get('detail') != post_detail:
                obj.priority = 1
                obj.detail_time = datetime.now()
            if post_number:
                obj.number = long(post_number)
            if post_orig:
                obj.orig = post_orig
            if post_start_time:
                obj.start_time = to_datetime(post_start_time)
            if post_follower:
                obj.follower = post_follower
            if post_detail:
                obj.detail = post_detail
            if post_error_type:
                obj.error_type = post_error_type
            if post_progess:
                obj.progess = post_progess
                obj.progess_time = datetime.now()
            if post_resaon:
                obj.resaon = post_resaon
            if post_end_time:
                try:
                    ExpressArchive.objects.create(
                        number=obj.number,
                        status=obj.status,
                        orig=obj.orig,
                        detail=obj.detail,
                        start_time=obj.start_time,
                        follower=obj.follower,
                        end_time=obj.end_time
                    )
                    obj.delete()
                    return None
                except Exception as e:
                    print 'Wrong!', e
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
        export_file = 'data.xls'
        excel = xlwt.Workbook(encoding='utf8')
        excel_sheet = excel.add_sheet('shet1')
        # Add EXCEL Header
        excel_sheet.write(0, 0, '运单号')
        excel_sheet.write(0, 1, '发件网点')
        excel_sheet.write(0, 2, '开单时间')
        excel_sheet.write(0, 3, '状态')
        excel_sheet.write(0, 4, '跟进人')
        excel_sheet.write(0, 5, '客户诉求')
        excel_sheet.write(0, 6, '完结时间')
        excel_sheet.write(0, 7, '完结后留言')
        # Write Data to EXCEL
        row = 1
        for data in queryset:
            datas = map(
                to_unicode,
                [ 
                    str(data.number),
                    data.orig,
                    data.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                    data.status,
                    data.follower.first_name,
                    data.detail,
                    data.end_time.strftime('%Y-%m-%d %H:%M:%S'),
                    data.message
                ]
            )
            for col, value in enumerate(datas):
                excel_sheet.write(row, col, value)
            row += 1
        if os.path.exists(export_file):
            os.remove(export_file)
        excel.save(export_file)
        response = StreamingHttpResponse(file_iter(export_file))
        response['Content-Type'] = 'application/octest-stream'
        response['Content-Disposition'] = 'attachment;filename="data.xls"' 
        return response
    export_data.short_description = '导出选中数据'


admin.site.register(Express, ExpressAdmin)
admin.site.register(ExpressArchive, ExpressArchiveAdmin)
admin.site.site_hader = 'ANE'
admin.site.site_title = 'ANE EXPRESS'
