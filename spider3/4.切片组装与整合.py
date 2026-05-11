import os
import requests
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import subprocess

# --- 配置 ---
REAL_M3U8_URL = "https://yzzy.play-cdn11.com/20221120/10115_a5f4a89d/2000k/hls/mixed.m3u8"
SAVE_DIR = "PrisonBreak_S01_E01" # 存储文件夹
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...',
    'Referer': 'https://1080zyk6.com/'
}

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def get_ts_urls():
    """解析 M3U8，获取所有 TS 的完整下载地址"""
    res = requests.get(REAL_M3U8_URL, headers=HEADERS)
    lines = res.text.strip().split('\n')
    ts_urls = []
    for line in lines:
        if not line.startswith('#'):
            # 自动拼接完整地址
            full_url = urljoin(REAL_M3U8_URL, line)
            ts_urls.append(full_url)
    return ts_urls

def download_ts(url_info):
    """单个 TS 下载任务"""
    url, index = url_info
    file_path = os.path.join(SAVE_DIR, f"{index:04d}.ts")
    
    # 如果已经下载过，跳过（断点续传）
    if os.path.exists(file_path):
        return

    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        with open(file_path, 'wb') as f:
            f.write(r.content)
    except Exception as e:
        print(f"下载失败 {url}: {e}")

def merge_ts_with_ffmpeg(video_name):
    print("--- 开始使用 FFmpeg 进行专业合并 ---")
    
    # 1. 生成一个 FFmpeg 认识的文本清单
    list_file = 'file_list.txt'
    # 获取文件夹内所有的 ts 文件并排序
    ts_files = sorted([f for f in os.listdir(SAVE_DIR) if f.endswith('.ts')])
    
    with open(list_file, 'w', encoding='utf-8') as f:
        for ts in ts_files:
            # 写入格式为：file '文件夹/文件名.ts'
            # 注意：ffmpeg 喜欢正斜杠 /
            filepath = os.path.join(SAVE_DIR, ts).replace('\\', '/')
            f.write(f"file '{filepath}'\n")

    # 2. 调用 FFmpeg 命令
    # -f concat: 使用合并功能
    # -safe 0: 允许读取任意路径
    # -c copy: 直接拷贝流，不重新编码（极快，且无损画质）
    # -y: 覆盖已存在的文件
    output_mp4 = f"{video_name}.mp4"
    command = f'ffmpeg -f concat -safe 0 -i {list_file} -c copy -y "{output_mp4}"'
    
    print(f"执行指令: {command}")
    
    # 运行命令
    result = subprocess.run(command, shell=True)
    
    if result.returncode == 0:
        print(f"\n--- 合并成功！ ---")
        print(f"最终视频: {os.path.abspath(output_mp4)}")
        # 合并成功后删除临时清单文件
        os.remove(list_file)
    else:
        print("\n--- FFmpeg 合并失败，请检查控制台报错信息 ---")

if __name__ == '__main__':
    # 1. 拿到所有 TS 地址
    all_ts = get_ts_urls()
    print(f"共发现 {len(all_ts)} 个切片。")

    # 2. 准备带索引的下载列表 [ (url, 0), (url, 1), ... ]
    download_tasks = [(url, i) for i, url in enumerate(all_ts)]

    # 3. 使用线程池下载 (开 20 个线程)
    with ThreadPoolExecutor(max_workers=20) as executor:
        # tqdm 包装任务，显示下载进度
        list(tqdm(executor.map(download_ts, download_tasks), total=len(all_ts), desc="正在并行下载"))

    # 4. 合并视频
    merge_ts_with_ffmpeg("越狱第一季第01集_修复版")