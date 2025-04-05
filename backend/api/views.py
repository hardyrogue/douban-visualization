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
from .models import UserProfile
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required, user_passes_test
from functools import wraps
def is_admin(user):
    print("🧪 当前用户：", user)
    if not hasattr(user, 'userprofile'):
        print("❌ 没有 userprofile")
        return False
    print("✅ userprofile.role =", user.userprofile.role)
    return user.userprofile.role == 'admin'

def user_passes_test_json(test_func):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return JsonResponse({'error': '未登录'}, status=401)
            if not test_func(request.user):
                return JsonResponse({'error': '权限不足'}, status=403)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


@csrf_exempt
@user_passes_test_json(is_admin)
def user_view(request):
    if request.method == 'GET':
        keyword = request.GET.get('q', '').strip()
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))

        query = User.objects.all()

        if keyword:
            query = query.filter(username__icontains=keyword)

        total = query.count()
        users = query.order_by('-id')[(page - 1) * page_size : page * page_size]

        user_list = list(users.values(
            'id', 'username', 'email', 'date_joined', 'userprofile__role'
        ))
        return JsonResponse({'users': user_list, 'total': total})

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            role = data.get('role', 'user')

            if not username or not password:
                return JsonResponse({'error': '用户名和密码必填'}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': '用户名已存在'}, status=400)

            user = User.objects.create_user(username=username, email=email, password=password)
            UserProfile.objects.create(user=user, role=role)

            return JsonResponse({'message': '创建成功'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@user_passes_test_json(is_admin)
def handle_user(request, user_id):
    from django.contrib.auth.models import User
    from api.models import UserProfile

    # 删除用户
    if request.method == 'DELETE':
        if request.user.id == user_id:
            return JsonResponse({'error': '不能删除自己'}, status=403)
        try:
            User.objects.get(id=user_id).delete()
            return JsonResponse({'message': '用户已删除'})
        except User.DoesNotExist:
            return JsonResponse({'error': '用户不存在'}, status=404)

    # 更新用户
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            user = User.objects.get(id=user_id)

            # 修改基本信息
            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)

            # ✅ 可选修改密码（如果提供了）
            new_password = data.get('password')
            if new_password:
                user.set_password(new_password)

            user.save()

            # 修改角色
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.role = data.get('role', profile.role)
            profile.save()

            return JsonResponse({'message': '更新成功'})
        except User.DoesNotExist:
            return JsonResponse({'error': '用户不存在'}, status=404)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)

    # 其他方法不支持
    else:
        return JsonResponse({'error': '方法不被允许'}, status=405)

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
        print("接收到的数据：", data)  # 打印接收到的数据
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

# backend/api/views.py

@login_required
def user_favorites(request):
    user = request.user
    favorites = Favorite.objects.filter(user=user)
    
    movie_list = []
    for fav in favorites:
        movie_data = {
            'title': fav.movie.title,
            'year': fav.movie.year,
            'cover': fav.movie.cover_url,  # 假设你有电影封面URL
            'douban_id': fav.movie.douban_id,
        }
        movie_list.append(movie_data)
    
    return JsonResponse({'movies': movie_list})




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
            
            # 获取用户角色（从数据库）
            try:
                role = user.userprofile.role
            except:
                role = 'user'  # 默认值防止报错

            return JsonResponse({
                'message': '登录成功',
                'username': user.username,
                'token': 'mock-token',
                'user': {
                    'username': user.username,
                    'role': role  # ✅ 从数据库真实字段拿到
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

# ✅ views.py 中保留 current_user
@require_GET
@login_required
def current_user(request):
    user = request.user
    try:
        profile = user.userprofile
        avatar_url = request.build_absolute_uri(profile.avatar.url) if profile.avatar else ''
        return JsonResponse({
            'username': user.username,
            'avatar': avatar_url,
            'bio': profile.bio or '',
            'role': 'admin' if user.is_staff else 'user',
        })
    except UserProfile.DoesNotExist:
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
    

User = get_user_model()

@method_decorator(csrf_exempt, name='dispatch')
class ProfileUpdateView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': '未登录'}, status=401)

        user = request.user
        profile, _ = UserProfile.objects.get_or_create(user=user)

        bio = request.POST.get('bio', '')
        avatar = request.FILES.get('avatar')

        if bio:
            profile.bio = bio

        if avatar:
            # 保存到 avatars 文件夹下
            path = default_storage.save(f'avatars/{user.username}_{avatar.name}', avatar)
            profile.avatar = path

        profile.save()

        return JsonResponse({
            'message': '保存成功',
            'bio': profile.bio,
            'avatar': request.build_absolute_uri(profile.avatar.url) if profile.avatar else ''
        })

@require_GET
def favorites_list(request):
    print("访问了获取收藏的电影列表的接口")  # 这行代码用于调试

    # 获取当前登录用户的收藏
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

