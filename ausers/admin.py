from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import EmailField
from ausers.models import User, NoneExistNumbers, ConversationHistory


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)
        field_classes = {"email": EmailField}


@admin.register(User)
class UserAdmin(UserAdmin):
    form = CustomUserCreationForm
    add_form = CustomUserCreationForm
    # fieldsets = (
    #     (None, {'fields': ('username', 'password')}),
    #     (
    #         _('Personal info'),
    #         {
    #             'fields': (
    #                 'first_name',
    #                 'last_name',
    #                 'email',
    #                 'phone_number',
    #                 'subscription_status',
    #                 'stripe_id',
    #             )
    #         },
    #     ),
    #     (_('Profile image'), {'fields': ('profile_picture',)}),
    #     (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    #     (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    # )
    search_fields = ('email', 'stripe_id')
    list_display = ("email", "first_name", "last_name", "stripe_id", "subscription_status")

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        return self.form


class NoneExistNumberAdmin(admin.ModelAdmin):
    """
    Admin functionality for None Exist Number
    """

    list_display = ("number", "is_user", "text_count")


admin.site.register(NoneExistNumbers, NoneExistNumberAdmin)
admin.site.register(ConversationHistory)
