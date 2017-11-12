# -*- coding:UTF-8 -*-
import datetime
from django.conf import settings
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication,SessionAuthentication

from django.utils.translation import ugettext_lazy as _

from django.core.cache import cache


EXPIRE_MINUTES=getattr(settings,'REST_FRAMEWORK_TOKEN_EXPIRE_MINUTES',1)


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


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return