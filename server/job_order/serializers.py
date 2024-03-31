from rest_framework import serializers

from base.serializers import UserSerializer
from django.contrib.gis.geos import Point
from .models import JobOrder, JobOrderImage

DEFAULT_LOCATION = Point(35.2154, 31.8974)#RAMMALLAH
class JobOrderImageSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)

    class Meta:
        model = JobOrderImage
        fields = ['file','uploaded_by']
        read_only_fields = ['created_at','job_order','uploaded_by']
class JobOrderSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    images = JobOrderImageSerializer(many=True, read_only=True)
    longitude = serializers.SerializerMethodField(read_only=True)
    latitude = serializers.SerializerMethodField(read_only=True)


    def get_longitude(self, obj):
        if obj.location:
            return obj.location.x
        return None
    def get_latitude(self, obj):
        if obj.location:
            return obj.location.y
        return None
    optional_fields = ['location','status','longitude','latitude']

    class Meta:
        model = JobOrder
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at','created_by','location']
    def validate(self, attrs):
        if 'location' not in attrs:
            attrs['location'] = DEFAULT_LOCATION
        return attrs