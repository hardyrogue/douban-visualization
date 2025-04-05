from django.urls import path
from . import views
from .views import ProfileUpdateView

urlpatterns = [
    path('movies/search/', views.search_movies),
    path('movies/detail/', views.movie_detail),
    path('movies/comments/', views.movie_comments),
    path('movies/favorite/', views.toggle_favorite),
    path('image-proxy/', views.image_proxy),  
    # 登录相关接口（统一加上 auth/）
    path('auth/login/', views.login_view),
    path('auth/logout/', views.logout_view),
    path('auth/user/', views.current_user),
    path('auth/register/', views.register_view),
    
    path('auth/profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
]
