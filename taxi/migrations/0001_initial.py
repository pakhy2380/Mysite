# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 10:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Apply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Contact', models.CharField(max_length=200)),
                ('Num_people', models.IntegerField(default=1)),
                ('Rearr', models.BooleanField(default=0)),
                ('Accept', models.BooleanField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('From', models.CharField(max_length=200)),
                ('To', models.CharField(max_length=200)),
                ('Popl', models.PositiveIntegerField(default=3)),
                ('dep_time', models.DateTimeField(verbose_name=b'departure time')),
                ('Contact', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name=b'date published')),
            ],
        ),
        migrations.AddField(
            model_name='apply',
            name='request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taxi.Request'),
        ),
    ]
