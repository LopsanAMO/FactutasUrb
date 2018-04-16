# -*- coding: utf-8 -*-
import json
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from .serializers import (
    AddreesSerializer, FiscalSerializer, FiscalDetailSerializer,
    UserInfoSerializer, UserSerializer, CreateUserSerializer,
    LoginSerializer
)
from usuarios.models import User, Fiscal, Address
from usuarios.handlers import generate_jwt
from utils.helpers import RequestInfo


class UserAPIView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        """Creates user accounts
        :param email: str
        :param first_name: str
        :param last_name: str
        :param password: str
        :return token: jwt_token
        """
        import re
        req_inf = RequestInfo()
        try:
            if request.data['username'] in [None, '', ' ']:
                request.data['username'] = re.sub(
                    "[!@#$%^&*()[]{};:,./<>?\|`~-=_+]",
                    " ",
                    request.data['email'][:(request.data['email'].find('@'))]
                )
        except Exception:
            pass
        try:
            serializer = CreateUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'token': generate_jwt(serializer.instance)
                })
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return req_inf.status(e.args[0], status.HTTP_400_BAD_REQUEST)
