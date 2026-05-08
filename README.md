# Python 爬虫实战系列 
## 实战1：小说爬取下载

这是我学习爬虫系列的第一个案例，主要实现了对特定小说网站分章节下载的功能。

### 功能特点
- 支持按“部/卷”精准定位下载。
- 自动过滤无效的 JavaScript 链接。
- 使用 `tqdm` 实现可视化下载进度条。
- 自动保存为 UTF-8 编码的 TXT 文件。

### 使用说明
1. 安装依赖：`pip install -r requirements.txt`
2. 运行脚本：`python main.py`

### 爬取的小说链接：https://www.23qb.net/book/5912/catalog  （这是一个免费的看小说的网站）

### 学习参考
https://mp.weixin.qq.com/s?__biz=MzIxODg1OTk1MA==&mid=2247484957&idx=1&sn=7fe85c937c0c3147369288be8bb50a4b&chksm=97e556dca092dfca06b4b806a899ef6b6d5c476e42d96ee3414195ec875d2e5e2d7dd60fbf4d&cur_album_id=1350803219538149376&scene=189#wechat_redirect

### 个人总结：
该项目参考学习参考的资料来进行操作，学习参考中涉及的小说网站已经失效，所以选择了我所提供的小说链接，同时我进行爬取的在这个网站的操作要比学习参考中遇到的情况更加的复杂，同时从这个爬虫中我学习到了按照“部”来精准定位下载