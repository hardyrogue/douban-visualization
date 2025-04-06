from django.http import JsonResponse
from api.spider.douban_interface import search_movie_by_keyword, fetch_movie_brief, get_movie_review, get_movie_review_by_page
from django.views.decorators.http import require_GET
import requests
import traceback
from django.http import HttpResponse
# 搜索电影
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

# 获取电影详情
@require_GET
def movie_detail(request):
    movie_id = request.GET.get('id')
    if not movie_id:
        return JsonResponse({'error': '缺少参数 id'}, status=400)

    try:
        movie_info = fetch_movie_brief(movie_id)
        comments = get_movie_review(movie_id)
        top_comments = comments[:5]

        rating_dist = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
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
            'rating_dist': rating_dist,
            'comments': top_comments
        })
    
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)

# 获取电影评论
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
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)

# 图片代理
@require_GET
def image_proxy(request):
    url = request.GET.get('url')
    if not url:
        return HttpResponse("Missing url", status=400)

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(url, headers=headers, timeout=10)
        content_type = resp.headers.get('Content-Type', 'image/jpeg')
        return HttpResponse(resp.content, content_type=content_type)
    except Exception as e:
        return HttpResponse(f"Error loading image: {str(e)}", status=500)
