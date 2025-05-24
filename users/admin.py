from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'phone_number', 'cities', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'cities')
    search_fields = ('email', 'username', 'phone_number')
    ordering = ('email',)
