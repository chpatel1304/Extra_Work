# accounts/serializers.py

from rest_framework import serializers
from .models import Customer

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'mobile', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Customer(**validated_data)
        user.set_password(password)  # Hash the password
        user.save()
        return user
