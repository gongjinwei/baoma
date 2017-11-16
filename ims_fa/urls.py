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
from django.conf.urls import url
from . import views

router = DefaultRouter()
# router.register(r'admin', views.AdminViewSet)
router.register(r'tasks', views.TasksViewSet)
router.register(r'stores', views.StoresViewSet)
router.register(r'saddress', views.SaddressViewSet)
router.register(r'publish', views.PublishViewSet)
# router.register(r'page', views.PageViewSet)
router.register(r'order', views.OrderViewSet)
# router.register(r'models', views.ModelsViewSet)
router.register(r'merchants', views.MerchantsViewSet)
# router.register(r'members', views.MembersViewSet)
# router.register(r'area', views.AreaViewSet)
router.register(r'imageup', views.ImageUpViewSet)
# router.register(r'feedback', views.FeedbackViewSet)
# router.register(r'images', views.ImagesViewSet)
router.register(r'imagesshow', views.ImagesShowViewSet)
# router.register(r'blogcomment', views.BlogCommentViewSet)
# router.register(r'blogpost', views.BlogPostViewSet)
# router.register(r'blogcategory', views.BlogCategoryViewSet)
router.register(r'consumerecords', views.ConsumeRecordsViewSet)

urlpatterns = [
    url('^task-order/(?P<pk>[0-9]+)/$', views.TaskOrderView.as_view())
]

urlpatterns += router.urls
