from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone
from rest_framework.authtoken.models import Token
from datetime import datetime, timedelta
from django.conf import settings


class CustomTokenAuthentication(TokenAuthentication):

    model = Token

    def authenticate_credentials(self, key, request=None):
        try:
            token = Token.objects.select_related('user').get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed({'error': 'Invalid token'})

        if not token.user.is_active:
            raise AuthenticationFailed({'error': 'User inactive or deleted'})

        if not token.user.is_staff:
            last_activity_time = token.created
            time_difference = datetime.now(timezone.utc) - last_activity_time
            if time_difference > timedelta(seconds=settings.FORCE_KILL_TOKEN):
                token.delete()
                raise AuthenticationFailed('Token has expired due to inactivity')
        return token.user, token

