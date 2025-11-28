from rest_framework import authentication
from rest_framework import exceptions
from auth_app.models import AuthToken
from datetime import datetime

class CustomTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Token '):
            return None
        try:
            token_value = auth_header.split(' ', 1)[1].strip()
            token_obj = AuthToken.objects.select_related('user').get(token=token_value)
        except AuthToken.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token_obj.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive')

        return (token_obj.user, token_obj)