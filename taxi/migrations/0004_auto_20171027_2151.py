# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 12:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxi', '0003_auto_20171027_2016'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Request',
            new_name='Recruit',
        ),
        migrations.RenameField(
            model_name='apply',
            old_name='request',
            new_name='recruit',
        ),
    ]
