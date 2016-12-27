from rest_framework import serializers

from models import Goods, SKU


class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = ('id', 'name', 'introduction', 'category',
                  'price', 'image_list', 'create_time', 'modified_time')


class SKUSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = SKU
        fields = ('number', 'rating', 'start_time', 'end_time', 'create_time', 'modified_time', 'winner', 'goods')
