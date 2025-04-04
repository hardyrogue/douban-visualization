# import requests
# from lxml import etree
# import time

# def fetch_89ip_proxies(pages=3):
#     proxies = []
#     headers = {
#         'User-Agent': 'Mozilla/5.0'
#     }

#     for i in range(1, pages + 1):
#         url = f"https://www.89ip.cn/index_{i}.html"
#         try:
#             res = requests.get(url, headers=headers, timeout=10)
#             res.encoding = 'utf-8'  # 指定编码，防止乱码
#             tree = etree.HTML(res.text)

#             ip_list = tree.xpath('//table[@class="layui-table"]/tbody/tr')
#             for row in ip_list:
#                 ip = row.xpath('./td[1]/text()')[0].strip()
#                 port = row.xpath('./td[2]/text()')[0].strip()
#                 proxy = f"http://{ip}:{port}"
#                 proxies.append(proxy)

#             time.sleep(1)  # 避免过快被限速
#         except Exception as e:
#             print(f"⚠️ 第{i}页抓取失败：", e)

#     return proxies

# def validate_proxy(proxy):
#     try:
#         res = requests.get("https://movie.douban.com", proxies={'http': proxy, 'https': proxy}, timeout=4)
#         return res.status_code == 200
#     except:
#         return False

# def filter_valid_proxies(proxy_list):
#     valid = []
#     print(f"🔍 正在验证 {len(proxy_list)} 个代理...")
#     for i, proxy in enumerate(proxy_list):
#         print(f"  [{i+1}/{len(proxy_list)}] 检查: {proxy}", end=' ')
#         if validate_proxy(proxy):
#             print("✅ 可用")
#             valid.append(proxy)
#         else:
#             print("❌ 无效")
#     return valid

# def save_proxies(proxies, file_path='./api/spider/proxies.txt'):
#     with open(file_path, 'w') as f:
#         for proxy in proxies:
#             f.write(proxy + '\n')
#     print(f"\n✅ 成功保存 {len(proxies)} 个可用代理到 {file_path}")

# def update_proxy_pool():
#     raw = fetch_89ip_proxies(pages=3)
#     valid = filter_valid_proxies(raw)
#     save_proxies(valid)

# if __name__ == '__main__':
#     update_proxy_pool()
