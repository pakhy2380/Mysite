# -*- coding: utf-8 -*-

import datetime

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible


class Recruit(models.Model):
    path_from = models.CharField(max_length=200) #어디에서
    path_to = models.CharField(max_length=200) #어디로
    popl = models.PositiveIntegerField(default=3) #몇 명? 보통 자기 제외하고 3명 구함
    dep_time = models.DateTimeField('departure time') #출발 시각
    cont_req = models.CharField(max_length=200) #올린이 연락처
    pub_date = models.DateTimeField('date published') #올린 날짜

    def __str__(self):
        #누가 쓴 건가. class 대표값
        return self.cont_req

    def was_published_recently(self):
        #3일 이내 생성된 recruit인가
        now = timezone.now()
        return timezone.now() - datetime.timedelta(days=3) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'dep_time'
    was_published_recently.boolean = True
    was_published_recently.short_decription = 'Published recently?'



class Apply(models.Model):
    recruit = models.ForeignKey(Recruit, on_delete=models.CASCADE) #어느 req
    cont_app = models.CharField(max_length=200) #appliance 연락처
    num_people = models.IntegerField(default=1) #동행인
    rearr = models.BooleanField(default=0) #시간 조정 필요 여부
    accept = models.BooleanField(default=0) #동행하기로 확정된 건가

    def __str__(self):
        return self.cont_app
