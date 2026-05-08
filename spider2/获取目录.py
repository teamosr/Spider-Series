from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

if __name__ == '__main__':
    # 你的目标网址
    target_url = "https://mycomic.com/comics/17965"

    # --- 关键：手动指定你刚下载好的驱动路径 ---
    # r 保证路径里的斜杠不会被转义
    driver_path = r'E:\pachong\chromedriver.exe' 
    service = Service(executable_path=driver_path)
    
    # 启动浏览器
    driver = webdriver.Chrome(service=service)
    
    try:
        print("正在启动浏览器...")
        driver.get(target_url)

        # 针对 CSR 网页，给足渲染时间
        print("正在等待页面渲染（8秒）...")
        time.sleep(8) 

        # 此时拿到的源码就是包含 <a> 标签的了
        html = driver.page_source
        bs = BeautifulSoup(html, 'lxml')

        # 寻找章节列表容器
        l = bs.find('div', class_="grid grid-cols-3 gap-4")
        
        if l:
            comic_list = l.find_all('a')
            chapter_names = []
            chapter_urls = []
            
            for comic in comic_list:
                href = comic.get('href')
                name = comic.text.strip()
                # 保持你原本的逻辑：逆序插入
                chapter_names.insert(0, name)
                chapter_urls.insert(0, href)

            print(f"成功！抓取到 {len(chapter_names)} 个章节。")
            print("前5章标题:", chapter_names[:5])
            print("前5章链接:", chapter_urls[:5])
        else:
            print("未找到列表，请检查网页是否加载完全或 class 是否准确。")

    except Exception as e:
        print(f"出错了: {e}")
        
    finally:
        # 完成后关闭浏览器
        driver.quit()