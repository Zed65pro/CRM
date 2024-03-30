from rest_framework import serializers

from base.serializers import UserSerializer
from .models import JobOrder, JobOrderImage

class JobOrderSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    optional_fields = ['location','status']

    class Meta:
        model = JobOrder
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at','created_by']

class JobOrderImageSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)
    job_order = JobOrderSerializer(read_only=True)

    class Meta:
        model = JobOrderImage
        fields = ['__all__']
        read_only_fields = ['created_at', 'updated_at','uploaded_by','job_order']