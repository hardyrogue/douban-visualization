from functools import wraps
from django.http import JsonResponse

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
def is_admin(user):
    """检查当前用户是否是管理员"""
    print("🧪 当前用户：", user)
    if not hasattr(user, 'userprofile'):
        print("❌ 没有 userprofile")
        return False
    print("✅ userprofile.role =", user.userprofile.role)
    return user.userprofile.role == 'admin'
