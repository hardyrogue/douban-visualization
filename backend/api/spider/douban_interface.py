import requests
from lxml import etree
import re
import time as t

# 设置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://movie.douban.com/',
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest'
}

# cookies 模拟登录状态
cookies = {
    "bid": "dQym6gwlwHs",
    "ll": "108288",
    "__utmz": "30149280.1741962662.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic",
    "dbcl2": "285724563:A9REG/2ELd4",
    "push_noty_num": "0",
    "push_doumail_num": "0",
    "__utmv": "30149280.28572",
    "_vwo_uuid_v2": "D43595C505F19A9AD72BCEA3F7014BFE5|010592450dc9fe985460249bf3856544",
    "ck": "eLKu",
    "__utma": "30149280.1415938108.1741962210.1743339137.1743499766.3",
    "__utmc": "30149280",
    "frodotk_db": "b2a8479027bcea7e17f8d6b07736bf7a",
    "_sharedID": "0d7f63a2-7894-46e1-8b8e-021ed9521da9",
    "_sharedID_cst": "2SzgLJUseQ==",
    "FCNEC": "[[\"AKsRol_pgWdSRM5Gab7WjkKoF975uoKXMblD3nyo177UPk2icOW2jKnTd9abZL0H0hLYg6pTlHIal4he20U__qxsn3GZ8KB0pydlVunS0m1zGxCiI1EjmylLJIAGVBEwrotSh1aQ3aoPr7tokjIYmQ22-so97zXsmQ==\"]]",
    "_ga_P83QWMDYS1": "GS1.1.1743501483.1.0.1743501562.0.0.0",
    "frodotk": "96dafb332b4dda80c490f19981e98f80",
    "talionusr": "{\"id\": \"285724563\", \"name\": \"hardy\"}",
    "Hm_lvt_6d4a8cfea88fa457c3127e14fb5fabc2": "1741962199,1743339406,1743520899",
    "HMACCOUNT": "EB23A7A07066B1B7",
    "_gid": "GA1.2.1247011277.1743520904",
    "Hm_lpvt_6d4a8cfea88fa457c3127e14fb5fabc2": "1743522874",
    "_ga": "GA1.1.1415938108.1741962210",
    "_ga_Y4GN1R87RG": "GS1.1.1743522869.4.1.1743522911.0.0.0"
}

# 根据关键词搜索电影
def search_movie_by_keyword(keyword):
    # 构造请求 URL
    url = f'https://movie.douban.com/j/subject_suggest?q={keyword}'
    try:
        res = requests.get(url, headers=headers, cookies=cookies, timeout=8)
        
        # 如果请求失败，返回空列表
        if res is None:
            return []  # 所有代理都失败了

        # 获取返回的 JSON 数据
        data = res.json()

        # 确保返回的是 JSON 格式
        if 'application/json' not in res.headers.get('Content-Type', ''):
            print("⚠️ 返回的不是 JSON，可能被豆瓣拦截")
            print(res.text[:300])  # 打印 HTML 内容前300字
            return []

        print("🐍 豆瓣返回数据：", data)

        # 处理返回的电影数据
        results = []
        for item in data:
            results.append({
                'id': item['id'],
                'title': item['title'],
                'year': item.get('year', '未知'),
                'cover': item.get('img', 'https://via.placeholder.com/200x300?text=No+Image'),
                'sub_title': item.get('sub_title', ''),
            })

        return results

    except Exception as e:
        print(f'❌ 报错: {e}')
        return []


# 获取电影简短信息
def fetch_movie_brief(movie_id):
    url = f'https://movie.douban.com/subject/{movie_id}/'

    res = requests.get(url, headers=headers, cookies=cookies, timeout=8)
    tree = etree.HTML(res.text)

    # 安全的 XPath 提取方法，避免解析失败
    def safe_xpath(tree, path):
        try:
            result = tree.xpath(path)
            return result[0].strip() if result else ""
        except Exception as e:
            print(f"[safe_xpath] 解析失败：{path}，错误：{e}")
            return ""

    # 获取电影的各类信息
    title = safe_xpath(tree, '//span[@property="v:itemreviewed"]/text()')
    rating = safe_xpath(tree, '//strong[@property="v:average"]/text()')
    summary = safe_xpath(tree, '//span[@property="v:summary"]/text()').replace('\n', '').strip()
    cover = safe_xpath(tree, '//img[@rel="v:image"]/@src')

    directors = tree.xpath('//a[@rel="v:directedBy"]/text()')
    actors = tree.xpath('//a[@rel="v:starring"]/text()')
    genres = tree.xpath('//span[@property="v:genre"]/text()')
    year = safe_xpath(tree, '//span[@property="v:initialReleaseDate"]/text()')

    print("请求豆瓣电影 ID：", movie_id)
    print("导演：", directors)
    print("主演：", actors)
    print("类型：", genres)
    print("上映时间：", year)

    # 返回电影详细信息
    return {
        "id": movie_id,
        "title": title,
        "rating": float(rating) if rating else 0,
        "summary": summary,
        "cover": cover,
        "directors": ", ".join(directors),
        "actors": ", ".join(actors),
        "genres": " / ".join(genres),
        "year": year,
    }


# 根据 URL 获取电影评论
def get_movie_review_by_url(url):
    comments_dict = []
    res = requests.get(url, headers=headers, cookies=cookies, timeout=8)
    tree = etree.HTML(res.text)

    comment_list = tree.xpath('//div[@class="comment-item"]')
    if not comment_list:
        return comments_dict

    for comment_div in comment_list:
        try:
            name = comment_div.xpath('.//span[@class="comment-info"]/a/text()')[0].strip()
        except:
            name = ''
        try:
            content = comment_div.xpath('.//p[@class="comment-content"]/span/text()')[0].strip()
        except:
            continue
        try:
            upvote = int(comment_div.xpath('.//span[@class="votes vote-count"]/text()')[0].strip())
        except:
            upvote = 0
        try:
            time = comment_div.xpath('.//span[@class="comment-time"]/@title')[0]
        except:
            time = ''

        try:
            star_attribute = comment_div.xpath('.//span[contains(@class,"rating")]/@class')[0]
            stars_raw = int(re.search(r'\d+', star_attribute).group())
            if 10 <= stars_raw <= 50:
                stars = stars_raw // 10
            else:
                stars = 0
        except:
            stars = 0


        comments_dict.append({
            'name': name,
            'content': content,
            'upvote': upvote,
            'time': time,
            'stars': stars
        })

    return comments_dict

# 获取电影评论
def get_movie_review(movie_id):
    url = f'https://movie.douban.com/subject/{movie_id}/comments?start=0&limit=20&sort=new_score&status=P'
    print(f"[获取影评] {url}")
    
    comments_dict = get_movie_review_by_url(url)

    print("==================影评获取完毕===================")
    print(f"共获取 {len(comments_dict)} 条影评")
    return comments_dict


# 分页获取电影评论
def get_movie_review_by_page(movie_id, start=0, limit=20):
    """
    分页获取指定电影的影评。

    :param movie_id: 豆瓣电影 ID
    :param start: 起始评论序号（比如第 0 条、第 20 条）
    :param limit: 每页获取条数（默认 20）
    :return: 评论列表
    """
    url = f'https://movie.douban.com/subject/{movie_id}/comments?start={start}&limit={limit}&sort=new_score&status=P'
    print(f"[分页获取评论] {url}")
    comments = get_movie_review_by_url(url)
    return comments


# 计算电影评分分布
def calc_rating_distribution(comments):
    # 将字符串评分转为整数
    stars = [int(c['stars']) for c in comments if c.get('stars') and int(c['stars']) > 0]

    # 统计分布（以5星映射到10分制）
    bins = {'<6': 0, '6~7': 0, '7~8': 0, '8~9': 0, '9~10': 0}
    for s in stars:
        score = s * 2  # 1~5 星 => 2~10 分
        if score < 6:
            bins['<6'] += 1
        elif score < 7:
            bins['6~7'] += 1
        elif score < 8:
            bins['7~8'] += 1
        elif score < 9:
            bins['8~9'] += 1
        else:
            bins['9~10'] += 1
    return bins
