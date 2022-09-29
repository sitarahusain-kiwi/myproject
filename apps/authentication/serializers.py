"""
Authentication app serializer used for registration & login etc. purpose.
"""
import re

from rest_framework import serializers

from apps.authentication.authentication_email import user_registration_mail
from apps.authentication.models import User
from apps.authentication.tokens import get_access_token
from apps.common import validation_messages, constants
from apps.common.utils import (
    generate_rnd_number, generate_hash_code, user_update_verify_otp_mail, check_user_instance
)


def email_validation(value):
    """
    To validate email exists or not
    :param value: email
    :return: error or value
    """
    if not check_user_instance(value):
        raise serializers.ValidationError(
            {'detail': validation_messages.ERROR_MESSAGE['email']['invalid']}
        )
    return value


class EmailSerializer(serializers.ModelSerializer):
    """
    Description: used for email
    """
    email = serializers.EmailField(
        required=True,
        validators=[email_validation],
        error_messages=validation_messages.VALIDATION['email']
    )

    class Meta:
        """
        Meta class for EmailSerializer
        """
        model = User
        fields = ('email', )


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Description: Used for common details of user
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

    class Meta:
        """
        Metaclass for User Detail Serializer
        """
        model = User
        fields = ['first_name', 'last_name', 'username']


class UserGetSerializer(UserDetailSerializer, EmailSerializer):
    """
    Serializer class to get user details
    """
    class Meta:
        """
        Class meta for SignUpSerializer
        """
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


def signup_email_validation(value):
    """
    TO validate email
    :param value:
    :return: error or value
    """
    if User.objects.filter(email=value.lower()).exists():
        raise serializers.ValidationError(validation_messages.ERROR_MESSAGE['email']['exists'])
    return value


def password_validation(value):
    """
    To validate password
    :param value: value
    :return: error or value
    """
    value = value.strip()
    if re.match(constants.REGEX_VALID['password'], value):
        return value
    return serializers.ValidationError(validation_messages.VALIDATION['password']['pattern'])


class SignUpSerializer(UserDetailSerializer):
    """
    Validate signup data and creating a new user.
    create: validate request data for auth-user-instance creation
    Return auth-user-instance object
    to_representation :
    Return modified serializer (add new keys-values required for processing, and those keys are not
    required for processing, remove from serializer data) data of auth-user-instance
    """
    email = serializers.EmailField(
        required=True,
        validators=[signup_email_validation],
        error_messages=validation_messages.VALIDATION['email']
    )
    password = serializers.CharField(
        required=True, min_length=validation_messages.CHAR_LIMIT_SIZE['pass_min'],
        max_length=validation_messages.CHAR_LIMIT_SIZE['pass_max'],
        validators=[password_validation],
        error_messages=validation_messages.VALIDATION['password']
    )

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


class AccountOtpVerificationSerializer(EmailSerializer):
    """
    Serializer class for account otp verification
    """
    email_verification_otp = serializers.CharField(
        required=True,
        error_messages=validation_messages.VALIDATION['email_verification_otp']
    )
    token = serializers.SerializerMethodField()

    def validate(self, value):
        """
        validate email
        """
        email = self.initial_data.get('email')
        otp = self.initial_data.get('email_verification_otp')
        if User.objects.filter(email=email, email_verified=True):
            raise serializers.ValidationError(
                {'detail': validation_messages.ERROR_MESSAGE['verification_otp']['verified']}
            )
        if not User.objects.filter(email_verification_otp=otp, email=email).exists():
            raise serializers.ValidationError(
                {'detail': validation_messages.ERROR_MESSAGE['verification_otp']['invalid']}
            )
        return value

    @staticmethod
    def get_token(value):
        """
        to get token
        """
        obj = User.objects.get(email=value['email'])
        obj.oauth2_provider_accesstoken.all().delete()
        user_token = get_access_token(obj)
        user_update_verify_otp_mail(obj)
        return user_token

    class Meta:
        """
        Meta class for AccountOtpVerificationSerializer
        """
        model = User
        fields = ['email_verification_otp', 'email', 'token']


class LoginSerializer(EmailSerializer):
    """
    Serializer class for user login
    """
    password = serializers.CharField(required=True, error_messages=validation_messages.VALIDATION['password'])
    token = serializers.SerializerMethodField()

    def validate(self, value):
        """
        Validate email
        :param value: user email
        :return: error or email
        """
        email = self.initial_data.get('email')
        password = self.initial_data.get('password')
        user = User.objects.get(email=email)
        if not user.check_password(password):
            raise serializers.ValidationError({'detail': validation_messages.ERROR_MESSAGE['password']['invalid']})
        if not user.is_active:
            raise serializers.ValidationError(validation_messages.ERROR_MESSAGE['user']['inactive'])
        if not user.email_verified:
            raise serializers.ValidationError(validation_messages.ERROR_MESSAGE['email']['not_verified'])
        value.update({"user": user})
        return value

    @staticmethod
    def get_token(obj):
        """
        to get token
        """
        return get_access_token(obj)

    class Meta:
        """
        Meta class for LoginSerializer
        """
        model = User
        fields = ['email', 'password', 'token']
