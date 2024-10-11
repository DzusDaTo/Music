from config import settings
from rest_framework import authentication, exceptions
import jwt
from datetime import datetime
from typing import Optional
from src.oauth.models import AuthUser


class AuthBackend(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request, token=None, **kwargs) -> Optional[tuple]:
        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header or auth_header[0].lower() != b'token':
            return None

        if len(auth_header) == 1:
            raise exceptions.AuthenticationFailed('Не валидный токен')
        elif len(auth_header) > 2:
            raise exceptions.AuthenticationFailed('В строке не должно быть пробелов')

        try:
            token = auth_header[1].decode('utf-8')
        except UnicodeError:
            raise exceptions.AuthenticationFailed('В токене присутствуют недопустимые символы')

        return self.authenticate_credential(token)

    def authenticate_credential(self, token) -> tuple:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        except jwt.PyJWTError:
            raise exceptions.AuthenticationFailed('Не удалось декодировать токен')

        token_exp = datetime.fromtimestamp(payload['exp'])
        if token_exp < datetime.utcnow():
            raise exceptions.AuthenticationFailed('Время токена истеко')

        try:
            user = AuthUser.objects.get(id=payload['user_id'])
        except AuthUser.DoesNotExist:
            raise exceptions.AuthenticationFailed('Пользователь по такому токену не найден')

        return user, None

