# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-21 08:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sku', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default=111, max_length=32),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='address',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='modified_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='goods',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='goods',
            name='modified_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='modified_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='rechargeinfo',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='share',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='share',
            name='modified_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='shoppingrecord',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='shoppingrecord',
            name='modified_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='sku',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='sku',
            name='modified_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='modified_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
