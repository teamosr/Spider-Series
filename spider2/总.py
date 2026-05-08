import os
import time
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# --- 配置 ---
DRIVER_PATH = r'E:\pachong\chromedriver.exe'
TARGET_URL = "https://mycomic.com/comics/17965" # 目录页

def get_driver():
    service = Service(executable_path=DRIVER_PATH)
    return webdriver.Chrome(service=service)

def download_chapters():
    driver = get_driver()
    try:
        # 1. 抓取目录（之前验证成功的 Selenium 逻辑）
        driver.get(TARGET_URL)
        time.sleep(5) 
        bs_menu = BeautifulSoup(driver.page_source, 'lxml')
        l = bs_menu.find('div', class_="grid grid-cols-3 gap-4")
        comic_list = l.find_all('a')
        
        # 整理章节信息
        tasks = []
        for comic in comic_list:
            tasks.insert(0, {
                'name': comic.text.strip(),
                'url': comic.get('href')
            })
        
        print(f"共发现 {len(tasks)} 个章节，准备开始下载...")

        # 2. 遍历章节进行下载
        for task in tasks:
            chapter_name = task['name']
            chapter_url = task['url']
            
            # 创建文件夹
            save_path = os.path.join("妖神记", chapter_name)
            if os.path.exists(save_path):
                continue
            os.makedirs(save_path)

            # 使用 Selenium 进入章节页（确保通过环境检测）
            driver.get(chapter_url)
            time.sleep(8) # 给够时间加载
            
            bs_chapter = BeautifulSoup(driver.page_source, 'lxml')
            # 找到所有包含 class='page' 的 img 标签
            img_tags = bs_chapter.find_all('img', class_='page')
            
            # 提取链接：尊重你的发现，同时检查 data-src 和 src
            img_urls = []
            for img in img_tags:
                actual_link = img.get('data-src') or img.get('src')
                if actual_link and 'biccam.com' in actual_link:
                    img_urls.append(actual_link)

            # 去重
            final_urls = []
            for u in img_urls:
                if u not in final_urls: final_urls.append(u)

            # 3. 下载图片（带上 Referer 绕过防盗链）
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...',
                'Referer': chapter_url
            }
            
            for i, img_url in enumerate(tqdm(final_urls, desc=f"正在下载 {chapter_name}", leave=False)):
                try:
                    r = requests.get(img_url, headers=headers, timeout=15)
                    file_name = f"{i+1:03d}.jpg" # 保证三位数排序
                    with open(os.path.join(save_path, file_name), 'wb') as f:
                        f.write(r.content)
                except:
                    continue

    finally:
        driver.quit()

if __name__ == '__main__':
    download_chapters()