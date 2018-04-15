import uuid
from django.db import models
from usuarios.models import User


class Concept(models.Model):
    product_key = models.CharField(
        verbose_name='Clave del producto o servicio',
        max_length=30,
        blank=False,
        null=False
    )
    quantity = models.IntegerField(
        verbose_name='Cantidad',
        blank=False,
        null=False
    )
    description = models.CharField(
        verbose_name='Descripcion',
        max_length=30,
        blank=False,
        null=False
    )
    amount = models.CharField(
        verbose_name='Monto de Factura',
        max_length=16,
        blank=False,
        null=False
    )
    
    def __str__(self):
        return '{}-{}'.format(self.product_key, self.amount)

    class Meta:
        verbose_name = 'Concepto'
        verbose_name_plural = 'Conceptos'


class Factura(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    emisor  = models.ForeignKey(
        User, 
        related_name='emisor',
        on_delete=models.CASCADE,
        verbose_name='Emisor',
        blank=True,
        null=False
    )
    receiver = models.ForeignKey(
        User,
        related_name='receptor',
        on_delete=models.CASCADE,
        verbose_name='Receptor',
        blank=True,
        null=False
    )
    date_expedition = models.DateTimeField(
        verbose_name='Fecha de expedicion',
        blank=False,
        null=False
    )
    moneda = models.CharField(
        max_length=4,
        blank=False,
        null=False
    )
    folio = models.CharField(
        max_length=20,
        blank=False,
        null=False
    )
    way_to_pay = models.CharField(
        verbose_name='Forma de Pago',
        max_length=30,
        blank=False,
        null=False
    )
    concepts = models.ManyToManyField(
        Concept,
        verbose_name='Comceptos',
        blank=True
    )

    def  __str__(self):
        return 'Factura {}-{}'.format(self.emisor.id, self.folio)
