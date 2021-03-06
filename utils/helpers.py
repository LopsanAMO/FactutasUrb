import re
import jwt
import json
from django.shortcuts import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from usuarios.models import User


class RequestInfo(object):
    def __init__(self, message=None, status=status.HTTP_400_BAD_REQUEST):
        self.empty = empty_list = ['', ' ', None]
        self.data = {
            'status': status,
            'detail': message
        }

    def status(self, message='', status=status.HTTP_200_OK):
        self.data['status'] = status
        self.data['detail'] = message
        return self.return_status(self.data)

    def return_status(self, data=None):
        if data is not None and data != self.data:
            self.data['data'] = data
        return HttpResponse(
            json.dumps(self.data),
            content_type='application/json',
            status=data['status']
        )


class ErrorMesages(object):
    var_required = ''
    var_invalid = ''

    def validate_email(self, email):
        try:
            user = User.objects.get(email=email)
            raise serializers.ValidationError('Email ya registrado')
        except ObjectDoesNotExist:
            return email
        except Exception as e:
            raise serializers.ValidationError(e)
        return email
