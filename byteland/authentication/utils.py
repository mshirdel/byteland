from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from byteland.core.utils import send_mail

from .tokens import user_email_activation_token


def send_activation_email(request, user):
    current_site = get_current_site(request)
    use_https = request.is_secure()
    email = settings.BYTELAND.get('INFO_EMAIL', 'info@byteland.ir')
    send_mail('authentication/email_confirmed_subject.txt',
              'authentication/email_confirmed_template.html',
              {
                  'sitename': current_site.name,
                  'protocol': 'https' if use_https else 'http',
                  'domain': current_site.domain,
                  'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                  'token': user_email_activation_token.make_token(user),
              },
              email, user.email)
