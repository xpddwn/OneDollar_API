# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-11 03:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sku', '0004_auto_20170111_0318'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shoppingrecord',
            old_name='payment',
            new_name='amount',
        ),
    ]