from django.urls import path, include
from usuarios.api.v1 import urls as UserUrls


urlpatterns = [
    path('v1/users/', include(UserUrls))
]
