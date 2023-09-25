# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  # Import the default UserAdmin
from .models import UserAccount

class CustomUserAdmin(UserAdmin):
    list_display = ('email','name', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('email', 'name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','name','is_staff', 'password1', 'password2'),
        }),
    )

# Register the CustomUser model with the CustomUserAdmin
admin.site.register(UserAccount, CustomUserAdmin)
