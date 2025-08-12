# clickstream/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, ClickEvent

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active','is_staff','is_superuser','groups','user_permissions')}),
        ('Important dates', {'fields': ('last_login','date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','first_name','last_name','email','password1','password2'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username','email','first_name','last_name')

@admin.register(ClickEvent)
class ClickEventAdmin(admin.ModelAdmin):
    list_display = ('event_type','path','user','timestamp')
    list_filter = ('event_type', 'timestamp')
    search_fields = ('path','user__username','user__email')
