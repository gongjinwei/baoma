from django.shortcuts import render

# Create your views here.
import datetime
from decimal import Decimal
from django.conf import settings

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters, views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from . import models
from . import serializers
from .permission import UserPermissionFilterBackend


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


class AdminViewSet(viewsets.ModelViewSet):
    queryset = models.Admin.objects.all()
    serializer_class = serializers.AdminSerializer


class TasksViewSet(viewsets.ModelViewSet):
    queryset = models.Tasks.objects.all()
    serializer_class = serializers.TasksSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter, UserPermissionFilterBackend]
    filter_fields = ['task_platform', 'task_name']
    search_fields = ['task_name', 'goods_title']
    ordering_fields = ['task_platform']
    filter_from = ['owner_id']

    def minus_task_fee(self):
        remaining_money=self.request.user.merchants.money_balance
        pub_quantity = int(self.request.data.get('pub_quantity',0))
        goods_price = Decimal(self.request.data.get('goods_price',0))
        goods_freight=Decimal(self.request.data.get('goods_freight',0))
        task_type=int(self.request.data.get('task_type',0))
        per_publish =task_type*20+60+goods_price+goods_freight
        total_fee = pub_quantity*(per_publish)
        if remaining_money>=total_fee:
            return (True,total_fee)
        return (False,0)

    def create(self, request, *args, **kwargs):
        if not hasattr(request.user,'merchants'):
            return Response('你必须先创建一个商家',status.HTTP_400_BAD_REQUEST)
        task_serializer = self.get_serializer(data=request.data)
        publish_serializer = serializers.PublishSerializer(data=request.data)
        task_serializer.is_valid(raise_exception=True)
        publish_serializer.is_valid(raise_exception=True)
        val,total_fee=self.minus_task_fee()
        if val:
            merchant_instance = self.request.user.merchants
            merchant_instance.money_balance = merchant_instance.money_balance - total_fee
            merchant_instance.save()
            self.perform_create(task_serializer)

            pub_date = request.data.get('pubs_start', '')
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
                                                pub_quantity=at)

            headers = self.get_success_headers(task_serializer.data)
            return Response(task_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response("你的余额不足，请充值")

    def perform_create(self, serializer):
        time_now = datetime.datetime.now()
        serializer.save(owner=self.request.user,createtime=datetime.datetime.timestamp(time_now))


class TaskOrderView(views.APIView):
    """
    输入task_id调出所有相关的订单列表
    """

    def get(self, request, pk, format=None):
        """
        :param pk: for task_id
        """

        queryset = models.Order.objects.filter(publish_id__task_id=pk)
        if request.user.is_superuser:
            pass
        else:
            queryset = queryset.filter(publish_id__task_id__owner_id=request.user.id)
        serializer = serializers.OrderSerializer(queryset, many=True)
        return Response(serializer.data)


class StoresViewSet(viewsets.ModelViewSet):
    queryset = models.Stores.objects.all()
    serializer_class = serializers.StoresSerializer
    filter_backends = [UserPermissionFilterBackend]
    filter_from = ['merchant_id__user_id']

    def perform_create(self, serializer):
        time_now = datetime.datetime.timestamp(datetime.datetime.now())
        merchant=self.request.user.merchants
        serializer.save(createtime=time_now,merchant_id=merchant)


class SaddressViewSet(viewsets.ModelViewSet):
    queryset = models.Saddress.objects.all()
    serializer_class = serializers.SaddressSerializer
    filter_backends = [UserPermissionFilterBackend]
    filter_from = ['merchant_id__user_id']

    def perform_create(self, serializer):
        serializer.save(merchant_id=self.request.user.merchants)


class PublishViewSet(viewsets.ModelViewSet):
    queryset = models.Publish.objects.all()
    serializer_class = serializers.PublishSerializer
    filter_backends = [UserPermissionFilterBackend]
    filter_from = ['task_id__owner_id']


class PageViewSet(viewsets.ModelViewSet):
    queryset = models.Page.objects.all()
    serializer_class = serializers.PageSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    filter_backends = [filters.OrderingFilter,UserPermissionFilterBackend]
    ordering_fields = ['goods_title']
    ordering = ('-order_id',)
    filter_from = ['publish_id__task_id__owner_id']

    @detail_route(methods=['patch'])
    def set_comment(self,request,pk=None):
        order_instance = models.Order.objects.get(pk=int(pk))

        serializer = self.get_serializer(order_instance, data=request.data, partial=True)
        if serializer.is_valid():
            selected = request.data.get('selected',[])
            platform_images=[]
            all_images = models.ImagesShow.objects.filter(owner_id=int(pk))
            if selected:
                for image in all_images:
                    if image.image_id in selected:
                        image.is_selected = 1
                        platform_images.append(image.path)
                        image.save()
                    else:
                        image.is_selected=0
                        image.save()
            serializer.save(platform_comment_images=','.join(platform_images))
            return Response(serializer.data)


class ModelsViewSet(viewsets.ModelViewSet):
    queryset = models.Models.objects.all()
    serializer_class = serializers.ModelsSerializer


class MerchantsViewSet(viewsets.ModelViewSet):
    queryset = models.Merchants.objects.all()
    serializer_class = serializers.MerchantsSerializer
    filter_backends = [UserPermissionFilterBackend]
    filter_from = ['user_id']

    def create(self, request, *args, **kwargs):
        """
            只能新建一个商家！
        """
        if hasattr(request.user,'merchants'):
            return Response("你只能创建一个商家信息！")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        createtime = datetime.datetime.timestamp(datetime.datetime.now())
        serializer.save(user=self.request.user,createtime=createtime)


class MembersViewSet(viewsets.ModelViewSet):
    queryset = models.Members.objects.all()
    serializer_class = serializers.MembersSerializer


class AreaViewSet(viewsets.ModelViewSet):
    queryset = models.Area.objects.all()
    serializer_class = serializers.AreaSerializer


class ImageUpViewSet(viewsets.ModelViewSet):
    queryset = models.ImageUp.objects.all()
    serializer_class = serializers.ImageUpSerializer
    filter_backends = [UserPermissionFilterBackend]
    filter_from = ['merchant__user_id']

    def perform_create(self, serializer):
        createtime = datetime.datetime.timestamp(datetime.datetime.now())
        serializer.save(merchant=self.request.user.merchants,createtime=createtime)


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = models.Feedback.objects.all()
    serializer_class = serializers.FeedbackSerializer


class ImagesViewSet(viewsets.ModelViewSet):
    queryset = models.Images.objects.all()
    serializer_class = serializers.ImagesSerializer


class ImagesShowViewSet(viewsets.ModelViewSet):
    queryset = models.ImagesShow.objects.all()
    serializer_class = serializers.ImagesShowSerializer
    filter_backends = [UserPermissionFilterBackend]
    filter_from = ['owner_id__publish_id__task_id__owner_id']


class BlogCommentViewSet(viewsets.ModelViewSet):
    queryset = models.BlogComment.objects.all()
    serializer_class = serializers.BlogCommentSerializer


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = models.BlogPost.objects.all()
    serializer_class = serializers.BlogPostSerializer


class BlogCategoryViewSet(viewsets.ModelViewSet):
    queryset = models.BlogCategory.objects.all()
    serializer_class = serializers.BlogCategorySerializer


class ConsumeRecordsViewSet(viewsets.ModelViewSet):
    queryset = models.ConsumeRecords.objects.all()
    serializer_class = serializers.ConsumeRecordsSerializer
    filter_backends = [UserPermissionFilterBackend]
    filter_from = ['merchant_id__user_id']
