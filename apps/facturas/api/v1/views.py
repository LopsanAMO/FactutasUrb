# -*- coding: utf-8 -*-
import json
import os
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import HttpResponse
from wsgiref.util import FileWrapper
from django.conf import settings
from .serializers import FacturaSerializer, FacturaDetailSerializer
from facturas.models import Factura
from usuarios.handlers import generate_jwt
from utils.helpers import RequestInfo
from dicttoxml import dicttoxml


@api_view(['GET'])
def bills(request):
    req_inf = RequestInfo()
    data = {
        "emisor_bill": FacturaSerializer(
            Factura.objects.filter(emisor=request.user),
            many=True).data,
        "receiver_bill": FacturaSerializer(
            Factura.objects.filter(receiver=request.user),
            many=True).data,
    }
    return Response({'data': data})


@api_view(['GET'])
@permission_classes((AllowAny, ))
def get_bill(request):
    req_inf = RequestInfo()
    try:
        bill = Factura.objects.get(id=request.GET.get('bill'))
        name = 'bill-{}{}.xml'.format(request.user.username, bill.id)
        with open(name, 'wb') as f:
            f.write(dicttoxml(FacturaDetailSerializer(bill).data, attr_type=False))
        bill_file = open('{}/{}'.format(settings.BASE_DIR, name), 'rb')
        response = HttpResponse(FileWrapper(bill_file), content_type='application/xml')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(name)
        os.remove('{}/{}'.format(settings.BASE_DIR, name))
        return response
    except ObjectDoesNotExist as e:
        return req_inf.status(e.args[0], status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return req_inf.status(e.args[0], status.HTTP_400_BAD_REQUEST)
