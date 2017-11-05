# -*- coding:UTF-8 -*-
from django.contrib.auth.models import User,Group
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class GroupSerialize(serializers.ModelSerializer):
    class Meta:
        model = Group