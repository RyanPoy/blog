# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-18 12:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_page_uri'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='uri',
            field=models.CharField(db_index=True, max_length=255, unique=True, verbose_name='跳转地址'),
        ),
    ]
