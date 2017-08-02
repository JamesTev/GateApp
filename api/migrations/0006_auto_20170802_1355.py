# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-02 11:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20170731_2034'),
    ]

    operations = [
        migrations.AddField(
            model_name='guest',
            name='mobile',
            field=models.CharField(default='0823235152', max_length=30, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='guest',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
