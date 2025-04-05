from django.db import models
from django.contrib.auth.models import User

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    douban_id = models.CharField(max_length=20)

    class Meta:
        unique_together = ('user', 'douban_id')  # 每人每电影只能收藏一次

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.URLField(blank=True, null=True)  # 头像 URL
    bio = models.TextField(blank=True, null=True)    # 签名/介绍

    def __str__(self):
        return f"{self.user.username} 的资料"
