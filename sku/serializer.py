from rest_framework import serializers

from models import Goods, SKU, User, Address, ShoppingRecord


class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = ('id', 'name', 'introduction', 'category',
                  'price', 'image_list')


class SKUSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(required=False)

    class Meta:
        model = SKU
        fields = ('id', 'number', 'rating', 'start_time',
                  'end_time', 'winner', 'goods')

    def create(self, validated_data):
        goods = validated_data.pop('goods')
        instance = super(SKUSerializer, self).create(validated_data)
        goods_id = goods.get('id')
        if goods_id:
            instance.goods = GoodsSerializer(data=Goods.objects.get(id=goods_id))
        else:
            goods_serializer = GoodsSerializer(data=goods)
            if goods_serializer.is_valid():
                goods_serializer.save()
                instance.goods = goods_serializer
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone', 'name', 'Email', 'balance')


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'user', 'street', 'city', 'state',
                  'zip_code', 'contact', 'contact_phone')


class ShoppingRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingRecord
        fields = ('id', 'user', 'number', 'sku', 'payment')
