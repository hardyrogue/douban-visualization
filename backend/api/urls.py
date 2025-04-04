from django.urls import path
from .views import search_movies
from . import views

urlpatterns = [
    path('movies/search/', views.search_movies),
    path('movies/detail/', views.movie_detail), 
    path('movies/comments/', views.movie_comments),
    path('image-proxy/', views.image_proxy),
    path('favorite/', views.toggle_favorite),
]
