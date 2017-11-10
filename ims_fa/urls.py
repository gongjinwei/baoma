# -*- coding:UTF-8 -*-
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'admin',views.AdminViewSet)
router.register(r'tasks',views.TasksViewSet)
router.register(r'stores',views.StoresViewSet)
router.register(r'saddress',views.SaddressViewSet)
router.register(r'publish',views.PublishViewSet)
router.register(r'page',views.PageViewSet)
router.register(r'order',views.OrderViewSet)
router.register(r'models',views.ModelsViewSet)
router.register(r'merchants',views.MerchantsViewSet)
router.register(r'members',views.MembersViewSet)
router.register(r'area',views.AreaViewSet)
router.register(r'imageup',views.ImageUpViewSet)

