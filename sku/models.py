# coding: utf-8
from __future__ import unicode_literals

from django.db import models


class User(models.Model):
    phone = models.CharField(max_length=32, null=True, verbose_name="账号")
    name = models.CharField(max_length=128, null=True)
    Email = models.CharField(max_length=128, null=True)
    balance = models.FloatField(default=0)
    password = models.CharField(max_length=32)
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)


class Goods(models.Model):
    name = models.CharField(max_length=128)
    introduction = models.TextField()
    category = models.CharField(max_length=64)
    image_list = models.CharField(max_length=255, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)


class SKU(models.Model):
    number = models.IntegerField(verbose_name="活动期号")
    goods = models.ForeignKey(Goods)
    winner = models.ManyToManyField(User, null=True, blank=True)
    rating = models.IntegerField(verbose_name="最大参与人数")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    price = models.FloatField()


class Address(models.Model):
    user = models.ForeignKey(User, related_name="address")
    street = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=128)
    zip_code = models.CharField(max_length=32)
    contact = models.CharField(max_length=128)
    contact_phone = models.CharField(max_length=32)
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)


class RechargeInfo(models.Model):
    user = models.ForeignKey(User, related_name="recharge")
    amount = models.FloatField()
    account = models.CharField(max_length=128)
    channel = models.CharField(max_length=128)
    create_time = models.DateTimeField(auto_now_add=True)


class ShoppingRecord(models.Model):
    user = models.ForeignKey(User, related_name="record")
    number = models.CharField(max_length=32, verbose_name="夺宝号")
    sku = models.ForeignKey(SKU, related_name="record")
    amount = models.IntegerField()
    status = models.IntegerField(default=0, verbose_name="付款收货状态")
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)


class Image(models.Model):
    url = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)


class Share(models.Model):
    sku = models.ForeignKey(SKU)
    user = models.ForeignKey(User)
    image = models.CharField(max_length=255)
    recommend = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
