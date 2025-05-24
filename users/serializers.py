from rest_framework import serializers
from .models import CustomUser
from school.serializers import PaymentSerializer


class CustomUserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'avatar',
            'cities',
            'confirmation_token',
            'is_active',
            'is_staff',
            'date_joined',
            'payments'
        ]
        extra_kwargs = {
            'password': {'write_only': True},  # Пароль не будет отображаться в API
            'confirmation_token': {'read_only': True}  # Токен только для чтения
        }
