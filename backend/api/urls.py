from django.urls import path
from .views import user_views, movie_views, favorite_views, profile_views

urlpatterns = [
    # 用户认证相关
    path('auth/login/', user_views.login_view),
    path('auth/logout/', user_views.logout_view),
    path('auth/user/', user_views.current_user),
    path('auth/register/', user_views.register_view),
    path('auth/profile/update/', profile_views.ProfileUpdateView.as_view(), name='profile_update'),
    path('auth/change-password/', user_views.change_password),

    # 用户管理相关
    path('users/', user_views.user_view),
    path('users/<int:user_id>/', user_views.handle_user),

    # 电影相关
    path('movies/search/', movie_views.search_movies),
    path('movies/detail/', movie_views.movie_detail),
    path('movies/comments/', movie_views.movie_comments),

    # 收藏相关
    path('movies/favorite/', favorite_views.toggle_favorite),
    path('movies/favorites/', favorite_views.user_favorites),
    path('movies/favorites/list/', favorite_views.favorites_list),

    # 图片代理
    path('image-proxy/', movie_views.image_proxy),
]
