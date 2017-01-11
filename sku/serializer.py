from rest_framework import serializers

from models import Goods, SKU, User, Address, ShoppingRecord, RechargeInfo, Image, Share


class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = ('id', 'name', 'introduction', 'category', 'image_list')


class SKUSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(required=False)

    class Meta:
        model = SKU
        fields = ('id', 'number', 'price', 'rating', 'start_time',
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
    user = UserSerializer()
    sku = SKUSerializer()

    class Meta:
        model = ShoppingRecord
        fields = ('id', 'user', 'number', 'sku', 'amount', 'status', 'create_time')


class RechargeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RechargeInfo
        fields = ('id', 'user', 'amount', 'channel', 'account', 'create_time')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'url')


class ShareSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    sku = SKUSerializer(required=False)

    class Meta:
        model = Share
        fields = ('id',  'sku', 'user', 'image', 'recommend', 'create_time')

    def create(self, validated_data):
        try:
            user = validated_data.get('user')
            sku = validated_data.get('sku')
            instance = Share(user=User.objects.get(id=user),
                             sku=SKU.objects.get(id=sku),
                             recommend=validated_data.get('recommend'),
                             image=validated_data.get('image'))
            return instance
        except Exception as e:
            print e
            raise Exception
