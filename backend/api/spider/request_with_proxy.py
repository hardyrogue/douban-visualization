# import requests
# import random
# import time

# # 加载代理列表
# def load_proxy_list(path='./api/spider/proxies.txt'):
#     try:
#         with open(path, 'r') as f:
#             proxies = f.read().splitlines()
#             return proxies
#     except Exception as e:
#         print("❌ 加载代理列表失败:", e)
#         return []

# # 带自动切换代理的请求函数
# def request_with_retry(url, headers, cookies, max_retries=5, timeout=8):
#     proxy_list = load_proxy_list()
#     tried = set()

#     for _ in range(max_retries):
#         if len(tried) == len(proxy_list):
#             break  # 全部试完了

#         proxy = random.choice(proxy_list)
#         while proxy in tried:
#             proxy = random.choice(proxy_list)
#         tried.add(proxy)

#         proxies = {
#             'http': proxy,
#             'https': proxy
#         }

#         print(f"🌐 尝试代理: {proxy}")
#         try:
#             response = requests.get(url, headers=headers, cookies=cookies, proxies=proxies, timeout=timeout)
#             if response.status_code == 200:
#                 print("✅ 请求成功")
#                 return response
#             else:
#                 print(f"⚠️ 状态码异常: {response.status_code}")
#         except Exception as e:
#             print(f"❌ 请求失败: {e}")

#         time.sleep(random.uniform(1, 2))  # 避免太频繁

#     print("🚫 所有代理都失败了")
#     return None
