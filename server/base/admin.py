# service/admin.py
from django.contrib import admin
from .models import Service,Customer

admin.site.register(Service)
admin.site.register(Customer)
