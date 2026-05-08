import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm

def get_content(target):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    req=requests.get(url=target)
    req.encoding='utf-8'
    html=req.text
    bs=BeautifulSoup(html,'lxml')
    texts=bs.find('div',class_='article-content')
    if texts:
        content=texts.text.strip()
    else:
        content="内容获取失败"
    return content

if __name__== '__main__':
    server='https://www.23qb.net'
    target='https://www.23qb.net/book/5912/catalog'
    book_name='诡秘之主第八部.txt'

    
    # 设置想要爬取的部名
    target_volume="第八部 愚者"

    req=requests.get(url=target)
    req.encoding='utf-8'
    html=req.text
    bs=BeautifulSoup(html,'lxml')

    # 先定位到那一部的标题标签
    start_tag=bs.find('h2',string=target_volume)

    chapters=[]
    if start_tag:
        # 获取该标题之后的所有兄弟节点
        for sibling in start_tag.find_next_siblings():
            if sibling.name=='h2': # 碰到下一个“第x部”的标题，立即停止
                break
            a_tag=sibling.find('a') # 寻找当前节点里的a标签
            if a_tag:
                chapters.append(a_tag) # 将属于这一部的链接存入列表
    with open(book_name,'w',encoding='utf-8') as f:
        print(f"开始下载：{target_volume}")
        for chapter in tqdm(chapters, desc=f"正在下载 {target_volume}"):
            url=chapter.get('href')
            # 如果url为空，或者以javascript开头，就跳过当前循环
            if not url or url.startswith('javascript:'):
                continue
            title=chapter.get('title')
            full_url=server+url

            # 1. 打印进度，方便观察执行到哪了
            print(f"正在下载: {title}")

            # 调用函数获取章节内容
            content=get_content(full_url)

            # 写入标题
            f.write(title+'\n')
            # 写入正文
            f.write(content+'\n')

            # 章节之间加个空格，方便阅读
            f.write('\n'+'*'*30+'\n\n')
            time.sleep(0.5)
    print(f"全部下载完成，文件已保存为: {book_name}")

        