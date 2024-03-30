from django.contrib import admin

from geo.models import WorldBorder
from leaflet.admin import LeafletGeoAdminMixin

class Hezkel(LeafletGeoAdminMixin, admin.ModelAdmin):
     pass

# Register your models here.
admin.site.register(WorldBorder, Hezkel)