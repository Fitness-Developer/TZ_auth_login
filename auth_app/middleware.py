from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from .models import AuthToken


class TokenAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION')
        request.user = None
        if not auth:
            return None
        if not auth.startswith('Token '):
            return None
        token = auth.split(' ', 1)[1].strip()
        try:
            token_obj = AuthToken.objects.select_related('user').get(token=token)
        except AuthToken.DoesNotExist:
            return None
        if not token_obj.user.is_active:
            return JsonResponse({'detail': 'User inactive'}, status=401)
        request.user = token_obj.user
        request._auth_token = token_obj
        return None
