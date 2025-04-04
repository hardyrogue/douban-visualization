# import requests
# from lxml import etree
# import re
# import time as t
# import random
# import os
# import json
# from .statistic import MovieReviewStatistic

# def get_html(url):
#     cookies = {
#         'bid': '1gMxgR_xU5U',
#         'll': '"118282"',
#         'Hm_lvt_19fc7b106453f97b6a84d64302f21a04': '1733372099',
#         '_ga_PRH9EWN86K': 'GS1.2.1733372100.1.0.1733372100.0.0.0',
#         '_pk_id.100001.8cb4': 'b471986e3f50b77b.1733372155.',
#         '_vwo_uuid_v2': 'D8DB7696A3F6AD5AF442F89BBAA685C83|ba3269f7a883157ff71737fd00d2c8c0',
#         '_ga': 'GA1.1.857826835.1733372040',
#         '_ga_Y4GN1R87RG': 'GS1.1.1735141304.2.1.1735141359.0.0.0',
#         'dbcl2': '"224267170:eEXqtpqkCjk"',
#         'push_noty_num': '0',
#         'push_doumail_num': '0',
#         'ck': 'N56a',
#         'ap_v': '0,6.0',
#         '_pk_ref.100001.8cb4': '%5B%22%22%2C%22%22%2C1742305309%2C%22https%3A%2F%2Fsearch.douban.com%2Fmovie%22%5D',
#         '_pk_ses.100001.8cb4': '1',
#         'frodotk_db': '"5321b30168c70291f96519043a5507b3"',
#         '__yadk_uid': 'gOqlfIhhHdGTu9Q4DmnXxqLQBNZrSMFz',
#         '__utma': '30149280.857826835.1733372040.1740574756.1742305312.7',
#         '__utmc': '30149280',
#         '__utmz': '30149280.1742305312.7.5.utmcsr=search.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/movie',
#         '__utmv': '30149280.22426',
#         '__utmb': '30149280.8.10.1742305312',
#     }
#     #cookie = 'bid=dQym6gwlwHs; ll="108288"; __utmz=30149280.1741962662.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=30149280.1415938108.1741962210.1741962662.1743339137.2; __utmc=30149280; __utma=223695111.1415938108.1741962210.1743339138.1743339138.1; __utmb=223695111.0.10.1743339138; __utmc=223695111; __utmz=223695111.1743339138.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _pk_id.100001.4cf6=9c2940b9c9b09700.1743339138.; _pk_ses.100001.4cf6=1; ap_v=0,6.0; _gid=GA1.2.584907224.1743339408; _ga=GA1.1.1415938108.1741962210; _ga_Y4GN1R87RG=GS1.1.1743339407.2.0.1743339431.0.0.0; dbcl2="285724563:A9REG/2ELd4"; ck=eLKu; frodotk_db="1ddc362addbbf1f85994a2809933d5e8"; push_noty_num=0; push_doumail_num=0; __utmt=1; __utmv=30149280.28572; __utmb=30149280.3.9.1743339527611; __yadk_uid=vAoQxPGrvG3hXYKA1UAMTKNHV5Rfbf8G'
#     headers = {
#         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#         'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8',
#         'cache-control': 'max-age=0',
#         'priority': 'u=0, i',
#         'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
#         'sec-ch-ua-mobile': '?0',
#         'sec-ch-ua-platform': '"Windows"',
#         'sec-fetch-dest': 'document',
#         'sec-fetch-mode': 'navigate',
#         'sec-fetch-site': 'none',
#         'sec-fetch-user': '?1',
#         'upgrade-insecure-requests': '1',
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
#         # 'cookie': 'bid=1gMxgR_xU5U; ll="118282"; Hm_lvt_19fc7b106453f97b6a84d64302f21a04=1733372099; _ga_PRH9EWN86K=GS1.2.1733372100.1.0.1733372100.0.0.0; _pk_id.100001.8cb4=b471986e3f50b77b.1733372155.; _vwo_uuid_v2=D8DB7696A3F6AD5AF442F89BBAA685C83|ba3269f7a883157ff71737fd00d2c8c0; _ga=GA1.1.857826835.1733372040; _ga_Y4GN1R87RG=GS1.1.1735141304.2.1.1735141359.0.0.0; dbcl2="224267170:eEXqtpqkCjk"; push_noty_num=0; push_doumail_num=0; ck=N56a; ap_v=0,6.0; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1742305309%2C%22https%3A%2F%2Fsearch.douban.com%2Fmovie%22%5D; _pk_ses.100001.8cb4=1; frodotk_db="5321b30168c70291f96519043a5507b3"; __yadk_uid=gOqlfIhhHdGTu9Q4DmnXxqLQBNZrSMFz; __utma=30149280.857826835.1733372040.1740574756.1742305312.7; __utmc=30149280; __utmz=30149280.1742305312.7.5.utmcsr=search.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/movie; __utmv=30149280.22426; __utmb=30149280.8.10.1742305312',
#     }
#     return requests.get(url=url, cookies=cookies, headers=headers).text

# def get_movie_id(movie_name):
#     url = f'https://search.douban.com/movie/subject_search?search_text={movie_name}'
    
#     response_text = get_html(url)
#     # 使用正则表达式提取 "id" 和 "title"
#     pattern = r'"id":\s*(\d+).*?"title":\s*"([^"]+)"'

#     matches = re.findall(pattern, response_text)

#     # 将结果转换为字典
#     result = {int(match[0]): match[1].encode().decode('unicode_escape') for match in matches}

#     return result
# def get_movie_detail(movie_id):
#     import requests
#     from lxml import etree

#     url = f'https://movie.douban.com/subject/{movie_id}/'
#     headers = {
#         'User-Agent': 'Mozilla/5.0'
#     }

#     res = requests.get(url, headers=headers, timeout=10)
#     tree = etree.HTML(res.text)

#     try:
#         cover = tree.xpath('//div[@id="mainpic"]/a/img/@src')[0]
#     except:
#         cover = 'https://via.placeholder.com/200x300?text=No+Image'

#     try:
#         rating = float(tree.xpath('//strong[@class="ll rating_num"]/text()')[0])
#     except:
#         rating = 0

#     try:
#         year_text = tree.xpath('//span[@class="year"]/text()')[0]
#         year = ''.join(filter(str.isdigit, year_text))  # 提取纯数字年份
#     except:
#         year = '未知'

#     return {
#         'cover': cover,
#         'rating': rating,
#         'year': year
#     }


# def get_movie_review_by_url(url):
#     comments_dict = []

#     tree = etree.HTML(get_html(url))

#     comment_list = tree.xpath('//div[@class="comment-item"]')
#     if len(comment_list) == 0:
#         return comments_dict
    
#     for comment_div in comment_list:
#         try:
#             name = comment_div.xpath('.//span[@class="comment-info"]/a/text()')[0].strip()
#         except:
#             name = ''
#         try:
#             content = comment_div.xpath('.//p[@class="comment-content"]/span/text()')[0].strip()
#         except:
#             continue
#         upvote = comment_div.xpath('.//span[@class="votes vote-count"]/text()')[0].strip()
#         time = comment_div.xpath('.//span[@class="comment-time"]/@title')[0]
#         try:
#             location = comment_div.xpath('.//span[@class="comment-location"]/text()')[0].strip()
#         except:
#             location = ''
        
#         try:
#             star_attribute = comment_div.xpath('.//span[contains(@class,"rating")]/@class')[0]
#             stars = re.search(r'\d+', star_attribute).group()[0]
#         except:
#             stars = 0

#         comments_dict.append({
#             'name': name,
#             'content': content,
#             'upvote': upvote,
#             'time': time,
#             # 'location': location,
#             'stars': stars
#         })

#     return comments_dict

# def get_movie_review(movie_id):
#     url = f'https://movie.douban.com/subject/{movie_id}/comments?start=0&limit=20&sort=new_score&status=P'
#     print(f"[获取影评] {url}")
    
#     comments_dict = get_movie_review_by_url(url)

#     print("==================影评获取完毕===================")
#     print(f"共获取 {len(comments_dict)} 条影评")
#     return comments_dict
# def get_movie_review_by_page(movie_id, start=0, limit=20):
#     """
#     分页获取指定电影的影评。

#     :param movie_id: 豆瓣电影 ID
#     :param start: 起始评论序号（比如第 0 条、第 20 条）
#     :param limit: 每页获取条数（默认 20）
#     :return: 评论列表
#     """
#     url = f'https://movie.douban.com/subject/{movie_id}/comments?start={start}&limit={limit}&sort=new_score&status=P'
#     print(f"[分页获取评论] {url}")
#     comments = get_movie_review_by_url(url)
#     return comments

          
# def save_movie_review(movie_name, comments_dict):
#     dir_path = f'./data/{movie_name}'
#     os.makedirs(dir_path, exist_ok=True)
#     with open(os.path.join(dir_path, 'comments.json'), 'w', encoding='utf-8') as f:
#         json.dump(comments_dict, f, ensure_ascii=False, indent=4)

# def main():
#     movie_name = input("请输入电影名称：")
#     movie_id_dict = get_movie_id(movie_name)
    
#     for index, movie_id in enumerate(movie_id_dict):
#         print(f"{index+1}. {movie_id_dict[movie_id]}")
    
#     movie_index = int(input("请输入电影ID："))
#     movie_id = list(movie_id_dict.keys())[movie_index-1]
    
#     comments_dict = get_movie_review(movie_id)
#     save_movie_review(movie_name, comments_dict)
    
#     movie_review_statistic = MovieReviewStatistic(movie_name, comments_dict)
#     movie_review_statistic.stastic_star()
#     movie_review_statistic.statistic_comment()
    

# if __name__ == '__main__':
#     main()