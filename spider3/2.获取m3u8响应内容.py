import requests
from bs4 import BeautifulSoup

# --- 1. 获取目录链接 ---
url = 'https://1080zyk6.com/?m=vod-detail-id-32068.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://1080zyk6.com/' 
}

r = requests.get(url, headers=headers)
r.encoding = 'utf-8'
soup = BeautifulSoup(r.text, 'lxml')

m3u8_links = []
# 寻找 play_2 下的所有 input
play_box = soup.find('div', id='play_2')
if play_box:
    for each in play_box.find_all('input'):
        val = each.get('value')
        if val and 'm3u8' in val:
            m3u8_links.append(val)
            # print(val) # 这里不再重复打印

# --- 2. 尝试请求第一个 M3U8 内容 ---
if m3u8_links:
    # 直接用列表里的第一个链接，不做任何处理！
    first_m3u8 = m3u8_links[0]
    print(f"正在请求第一个资源: {first_m3u8}")
    
    # 这里是关键，一定要关加速器，带上 headers
    res = requests.get(first_m3u8, headers=headers)
    
    print("\n--- 响应内容如下 ---")
    print(res.text)