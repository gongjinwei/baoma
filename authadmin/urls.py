# -*- coding:UTF-8 -*-
from rest_framework import routers

from . import views

user_router = routers.DefaultRouter()
user_router.register(r'users',views.UserViewSet)
user_router.register(r'groups',views.GroupViewSet)