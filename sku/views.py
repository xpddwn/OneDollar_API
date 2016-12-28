# coding:utf-8
from rest_framework import filters

from models import SKU, Goods
from serializer import SKUSerializer, GoodsSerializer
from sku.filters import GoodsFilter, JsonOrderingFilter, JsonDjangoFilterBackend, SKUFilter
from utilities import ModelViewSet


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




