# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Recruit, Apply


class ApplyInline(admin.TabularInline):#tabular는 table 형식으로 나옴
    model = Apply
    extra = 1 #밑에 extra로 더 나올 양


class RecruitAdmin(admin.ModelAdmin):
    fieldsets = [
            ('Taxi Info',  {'fields': ['path_from', 'path_to', 'dep_time', 'popl']}),
            ('Person Info',  {'fields': ['cont_req', 'pub_date']}),
        ]
    inlines = [ApplyInline] #apply를 추가할 수 있는 항목
    list_display = ('path_from', 'path_to', 'dep_time','cont_req', 'was_published_recently')
    #보여주는 항목
    list_filter = ['dep_time'] #sort할 수 있는 기준
    search_fields = ['cont_req']
    list_per_page = 30

admin.site.register(Recruit, RecruitAdmin)
