import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'


class Fiscal(models.Model):
    user = models.OneToOneField(User, null=False, blank=True, on_delete=models.CASCADE)
    rfc = models.CharField(max_length=13, blank=False, null=False, verbose_name='RFC')
    business_name = models.CharField(max_length=200, blank=False, null=False, verbose_name='Razon Social')
    physical_person = models.BooleanField(default=True, blank=False, null=False, verbose_name='Persona Fisica')

    @classmethod
    def create(cls, user):
        _fiscal = cls(rfc='-', business_name='-', user=user)
        _fiscal.save()
        return _fiscal

    def __str__(self):
        return "{}".format(self.user.username)

    class Meta:
        verbose_name = 'Datos Fiscales'
        verbose_name_plural = 'Datos Fiscales'


class Address(models.Model):
    fiscal = models.OneToOneField(Fiscal, blank=True, null=False, on_delete=models.CASCADE)
    street = models.CharField(verbose_name='Calle', max_length=128)
    street_number = models.CharField(verbose_name='Numero de domicilio', max_length=10, blank=True, null=True)
    zip_code = models.CharField(verbose_name='Codigo Postal', max_length=5)
    neighborhood = models.CharField(verbose_name='Delegación', max_length=128)
    city = models.CharField(verbose_name='Ciudad', max_length=128)
    state = models.CharField(verbose_name='Estado', max_length=128)

    @classmethod
    def create(cls, fiscal):
        _address = cls(
            fiscal=fiscal,
            street='-',
            street_number='-',
            zip_code='-',
            neighborhood='-',
            city='-',
            state='-'
        )
        _address.save()

    def __str__(self):
        return '{}'.format(self.fiscal.user.username)

    class Meta:
        verbose_name = 'Direccion Fiscal'
        verbose_name_plural = 'Direccion Fiscal'
