from django.contrib.auth.tokens import PasswordResetTokenGenerator


class UserEmailActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) +
            str(timestamp) +
            str(user.email_confirmed)
        )

user_email_activation_token = UserEmailActivationTokenGenerator()
