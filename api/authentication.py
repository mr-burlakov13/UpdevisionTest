from rest_framework import authentication, exceptions
from django.utils import timezone
from .models import Token

class BearerTokenAuthentication(authentication.BaseAuthentication):
    keyword = 'Bearer'

    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request).split()
        if not auth_header:
            return None  # Нет заголовка — вернём None, чтобы остался анонимным пользователь

        if auth_header[0].decode().lower() != self.keyword.lower():
            return None

        if len(auth_header) == 1:
            msg = 'Неверный формат заголовка. Отсутствует токен.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth_header) > 2:
            msg = 'Неверный формат заголовка. Токен содержит пробелы.'
            raise exceptions.AuthenticationFailed(msg)

        token_key = auth_header[1].decode()
        try:
            token = Token.objects.get(key=token_key)
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed('Неверный токен.')

        # Если токен истёк — удаляем его и возвращаем ошибку
        if token.expires_at < timezone.now():
            token.delete()
            raise exceptions.AuthenticationFailed('Срок действия токена истёк.')

        # Продлеваем время жизни токена, если запрос не к /signin
        if request.path != '/signin':
            token.extend_expiration()

        return (token.user, token)
