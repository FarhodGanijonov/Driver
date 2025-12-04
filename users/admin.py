# Users/admin.py
from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from django.contrib.gis.db import models as gis_models
from django import forms
from users.models import AbstractUser

# Client va Driver userlar uchun admin.py
@admin.register(AbstractUser)
class UserAdmin(OSMGeoAdmin):
    list_display = ('id', 'full_name', 'phone', 'role', 'status', 'is_online')
    list_filter = ('role', 'status', 'is_online')
    search_fields = ('full_name', 'phone')

    map_width = 1100
    map_height = 600
    default_lat = 41.311081
    default_lon = 69.279759
    default_zoom = 12

    formfield_overrides = {
        gis_models.PointField: {"widget": forms.TextInput(attrs={"placeholder": "lat, lon"})},
    }

