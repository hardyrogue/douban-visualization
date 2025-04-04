# backend/api/management/commands/load_demo_movies.py

from django.core.management.base import BaseCommand
from api.models import Movie

class Command(BaseCommand):
    help = '加载一些测试电影数据'

    def handle(self, *args, **kwargs):
        data = [
            {
                'title': '星际穿越',
                'year': 2014,
                'director': '克里斯托弗·诺兰',
                'genre': '科幻',
                'rating': 9.3,
                'cover': 'https://img9.doubanio.com/view/photo/s_ratio_poster/public/p2206088801.jpg',
            },
            {
                'title': '霸王别姬',
                'year': 1993,
                'director': '陈凯歌',
                'genre': '剧情 / 历史',
                'rating': 9.6,
                'cover': 'https://img2.doubanio.com/view/photo/s_ratio_poster/public/p2561716440.jpg',
            },
            {
                'title': '盗梦空间',
                'year': 2010,
                'director': '诺兰',
                'genre': '动作 / 科幻 / 悬疑',
                'rating': 9.2,
                'cover': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p513344864.jpg',
            }
        ]

        for item in data:
            movie, created = Movie.objects.get_or_create(title=item['title'], defaults=item)
            if created:
                self.stdout.write(self.style.SUCCESS(f'添加电影：{movie.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'已存在：{movie.title}'))
