# coding:utf-8
from rest_framework import filters
from models import SKU, Goods, User, Address, ShoppingRecord
from serializer import SKUSerializer, GoodsSerializer, UserSerializer, AddressSerializer, ShoppingRecordSerializer
from sku.filters import GoodsFilter, JsonOrderingFilter, JsonDjangoFilterBackend, SKUFilter, UserFilter, AddressFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response


class SKUViewSet(ModelViewSet):
    queryset = SKU.objects.all()
    serializer_class = SKUSerializer
    filter_backends = (JsonOrderingFilter,
                       JsonDjangoFilterBackend,
                       filters.SearchFilter)
    filter_class = SKUFilter


class GoodsViewSet(ModelViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    filter_backends = (JsonOrderingFilter,
                       JsonDjangoFilterBackend,
                       filters.SearchFilter)
    filter_class = GoodsFilter


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (JsonOrderingFilter,
                       JsonDjangoFilterBackend,
                       filters.SearchFilter)
    filter_class = UserFilter


class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filter_backends = (JsonOrderingFilter,
                       JsonDjangoFilterBackend,
                       filters.SearchFilter)
    filter_class = AddressFilter

class ShoppingRecordViewSet(ModelViewSet):
    queryset = ShoppingRecord.objects.all()
    serializer_class = ShoppingRecordSerializer
    filter_backends = (JsonOrderingFilter,
                       JsonDjangoFilterBackend,
                       filters.SearchFilter)
