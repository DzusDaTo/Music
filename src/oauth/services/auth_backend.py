import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from src.oauth.models import AuthUser
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model


class AuthBackend(authentication.BaseAuthentication):
    authentication_header_prefix = 'Bearer'

    def authenticate(self, request, username=None, password=None, **kwargs):

        if username and password:
            try:
                user = get_user_model().objects.get(email=username)
            except get_user_model().DoesNotExist:
                raise exceptions.AuthenticationFailed('Invalid credentials')

            if not user.check_password(password):
                raise exceptions.AuthenticationFailed('Invalid credentials')

            return (user, None)

        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header or auth_header[0].lower() != b'bearer':
            return None

        if len(auth_header) == 1:
            raise exceptions.AuthenticationFailed('Invalid token header. No credential provided.')
        elif len(auth_header) > 2:
            raise exceptions.AuthenticationFailed(
                'Invalid token header. Token string should not contain spaces'
            )

        try:
            token = auth_header[1].decode('utf-8')
        except UnicodeError:
            raise exceptions.AuthenticationFailed(
                'Invalid token header. Token string should not contain invalid characters.'
            )

        return self.authenticate_credential(token)

    def authenticate_credential(self, token) -> tuple:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        except jwt.PyJWTError:
            raise exceptions.AuthenticationFailed('Invalid authentication. Could not decode token.')
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired.')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token.')

        token_exp = datetime.utcfromtimestamp(payload['exp'])
        if token_exp < datetime.utcnow():
            raise exceptions.AuthenticationFailed('Token expired.')

        try:
            user = AuthUser.objects.get(id=payload['user_id'])
        except AuthUser.DoesNotExist:
            raise exceptions.AuthenticationFailed('No user matching this token was found.')

        return user, None


def generate_jwt_token(user):
    """
    Генерация JWT токена для пользователя
    """
    payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(days=7),
        'iat': datetime.utcnow(),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token
