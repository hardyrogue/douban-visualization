from django.http import JsonResponse, HttpResponse
from api.spider.douban_interface import search_movie_by_keyword, fetch_movie_brief, get_movie_review, get_movie_review_by_page
from django.views.decorators.http import require_GET
import requests
import traceback
from collections import Counter
import numpy as np
from api.spider.analysis_utils import analyze_rating_distribution_with_trend
import pandas as pd
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

# 获取电影详情（已加上评分数值分析）
from sklearn.linear_model import LinearRegression  # ✅ 新增导入

@require_GET
def movie_detail(request):
    movie_id = request.GET.get('id')
    if not movie_id:
        return JsonResponse({'error': '缺少参数 id'}, status=400)

    try:
        movie_info = fetch_movie_brief(movie_id)
        comments = get_movie_review(movie_id)
        print("示例评论：", comments[0] if comments else "无评论")
        top_comments = comments[:5]

        # 原始评分分布统计
        rating_dist = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
        rating_list = []

        for c in comments:
            try:
                stars = int(c.get("stars", 0))
                if 1 <= stars <= 5:
                    rating_dist[str(stars)] += 1
                    rating_list.append(stars)
            except:
                continue

        # 数值分析
        if rating_list:
            arr = np.array(rating_list)
            average = round(float(np.mean(arr)), 2)
            median = int(np.median(arr))
            mode = int(Counter(arr).most_common(1)[0][0])
            std_dev = round(float(np.std(arr)), 2)
            skewness = round(float((np.mean(arr) - np.median(arr)) / (np.std(arr) + 1e-6)), 2)

            rating_stats = {
                "average": average,
                "median": median,
                "mode": mode,
                "std_dev": std_dev,
                "skewness": skewness,
                "count": len(rating_list)
            }
        else:
            rating_stats = {
                "average": None,
                "median": None,
                "mode": None,
                "std_dev": None,
                "skewness": None,
                "count": 0
            }

        # 趋势分析 + 预测
        rating_trend = {}
        try:
            df = pd.DataFrame(comments)
            if not df.empty and 'stars' in df.columns and 'time' in df.columns:
                df = df[df['stars'].apply(lambda x: str(x).isdigit() and 1 <= int(x) <= 5)]
                df['stars'] = df['stars'].astype(int)
                df['time'] = pd.to_datetime(df['time'], errors='coerce')
                df = df.dropna(subset=['time'])
                df['year'] = df['time'].dt.year
                trend_data = df.groupby('year')['stars'].mean().round(2).to_dict()
                rating_trend = {str(k): float(v) for k, v in trend_data.items()}

                # ✅ 使用线性回归预测未来 2 年
                if len(rating_trend) >= 2:
                    trend_df = pd.DataFrame(list(rating_trend.items()), columns=["year", "score"])
                    trend_df["year"] = trend_df["year"].astype(int)
                    X = trend_df["year"].values.reshape(-1, 1)
                    y = trend_df["score"].values
                    model = LinearRegression().fit(X, y)
                    future_years = np.array([2024, 2025]).reshape(-1, 1)
                    predictions = model.predict(future_years).round(2)
                    rating_trend["2024"] = float(predictions[0])
                    rating_trend["2025"] = float(predictions[1])
        except Exception as e:
            print("评分趋势计算或预测失败：", e)
            rating_trend = {}

        print(f"评分趋势数据（含预测）：{rating_trend}")
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
            'rating_stats': rating_stats,
            'rating_trend': rating_trend,
            'comments': top_comments
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
