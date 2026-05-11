import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin # 专门用于拼接 URL 的工具

# --- 1. 获取目录（这部分你已经跑通了） ---
url = 'https://1080zyk6.com/?m=vod-detail-id-32068.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://1080zyk6.com/' 
}
r = requests.get(url, headers=headers)
r.encoding = 'utf-8'
soup = BeautifulSoup(r.text, 'lxml')

m3u8_links = []
play_box = soup.find('div', id='play_2')
for each in play_box.find_all('input'):
    val = each.get('value')
    if val and 'm3u8' in val:
        m3u8_links.append(val)

if m3u8_links:
    # --- 2. 请求第一级 M3U8 ---
    first_m3u8 = m3u8_links[0]
    print(f"第一级地址: {first_m3u8}")
    res1 = requests.get(first_m3u8, headers=headers)
    
    # 逻辑：从返回的内容里寻找下一级的路径
    # 我们找不以 # 开头的最后一行
    lines = res1.text.strip().split('\n')
    next_path = ""
    for line in lines:
        if not line.startswith('#'):
            next_path = line
            break
    
    if next_path:
        # --- 3. 自动拼接并请求第二级 M3U8 (真正的切片列表) ---
        # urljoin 会自动处理相对路径拼接
        real_m3u8_url = urljoin(first_m3u8, next_path)
        print(f"真实切片列表地址: {real_m3u8_url}")
        
        res2 = requests.get(real_m3u8_url, headers=headers)
        print("\n--- 终极内容预览 (TS 列表) ---")
        print(res2.text[:500]) # 先打印前 500 个字符看看