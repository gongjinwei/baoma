# -*- coding:UTF-8 -*-
"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'merchants', views.MerchantsViewSet)
router.register(r'stores', views.StoresViewSet)
router.register(r'tasks', views.TasksViewSet)
router.register(r'order', views.OrderViewSet)
router.register(r'imageup', views.ImageUpViewSet)
router.register(r'saddress', views.SaddressViewSet)
router.register(r'consumerecords', views.ConsumeRecordsViewSet)
router.register(r'merchantrecharge', views.MerchantRechargeViewSet)
router.register(r'salesman',views.SalesmanViewSet)
router.register(r'orderRemind',views.OrderRemindView,base_name='orderRemind')
router.register(r'taskResult',views.TaskResultView,base_name='taskResult')

urlpatterns = router.urls
