from django.http import JsonResponse
from django.http import HttpResponse
import traceback
import requests
import json
from .models import Favorite
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from .spider.douban_interface import search_movie_by_keyword
from .spider.douban_interface import get_movie_review_by_page
from django.views.decorators.http import require_GET
from api.spider.douban_interface import fetch_movie_brief
from api.spider.douban_interface import get_movie_review
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile
from django.contrib.auth.models import User
@require_GET
def search_movies(request):
    keyword = request.GET.get('q', '').strip()
    if not keyword:
        return JsonResponse({'results': []})
    
    try:
        result = search_movie_by_keyword(keyword)
        return JsonResponse({'results': result})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_GET
def movie_detail(request):
    movie_id = request.GET.get('id')
    if not movie_id:
        return JsonResponse({'error': '缺少参数 id'}, status=400)

    try:
        # 获取电影简要信息
        movie_info = fetch_movie_brief(movie_id)
        print("✅ 获取到的电影信息：", movie_info)

        # 获取全部评论（用于统计 + 展示前几条）
        comments = get_movie_review(movie_id)
        top_comments = comments[:5]

        # 评分分布统计
        rating_dist = {
            "1": 0, "2": 0, "3": 0, "4": 0, "5": 0
        }
        for c in comments:
            try:
                stars = int(c.get("stars", 0))
                if 1 <= stars <= 5:
                    rating_dist[str(stars)] += 1
            except:
                continue

        return JsonResponse({
            'id': movie_id,
            'title': movie_info['title'],
            'year': movie_info['year'],
            'directors': movie_info['directors'],
            'actors': movie_info['actors'],
            'genres': movie_info['genres'],
            'rating': movie_info['rating'],
            'summary': movie_info['summary'],
            'cover': movie_info['cover'],
            'rating_dist': rating_dist,     # ✅ 分布
            'comments': top_comments        # ✅ 热门评论（前5）
        })
    
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)
        
@require_GET
def movie_comments(request):
    movie_id = request.GET.get('id')
    start = int(request.GET.get('start', 0))
    limit = int(request.GET.get('limit', 5))  # 每页默认 5 条

    if not movie_id:
        return JsonResponse({"error": "Missing id"}, status=400)

    try:
        comments = get_movie_review_by_page(movie_id, start=start, limit=limit)
        return JsonResponse({
            "comments": comments,
            "start": start,
            "limit": limit,
            "count": len(comments)
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)


@require_GET
def image_proxy(request):
    url = request.GET.get('url')
    print("📸 image_proxy 代理访问：", url)  # ✅ 打印出来

    if not url:
        return HttpResponse("Missing url", status=400)

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(url, headers=headers, timeout=10)
        content_type = resp.headers.get('Content-Type', 'image/jpeg')
        return HttpResponse(resp.content, content_type=content_type)
    except Exception as e:
        print("❌ 图片加载失败：", e)
        return HttpResponse(f"Error loading image: {str(e)}", status=500)

    



@csrf_exempt
@require_POST
def toggle_favorite(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "未登录"}, status=401)

    try:
        data = json.loads(request.body)
        movie_id = data.get("id")
        user = request.user

        fav, created = Favorite.objects.get_or_create(user=user, douban_id=movie_id)
        if not created:
            fav.delete()
            return JsonResponse({"message": "取消收藏", "status": "removed"})
        else:
            return JsonResponse({"message": "已收藏", "status": "added"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)






@csrf_exempt
# views.py 登录接口
@csrf_exempt
@require_POST
def login_view(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({
                'message': '登录成功',
                'username': user.username,
                'token': 'mock-token',  # ✅ 可换成 JWT
                'user': {
                    'username': user.username,
                    'role': 'user'  # 或从数据库判断角色字段
                }
            })
        else:
            return JsonResponse({'error': '用户名或密码错误'}, status=401)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({'message': '已退出登录'})


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET

@require_GET
def current_user(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error': '未登录'}, status=401)

    try:
        profile = user.userprofile  # 如果有绑定 UserProfile
        return JsonResponse({
            'username': user.username,
            'avatar': profile.avatar if profile.avatar else '',
            'bio': profile.bio if profile.bio else '',
            'role': 'admin' if user.is_staff else 'user',
        })
    except Exception:
        return JsonResponse({
            'username': user.username,
            'avatar': '',
            'bio': '',
            'role': 'admin' if user.is_staff else 'user',
        })



@csrf_exempt
@require_POST
def register_view(request):
    import json
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({'error': '用户名和密码不能为空'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': '用户名已存在'}, status=409)

        user = User.objects.create_user(username=username, password=password)
        return JsonResponse({
            'message': '注册成功并已登录',
            'username': user.username,
            'token': 'mock-token',  # 或你用 JWT 的 token
            'role': 'user'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)