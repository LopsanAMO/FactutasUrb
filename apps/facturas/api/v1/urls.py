from django.urls import path
from .views import bills, get_bill

urlpatterns = [
    path('', bills),
    path('get_bill/', get_bill)
]