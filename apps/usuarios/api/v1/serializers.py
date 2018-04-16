import rest_auth.serializers
from rest_framework import serializers
from usuarios.models import User, Fiscal, Address
from utils.helpers import ErrorMesages


class AddreesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('street', 'street_number', 'zip_code', 'neighborhood', 'city', 'state')


class FiscalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fiscal
        fields = ('rfc', 'business_name')


class FiscalDetailSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()

    class Meta:
        model = Fiscal
        fields = ('rfc', 'business_name', 'address')

    def get_address(self, obj):
        return AddreesSerializer(Address.objects.get(fiscal_id=obj.id)).data


class UserInfoSerializer(serializers.ModelSerializer):
    fiscal_information = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'fiscal_information')

    def get_fiscal_information(self, obj):
        return FiscalDetailSerializer(Fiscal.objects.get(user_id=obj.id)).data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class CreateUserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        ErrorMesages().validate_email(value)
        return value


class LoginSerializer(rest_auth.serializers.LoginSerializer):
    def get_fields(self):
        fields = super(LoginSerializer, self).get_fields()
        fields['email'] = fields['username']
        del fields['username']
        return fields
