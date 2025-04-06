from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views import View
from django.core.files.storage import default_storage
from api.models import UserProfile
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
User = get_user_model()

@method_decorator(csrf_exempt, name='dispatch')
class ProfileUpdateView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': '未登录'}, status=401)

        user = request.user
        profile, _ = UserProfile.objects.get_or_create(user=user)

        bio = request.POST.get('bio', '')
        email = request.POST.get('email', '')
        avatar = request.FILES.get('avatar')

        if bio:
            profile.bio = bio
        if email:
            profile.email = email
            print("📨 前端传来的邮箱：", email)
        if avatar:
            # 保存到 avatars 文件夹下
            path = default_storage.save(f'avatars/{user.username}_{avatar.name}', avatar)
            profile.avatar = path

        profile.save()

        return JsonResponse({
            'message': '保存成功',
            'bio': profile.bio,
            'email': profile.email,
            'avatar': request.build_absolute_uri(profile.avatar.url) if profile.avatar else ''
        })