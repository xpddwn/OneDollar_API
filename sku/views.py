# coding:utf-8

from models import SKU, Goods
from serializer import SKUSerializer, GoodsSerializer
from utilities import ModelViewSet


class SKUViewSet(ModelViewSet):
    queryset = SKU.objects.all()
    serializer_class = SKUSerializer


class GoodsViewSet(ModelViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer





