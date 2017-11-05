from django.shortcuts import render
import datetime

from django.conf import settings
from rest_framework import permissions,viewsets,status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

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


EXPIRE_MINUTES = getattr(settings,"REST_FRAMEWORK_TOKEN_EXPIRE_MINUTES",1)


class ObtainExpireAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            time_now = datetime.datetime.now()

            if created or token.created<time_now -datetime.timedelta(minutes=EXPIRE_MINUTES):
                token.delete()
                token = Token.objects.create(user=user)
                token.created = time_now
                token.save()
            return Response({'token': token.key})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


obtain_expiring_auth_token = ObtainExpireAuthToken.as_view()