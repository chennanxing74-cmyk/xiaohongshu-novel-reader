# Spider小说阅读器项目

一个完整的小说爬取、处理和阅读系统，包含多个功能模块。

## 🚀 在线体验

### 小红书风格阅读器
访问：[https://chennanxing74-cmyk.github.io/spider-novel-reader/xiaohongshu_app/](https://chennanxing74-cmyk.github.io/spider-novel-reader/xiaohongshu_app/)

### 传统阅读器  
访问：[https://chennanxing74-cmyk.github.io/spider-novel-reader/xiaohongshu_reader.py](https://chennanxing74-cmyk.github.io/spider-novel-reader/xiaohongshu_reader.py)

## 📁 项目结构

```
spider/
├── xiaohongshu_app/          # 小红书风格PWA阅读器
│   ├── index.html           # 主页面
│   ├── app.js              # 应用逻辑
│   ├── styles.css          # 样式文件
│   ├── data.js             # 小说数据
│   └── ...                 # 其他资源文件
├── templates/               # HTML模板
│   ├── xiaohongshu_base.html
│   ├── xiaohongshu_index.html
│   ├── xiaohongshu_detail.html
│   └── xiaohongshu_read.html
├── xiaohongshu_reader.py    # Python阅读器服务
├── simple_qidian_crawler.py # 起点小说爬虫
├── novel_generator.py       # 小说生成器
├── novels_data.json         # 小说数据
└── md文件夹/                # 生成的小说文件
```

## ✨ 功能特性

### 📱 小红书风格阅读器
- 现代化移动端UI设计
- PWA支持，可安装为APP
- 响应式布局，完美适配各种设备
- 夜间模式、字体调节
- 收藏、历史记录功能
- 离线阅读支持

### 🐍 Python阅读器
- Flask Web服务
- 小说数据管理
- 章节阅读功能
- API接口支持

### 🕷️ 爬虫系统
- 起点小说爬取
- 数据清洗和处理
- 自动化内容生成

## 🛠️ 本地开发

### 环境要求
- Python 3.7+
- Flask
- Requests
- BeautifulSoup4

### 安装依赖
```bash
pip install flask requests beautifulsoup4 lxml
```

### 启动服务

#### 小红书风格阅读器
```bash
cd xiaohongshu_app
python server.py
# 访问 http://localhost:8000
```

#### Python阅读器
```bash
python xiaohongshu_reader.py
# 访问 http://localhost:5000
```

#### 爬虫系统
```bash
python simple_qidian_crawler.py
```

## 📦 部署说明

### GitHub Pages部署
1. Fork或Clone此仓库
2. 在GitHub仓库设置中启用Pages
3. 选择main分支作为源
4. 访问部署的网站

### 自定义部署
- 小红书风格阅读器：纯静态文件，可部署到任何静态托管服务
- Python阅读器：需要Python环境，可部署到Heroku、Railway等

## 🎯 使用指南

### 小红书风格阅读器
1. 访问在线地址或本地启动
2. 浏览小说列表
3. 点击小说查看详情
4. 开始阅读并享受功能

### Python阅读器
1. 启动xiaohongshu_reader.py
2. 访问Web界面
3. 选择小说和章节
4. 开始阅读

### 爬虫使用
1. 配置目标网站
2. 运行爬虫脚本
3. 获取小说数据
4. 导入到阅读器

## 🔧 配置说明

### 修改GitHub用户名
编辑以下文件中的`your-username`：
- README.md
- xiaohongshu_app/package.json
- xiaohongshu_app/DEPLOYMENT.md

### 自定义小说数据
编辑`xiaohongshu_app/data.js`添加您的小说数据。

### 爬虫配置
编辑`simple_qidian_crawler.py`中的配置参数。

## 📱 PWA安装

### Android/Chrome
1. 访问小红书风格阅读器
2. 点击浏览器菜单中的"添加到主屏幕"
3. 确认安装

### iOS/Safari
1. 访问小红书风格阅读器
2. 点击分享按钮
3. 选择"添加到主屏幕"

## 🤝 贡献

欢迎提交Issue和Pull Request！

### 开发流程
1. Fork项目
2. 创建功能分支
3. 提交更改
4. 发起Pull Request

## 📄 许可证

MIT License

## 📞 联系

如有问题，请提交Issue或联系开发者。

---

**享受阅读时光！** 📚✨
