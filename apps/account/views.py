"""
Account app views file
"""
from rest_framework import status

from apps.authentication.authentication_email import send_forgot_password_code
from apps.authentication.models import User
from apps.account.serializers import VerifyCodeSerializer, SetPasswordSerializer
from apps.authentication.serializers import EmailSerializer
from apps.common.app_messages import SUCCESS_MESSAGE
from apps.common.utils import generate_rnd_number, custom_response, custom_error_response, generate_hash_code
from apps.common.viewsets import CustomModelViewSet


class ForgotPasswordViewSet(CustomModelViewSet):
    """
    Forgot password view is used to set new password
    """
    http_method_names = ('post', )
    serializer_class = EmailSerializer

    def create(self, request, *args, **kwargs):
        """
        To send otp on email
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            instance = User.objects.filter(email=email).first()
            email_otp = generate_rnd_number()
            User.objects.filter(email=email).update(password_otp=email_otp)
            send_forgot_password_code(instance.id)
            return custom_response(data=request.data)
        return custom_error_response(status=status.HTTP_400_BAD_REQUEST, detail=serializer.errors)


class VerifyCodeViewSet(CustomModelViewSet):
    """
    Description: verify code for forgot password
    """
    http_method_names = ('post', )
    serializer_class = VerifyCodeSerializer

    def create(self, request, *args, **kwargs):
        """
        To verify code and generate token to reset password
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = request.data['email']
            user_obj = User.objects.filter(email__iexact=email).first()
            hash_token = generate_hash_code(user_obj.id)
            User.objects.filter(email__iexact=email).update(
                password_otp='', password_hashcode=hash_token
            )
            request.data['token'] = hash_token
            request.data.pop('email_code', None)
            return custom_response(data=request.data)
        return custom_error_response(status=status.HTTP_400_BAD_REQUEST, detail=serializer.errors)


class SetPasswordViewSet(CustomModelViewSet):
    """
    Set password view to set new password
    """
    http_method_names = ('post', )
    serializer_class = SetPasswordSerializer
    queryset = User

    def create(self, request, *args, **kwargs):
        """
        Set new password
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = request.data['token']
            password = serializer.validated_data.get('new_password')
            user_obj = self.queryset.objects.filter(password_hashcode=token).first()
            user_obj.set_password(password)
            user_obj.save()
            self.queryset.objects.filter(id=user_obj.id).update(password_hashcode='')
            return custom_response(data=SUCCESS_MESSAGE['set_password']['success'])
        return custom_error_response(status=status.HTTP_400_BAD_REQUEST, detail=serializer.errors)
