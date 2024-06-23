from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

#  PasswordTokenGenerator class that is used to reset the password.


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()
