"""
Authentication app serializer used for registration & login etc. purpose.
"""
import re

from rest_framework import serializers

from apps.authentication.authentication_email import user_registration_mail
from apps.authentication.models import User
from apps.common import validation_messages, constants
from apps.common.utils import generate_rnd_number, generate_hash_code


class SignUpSerializer(serializers.ModelSerializer):
    """
    Validate signup data and creating a new user.
    create: validate request data for auth-user-instance creation
    Return auth-user-instance object
    to_representation :
    Return modified serializer (add new keys-values required for processing, and those keys are not
    required for processing, remove from serializer data) data of auth-user-instance
    """
    first_name = serializers.CharField(
        required=True, max_length=validation_messages.CHAR_LIMIT_SIZE['first_name_max'],
        error_messages=validation_messages.VALIDATION['first_name']
    )
    last_name = serializers.CharField(
        required=True, max_length=validation_messages.CHAR_LIMIT_SIZE['last_name_max'],
        error_messages=validation_messages.VALIDATION['last_name']
    )
    username = serializers.CharField(
        required=True, max_length=validation_messages.CHAR_LIMIT_SIZE['max_username'],
        min_length=validation_messages.CHAR_LIMIT_SIZE['min_username'],
        error_messages=validation_messages.VALIDATION['username']
    )
    email = serializers.EmailField(
        required=True,  error_messages=validation_messages.VALIDATION['email']
    )
    password = serializers.CharField(
        required=True, min_length=validation_messages.CHAR_LIMIT_SIZE['pass_min'],
        max_length=validation_messages.CHAR_LIMIT_SIZE['pass_max'],
        error_messages=validation_messages.VALIDATION['password']
    )

    @staticmethod
    def validate_password(value):
        """
        To validate password
        :param value: value
        :return: error or value
        """
        value = value.strip()
        if re.match(constants.REGEX_VALID['password'], value):
            return value
        return serializers.ValidationError(validation_messages.VALIDATION['password']['pattern'])

    @staticmethod
    def validate_email(value):
        """
        TO validate email
        :param value:
        :return: error or value
        """
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError(validation_messages.ERROR_MESSAGE['email']['exists'])
        return value

    def to_representation(self, obj):
        """
        get the original representation modified password
        :param obj: auth-user instance
        :return: modified instance
        """
        attr = super().to_representation(obj)
        if 'password' in attr:
            attr.pop('password')
        return attr

    def create(self, validated_data):
        """
        to add a new user
        :return: instance
        """
        email_otp = generate_rnd_number()
        password = validated_data.pop('password')
        instance = User.objects.create(**validated_data)
        email_hash = generate_hash_code(instance.id)
        instance.email_verification_token = email_hash
        instance.email_verification_otp = email_otp
        instance.set_password(password)
        instance.is_active = True
        instance.save()
        # sending mail
        user_registration_mail(instance.id)
        return instance

    class Meta:
        """
        Meta class for SignUpSerializer
        """
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']