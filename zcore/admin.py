from django.contrib import admin
from .models import Description
from django.contrib.auth.models import User


admin.site.register(Description)
admin.site.site_header = "CBN AI"

