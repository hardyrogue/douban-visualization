from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from api.models import Favorite
import json

# 收藏电影
@csrf_exempt
@require_POST
def toggle_favorite(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "未登录"}, status=401)

    try:
        data = json.loads(request.body)
        movie_id = data.get("id")
        movie_title = data.get("title")
        movie_cover = data.get("cover")
        movie_rating = data.get("rating", 0)
        user = request.user

        if not movie_title:
            return JsonResponse({"error": "Title is required"}, status=400)

        fav, created = Favorite.objects.get_or_create(
            user=user,
            douban_id=movie_id,
            defaults={
                'title': movie_title,
                'cover': movie_cover,
                'rating': movie_rating
            }
        )

        if not created:
            fav.delete()
            return JsonResponse({"message": "取消收藏", "status": "removed"})
        else:
            return JsonResponse({"message": "已收藏", "status": "added"})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# 获取用户收藏
@login_required
def user_favorites(request):
    user = request.user
    favorites = Favorite.objects.filter(user=user)
    
    movie_list = []
    for fav in favorites:
        movie_data = {
            'title': fav.movie.title,
            'year': fav.movie.year,
            'cover': fav.movie.cover_url,
            'douban_id': fav.movie.douban_id,
        }
        movie_list.append(movie_data)
    
    return JsonResponse({'movies': movie_list})
@login_required
def favorites_list(request):
    """获取当前登录用户收藏的电影列表"""
    user = request.user
    try:
        # 查询当前用户的所有收藏
        favorites = Favorite.objects.filter(user=user)

        # 如果没有收藏
        if not favorites:
            return JsonResponse({'message': '没有收藏的电影'}, status=404)

        # 返回收藏的电影的详细信息
        movie_list = []
        for fav in favorites:
            movie_data = {
                'douban_id': fav.douban_id,  # 电影的豆瓣ID
                'title': fav.title,          # 电影标题
                'cover': fav.cover,          # 电影封面
                'rating': fav.rating,        # 电影评分
            }
            movie_list.append(movie_data)

        return JsonResponse({'favorites': movie_list})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)