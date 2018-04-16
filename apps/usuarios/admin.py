from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Fiscal, Address


@admin.register(User)
class UserAdmin(UserAdmin):
    pass


@admin.register(Fiscal)
class FiscalAdmin(admin.ModelAdmin):
    pass


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass