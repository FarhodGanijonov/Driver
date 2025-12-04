# order/admin.py
from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from django.contrib.gis.db import models as gis_models
from django import forms
from .models import Order

# Order admin
@admin.register(Order)
class OrderAdmin(OSMGeoAdmin):
    list_display = ('id', 'client', 'driver', 'status', 'client_is_finished', 'driver_is_finished', 'created_at')
    list_filter = ('status', 'client_is_finished', 'driver_is_finished', 'created_at')
    search_fields = ('client__full_name', 'driver__full_name', 'description', 'gender')

    map_width = 1100
    map_height = 600
    default_lat = 41.311081
    default_lon = 69.279759
    default_zoom = 12

    formfield_overrides = {
        gis_models.PointField: {"widget": forms.TextInput(attrs={"placeholder": "lat, lon"})},
    }