from django.contrib import admin
from .models import UserCart

# Register your models here.
@admin.register(UserCart)
class UserCartAdmin(admin.ModelAdmin):
    list_display = ['user', 'items']