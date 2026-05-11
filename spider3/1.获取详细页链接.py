import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time

def search_video_with_manual_verify(keyword):
    # 1. 使用 undetected_chromedriver 避开 Cloudflare 检测
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options)
    
    try:
        # 直接访问搜索链接 (尝试使用 GET 方式进入，如果不行再手动点击)
        search_url = f"https://1080zyk6.com/index.php?m=vod-search&wd={keyword}"
        driver.get(search_url)
        
        print("--- 检查是否出现验证码 ---")
        
        # 2. 循环检测，直到验证码消失并出现结果
        while True:
            html = driver.page_source
            if "安全验证" in html or "请输入验证码" in html:
                print("请在打开的浏览器中手动输入验证码并点击提交...")
                time.sleep(3) # 每3秒检查一次
            elif keyword in html and "xing_vb4" in html:
                print("验证通过，正在解析结果...")
                break
            else:
                print("等待页面加载或手动操作中...")
                time.sleep(3)

        # 3. 此时已经进入了搜索结果页
        bs = BeautifulSoup(driver.page_source, 'lxml')
        links = bs.select('span.xing_vb4 a')
        
        if links:
            for a in links:
                title = a.get_text(strip=True)
                href = a.get('href')
                full_url = "https://1080zyk6.com" + href
                print(f"\n找到结果: {title}")
                print(f"详情页链接: {full_url}")
                return full_url
        else:
            print("未找到结果，请确认搜索词是否正确。")

    finally:
        # 为了调试方便，你可以先注释掉这一行，手动看完结果再关
        # driver.quit()
        pass

if __name__ == '__main__':
    search_video_with_manual_verify("越狱第一季")