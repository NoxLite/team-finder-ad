from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
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

admin.site.register(User, UserAdmin)