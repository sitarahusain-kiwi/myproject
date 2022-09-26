"""
To send email from authentication app
"""
from celery import shared_task

from apps.authentication.models import User
from apps.common.email_messages import EMAIL_DATA_SET
from apps.common.send_mail import send_email


@shared_task()
def user_registration_mail(user_id):
    """
    User registration success full mail send.
    :param user_id: request user id str.
    :return: user registration success full mail send.
    """
    data = User.objects.filter(id=user_id).first()
    if data:
        email_data_set = EMAIL_DATA_SET['user_signup']
        email_data = {
            'to': data.email,
            'subject': email_data_set['subject'],
            'message': email_data_set['body'],
            'detail': {'user': data}
        }
        send_email(email_data, 'emails/authentication/signup.html')
