from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets,permissions
from rest_framework.authentication import TokenAuthentication

from . import models
from . import serializers


class AdminViewSet(viewsets.ModelViewSet):
    queryset = models.Admin.objects.all()
    serializer_class = serializers.AdminSerializer


class TasksViewSet(viewsets.ModelViewSet):
    queryset = models.Tasks.objects.all()
    serializer_class = serializers.TasksSerializer


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
