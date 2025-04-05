from django.urls import path
from . import views
from .views import ProfileUpdateView

urlpatterns = [
    path('movies/search/', views.search_movies),
    path('movies/detail/', views.movie_detail),
    path('movies/comments/', views.movie_comments),
    path('movies/favorite/', views.toggle_favorite),
    path('movies/favorites/', views.user_favorites),  # ✅ 新接口
    path('movies/favorites/list/', views.favorites_list), 
    path('image-proxy/', views.image_proxy),  
    path('auth/login/', views.login_view),
    path('auth/logout/', views.logout_view),
    path('auth/user/', views.current_user), 
    path('auth/register/', views.register_view),
    path('users/', views.user_view), 
    path('users/<int:user_id>/', views.handle_user),
    path('auth/profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
]
