from rest_framework.authtoken import views
from rest_framework_jwt.views import refresh_jwt_token
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from api import urls as APIV1Urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(APIV1Urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path(
        'api-auth/',
        include(
            'rest_framework.urls',
            namespace='rest_framework')),
    path('refresh-token/', refresh_jwt_token),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
