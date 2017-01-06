# coding:utf-8
from rest_framework import filters
from models import SKU, Goods, User, Address, ShoppingRecord
from serializer import SKUSerializer, GoodsSerializer, UserSerializer, AddressSerializer, ShoppingRecordSerializer
from sku.filters import GoodsFilter, JsonOrderingFilter, JsonDjangoFilterBackend, SKUFilter, UserFilter, AddressFilter, \
    ShoppingRecordFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

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
    filter_class = ShoppingRecordFilter

    def create(self, request, *args, **kwargs):
        user = User.objects.get(id=request.data['user'])
        sku = SKU.objects.get(id=request.data['sku'])
        if user.balance - sku.goods.price < 0:
            return Response({"error": "insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)
        data = dict()
        data['user'] = user.id
        data['sku'] = sku.id
        data['number'] = sku.number
        data['payment'] = sku.goods.price
        serializer = ShoppingRecordSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user.balance -= sku.goods.price
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)