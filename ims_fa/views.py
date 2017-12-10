# -*- coding:utf-8 -*-
from django.shortcuts import render

# Create your views here.
import datetime, re
from decimal import Decimal
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.cache import cache

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters, serializers as ser
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from . import models
from . import serializers
from .permission import UserPermissionFilterBackend
from .SmsClient import SmsSender


class ObtainExpireAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            time_now = datetime.datetime.now()
            EXPIRE_MINUTES = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_MINUTES', 1)
            if created or token.created < time_now - datetime.timedelta(minutes=EXPIRE_MINUTES):
                token.delete()
                token = Token.objects.create(user=user)
                token.created = time_now
                token.save()
            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TasksViewSet(viewsets.ModelViewSet):
    queryset = models.Tasks.objects.all()
    serializer_class = serializers.TasksSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter, UserPermissionFilterBackend]
    filter_fields = ['task_platform', 'task_name']
    search_fields = ['task_name', 'goods_title']
    ordering_fields = ['task_id']
    ordering = ['-task_id']
    filter_from = ['owner_id']

    @detail_route()
    def orders(self, request, pk=None):
        """
        :param pk: for task_id
        """
        queryset = models.Order.objects.filter(publish_id__task_id=pk)
        if not request.user.is_superuser:
            queryset = queryset.filter(publish_id__task_id__owner_id=request.user.id)
        serializer = serializers.OrderSerializer(queryset, many=True)

        return Response(serializer.data)

    @detail_route()
    def publish(self, request, pk=None):
        """
        :param pk: for task_id
        """
        queryset = models.Publish.objects.filter(task_id=pk)
        if not request.user.is_superuser:
            queryset = queryset.filter(task_id__owner_id=request.user.id)
        serializer = serializers.PublishSerializer(queryset, many=True)
        return Response(serializer.data)

    def minus_task_fee(self, task_serializer, publish_serializer):
        merchant = self.request.user.merchants
        remaining_money = merchant.money_balance
        discount = merchant.level.discount / 100 if hasattr(merchant.level, 'discount') else 1
        pub_quantity = publish_serializer.validated_data.get('pub_quantity', 0)
        if pub_quantity == 0:
            raise ser.ValidationError({'msg': '你的发布数量为0', 'status': 400})
        goods_price = task_serializer.validated_data.get('goods_price', 0)
        goods_freight = task_serializer.validated_data.get('goods_freight', 0)
        task_type = task_serializer.validated_data.get('task_type', 0)
        per_publish = task_type * 20 + 60 + goods_price + goods_freight
        total_fee = pub_quantity * (per_publish) * Decimal(discount)
        if remaining_money >= total_fee:
            return (True, total_fee)
        return (False, 0)

    def create(self, request, *args, **kwargs):
        task_serializer = self.get_serializer(data=request.data)
        publish_serializer = serializers.PublishSerializer(data=request.data)
        task_serializer.is_valid(raise_exception=True)
        publish_serializer.is_valid(raise_exception=True)
        if not request.user.is_superuser and task_serializer.validated_data[
            'store_id'].merchant_id.user_id != request.user.id:
            raise ser.ValidationError({'msg': ['你不能对不属于你的店铺做任务发布'], 'status': 400})
        if not request.data.get('pubs_start', ''):
            raise ser.ValidationError({'msg': ['请填写体验日期'], 'status': 400})
        val, total_fee = self.minus_task_fee(task_serializer, publish_serializer)
        if val:
            merchant_instance = self.request.user.merchants
            merchant_instance.money_balance = merchant_instance.money_balance - total_fee
            merchant_instance.save()
            self.perform_create(task_serializer)

            pub_date = request.data.get('pubs_start')
            time_array = request.data.get('time_array', [])
            if time_array and pub_date:
                pub_date = datetime.datetime.strptime(pub_date, '%Y-%m-%d')
                for index, at in enumerate(time_array):
                    if at:
                        publish_serializer = serializers.PublishSerializer(data=request.data)
                        publish_serializer.is_valid(raise_exception=True)
                        pub_start = pub_date + datetime.timedelta(hours=index)
                        pub_start = pub_start.timestamp()
                        publish_serializer.save(task_id=task_serializer.instance, pub_start=pub_start,
                                                pub_quantity=at, pub_surplus=at)

            headers = self.get_success_headers(task_serializer.data)
            return Response(task_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response({'msg': ["你的余额不足，请充值"], 'status': 406}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def perform_create(self, serializer):
        time_now = datetime.datetime.now()
        serializer.save(owner=self.request.user, createtime=datetime.datetime.timestamp(time_now))


class StoresViewSet(viewsets.ModelViewSet):
    queryset = models.Stores.objects.all()
    serializer_class = serializers.StoresSerializer
    filter_backends = [UserPermissionFilterBackend]
    filter_from = ['merchant_id__user_id']

    def perform_create(self, serializer):
        time_now = datetime.datetime.timestamp(datetime.datetime.now())
        merchant = self.request.user.merchants
        serializer.save(createtime=time_now, merchant_id=merchant)


class SaddressViewSet(viewsets.ModelViewSet):
    queryset = models.Saddress.objects.all()
    serializer_class = serializers.SaddressSerializer
    filter_backends = [UserPermissionFilterBackend]
    filter_from = ['merchant_id__user_id']

    def perform_create(self, serializer):
        serializer.save(merchant_id=self.request.user.merchants)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    filter_backends = [filters.OrderingFilter, UserPermissionFilterBackend]
    ordering_fields = ['goods_title']
    ordering = ('-order_id',)
    filter_from = ['publish_id__task_id__owner_id']


    @detail_route(methods=['patch'])
    def set_comment(self, request, pk=None):
        order_instance = models.Order.objects.get(pk=int(pk))
        if not request.user.is_superuser and order_instance.publish_id.task_id.owner_id != request.user.id:
            raise ser.ValidationError({'msg': '你没有改订单的操作权限', 'status': 400})
        serializer = self.get_serializer(order_instance, data=request.data, partial=True)
        if serializer.is_valid():
            selected = request.data.get('selected', [])
            platform_images = []
            all_images = models.ImagesShow.objects.filter(owner_id=int(pk))
            if selected:
                for image in all_images:
                    if image.image_id in selected:
                        image.is_selected = 1
                        platform_images.append(image.path.name)
                        image.save()
                    else:
                        image.is_selected = 0
                        image.save()
            serializer.save(platform_comment_images=','.join(platform_images), order_state=50)
            return Response(serializer.data)


class MerchantsViewSet(viewsets.ModelViewSet):
    queryset = models.Merchants.objects.all()
    serializer_class = serializers.MerchantsSerializer
    filter_backends = [UserPermissionFilterBackend]
    filter_from = ['user_id']

    def create(self, request, *args, **kwargs):
        """
            只能新建一个商家！
        """

        raise ser.ValidationError({'msg': "you can't create in this way,please create it from register", 'status': 400})

    @detail_route(methods=['post'],serializer_class=serializers.PasswordResetSerializer)
    def password_reset(self, request, pk=None):
        """
            输入旧密码，改成新密码
        """
        password_serializer = self.get_serializer(data=request.data)
        if password_serializer.is_valid(raise_exception=True):
            old_password = password_serializer.validated_data['old_password']
            new_password = password_serializer.validated_data['new_password']
            if old_password != new_password:
                user_login = User.objects.get(username=request.user)
                if user_login.check_password(old_password):
                    merchant = models.Merchants.objects.get(pk=int(pk))
                    user_change = merchant.user
                    if user_login.is_superuser or user_change == user_login:
                        user_change.password = make_password(new_password)
                        user_change.save()
                        return Response('Password is set done')
                    return Response("No permission to do this", status=status.HTTP_400_BAD_REQUEST)
                return Response("password is wrong", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("password can't be null and the same", status=status.HTTP_400_BAD_REQUEST)


class ImageUpViewSet(viewsets.ModelViewSet):
    queryset = models.ImageUp.objects.all()
    serializer_class = serializers.ImageUpSerializer
    filter_backends = [filters.OrderingFilter, UserPermissionFilterBackend]
    filter_from = ['merchant__user_id']
    ordering_fields = ['id']
    ordering = ['-id']

    def perform_create(self, serializer):
        createtime = datetime.datetime.timestamp(datetime.datetime.now())
        serializer.save(merchant=self.request.user.merchants, createtime=createtime)


class ConsumeRecordsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.ConsumeRecords.objects.all()
    serializer_class = serializers.ConsumeRecordsSerializer
    filter_backends = [filters.OrderingFilter, UserPermissionFilterBackend]
    filter_from = ['merchant_id__user_id']
    ordering_fields = ['consume_id']
    ordering = ['-consume_id']


class MerchantRechargeViewSet(viewsets.ModelViewSet):
    queryset = models.MerchantRecharge.objects.all()
    serializer_class = serializers.MerchantRechargeSerializer
    filter_backends = [filters.OrderingFilter, UserPermissionFilterBackend]
    filter_from = ['merchant_id__user_id']
    ordering_fields = ['recharge_id']
    ordering = ['-recharge_id']

    def perform_create(self, serializer):
        createtime = datetime.datetime.timestamp(datetime.datetime.now())
        serializer.save(merchant=self.request.user.merchants, createtime=createtime)


class RegisterView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.MerchantRegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            mobile_recv = serializer.validated_data['mobile']
            register_code = serializer.validated_data['code']
            password = serializer.validated_data['password']

            mobile_cache = cache.get(register_code + 'register' + '_mobile')
            if mobile_recv == mobile_cache:
                user_serializer = serializers.UserSerializer(data=serializer.validated_data['user'])
                if user_serializer.is_valid(raise_exception=True):
                    user = user_serializer.save(is_active=True)
                    merchant_serializer = serializers.MerchantsSerializer(data=serializer.validated_data)
                    if merchant_serializer.is_valid(
                            raise_exception=True):
                        user.set_password(password)
                        user.save()
                        createtime = datetime.datetime.timestamp(datetime.datetime.now())
                        merchant_serializer.save(user=user, createtime=createtime)
                        return Response(merchant_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response('验证码错误或已失效')


class RegisterSendView(GenericAPIView):
    """
        发送注册的手机验证码
    """
    permission_classes = [AllowAny]
    serializer_class=serializers.RegisterMobileSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            mobile = serializer.validated_data['mobile']
            sender = SmsSender(mobile)
            code, msg = sender.send(type='register')
            return Response(msg)


class ForgetSendView(GenericAPIView):
    """
        发送密码重置的手机验证码
    """
    permission_classes = [AllowAny]
    serializer_class=serializers.ForgetMobileSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            mobile = serializer.validated_data['mobile']
            if models.Merchants.objects.filter(mobile=mobile).exists():
                sender = SmsSender(mobile)
                code, msg = sender.send(type='forget')
                return Response(msg)
            else:
                return Response('不存在此电话号码')


class PasswordForgetView(GenericAPIView):
    """
        忘记密码后的重置操作，需要提供重置的手机号，有效验证码及新密码
    """
    serializer_class = serializers.PasswordSetSerializer
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            mobile_recv = serializer.validated_data['mobile']
            code = serializer.validated_data['code']
            password = serializer.validated_data['password']
            mobile_cache = cache.get(code + 'forget' + '_mobile')
            if mobile_cache == mobile_recv:
                merchant = models.Merchants.objects.get(mobile=mobile_recv)
                user = merchant.user
                user.password = make_password(password)
                user.save()
                cache.delete(code + 'forget' + '_mobile')
                return Response('设置成功')
            else:
                return Response('验证码不正确或已失效')
