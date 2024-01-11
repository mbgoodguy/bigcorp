from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')  # Добавьте 'is_active' здесь


# Перерегистрируйте UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
