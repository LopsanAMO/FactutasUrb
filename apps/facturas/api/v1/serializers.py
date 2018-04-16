from rest_framework import serializers
from facturas.models import Factura, Concept
from usuarios.api.v1.serializers import FiscalFacturaSerializer
from usuarios.models import Fiscal


class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = ('_id', 'date_expedition')


class ConceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concept
        fields = ('product_key', 'quantity', 'description', 'amount')


class SimpleFacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = ('emisor', 'receiver', 'date_expedition', 'coin', 'folio', 'way_to_pay')


class FacturaDetailSerializer(serializers.ModelSerializer):
    emisor = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()
    concepts = serializers.SerializerMethodField()

    class Meta:
        model = Factura
        fields = ('emisor', 'receiver', 'date_expedition', 'coin', 'folio', 'way_to_pay', 'concepts')

    def get_emisor(self, obj):
        return FiscalFacturaSerializer(Fiscal.objects.get(user_id=obj.emisor.id)).data

    def get_receiver(self, obj):
        return FiscalFacturaSerializer(Fiscal.objects.get(user_id=obj.receiver.id)).data

    def get_concepts(self, obj):
        return ConceptSerializer(obj.concepts, many=True).data