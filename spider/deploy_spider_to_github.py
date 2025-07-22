#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spider项目GitHub部署脚本
将整个spider项目部署到GitHub Pages，支持xiaohongshu_reader.py运行
"""

import os
import shutil
import subprocess
import json
from pathlib import Path

class SpiderGitHubDeployer:
    """Spider项目GitHub部署器"""
    
    def __init__(self):
        self.spider_dir = Path(__file__).parent
        self.repo_name = "spider-novel-reader"
        self.github_username = "your-username"  # 需要替换
        
    def create_main_readme(self):
        """创建主README文件"""
        readme_content = f"""# Spider小说阅读器项目

一个完整的小说爬取、处理和阅读系统，包含多个功能模块。

## 🚀 在线体验

### 小红书风格阅读器
访问：[https://{self.github_username}.github.io/{self.repo_name}/xiaohongshu_app/](https://{self.github_username}.github.io/{self.repo_name}/xiaohongshu_app/)

### 传统阅读器  
访问：[https://{self.github_username}.github.io/{self.repo_name}/xiaohongshu_reader.py](https://{self.github_username}.github.io/{self.repo_name}/xiaohongshu_reader.py)

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
"""
        
        with open(self.spider_dir / "README.md", 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print("✅ 主README.md已创建")
    
    def create_github_workflow(self):
        """创建GitHub Actions工作流"""
        github_dir = self.spider_dir / ".github" / "workflows"
        github_dir.mkdir(parents=True, exist_ok=True)
        
        workflow_content = """name: Deploy Spider Project to GitHub Pages

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout
      uses: actions/checkout@v3
      
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install flask requests beautifulsoup4 lxml
        
    - name: Test Python scripts
      run: |
        # 测试Python脚本语法
        python -m py_compile xiaohongshu_reader.py
        python -m py_compile simple_qidian_crawler.py
        python -m py_compile novel_generator.py
        echo "Python scripts syntax check passed"
        
    - name: Prepare deployment
      run: |
        # 创建部署目录
        mkdir -p deploy
        
        # 复制所有文件
        cp -r * deploy/ || true
        
        # 确保xiaohongshu_app是主要入口
        cp -r xiaohongshu_app/* deploy/
        
        # 创建Python脚本访问页面
        echo '<!DOCTYPE html>
        <html>
        <head>
            <title>Spider项目 - Python脚本</title>
            <meta charset="UTF-8">
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .script-link { display: block; margin: 10px 0; padding: 10px; 
                              background: #f0f0f0; text-decoration: none; border-radius: 5px; }
                .script-link:hover { background: #e0e0e0; }
            </style>
        </head>
        <body>
            <h1>Spider小说阅读器项目</h1>
            <h2>可用功能：</h2>
            <a href="xiaohongshu_app/" class="script-link">📱 小红书风格阅读器 (推荐)</a>
            <a href="xiaohongshu_reader.py" class="script-link">🐍 Python阅读器脚本</a>
            <a href="simple_qidian_crawler.py" class="script-link">🕷️ 起点爬虫脚本</a>
            <a href="novel_generator.py" class="script-link">📝 小说生成器脚本</a>
            <a href="novels_data.json" class="script-link">📊 小说数据文件</a>
            
            <h2>使用说明：</h2>
            <p>• 小红书风格阅读器：直接在浏览器中使用的现代化阅读器</p>
            <p>• Python脚本：需要下载到本地运行，需要Python环境</p>
            <p>• 详细说明请查看 <a href="README.md">README.md</a></p>
        </body>
        </html>' > deploy/python-scripts.html
        
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      if: github.ref == 'refs/heads/main'
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./deploy
        exclude_assets: '.github,__pycache__,*.pyc'
"""
        
        with open(github_dir / "deploy.yml", 'w', encoding='utf-8') as f:
            f.write(workflow_content)
        
        print("✅ GitHub Actions工作流已创建")
    
    def create_gitignore(self):
        """创建.gitignore文件"""
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Temporary files
*.tmp
*.temp

# Node modules (if any)
node_modules/

# Deployment
deploy/
.github/

# Local development
.env
.env.local
"""
        
        with open(self.spider_dir / ".gitignore", 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        
        print("✅ .gitignore已创建")
    
    def create_requirements_txt(self):
        """创建requirements.txt"""
        requirements = """Flask==2.3.3
requests==2.31.0
beautifulsoup4==4.12.2
lxml==4.9.3
Werkzeug==2.3.7
"""
        
        with open(self.spider_dir / "requirements.txt", 'w', encoding='utf-8') as f:
            f.write(requirements)
        
        print("✅ requirements.txt已创建")
    
    def create_package_json(self):
        """创建package.json"""
        package_data = {
            "name": self.repo_name,
            "version": "1.0.0",
            "description": "Spider小说阅读器项目 - 完整的小说爬取、处理和阅读系统",
            "main": "xiaohongshu_reader.py",
            "scripts": {
                "start": "python xiaohongshu_reader.py",
                "dev": "cd xiaohongshu_app && python server.py",
                "crawler": "python simple_qidian_crawler.py",
                "generate": "python novel_generator.py"
            },
            "keywords": [
                "novel",
                "reader",
                "crawler",
                "spider",
                "xiaohongshu",
                "pwa",
                "flask"
            ],
            "author": "Spider Team",
            "license": "MIT",
            "homepage": f"https://{self.github_username}.github.io/{self.repo_name}/",
            "repository": {
                "type": "git",
                "url": f"https://github.com/{self.github_username}/{self.repo_name}.git"
            },
            "bugs": {
                "url": f"https://github.com/{self.github_username}/{self.repo_name}/issues"
            }
        }
        
        with open(self.spider_dir / "package.json", 'w', encoding='utf-8') as f:
            json.dump(package_data, f, indent=2, ensure_ascii=False)
        
        print("✅ package.json已创建")
    
    def update_xiaohongshu_reader(self):
        """更新xiaohongshu_reader.py以支持GitHub Pages"""
        reader_file = self.spider_dir / "xiaohongshu_reader.py"
        
        if reader_file.exists():
            content = reader_file.read_text(encoding='utf-8')
            
            # 添加GitHub Pages支持注释
            github_comment = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书风格小说阅读器 - GitHub Pages版本

注意：此文件在GitHub Pages上作为静态文件提供下载。
要运行此脚本，请：
1. 下载到本地
2. 安装依赖：pip install flask requests beautifulsoup4 lxml
3. 运行：python xiaohongshu_reader.py
4. 访问：http://localhost:5000

在线版本请访问：xiaohongshu_app/
"""

'''
            
            # 如果文件开头没有这个注释，就添加
            if "GitHub Pages版本" not in content:
                # 保留原有的编码声明，在其后添加注释
                lines = content.split('\n')
                new_lines = []
                added_comment = False
                
                for i, line in enumerate(lines):
                    new_lines.append(line)
                    if line.startswith('# -*- coding:') and not added_comment:
                        new_lines.extend([
                            '"""',
                            '小红书风格小说阅读器 - GitHub Pages版本',
                            '',
                            '注意：此文件在GitHub Pages上作为静态文件提供下载。',
                            '要运行此脚本，请：',
                            '1. 下载到本地',
                            '2. 安装依赖：pip install flask requests beautifulsoup4 lxml',
                            '3. 运行：python xiaohongshu_reader.py',
                            '4. 访问：http://localhost:5000',
                            '',
                            '在线版本请访问：xiaohongshu_app/',
                            '"""',
                            ''
                        ])
                        added_comment = True
                
                updated_content = '\n'.join(new_lines)
                reader_file.write_text(updated_content, encoding='utf-8')
                print("✅ xiaohongshu_reader.py已更新GitHub Pages支持")
    
    def create_index_html(self):
        """创建主index.html文件"""
        index_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spider小说阅读器项目</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}
        h1 {{
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5rem;
        }}
        .feature-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .feature-card {{
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            transition: transform 0.3s ease;
        }}
        .feature-card:hover {{
            transform: translateY(-5px);
        }}
        .feature-icon {{
            font-size: 3rem;
            margin-bottom: 15px;
        }}
        .btn {{
            display: inline-block;
            padding: 12px 24px;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            text-decoration: none;
            border-radius: 25px;
            border: 2px solid white;
            transition: all 0.3s ease;
            margin: 10px;
        }}
        .btn:hover {{
            background: white;
            color: #667eea;
        }}
        .btn-primary {{
            background: #ff6b6b;
            border-color: #ff6b6b;
        }}
        .btn-primary:hover {{
            background: white;
            color: #ff6b6b;
        }}
        .description {{
            text-align: center;
            margin: 20px 0;
            font-size: 1.1rem;
            opacity: 0.9;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 Spider小说阅读器项目</h1>
        
        <p class="description">
            完整的小说爬取、处理和阅读系统，包含现代化Web阅读器和Python工具集
        </p>
        
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">📱</div>
                <h3>小红书风格阅读器</h3>
                <p>现代化PWA阅读器，支持离线阅读、夜间模式、收藏功能</p>
                <a href="xiaohongshu_app/" class="btn btn-primary">立即体验</a>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">🐍</div>
                <h3>Python阅读器</h3>
                <p>Flask Web服务，提供API接口和后端功能</p>
                <a href="xiaohongshu_reader.py" class="btn">下载脚本</a>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">🕷️</div>
                <h3>爬虫系统</h3>
                <p>起点小说爬取工具，自动获取小说数据</p>
                <a href="simple_qidian_crawler.py" class="btn">下载爬虫</a>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">📝</div>
                <h3>小说生成器</h3>
                <p>AI辅助小说生成工具，创作您的专属小说</p>
                <a href="novel_generator.py" class="btn">下载生成器</a>
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <h3>🚀 快速开始</h3>
            <p>推荐直接使用小红书风格阅读器，无需安装任何软件</p>
            <a href="xiaohongshu_app/" class="btn btn-primary">开始阅读</a>
            <a href="README.md" class="btn">查看文档</a>
        </div>
        
        <div style="text-align: center; margin-top: 30px; opacity: 0.8;">
            <p>📊 <a href="novels_data.json" style="color: white;">小说数据</a> | 
               📁 <a href="templates/" style="color: white;">模板文件</a> | 
               📖 <a href="md文件夹/" style="color: white;">生成小说</a></p>
        </div>
    </div>
    
    <script>
        // 简单的交互效果
        document.querySelectorAll('.feature-card').forEach(card => {{
            card.addEventListener('mouseenter', () => {{
                card.style.background = 'rgba(255, 255, 255, 0.2)';
            }});
            card.addEventListener('mouseleave', () => {{
                card.style.background = 'rgba(255, 255, 255, 0.1)';
            }});
        }});
    </script>
</body>
</html>"""
        
        with open(self.spider_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        print("✅ 主index.html已创建")
    
    def run_deployment_prep(self):
        """运行部署准备"""
        print("🚀 开始准备Spider项目GitHub部署...")
        print("=" * 60)
        
        try:
            # 创建所有必需文件
            self.create_main_readme()
            self.create_github_workflow()
            self.create_gitignore()
            self.create_requirements_txt()
            self.create_package_json()
            self.update_xiaohongshu_reader()
            self.create_index_html()
            
            print("\n" + "=" * 60)
            print("🎉 Spider项目GitHub部署准备完成！")
            print("\n📋 接下来的步骤：")
            print("1. 修改github_username变量")
            print("2. 创建GitHub仓库")
            print("3. 推送代码到GitHub")
            print("4. 启用GitHub Pages")
            print("5. 访问部署的网站")
            
            print(f"\n🌐 部署后访问地址：")
            print(f"   主页：https://{self.github_username}.github.io/{self.repo_name}/")
            print(f"   阅读器：https://{self.github_username}.github.io/{self.repo_name}/xiaohongshu_app/")
            print(f"   Python脚本：https://{self.github_username}.github.io/{self.repo_name}/xiaohongshu_reader.py")
            
            print(f"\n💡 使用说明：")
            print(f"   - 小红书风格阅读器：直接在线使用")
            print(f"   - Python脚本：下载到本地运行")
            print(f"   - 详细文档：查看README.md")
            
        except Exception as e:
            print(f"❌ 部署准备失败：{e}")
            return False
        
        return True

def main():
    """主函数"""
    deployer = SpiderGitHubDeployer()
    
    # 获取GitHub用户名
    username = input("请输入您的GitHub用户名: ").strip()
    if username:
        deployer.github_username = username
        
        # 更新所有相关文件中的用户名
        for file_path in [
            deployer.spider_dir / "xiaohongshu_app" / "README.md",
            deployer.spider_dir / "xiaohongshu_app" / "package.json",
            deployer.spider_dir / "xiaohongshu_app" / "DEPLOYMENT.md"
        ]:
            if file_path.exists():
                content = file_path.read_text(encoding='utf-8')
                content = content.replace("your-username", username)
                file_path.write_text(content, encoding='utf-8')
    
    deployer.run_deployment_prep()

if __name__ == "__main__":
    main()
