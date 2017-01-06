# coding: utf-8
from django.conf.urls import url
from django.contrib import admin
from rest_framework import routers
import views

router = routers.DefaultRouter()
router.register(r'goods', views.GoodsViewSet)
router.register(r'sku', views.SKUViewSet)
router.register(r'user', views.UserViewSet)
router.register(r'address', views.AddressViewSet)
router.register(r'record', views.ShoppingRecordViewSet)

urlpatterns = [
    # url('^goods/', views.GoodsViewSet.as_view()),
    # url('^sku/', views.SKUViewSet.as_view()),
    # url('^user/', views.UserViewSet.as_view()),
] + router.urls
