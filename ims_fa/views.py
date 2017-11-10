from django.shortcuts import render

# Create your views here.
import datetime
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets,status,filters,generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
import copy

from . import models
from . import serializers


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
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filter_fields =['task_platform','task_name']
    search_fields =['task_name','goods_title']
    ordering_fields=['task_platform']

    def create(self, request, *args, **kwargs):
        task_serializer = self.get_serializer(data=request.data)
        task_serializer.is_valid(raise_exception=True)
        self.perform_create(task_serializer)
        altered_data = copy.deepcopy(request.data)
        altered_data.update({'task_id': task_serializer.instance.pk})
        publish_serializer = serializers.PublishSerializer(data=altered_data)
        publish_serializer.is_valid(raise_exception=True)
        self.perform_create(publish_serializer)
        headers = self.get_success_headers(task_serializer.data)
        return Response(task_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class StoresViewSet(viewsets.ModelViewSet):
    queryset = models.Stores.objects.all()
    serializer_class = serializers.StoresSerializer


class SaddressViewSet(viewsets.ModelViewSet):
    queryset = models.Saddress.objects.all()
    serializer_class = serializers.SaddressSerializer


class PublishViewSet(viewsets.ModelViewSet):
    queryset = models.Publish.objects.all()
    serializer_class = serializers.PublishSerializer


class PageViewSet(viewsets.ModelViewSet):
    queryset = models.Page.objects.all()
    serializer_class = serializers.PageSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer


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
