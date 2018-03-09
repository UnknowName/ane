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
        post_data = form.cleaned_data
        old_detail = form.initial.get('detail')
        start_time = obj.start_time
        new_detail = post_data.get('detail')
        end_date = post_data.get('end_time')
        number= long(post_data.get('number'))
        orig = post_data.get('orig')
        error_type = post_data.get('error_type')
        status = post_data.get('status')
        follower = post_data.get('follower')
        if change and new_detail != old_detail:
            obj.priority = 1
        elif end_date and change:
            try:
                ExpressArchive.objects.create(
                    number=number, orig=orig, start_time=start_time,
                    status=status,follower=follower,
                    detail=new_detail, end_time=end_date
                )
                obj.delete()
                return None
            except Exception as e:
                print e
                return None
        else:
            obj.priority = 0
        obj.number = number 
        obj.orig = orig
        obj.status = status
        obj.follower = follower
        obj.detail = new_detail
        obj.error_type = error_type
        obj.progess = post_data.get('progess')
        obj.resaon = post_data.get('resaon')
        obj.end_time = end_date
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
