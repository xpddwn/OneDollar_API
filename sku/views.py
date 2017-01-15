# coding:utf-8
from rest_framework import filters
from rest_framework.decorators import detail_route, list_route

from models import SKU, Goods, User, Address, ShoppingRecord, RechargeInfo, Image, Share
from serializer import SKUSerializer, GoodsSerializer, UserSerializer, AddressSerializer, ShoppingRecordSerializer, \
    RechargeInfoSerializer, ImageSerializer, ShareSerializer
from sku.filters import GoodsFilter, JsonOrderingFilter, JsonDjangoFilterBackend, SKUFilter, UserFilter, AddressFilter, \
    ShoppingRecordFilter, ShareFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from django.contrib.auth.hashers import make_password


def check_login(request, user):
    if request.session.get('user') == user:
        return True
    return False


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

    def create(self, request, *args, **kwargs):
        data = dict()
        data['phone'] = request.data['phone']
        if User.objects.filter(phone=data['phone']).exists():
            return Response({'error': "account exist"}, status=status.HTTP_400_BAD_REQUEST)
        data['name'] = request.data.get('name')
        data['Email'] = request.data.get('Email')
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')
        if password1 != password2:
            return Response({'error': "passwords inconsistent"}, status=status.HTTP_400_BAD_REQUEST)
        if password1 is not None and password2 is not None:
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                user = User.objects.get(id=serializer.data['id'])
                user.password = make_password(password1, "a", 'pbkdf2_sha256')[22:54]
                user.save()

                return Response({'error': 0, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'error': "data invalid"}, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['post'], url_path='login')
    def login(self, request):
        try:
            user = User.objects.get(phone=request.data.get('account'))
            password = make_password(request.data.get('password'), "a", 'pbkdf2_sha256')
            if user.password == password[22:54]:
                request.session['user'] = user.id
                return Response({'error': 0, 'user_id': user.id},
                                status=status.HTTP_200_OK)
            else:
                return Response({'error': 'password insistent'},
                                status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': "account does not exists"},
                            status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['post'], url_path='logout')
    def logout(self, request):
        try:
            user = User.objects.get(phone=request.data.get('account'))
            del request.session['user']
            return Response({'error': 0, 'data': 'logout success'},
                            status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': "account does not exists"},
                            status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'error': 'not logged in'})


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

    def _set_number(self, *args, **kwargs):
       return 111

    def _pay(self, user, record):
        if user.balance - record.sku.price * record.amount < 0:
            return 1
        if record.sku.rating <= ShoppingRecord.objects.filter(sku=record.sku).count():
            return 2
        user.balance -= record.sku.price * record.amount
        user.save()
        return 0

    def create(self, request, *args, **kwargs):
        user = User.objects.get(id=request.data['user'])
        if not check_login(request, user.id):
            return Response({"error": "not logged in"}, status=status.HTTP_400_BAD_REQUEST)
        sku = SKU.objects.get(id=request.data['sku'])
        amount = request.data.get('amount')
        sta = request.data.get('status')
        if amount is None or amount == 0:
            return Response({"error": "invalid amount"}, status=status.HTTP_400_BAD_REQUEST)
        record = ShoppingRecord(user=user, sku=sku, amount=amount, status=sta)
        if sta == 1:
            success = self._pay(user, record)
            if success == 1:
                return Response({"error": "insufficient funds"},
                                status=status.HTTP_400_BAD_REQUEST)
            if success == 2:
                return Response({"error": "sold out"}, status=status.HTTP_400_BAD_REQUEST)
            record.number = self._set_number()
        record.save()
        return Response(ShoppingRecordSerializer(record).data,
                        status=status.HTTP_201_CREATED)

    @list_route(methods=['post'], url_path='pay')
    def pay(self, request):
        user = User.objects.get(id=request.data.get('user'))
        if not check_login(request, user.id):
            return Response({"error": "not logged in"}, status=status.HTTP_400_BAD_REQUEST)
        record = ShoppingRecord.objects.get(id=request.data.get('record'), user_id=user.id)
        success = self._pay(user, record)
        if success == 1:
            return Response({"error": "insufficient funds"},
                            status=status.HTTP_400_BAD_REQUEST)
        if success == 2:
            return Response({"error": "sold out"}, status=status.HTTP_400_BAD_REQUEST)
        record.status = 1
        record.number = self._set_number()
        record.save()
        return Response({"error": 0, "data": "succeed"}, status=status.HTTP_200_OK)

    @list_route(methods=['get'], url_path='number')
    def get_number(self, request):
        sku_id = request.query_params.get('sku')
        user_id = request.session.get('user')
        if not ShoppingRecord.objects.filter(sku_id=sku_id, user_id=user_id, status__gte=1).exists():
            return Response({"error": "no permission"}, status=status.HTTP_400_BAD_REQUEST)
        number_list = ShoppingRecord.objects.filter(sku_id=sku_id).values_list("number", flat=True)
        return Response({"data": number_list}, status=status.HTTP_200_OK)


class RechargeInfoViewSet(ModelViewSet):
    queryset = RechargeInfo.objects.all()
    serializer_class = RechargeInfoSerializer
    filter_backends = (JsonOrderingFilter,
                       JsonDjangoFilterBackend,
                       filters.SearchFilter)


class ImageViewSet(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class ShareViewSet(ModelViewSet):
    queryset = Share.objects.all()
    serializer_class = ShareSerializer
    filter_backends = (JsonOrderingFilter,
                       JsonDjangoFilterBackend,
                       filters.SearchFilter)
    filter_class = ShareFilter

    def _getimage(self, image):
        return image

    def create(self, request, *args, **kwargs):
        if User.objects.filter(id=request.data['user']).exists() \
                and SKU.objects.filter(id=request.data['sku']).exists():
            share = Share(user=User.objects.get(id=request.data['user']))
            share.sku_id = request.data['sku']
            share.image = self._getimage(request.data['image'])
            share.recommend = request.data['recommend']
            share.save()
            return Response({"error": 0, "result": "success"}, status=status.HTTP_201_CREATED)
        return Response({"error": "invalid values"}, status=status.HTTP_400_BAD_REQUEST)
