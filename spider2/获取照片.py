import requests
from bs4 import BeautifulSoup
import os
import time
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# 配置你的驱动路径
DRIVER_PATH = r'E:\pachong\chromedriver.exe'

def download_manga_chapter(chapter_url, chapter_name):
    # 1. 创建文件夹
    save_path = os.path.join("妖神记", chapter_name)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # 2. 使用 Selenium 获取渲染后的页面
    service = Service(executable_path=DRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    
    try:
        print(f"\n正在通过浏览器打开章节: {chapter_name}")
        driver.get(chapter_url)
        
        # 关键：给足够的时间让图片标签渲染出来
        # 如果漫画页数很多，建议增加等待时间
        time.sleep(8) 

        # 3. 解析渲染后的源码
        html = driver.page_source
        bs = BeautifulSoup(html, 'lxml')

        # 4. 提取图片链接
        # 尝试更宽泛的搜索：寻找所有包含 'chapters' 的图片链接
        img_tags = bs.find_all('img')
        img_urls = []
        for img in img_tags:
            url = img.get('src') or img.get('data-src')
            # 过滤：只要包含该章节 ID 或特定图片服务器地址的链接
            if url and ('chapters' in url or 'biccam.com' in url):
                if not url.endswith('.png'): # 排除掉小图标
                    img_urls.append(url)

        # 5. 去重并保持顺序
        # 有时候由于渲染机制，会抓到重复的链接
        unique_urls = []
        for u in img_urls:
            if u not in unique_urls:
                unique_urls.append(u)

        print(f"解析成功，准备下载 {len(unique_urls)} 页漫画图片...")

        # 6. 使用 Requests 携带 Referer 下载
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...',
            'Referer': chapter_url  # 必须带上当前章节页作为来源
        }

        for i, img_url in enumerate(tqdm(unique_urls, desc="下载进度")):
            try:
                # 补全协议
                if img_url.startswith('//'):
                    img_url = 'https:' + img_url
                
                # 下载二进制数据
                img_data = requests.get(img_url, headers=headers, timeout=15).content
                
                # 保存文件：001.jpg, 002.jpg ...
                file_name = f"{i+1:03d}.jpg"
                with open(os.path.join(save_path, file_name), 'wb') as f:
                    f.write(img_data)
            except Exception as e:
                print(f"\n第 {i+1} 页下载失败: {e}")

    finally:
        driver.quit()

if __name__ == '__main__':
    # 测试下载第一回
    download_manga_chapter("https://mycomic.com/chapters/194612", "第01回 重生")