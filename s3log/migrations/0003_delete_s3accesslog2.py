# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-06 15:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('s3log', '0002_s3accesslog2'),
    ]

    operations = [
        migrations.DeleteModel(
            name='S3AccessLog2',
        ),
    ]