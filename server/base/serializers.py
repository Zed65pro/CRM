# service/serializers.py
from rest_framework import serializers
from .models import Service, Customer
from django.contrib.auth.models import User  # Import User model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email','is_staff']
class ServiceSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'price', 'duration_months', 'created_at', 'updated_at', 'created_by']
        read_only_fields = ['created_at', 'updated_at', 'created_by']

class CustomerSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    services = ServiceSerializer(many=True, read_only=True)
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'address', 'phone_number', 'created_at', 'updated_at', 'created_by', 'services']
        read_only_fields = ['created_at', 'updated_at', 'created_by','services']
