from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..services import spotify


def spotify_login(request):
    """ Страница входа через Spotify
    """
    return render(request, 'oauth/spotify_login.html')


@api_view(['GET'])
def spotify_auth(request):
    """ Подтверждение авторизации через Spotify
    """
    token = spotify.spotify_auth(request.query_params.get('code'))
    print(f'Token {token}')
    return Response(token)





