from django.contrib import admin
from .models import User, UserTier
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _


admin.site.register(UserTier)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('tier', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )
