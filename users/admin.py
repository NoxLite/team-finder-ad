from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ('email',)

    search_fields = ('email', 'name', 'surname')
    
    list_display = (
        'email',
        'name',
        'surname',
        'phone',
        'is_staff',
        'is_active'
    )
    list_editable = (
        'is_staff',
        'is_active'
    )
