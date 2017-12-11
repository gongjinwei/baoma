"""baoma URL Configuration

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
from django.conf.urls import url,include

from django.contrib import admin
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from django.views.static import serve
from django.views.generic.base import RedirectView
from .settings import MEDIA_ROOT ,STATIC_ROOT

from ims_fa.views import UserRegisterView,PasswordForgetView,ForgetSendView,RegisterSendView,ObtainExpireAuthToken

register_router = DefaultRouter()
register_router.register(r'register_send',RegisterSendView,base_name='register_send')
register_router.register(r'token',ObtainExpireAuthToken,base_name='token')
register_router.register(r'register_user',UserRegisterView,base_name='register_user')
register_router.register(r'forget_send',ForgetSendView,base_name='forget_send')
register_router.register(r'forget',PasswordForgetView,base_name='forget_password')


urlpatterns = [
    url(r'^admin/',admin.site.urls),
    # url(r'^api-token-auth/$',ObtainExpireAuthToken.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/',include('ims_fa.urls',namespace='api')),
    url(r'^open/',include(register_router.urls,namespace='open')),
    # url(r'^pandas/',include('authadmin.urls',namespace='pandas')),
    # url(r'^media/(?P<path>.*$)',serve,{'document_root': MEDIA_ROOT}),
    # url(r'^static/(?P<path>.*$)',serve,{'document_root': STATIC_ROOT}),
    url(r'^docs/',include_docs_urls(title='BaoMa API')),
    url(r'^favicon.ico$',RedirectView.as_view(url=r'media/favicon.ico'))
]
