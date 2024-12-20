from django.urls import path
from . import views


urlpatterns = [
    path('genre/', views.GenreView.as_view()),
]