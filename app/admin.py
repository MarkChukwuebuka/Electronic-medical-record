from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


# Register your models here.
admin.site.register(Worker)
admin.site.register(Patient)
admin.site.register(MedUser, UserAdmin)