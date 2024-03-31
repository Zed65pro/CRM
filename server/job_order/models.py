from django.contrib.gis.db import models
from django.core.validators import RegexValidator, MinLengthValidator, EmailValidator
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point

DEFAULT_LOCATION = Point(35.2154, 31.8974)#RAMMALLAH
class JobOrder(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('complete', 'Complete'),
    )

    name = models.CharField(max_length=255,unique=True, validators=[MinLengthValidator(1)])
    description = models.TextField(blank=True)
    area = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=9, validators=[RegexValidator(r'^\d{9}$', message="Phone number must be 9 digits")])
    email = models.EmailField(validators=[EmailValidator()])
    location = models.PointField(null=DEFAULT_LOCATION, blank=True)
    feedback = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class JobOrderImage(models.Model):
    job_order = models.ForeignKey(JobOrder, related_name='images', on_delete=models.CASCADE)
    file = models.FileField(upload_to='media/job_order_files/')
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.file.name