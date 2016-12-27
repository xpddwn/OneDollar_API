# coding: utf-8
from django.conf.urls import url
from django.contrib import admin
from rest_framework import routers
import views

router = routers.DefaultRouter()
# router.register(r'sku', SKUViewSet)

urlpatterns = [
    url('^goods/', views.GoodsViewSet.as_view()),
    url('^sku/', views.SKUViewSet.as_view()),
] + router.urls
