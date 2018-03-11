# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.contrib.auth import login, authenticate

from express.forms import LoginForm


def auth_login(request):
    if request.method == 'POST':
        forms = LoginForm(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data.get('username')
            password = forms.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    http_referer = request.META.get('HTTP_REFERER')
                    if http_referer:
                        try:
                            _, url = http_referer.split('next=')
                        except ValueError:
                            return render(request, 'manager.html') 
                        return redirect(url)
    else:
        form = LoginForm()
        return render(request, 'login.html', locals())
