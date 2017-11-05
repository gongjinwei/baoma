# -*- coding:UTF-8 -*-
from django.contrib import admin

# Register your models here.

import datetime

from django.conf import settings
from rest_framework import status, exceptions
from rest_framework.authentication import BaseAuthentication,TokenAuthentication,get_authorization_header
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.utils.translation import ugettext_lazy as _

from django.core.cache import cache

EXPIRE_MINUTES = getattr(settings, "REST_FRAMEWORK_TOKEN_EXPIRE_MINUTES", 1)


class ObtainExpireAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            time_now = datetime.datetime.now()

            if created or token.created < time_now - datetime.timedelta(minutes=EXPIRE_MINUTES):
                token.delete()
                token = Token.objects.create(user=user)
                token.created = time_now
                token.save()
            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        cache_user = cache.get(key)
        if cache_user:
            return (cache_user, key)
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))
        if token.created < datetime.datetime.now() - datetime.timedelta(minutes=EXPIRE_MINUTES):
            token.delete()
            raise exceptions.AuthenticationFailed(_('Token has expired then delete.'))

        if token:
            cache.set(key, token.user, EXPIRE_MINUTES * 60)
        return (token.user, token)

