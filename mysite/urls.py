# -*- coding: utf-8 -*-
"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.auth import views as auth_views #로그인 위해서

urlpatterns = [
    url(r'^taxi/', include('taxi.urls')),
    url(r'^admin/', admin.site.urls),
    url(
        r'^accounts/login/', #로그인하는 url
        auth_views.login, #객체가 존재하는 모듈
        name='login', #그냥 이름 붙인 것. 없어도 무방
        kwargs={
            'template_name': 'login.html' #dictionary 형태로 url패턴에 전달.
        }
    ),
    url(
        r'^accounts/logout/',
        auth_views.logout,
        name='logout',
        kwargs={
            'next_page': settings.LOGIN_URL, #로그아웃 후 이동할 url(지금은 login으로). 없으면 내장된 로그아웃 페이지.
        }
    ),
]
