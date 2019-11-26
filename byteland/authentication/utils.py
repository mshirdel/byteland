from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from byteland.core.utils import send_mail

from .tokens import user_email_activation_token
from .models import User


def send_activation_email(user_id, use_https, site_name, site_domain):
    """
    Use celery to send email
    """
    user = User.objects.get(pk=user_id)
    email = settings.BYTELAND.get('INFO_EMAIL', 'info@byteland.ir')
    return send_mail('authentication/email_confirmed_subject.txt',
              'authentication/email_confirmed_template.html',
              {
                  'sitename': site_name,
                  'protocol': 'https' if use_https else 'http',
                  'domain': site_domain,
                  'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                  'token': user_email_activation_token.make_token(user),
              },
              email, user.email)
