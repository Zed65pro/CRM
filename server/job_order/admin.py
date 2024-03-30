# service/admin.py
from .models import JobOrder
from django.contrib import admin
from leaflet.admin import LeafletGeoAdminMixin

class AdminJobOrder(LeafletGeoAdminMixin, admin.ModelAdmin):
     pass

# Register your models here.
admin.site.register(JobOrder, AdminJobOrder)