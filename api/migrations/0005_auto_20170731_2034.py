# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-31 18:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20170731_2016'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Guests',
            new_name='Guest',
        ),
        migrations.RenameModel(
            old_name='GuestPermissions',
            new_name='GuestPermission',
        ),
    ]
