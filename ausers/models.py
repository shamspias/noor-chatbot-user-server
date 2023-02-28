import uuid
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
from easy_thumbnails.fields import ThumbnailerImageField
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.utils import timezone

from common.helpers import build_absolute_uri
from notifications.services import notify, ACTIVITY_USER_RESETS_PASS
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    """
    reset_password_path = reverse('password_reset:reset-password-confirm')
    context = {
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': build_absolute_uri(f'{reset_password_path}?token={reset_password_token.key}'),
    }

    notify(ACTIVITY_USER_RESETS_PASS, context=context, email_to=[reset_password_token.user.email])


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(username=email, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        # if extra_fields['sex']:
        #     extra_fields.pop('sex')
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(_("phone number"), max_length=35, blank=True, null=True, unique=True)
    profile_picture = ThumbnailerImageField('ProfilePicture', upload_to='profile_pictures/', blank=True, null=True)
    email = models.EmailField(_("email address"), unique=True)
    subscription_status = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=250, blank=True, null=True)
    user_time_zone = models.DateField(default=timezone.now())
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_tokens(self):
        refresh = RefreshToken.for_user(self)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def __str__(self):
        return self.username

    def check_user_status(self):
        return self.subscription_status


class NoneExistNumbers(models.Model):
    """
    model that contain numbers
    """
    number = models.CharField(max_length=50, blank=True, null=True)
    is_user = models.BooleanField(default=False)
    text_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'New Number'
        verbose_name_plural = 'New Numbers'

    def __str__(self):
        if self.number is not None:
            return self.number
        else:
            return "No number"


class ConversationHistory(models.Model):
    """
    To store the conversation history
    """
    phone_number = models.ForeignKey(NoneExistNumbers, on_delete=models.CASCADE)
    conversation_id = models.PositiveIntegerField(default=0)
    user_input = models.TextField(blank=True, null=True)
    chatbot_response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Conversation History'
        verbose_name_plural = 'Conversation History'
        ordering = ('-created_at',)

    def __str__(self):
        return self.phone_number.number

    def last_conversation_id(self):
        """
        to retrieve the last conversation id
        """
        try:
            last_conversation = self.objects.latest('conversation_id')
            return last_conversation.conversation_id
        except self.DoesNotExist:
            return None
