from rest_framework import serializers

from apps.authentication.models import User
from apps.authentication.serializers import EmailSerializer, password_validation
from apps.common import validation_messages


class VerifyCodeSerializer(EmailSerializer):
    """
    serializer class for code verification
    """
    email_code = serializers.CharField(
        required=True, max_length=6, min_length=6,
        error_messages=validation_messages.VALIDATION['email_verification_otp']
    )

    def validate(self, attrs):
        """
        validate email & email code for forgot password
        :param attrs: request attr
        :return: attrs
        """
        email = attrs.get("email")
        otp_code = attrs.get("email_code")
        if not User.objects.filter(email=email.lower(), password_otp=otp_code).exists():
            raise serializers.ValidationError({
                'invalid': validation_messages.ERROR_MESSAGE['verification_otp']['invalid']
            })
        return attrs

    class Meta:
        """
        Metaclass for VerifyCodeSerializer
        """
        model = User
        fields = ['email', 'email_code']


class SetPasswordSerializer(serializers.ModelSerializer):
    """
    Serializer class for set new password
    """
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True, min_length=validation_messages.CHAR_LIMIT_SIZE['pass_min'],
        max_length=validation_messages.CHAR_LIMIT_SIZE['pass_max'],
        validators=[password_validation],
        error_messages=validation_messages.VALIDATION['password']
    )

    def validate(self, attrs):
        """
        validate token & token code
        :param attrs: request attr
        :return: attrs
        """
        token = attrs.get("token")
        if not User.objects.filter(password_hashcode=token).exists():
            raise serializers.ValidationError({
                'token': validation_messages.ERROR_MESSAGE['verification_otp']['invalid']
            })
        return attrs

    class Meta:
        """
        Class meta for SetPasswordSerializer
        """
        model = User
        fields = ['token', 'new_password']
