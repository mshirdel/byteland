from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    @property
    def auth_token(self):
        """
        Generate a JSON web token that stores this user's ID
        and has an expiry date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)
        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY,
            algorithm='HS256')

        return token.decode('utf-8')
