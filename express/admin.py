# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.models import User
from models import Express, ExpressArchive


class ExpressAdmin(admin.ModelAdmin):
    search_fields = ('=number', '=status', '=follower')
    show_full_result_count = False
    list_display = (
        'number', 'orig', 'start_time', 'status', 'follower',
        'detail', 'error_type', 'progess', 'resaon', 'end_time'
    )
    list_display_links = (
        'number', 'orig', 'status', 'detail', 'follower',
        'error_type', 'progess', 'resaon', 'end_time'
    )
    list_per_page = 50
    fieldsets = [
        ('基本信息', {'fields': ['number', 'orig', 'status']}),
        ('业务信息', {'fields': ['follower', 'detail']}),
        ('业务详情', {'fields': ['error_type', 'progess', 'resaon']}),
        (None, {'fields': ['end_time']}),
    ]
    exclude = ['priority']

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
                detail=post_detail,
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
            if post_resaon:
                obj.resaon = post_resaon
            if post_end_time:
                try:
                    ExpressArchive.objects.create(
                        number=obj.number,
                        orig=obj.orig,
                        start_time=obj.start_time,
                        status=obj.status,
                        follower=obj.follower,
                        detail=obj.detail,
                        end_time=obj.end_time
                    )
                    obj.delete()
                    return None
                except Exception as e:
                    print 'Wrong!', e
            obj.save()

    def get_queryset(self, request):
        user = request.user
        qs = super(ExpressAdmin, self).get_queryset(request)
        if user.is_superuser or user.has_perm('express.change_detail'):
            return qs
        user = User.objects.get(username=user)
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
            read_only_fields = ('number', 'orig', 'follower', 'start_time', 'detail')
        return read_only_fields


class ExpressArchiveAdmin(admin.ModelAdmin):
    search_fields = ('number',)
    show_full_result_count = False
    fieldsets = [
        ('完结基本信息', {'fields':[
                                    'number', 'orig', 'start_time', 'status',
                                     'follower', 'detail', 'end_time'
                                   ]
                         }
        ),
        (None, {'fields':['message']})
    ]
    list_display = (
        'number', 'orig', 'start_time', 'status',
        'follower', 'detail', 'end_time', 'message'
    )

    def get_readonly_fields(self, request, obj):
        reads = [ field for field in self.list_display if field != 'message' ]
        return reads


admin.site.register(Express, ExpressAdmin)
admin.site.register(ExpressArchive, ExpressArchiveAdmin)
admin.site.site_hader = 'ANE'
admin.site.site_title = 'ANE EXPRESS'
