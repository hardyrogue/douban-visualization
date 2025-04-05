from django.db import models
from django.contrib.auth.models import User

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    douban_id = models.CharField(max_length=20)
    title = models.CharField(max_length=255)  # 电影标题
    cover = models.URLField()  # 电影封面链接
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)


    class Meta:
        unique_together = ('user', 'douban_id')  # 每人每电影只能收藏一次

    def __str__(self):
        return f"{self.user.username} 收藏的电影：{self.title}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} 的资料"
