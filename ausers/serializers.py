from rest_framework import serializers

from ausers.models import User
from common.serializers import ThumbnailerJSONSerializer


class AuserSerializer(serializers.ModelSerializer):
    profile_picture = ThumbnailerJSONSerializer(required=False, allow_null=True, alias_target='users')

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'stripe_id',
            'subscription_status',
            'profile_picture',
        )
        read_only_fields = ('username', 'email',)


class CreateUserSerializer(serializers.ModelSerializer):
    profile_picture = ThumbnailerJSONSerializer(required=False, allow_null=True, alias_target='users')
    sex = serializers.CharField(max_length=15, allow_blank=True, required=False)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, user):
        return user.get_tokens()

    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        user = User.objects.create_user(**validated_data)

        return user

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'phone_number',
            'password',
            'first_name',
            'last_name',
            'sex',
            'stripe_id',
            'tokens',
            'profile_picture',
        )
        read_only_fields = ('tokens',)
        extra_kwargs = {'password': {'write_only': True}}
