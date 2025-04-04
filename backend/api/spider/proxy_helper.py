import random

def get_random_proxy():
    try:
        with open('./api/spider/proxies.txt', 'r') as f:
            lines = f.read().splitlines()
            proxy = random.choice(lines)
            return {
                'http': proxy,
                'https': proxy
            }
    except Exception as e:
        print("❌ 加载代理失败:", e)
        return None
