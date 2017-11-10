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
from ims_fa.views import ObtainExpireAuthToken
from ims_fa.urls import router
from django.views.static import serve
from .settings import MEDIA_ROOT ,STATIC_ROOT

urlpatterns = [
    url(r'^admin/',admin.site.urls),
    url(r'^api-token-auth/',ObtainExpireAuthToken.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/',include(router.urls)),
    url(r'^media/(?P<path>.*$)',serve,{'document_root': MEDIA_ROOT}),
    # url(r'^static/(?P<path>.*$)',serve,{'document_root': STATIC_ROOT}),
    url(r'^docs/',include_docs_urls(title='BaoMa API'))
]
