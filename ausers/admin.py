from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from ausers.models import User, NoneExistNumbers, ConversationHistory


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (
            _('Personal info'),
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'email',
                    'phone_number',
                    'subscription_status',
                    'stripe_id',
                )
            },
        ),
        (_('Profile image'), {'fields': ('profile_picture',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ("email", "first_name", "last_name", "stripe_id", "subscription_status")


admin.site.register(NoneExistNumbers)
admin.site.register(ConversationHistory)
