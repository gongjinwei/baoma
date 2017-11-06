# -*- coding:UTF-8 -*-
from rest_framework import serializers
from . import models


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Admin
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Order
        fields = '__all__'


class PublishSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True,read_only=True)

    class Meta:
        model = models.Publish
        fields = '__all__'


class TasksSerializer(serializers.ModelSerializer):
    publishes = PublishSerializer(many=True,read_only=True)

    class Meta:
        model = models.Tasks
        fields = '__all__'


class StoresSerializer(serializers.ModelSerializer):
    tasks = TasksSerializer(many=True,read_only=True)

    class Meta:
        model = models.Stores
        fields = '__all__'


class SaddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Saddress
        fields = '__all__'


class MerchantsSerializer(serializers.ModelSerializer):
    stores = StoresSerializer(many=True,read_only=True)
    addresses = SaddressSerializer(many=True,read_only=True)

    class Meta:
        model = models.Merchants
        fields = '__all__'


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Page
        fields = '__all__'


class MembersSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True,read_only=True)

    class Meta:
        model = models.Members
        fields = '__all__'


class ModelsSerializer(serializers.ModelSerializer):
    member_id = MembersSerializer()

    class Meta:
        model = models.Models
        fields = '__all__'
