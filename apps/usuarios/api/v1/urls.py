from django.urls import path, include
from rest_auth.views import LoginView
from .views import UserAPIView, FiscalAPIView, create_simple_user

urlpatterns = [
    path('', UserAPIView.as_view(), name='users'),
    path('create-simple-user/', create_simple_user, name='simple_user'),
    path('login/', LoginView.as_view(), name='user_login'),
    path('fiscal-info/', FiscalAPIView.as_view(), name='fiscal_info')
]
