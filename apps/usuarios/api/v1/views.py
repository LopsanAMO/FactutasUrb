# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes, api_view
from django.core.exceptions import ObjectDoesNotExist
from .serializers import (
    AddreesSerializer, FiscalSerializer, FiscalDetailSerializer,
    UserInfoSerializer, UserSerializer, CreateUserSerializer,
    LoginSerializer, BasicUserSerializer
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
            username = request.data['basic_info']['username']
        except KeyError:
            request.data['username'] = re.sub(
                "[!@#$%^&*()[]{};:,./<>?\|`~-=_+]",
                " ",
                request.data['email'][:(request.data['email'].find('@'))]
            )
            request.data['username'] = '{}{}'.format(
                request.data['username'],
                random.randrange(10**8)
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
        except ObjectDoesNotExist as e:
            return req_inf.status(e.args[0], status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return req_inf.status(e.args[0], status.HTTP_400_BAD_REQUEST)


class FiscalAPIView(APIView):
    def get(self, request):
        req_inf = RequestInfo()
        try:
            return Response(UserInfoSerializer(request.user).data)
        except ObjectDoesNotExist as e:
            return req_inf.status(e.args[0], status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return req_inf.status(e.args[0], status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        req_inf = RequestInfo()
        errors = []
        try:
            fiscal_serializer = FiscalSerializer(
                Fiscal.objects.get(user=request.user),
                data=request.data.get('fiscal')
            )
            address_serializer = AddreesSerializer(
                Address.objects.get(fiscal_id=fiscal_serializer.instance.id),
                data=request.data.get('address')
            )
            if fiscal_serializer.is_valid() and address_serializer.is_valid():
                fiscal_serializer.save()
                address_serializer.save()
                return req_inf.status()
            else:
                try:
                   errors.append(fiscal_serializer.errors)
                except Exception:
                    pass
                try:
                    errors.append(address_serializer.errors)
                except Exception:
                    pass
                return req_inf.status(errors, status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            return req_inf.status(e.args[0], status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return req_inf.status(e.args[0], status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((AllowAny, ))
def create_simple_user(request):
    import pudb; pudb.set_trace()
    import random
    import re
    req_inf = RequestInfo()
    try:
        try:
            username = request.data['basic_info']['username']
        except KeyError:
            request.data['basic_info']['username'] = re.sub(
                "[!@#$%^&*()[]{};:,./<>?\|`~-=_+]",
                " ",
                request.data['basic_info']['email'][:(request.data['basic_info']['email'].find('@'))]
            )
            request.data['basic_info']['username'] = '{}{}'.format(
                request.data['basic_info']['username'],
                random.randrange(10**8)
            )
        except Exception:
            pass
        user_serializer = BasicUserSerializer(data=request.data.get('basic_info'))
        if user_serializer.is_valid():
            user_serializer.save()
            request.data['fiscal']['user'] = user_serializer.instance.id
            fiscal_serializer = FiscalSerializer(
                Fiscal.objects.get(user_id=user_serializer.instance.id),
                data=request.data.get('fiscal')
            )
            if fiscal_serializer.is_valid():
                fiscal_serializer.save()
                request.data['address']['fiscal'] = fiscal_serializer.instance.id
                address_serializer = AddreesSerializer(
                    Address.objects.get(fiscal_id=fiscal_serializer.instance.id),
                    data=request.data.get('address'))
                if address_serializer.is_valid():
                    address_serializer.save()
                    return req_inf.status()
    except Exception as e:
        return req_inf.status(e.args[0], status.HTTP_400_BAD_REQUEST)
