
<h1 align="center">webvideo-downloader-admin</h1>

视频下载器，用于下载网站中可以在线播放的视频。
基于 FastAPI + Vue3 + Naive UI 的现代化前后端

### 功能介绍
可下载管理主流视频网站的在线视频。
#### 主要支持网站
 哔哩哔哩（单P/多P）、爱奇艺 、腾讯视频、芒果TV、 WeTV、爱奇艺国际站 

### 快速开始
#### 安装
##### 浏览器安装插件
- [Violentmonkey](https://violentmonkey.github.io/) /  [Tampermonkey](https://www.tampermonkey.net/) (二选一)
##### 浏览器插件脚本
浏览器安装以下基于 Violentmonkey/Tampermonkey 的脚本。直接点击以下链接即可安装：
- [WebVideoDownloader 脚本](https://github.com/jaysonlong/webvideo-downloader/raw/master/violentmonkey/WebVideoDownloader.user.js)（主脚本，支持6个主流网站视频下载）
- [CommonHlsDownloader 脚本](https://github.com/jaysonlong/webvideo-downloader/raw/master/violentmonkey/CommonHlsDownloader.user.js)（通用 HLS 下载脚本，按需安装，作用于除以上6个主流网站以外的使用 HLS 的网站）

#### 本地启动服务端
#### 后端
启动项目需要以下环境：
- Python 3.11

#### 方法一（推荐）：使用 conda 安装依赖
1. 创建conda环境
```sh
conda create -n webvideo-downloader-admin python=3.11
```

2. 创建并激活虚拟环境
```sh
conda activate webvideo-downloader-admin

```

3. 安装依赖
```sh
conda install pip
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

4. 启动服务
```sh
python run.py
```

#### 方法二：使用 Pip 安装依赖
1. 创建虚拟环境
```sh
python3 -m venv venv
```

2. 激活虚拟环境
```sh
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. 安装依赖
```sh
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

4. 启动服务
```sh
python run.py
```

服务现在应该正在运行，访问 http://localhost:9999/docs 查看API文档

#### 前端
启动项目需要以下环境：
- node v18.8.0+

1. 进入前端目录
```sh
cd web
```

2. 安装依赖(建议使用pnpm: https://pnpm.io/zh/installation)
```sh
npm i -g pnpm # 已安装可忽略
pnpm i # 或者 npm i
```

3. 启动
```sh
pnpm dev
```

#### 使用
1. 打开视频网站
2. 点击下载视频，录入相关信息
3. 后台即会下载
#### 后台管理
1. 打开浏览器，访问 http://localhost:3100/
2. 输入用户名密码 
   - 默认用户名：admin
   - 默认密码：123456
3. 点击左侧菜单栏的“下载任务”进入下载页面

## 背景故事
每每点开自己的某B站的收藏夹，满满视频百分之七八十都已变成“已失效视频”（连原视频的内容和标题），看着这些这么优秀的视频被删除，心中不禁充满遗憾。
那些剩下的还活着的视频，心中总是有些不安，万一哪天这些也被视频被删除了怎么办？
于是就想着找个下载器备份起来，于是就找到了[jaysonlong/webvideo-downloader](https://github.com/jaysonlong/webvideo-downloader)。
webvideo-downloader虽然满足了我们的需求但是感觉还不够友好，每次下载都是命令行。于是想着结合web写一个下载管理，能把视频都下载下来并管理起来。
于是就有了这个项目。我希望这个项目能帮助到你们，能让你们把喜欢的视频都下载下来，保存备份起来。希望未来能有以下功能：
1. 支持桌面端，能够直接双击运行启动一个客户端，管理下载
2. 支持作为服务端，能远程管理与下载
3. 可以管理下载的视频，甚至能双击就可以播放。

功能开发顺序将会是:
1,3,2


## 感谢
感谢以下项目，此项目是以下项目的整合
[mizhexiaoxiao/vue-fastapi-admin](https://github.com/mizhexiaoxiao/vue-fastapi-admin)
[jaysonlong/webvideo-downloader](https://github.com/jaysonlong/webvideo-downloader)

<img align="left" src = "https://profile-counter.glitch.me/webvideo-downloader-admin/count.svg" alt="Loading">

## 免责
1. 本项目仅供学习研究技术，学习交流使用，禁止用于商业用途，禁止用于任何违法用途。
2. 本项目不对任何因使用本项目而导致的损失或损害承担责任。
3. 本项目不对任何因使用本项目而导致的法律责任承担责任。
4. 如有侵权行为，请联系作者删除。
5. 复制、使用、修改本项目即视为同意免责条款。
