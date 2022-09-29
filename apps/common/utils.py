"""
custom error and success response.
"""
from datetime import datetime

from django.core.signing import TimestampSigner
from django.utils.crypto import get_random_string
from rest_framework import status as rest_status
from rest_framework.response import Response

from apps.authentication.models import User
from apps.common import constants


def custom_response(status=rest_status.HTTP_200_OK, detail=None, data=None, **kwargs):
    """
    function is used for getting same global response for all api
    :param detail: success message
    :param data: data
    :param status: http status
    :return: Json response
    """
    return Response({"detail": detail, "data": data}, status=status, **kwargs)


def custom_error_response(status, detail, **kwargs):
    """
    function is used for getting same global error response for all api
    :param detail: error message .
    :param status: http status.
    :return: Json response
    """
    if not detail:
        detail = {}
    return Response({"detail": detail}, status=status, **kwargs)


def generate_rnd_number():
    """
    generates random string
    :return: unique_id
    """
    unique_id = get_random_string(length=6, allowed_chars='123456789')
    return unique_id


def generate_hash_code(registered_id):
    """
    Generate hask key
    :param registered_id: registered_id in str
    :return: hash key string
    """
    signer = TimestampSigner()
    signed_value = signer.sign(registered_id)
    email_hash = signed_value.split(':')[constants.NUMBER['one']:][constants.NUMBER['one']]
    return email_hash


def user_update_verify_otp_mail(obj):
    """
    User update fields
    :param obj: user obj
    :return: None
    """
    obj.last_login = datetime.now()
    obj.email_verified = True
    obj.email_verification_token = ''
    obj.email_verification_otp = ''
    obj.save()


def check_user_instance(email):
    """
    To check user instance
    """
    if User.objects.filter(email=email).exists():
        return True
    return False
