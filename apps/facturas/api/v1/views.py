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
from .serializers import FacturaSerializer, FacturaDetailSerializer, SimpleFacturaSerializer, ConceptSerializer
from facturas.models import Factura
from usuarios.handlers import generate_jwt
from usuarios.models import Fiscal
from utils.helpers import RequestInfo
from dicttoxml import dicttoxml


@api_view(['GET'])
def bills(request):
    """get list of disponible bills
    """
    req_inf = RequestInfo()
    data = {
        "emisor_bill": FacturaSerializer(
            Factura.objects.filter(emisor=request.user),
            many=True).data,
        "receiver_bill": FacturaSerializer(
            Factura.objects.filter(receiver=request.user),
            many=True).data
    }
    return Response(data)


@api_view(['GET'])
@permission_classes((AllowAny, ))
def get_bill(request):
    """download bill
    """
    req_inf = RequestInfo()
    try:
        bill = Factura.objects.get(_id=request.GET.get('bill'))
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


@api_view(['POST'])
def create_bill(request):
    """create bill
    :param basic_information: (dict)
		:param emisor_rfc: (str)
		:param receiver_rfc: (str)
		:param date_expedition: (date)
		:param coin: (str)
		:param folio: (str)
		:param way_to_pay: (str)
	:param concepts: (list of dicts)
        :param product_key: (str)
        :param quantity: (str)
        :param description: (str)
        :param amount: (str)
    """
    req_inf = RequestInfo()
    errors = []
    concepts = []
    try:
        request.data['basic_information']['emisor'] = Fiscal.objects.get(
            rfc=request.data['basic_information']['emisor_rfc']).user.id
        request.data['basic_information']['receiver'] = Fiscal.objects.get(
            rfc=request.data['basic_information']['receiver_rfc']).user.id
        request.data['basic_information'].pop('emisor_rfc')
        request.data['basic_information'].pop('receiver_rfc')
        for data in request.data.get('concepts'):
            concept_serializer = ConceptSerializer(data=data)
            if concept_serializer.is_valid():
                concept_serializer.save()
                concepts.append(concept_serializer.instance)
            else:
                errors.append(concept_serializer.errors)
        if len(errors) == 0:
            bill_serializer = SimpleFacturaSerializer(data=request.data.get('basic_information'))
            if bill_serializer.is_valid():
                bill_serializer.save()
                for con in concepts:
                    bill_serializer.instance.concepts.add(con)
                    bill_serializer.save()
                return req_inf.status()
            else:
                return req_inf.status(bill_serializer.errors, status.HTTP_400_BAD_REQUEST)
        else:
            return req_inf.return_status(errors)
    except Exception as e:
        return req_inf.status(e.args[0], status.HTTP_400_BAD_REQUEST)
