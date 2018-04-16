from django.urls import path, include
from usuarios.api.v1 import urls as UserUrls
from facturas.api.v1 import urls as FacturasUrls


urlpatterns = [
    path('v1/users/', include(UserUrls)),
    path('v1/bills/', include(FacturasUrls))
]
