from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from api.models import UserProfile
import json
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from api.views.decorators import user_passes_test_json, is_admin
# 用户登录
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
            try:
                role = user.userprofile.role
            except:
                role = 'user'
            return JsonResponse({
                'message': '登录成功',
                'username': user.username,
                'token': 'mock-token',
                'user': {
                    'username': user.username,
                    'role': role
                }
            })
        else:
            return JsonResponse({'error': '用户名或密码错误'}, status=401)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# 用户注册
@csrf_exempt
@require_POST
def register_view(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        bio = data.get('bio', '')
        email = data.get('email', '')

        if not username or not password:
            return JsonResponse({'error': '用户名和密码不能为空'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': '用户名已存在'}, status=409)

        user = User.objects.create_user(username=username, password=password)
        UserProfile.objects.create(user=user, bio=bio, email=email)

        return JsonResponse({
            'message': '注册成功并已登录',
            'username': user.username,
            'token': 'mock-token',
            'role': 'user'
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# 用户登出
@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({'message': '已退出登录'})

# 获取当前用户信息
@csrf_exempt
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
            'email': profile.email or '',
            'role': 'admin' if user.is_staff else 'user',
        })
    except UserProfile.DoesNotExist:
        return JsonResponse({
            'username': user.username,
            'avatar': '',
            'bio': '',
            'email':  '',
            'role': 'admin' if user.is_staff else 'user',
        })
@csrf_exempt
@user_passes_test_json(is_admin)
def handle_user(request, user_id):
    """处理用户的删除和更新操作"""
    
    # 删除用户
    if request.method == 'DELETE':
        # 防止删除当前登录的用户
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

            # 修改用户名
            user.username = data.get('username', user.username)

            # 可选修改密码（如果提供了）
            new_password = data.get('password')
            if new_password:
                user.set_password(new_password)

            user.save()

            # 修改用户的角色和其他信息
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.role = data.get('role', profile.role)
            profile.email = data.get('email', profile.email)
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
# 修改密码
@csrf_exempt
@require_POST
@login_required
def change_password(request):
    """修改当前用户的密码"""
    try:
        data = json.loads(request.body)
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        user = request.user

        if not old_password or not new_password:
            return JsonResponse({'error': '请输入原密码和新密码'}, status=400)

        if not user.check_password(old_password):
            return JsonResponse({'error': '原密码错误'}, status=403)

        if old_password == new_password:
            return JsonResponse({'error': '新密码不能与原密码相同'}, status=400)

        user.set_password(new_password)
        user.save()

        return JsonResponse({'message': '密码修改成功'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
# 获取用户列表（仅限管理员）
@csrf_exempt
@user_passes_test_json(is_admin)
def user_view(request):
    """列出所有用户，并支持分页和搜索功能"""
    if request.method == 'GET':
        # 获取查询参数
        keyword = request.GET.get('q', '').strip()  # 搜索关键字
        page = int(request.GET.get('page', 1))  # 当前页
        page_size = int(request.GET.get('page_size', 10))  # 每页条数

        query = User.objects.all()

        # 如果提供了搜索关键词，过滤用户名
        if keyword:
            query = query.filter(username__icontains=keyword)

        # 获取用户总数
        total = query.count()

        # 分页查询用户数据
        users = query.order_by('-id')[(page - 1) * page_size : page * page_size]

        # 格式化用户数据
        user_list = list(users.values(
            'id', 'username', 'userprofile__email', 'date_joined', 'userprofile__role'
        ))

        return JsonResponse({'users': user_list, 'total': total})

    elif request.method == 'POST':
        """创建新用户"""
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

            user = User.objects.create_user(username=username, password=password)
            UserProfile.objects.create(user=user, role=role, email=email)

            return JsonResponse({'message': '创建成功'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
