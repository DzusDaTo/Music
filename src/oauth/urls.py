from django.urls import path
from .endpoint import views


urlpatterns = [
    path('me/', views.UserView.as_view({'get': 'retrieve', 'put': 'update'})),
]