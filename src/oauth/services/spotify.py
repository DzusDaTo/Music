import base64
import logging
from typing import Optional

import requests
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

from src.oauth.models import AuthUser
from src.oauth.services import base_auth

logger = logging.getLogger(__name__)

SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_USER_URL = 'https://api.spotify.com/v1/me'


def get_spotify_jwt(code: str) -> Optional[str]:
    """ Получение токена доступа Spotify """
    basic_str = f'{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_SECRET}'.encode('ascii')
    basic = base64.b64encode(basic_str)
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://127.0.0.1:8000/spotify-callback/'
    }
    headers = {
        'Authorization': f'Basic {basic.decode("ascii")}'
    }
    res = requests.post(SPOTIFY_TOKEN_URL, data=data, headers=headers)

    if res.status_code != 200:
        logger.error(f"Error fetching Spotify JWT: {res.status_code}, Response: {res.text}")
        return None

    r = res.json()
    logger.info(f"Received Spotify JWT: {r}")
    return r.get('access_token')


def get_spotify_user(token: str) -> Optional[str]:
    """ Получение email пользователя Spotify """
    headers = {'Authorization': f'Bearer {token}'}
    res = requests.get(SPOTIFY_USER_URL, headers=headers)

    if res.status_code != 200:
        logger.error(f"Error fetching Spotify user data: {res.status_code}, Response: {res.text}")
        return None

    r = res.json()
    logger.info(f"Received Spotify user data: {r}")
    return r.get('email')


def get_spotify_email(code: str) -> Optional[str]:
    """ Получение email через Spotify API """
    token = get_spotify_jwt(code)
    if token:
        return get_spotify_user(token)
    logger.warning("Failed to get Spotify token")
    return None


def spotify_auth(code: str):
    """ Авторизация через Spotify """
    email = get_spotify_email(code)
    if email:
        user, _ = AuthUser.objects.get_or_create(email=email)
        logger.info(f"User authenticated: {user}")
        return base_auth.create_token(user.id)
    else:
        logger.error(f"Failed to authenticate user with code: {code}")
        raise AuthenticationFailed(code=403, detail='Bad token Spotify')
