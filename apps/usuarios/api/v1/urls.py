from django.urls import path, include
from rest_auth.views import LoginView
from .views import UserAPIView, FiscalAPIView

urlpatterns = [
    path('', UserAPIView.as_view(), name='users'),
    path('login/', LoginView.as_view(), name='user_login'),
    path('fiscal-info/', FiscalAPIView.as_view(), name='fiscal_info')
]
