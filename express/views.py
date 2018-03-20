# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required

from express.forms import FileForm
from express.models import Express
from express.utils import read_excel
from express.paginator import split_page

import time
from xpinyin import Pinyin


@login_required(login_url='/admin/login/')
def data_import(request):
    time.clock()
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['filename']
            op_type = form.cleaned_data.get('op_type')
            if not excel_file.name.endswith(('xls', 'xlsx')):
                return HttpResponse(u'请上传EXCEL文件!')
            gener = read_excel(excel_file.read())
            next(gener)
            total_sucess = 0
            if op_type == 'status':
                for datas in gener:
                    num, status = datas
                    try:
                        express = Express.objects.get(number=num)
                        express.status = status
                        express.save()
                        total_sucess += 1
                    except Express.DoesNotExist:
                        pass
                process_time = str(time.clock()).encode('utf8')
            if op_type == 'import':
                expresses = list()
                count = 0
                for datas in gener:
                    total_sucess += 1
                    num, start_time, orig, follower_firstname, status = datas
                    try:
                        follower = User.objects.get(
                            first_name=follower_firstname
                        )
                    except User.DoesNotExist:
                        pinyin = Pinyin()
                        username = pinyin.get_pinyin(
                            follower_firstname.decode('utf8'), ''
                        )
                        follower = User.objects.create(
                            username=username,
                            is_staff=True,
                            is_active=True,
                            first_name=follower_firstname
                        )
                        follower.set_password(username)
                        perm = Group.objects.get(name=u'跟单权限')
                        follower.groups = [perm]
                        follower.save()
                    expresses.append(
                        Express(
                            number=num,
                            start_time=start_time,
                            orig=orig,
                            follower=follower,
                            status=status
                        )
                    )
                    count += 1
                    if count == 500:
                        count = 0
                        Express.objects.bulk_create(expresses)
                        expresses = list()
                        continue
                Express.objects.bulk_create(expresses)
                process_time = str(time.clock()).encode('utf8')
            if op_type == 'follower':
                for datas in gener:
                    try:
                        num, follower_firstname = datas
                        follower = User.objects.get(first_name=follower_firstname)
                        express = Express.objects.get(number=num)
                        express.follower = follower
                        express.save()
                        total_sucess += 1
                    except Express.DoesNotExist:
                        pass
                process_time = str(time.clock()).encode('utf8')
            return HttpResponse(
                u'%s条数据成功,共花费时间%s秒' % (total_sucess, process_time)
            )

    else:
        form = FileForm()
    return render(request, 'import.html', locals())


@login_required(login_url='/admin/login/')
def change_follower(request):
    if request.method == 'POST':
        numbers = request.POST.getlist('numbers')
        users = request.POST.getlist('user')
        if numbers and users:
            query = Express.objects
            try:
                user = User.objects.get(first_name=users[0])
            except User.DoesNotExist:
                user = User.objects.get(username=users[0])
            for number in numbers:
                express = query.get(number=number)
                express.follower = user
                express.save()
            return HttpResponse('Change Suceess!')
        return HttpResponse('Please select number and user!')
    else:
        users = User.objects.filter(is_superuser=0)
        expresses = Express.objects.all()
        numbers = split_page(request, expresses)
        return render(request, 'change.html', locals())
