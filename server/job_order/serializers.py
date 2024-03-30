from rest_framework import serializers

from base.serializers import UserSerializer
from .models import JobOrder, JobOrderImage

class JobOrderSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = JobOrder
        fields = '__all__'

class JobOrderImageSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)
    class Meta:
        model = JobOrderImage
        fields = ['__all__']