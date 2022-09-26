"""
This file is for send mail related functions
"""
# python imports
import logging

# Third party import
# django import
from django.contrib.auth import (get_user_model)
from django.core.mail import EmailMessage
from django.template.loader import get_template

from apps.common import constants as util_constants
# django imports
from myproject import settings

USER = get_user_model()

mail_logger = logging.getLogger('mail-logger')


def send_email(email_data, template):
    """
    Common function for send email
    :param email_data: dict type Ex. {'to':'','subject':'','message':'','detail':''}
    :param template: email_template string type
    :param is_admin : True or false
    :return:
    """
    email_from = util_constants.EMAIL_FROM_TEXT
    subject = email_data['subject']
    receivers = list()
    receivers.append(email_data['to'])
    body_content = email_data['message']
    ctx = dict()
    ctx['body_content'] = body_content
    ctx['detail'] = email_data['detail']
    message = get_template(template).render(context=ctx)
    msg = EmailMessage(subject, message, to=receivers, from_email=email_from)
    msg.content_subtype = 'html'
    msg.send()
    return True
