import numpy as np
import pandas as pd
from collections import Counter

def analyze_rating_distribution_with_trend(comments):
    """
    综合分析评分统计值和趋势：
    参数 comments: 评论列表（每条包含 stars 和 time）
    返回: rating_stats + rating_trend
    """
    df = pd.DataFrame(comments)
    if df.empty or 'stars' not in df.columns:
        return {
            "rating_stats": {
                "average": None,
                "median": None,
                "mode": None,
                "std_dev": None,
                "skewness": None,
                "count": 0
            },
            "rating_trend": {}
        }

    # 数据清洗：保留有效评分
    df = df[df['stars'].apply(lambda x: str(x).isdigit() and 1 <= int(x) <= 5)]
    df['stars'] = df['stars'].astype(int)

    # 评分统计分析
    rating_list = df['stars'].tolist()
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

    # 趋势分析（如果包含时间字段）
    rating_trend = {}
    if 'time' in df.columns:
        df['time'] = pd.to_datetime(df['time'], errors='coerce')
        df = df.dropna(subset=['time'])
        df['year'] = df['time'].dt.year
        rating_trend = df.groupby('year')['stars'].mean().round(2).to_dict()
        rating_trend = {str(year): float(score) for year, score in rating_trend.items()}

    return {
        "rating_stats": rating_stats,
        "rating_trend": rating_trend
    }
