# -*- coding:UTF-8 -*-
from rest_framework.routers import DefaultRouter
from django.conf.urls import url,include
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
router.register(r'feedback',views.FeedbackViewSet)
router.register(r'images',views.ImagesViewSet)
router.register(r'imagesshow',views.ImagesShowViewSet)
router.register(r'blogcomment',views.BlogCommentViewSet)
router.register(r'blogpost',views.BlogPostViewSet)
router.register(r'blogcategory',views.BlogCategoryViewSet)


urlpatterns=[
    url('^task-order/(?P<pk>[0-9]+)/$',views.TaskOrderView.as_view())
]

urlpatterns +=router.urls
