from django.urls import path
from .endpoint import views, auth_views
from .views import RegisterUserView, LoginUserView

urlpatterns = [
    path('me/', views.UserView.as_view({'get': 'retrieve', 'put': 'update'})),

    path('author/', views.AuthorView.as_view({'get': 'list'})),
    path('author/<int:pk>/', views.AuthorView.as_view({'get': 'retrieve'})),

    path('social/', views.SocialLinkView.as_view({'get': 'list', 'post': 'create'})),
    path('social/<int:pk>/', views.SocialLinkView.as_view({'put': 'update', 'delete': 'destroy'})),

    path('spotify-login/', auth_views.spotify_login),
    path('spotify-callback/', auth_views.spotify_auth),

    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
]