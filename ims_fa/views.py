from django.shortcuts import render

# Create your views here.
import datetime
from django.conf import settings

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters, views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from guardian.shortcuts import assign_perm

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

    def create(self, request, *args, **kwargs):
        task_serializer = self.get_serializer(data=request.data)

        task_serializer.is_valid(raise_exception=True)
        self.perform_create(task_serializer)

        assign_perm('view_task', self.request.user, task_serializer.instance)
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
                    publish_serializer.save(task_id=task_serializer.instance, owner=request.user, pub_start=pub_start,
                                            pub_quantity=at)
        headers = self.get_success_headers(task_serializer.data)
        return Response(task_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


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


class SaddressViewSet(viewsets.ModelViewSet):
    queryset = models.Saddress.objects.all()
    serializer_class = serializers.SaddressSerializer


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
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['goods_title']
    ordering = ('-order_id',)

    @detail_route(methods=['patch'])
    def set_comment(self,request,pk=None):
        instance = models.Order.objects.get(pk=int(pk))
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            selected = request.data.get('selected',[])
            platform_images=[]
            if selected:
                for show_id in selected:
                    instance = models.ImagesShow.objects.get(pk=show_id)
                    instance.is_selected = 1
                    platform_images.append(instance.path)
                    instance.save()
            serializer.save(platform_comment_images=','.join(platform_images))
            return Response(serializer.data)


class ModelsViewSet(viewsets.ModelViewSet):
    queryset = models.Models.objects.all()
    serializer_class = serializers.ModelsSerializer


class MerchantsViewSet(viewsets.ModelViewSet):
    queryset = models.Merchants.objects.all()
    serializer_class = serializers.MerchantsSerializer


class MembersViewSet(viewsets.ModelViewSet):
    queryset = models.Members.objects.all()
    serializer_class = serializers.MembersSerializer


class AreaViewSet(viewsets.ModelViewSet):
    queryset = models.Area.objects.all()
    serializer_class = serializers.AreaSerializer


class ImageUpViewSet(viewsets.ModelViewSet):
    queryset = models.ImageUp.objects.all()
    serializer_class = serializers.ImageUpSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = models.Feedback.objects.all()
    serializer_class = serializers.FeedbackSerializer


class ImagesViewSet(viewsets.ModelViewSet):
    queryset = models.Images.objects.all()
    serializer_class = serializers.ImagesSerializer


class ImagesShowViewSet(viewsets.ModelViewSet):
    queryset = models.ImagesShow.objects.all()
    serializer_class = serializers.ImagesShowSerializer


class BlogCommentViewSet(viewsets.ModelViewSet):
    queryset = models.BlogComment.objects.all()
    serializer_class = serializers.BlogCommentSerializer


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = models.BlogPost.objects.all()
    serializer_class = serializers.BlogPostSerializer


class BlogCategoryViewSet(viewsets.ModelViewSet):
    queryset = models.BlogCategory.objects.all()
    serializer_class = serializers.BlogCategorySerializer
