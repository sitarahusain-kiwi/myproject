"""
file used for tokens
"""
from datetime import timedelta, datetime

from oauth2_provider.models import Application, AccessToken, RefreshToken
from oauth2_provider.settings import oauth2_settings
from oauthlib.common import generate_token


def get_access_token(user):
    """
    To get access and refresh tokens
    :param user: user instance
    :return: token
    """
    app = Application.objects.get_or_create(
        user=user, client_type=Application.CLIENT_CONFIDENTIAL, authorization_grant_type=Application.GRANT_PASSWORD)[0]
    token = generate_token()
    refresh_token = generate_token()
    expires = datetime.now() + timedelta(
        seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
    scope = "read write"
    access_token_instance = AccessToken.objects.create(
        user=user, application=app, expires=expires, token=token, scope=scope)
    RefreshToken.objects.create(
        user=user, application=app, token=refresh_token,
        access_token=access_token_instance)
    return access_token_instance.token
