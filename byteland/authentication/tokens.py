from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class UserEmailActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) +
            six.text_type(timestamp) +
            six.text_type(user.email_confirmed)
        )

user_email_activation_token = UserEmailActivationTokenGenerator()
