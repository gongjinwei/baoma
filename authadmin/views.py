from django.shortcuts import render

from rest_framework import permissions,viewsets
from rest_framework.permissions import BasePermission


from .serializers import User,Group,UserSerializer,GroupSerialize

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope,TokenHasScope

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerialize


