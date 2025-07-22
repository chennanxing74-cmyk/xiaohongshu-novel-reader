#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Pages 部署脚本
自动将小红书风格小说阅读器部署到GitHub Pages
"""

import os
import shutil
import subprocess
import json
from pathlib import Path

class GitHubDeployer:
    """GitHub Pages 部署器"""
    
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.app_name = "xiaohongshu-novel-reader"
        self.github_username = "your-username"  # 需要替换为实际的GitHub用户名
        
    def create_github_repo_files(self):
        """创建GitHub仓库必需的文件"""
        print("📝 创建GitHub仓库文件...")
        
        # 创建README.md
        readme_content = f"""# 小红书风格小说阅读器

一个现代化的移动端小说阅读应用，采用小红书风格设计。

## ✨ 特性

- 📱 **移动端优化** - 完美适配手机和平板
- 🎨 **小红书风格** - 现代化的UI设计
- 📚 **丰富功能** - 搜索、分类、收藏、历史记录
- 🌙 **主题切换** - 支持日间/夜间模式
- 📖 **阅读体验** - 字体调节、背景主题、翻页手势
- 💾 **离线支持** - PWA技术，支持离线阅读
- 🔍 **智能搜索** - 支持书名、作者、标签搜索

## 🚀 在线体验

访问：[https://{self.github_username}.github.io/{self.app_name}/](https://{self.github_username}.github.io/{self.app_name}/)

## 📱 安装为APP

### Android/Chrome
1. 访问网站
2. 点击浏览器菜单
3. 选择"添加到主屏幕"
4. 确认安装

### iOS/Safari  
1. 访问网站
2. 点击分享按钮
3. 选择"添加到主屏幕"
4. 确认安装

## 🛠️ 技术栈

- **前端**: HTML5, CSS3, JavaScript (ES6+)
- **框架**: Bootstrap 5
- **图标**: Font Awesome
- **PWA**: Service Worker, Web App Manifest
- **部署**: GitHub Pages

## 📖 功能说明

### 首页
- 小说列表展示
- 分类筛选
- 搜索功能
- 推荐算法

### 详情页
- 小说信息展示
- 章节目录
- 收藏功能
- 阅读进度

### 阅读页
- 沉浸式阅读体验
- 字体大小调节
- 主题切换（日间/夜间/护眼）
- 翻页手势支持
- 阅读进度保存

### 个人中心
- 收藏管理
- 阅读历史
- 设置选项

## 🔧 本地开发

```bash
# 克隆项目
git clone https://github.com/{self.github_username}/{self.app_name}.git

# 进入目录
cd {self.app_name}

# 启动本地服务器
python -m http.server 8000

# 访问 http://localhost:8000
```

## 📦 部署

项目使用GitHub Pages自动部署，推送到main分支即可自动更新。

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 📞 联系

如有问题，请提交Issue或联系开发者。

---

**享受阅读时光！** 📚✨
"""
        
        with open(self.project_dir / "README.md", 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        # 创建.gitignore
        gitignore_content = """# 依赖
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# 构建输出
dist/
build/

# 环境变量
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# 操作系统
.DS_Store
Thumbs.db

# 日志
logs
*.log

# 临时文件
*.tmp
*.temp

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# 部署相关
deploy_to_github.py
"""
        
        with open(self.project_dir / ".gitignore", 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        
        # 创建GitHub Actions工作流
        github_dir = self.project_dir / ".github" / "workflows"
        github_dir.mkdir(parents=True, exist_ok=True)
        
        workflow_content = """name: Deploy to GitHub Pages

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
      
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        
    - name: Install dependencies
      run: |
        # 如果有package.json，安装依赖
        if [ -f package.json ]; then
          npm install
        fi
        
    - name: Build
      run: |
        # 如果有构建脚本，执行构建
        if [ -f package.json ] && npm run build --if-present; then
          echo "Build completed"
        else
          echo "No build step required"
        fi
        
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      if: github.ref == 'refs/heads/main'
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./
        exclude_assets: '.github,deploy_to_github.py,README.md'
"""
        
        with open(github_dir / "deploy.yml", 'w', encoding='utf-8') as f:
            f.write(workflow_content)
        
        print("✅ GitHub仓库文件创建完成")
    
    def generate_icons(self):
        """生成不同尺寸的图标"""
        print("🎨 生成应用图标...")
        
        try:
            # 尝试使用PIL生成图标
            from PIL import Image, ImageDraw
            
            sizes = [72, 96, 128, 144, 152, 192, 384, 512]
            
            for size in sizes:
                # 创建图像
                img = Image.new('RGBA', (size, size), (255, 36, 66, 255))
                draw = ImageDraw.Draw(img)
                
                # 绘制简单的书本图标
                margin = size // 8
                book_width = size - 2 * margin
                book_height = int(book_width * 1.2)
                
                # 书本主体
                book_x = margin
                book_y = (size - book_height) // 2
                draw.rectangle([book_x, book_y, book_x + book_width, book_y + book_height], 
                             fill=(255, 255, 255, 230))
                
                # 书脊
                spine_width = size // 20
                draw.rectangle([book_x, book_y, book_x + spine_width, book_y + book_height], 
                             fill=(255, 36, 66, 255))
                
                # 保存图标
                img.save(self.project_dir / f"icon-{size}.png", "PNG")
            
            print("✅ 图标生成完成")
            
        except ImportError:
            print("⚠️  PIL未安装，跳过图标生成")
            print("   可以手动创建图标文件或安装PIL: pip install Pillow")
    
    def create_package_json(self):
        """创建package.json文件"""
        print("📦 创建package.json...")
        
        package_data = {
            "name": self.app_name,
            "version": "1.0.0",
            "description": "小红书风格小说阅读器",
            "main": "index.html",
            "scripts": {
                "start": "python -m http.server 8000",
                "dev": "python -m http.server 8000",
                "build": "echo 'No build step required'",
                "deploy": "python deploy_to_github.py"
            },
            "keywords": [
                "novel",
                "reader",
                "xiaohongshu",
                "pwa",
                "mobile"
            ],
            "author": "Novel Reader Team",
            "license": "MIT",
            "homepage": f"https://{self.github_username}.github.io/{self.app_name}/",
            "repository": {
                "type": "git",
                "url": f"https://github.com/{self.github_username}/{self.app_name}.git"
            },
            "bugs": {
                "url": f"https://github.com/{self.github_username}/{self.app_name}/issues"
            }
        }
        
        with open(self.project_dir / "package.json", 'w', encoding='utf-8') as f:
            json.dump(package_data, f, indent=2, ensure_ascii=False)
        
        print("✅ package.json创建完成")
    
    def optimize_for_github_pages(self):
        """为GitHub Pages优化文件"""
        print("⚡ 优化GitHub Pages部署...")
        
        # 创建CNAME文件（如果有自定义域名）
        # cname_content = "your-domain.com"
        # with open(self.project_dir / "CNAME", 'w') as f:
        #     f.write(cname_content)
        
        # 创建.nojekyll文件（禁用Jekyll处理）
        (self.project_dir / ".nojekyll").touch()
        
        # 创建404页面
        error_404_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>页面未找到 - 小说阅读器</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #ff2442 0%, #ff6b6b 100%);
            color: white;
            text-align: center;
        }
        .container {
            max-width: 500px;
            padding: 2rem;
        }
        h1 {
            font-size: 4rem;
            margin-bottom: 1rem;
        }
        p {
            font-size: 1.2rem;
            margin-bottom: 2rem;
        }
        .btn {
            display: inline-block;
            padding: 12px 24px;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            text-decoration: none;
            border-radius: 25px;
            border: 2px solid white;
            transition: all 0.3s ease;
        }
        .btn:hover {
            background: white;
            color: #ff2442;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>404</h1>
        <p>抱歉，您访问的页面不存在</p>
        <a href="./" class="btn">返回首页</a>
    </div>
    <script>
        // 自动重定向到首页
        setTimeout(() => {
            window.location.href = './';
        }, 3000);
    </script>
</body>
</html>"""
        
        with open(self.project_dir / "404.html", 'w', encoding='utf-8') as f:
            f.write(error_404_content)
        
        print("✅ GitHub Pages优化完成")
    
    def create_deployment_instructions(self):
        """创建部署说明文件"""
        print("📋 创建部署说明...")
        
        instructions = f"""# GitHub Pages 部署说明

## 🚀 快速部署

### 1. 创建GitHub仓库
1. 访问 https://github.com/new
2. 仓库名称：`{self.app_name}`
3. 设置为Public
4. 不要初始化README、.gitignore或license

### 2. 上传代码
```bash
# 在项目目录中执行
git init
git add .
git commit -m "Initial commit: 小红书风格小说阅读器"
git branch -M main
git remote add origin https://github.com/{self.github_username}/{self.app_name}.git
git push -u origin main
```

### 3. 启用GitHub Pages
1. 进入仓库设置页面
2. 滚动到"Pages"部分
3. Source选择"Deploy from a branch"
4. Branch选择"main"
5. 文件夹选择"/ (root)"
6. 点击Save

### 4. 访问网站
等待几分钟后，访问：
https://{self.github_username}.github.io/{self.app_name}/

## 🔧 自定义配置

### 修改GitHub用户名
1. 编辑 `deploy_to_github.py`
2. 修改 `github_username` 变量
3. 重新运行脚本

### 自定义域名
1. 在仓库根目录创建 `CNAME` 文件
2. 文件内容为你的域名，如：`novel.yourdomain.com`
3. 在域名DNS设置中添加CNAME记录指向 `{self.github_username}.github.io`

### 自动部署
项目已配置GitHub Actions，推送到main分支会自动部署。

## 📱 PWA安装

部署后，用户可以将网站安装为APP：

### Android/Chrome
1. 访问网站
2. 浏览器会显示"添加到主屏幕"提示
3. 点击安装

### iOS/Safari
1. 访问网站
2. 点击分享按钮
3. 选择"添加到主屏幕"

## 🛠️ 故障排除

### 页面404错误
- 检查仓库是否为Public
- 确认GitHub Pages已启用
- 等待几分钟让部署完成

### 样式或脚本加载失败
- 检查文件路径是否正确
- 确认所有文件都已上传

### PWA功能不工作
- 确认网站使用HTTPS访问
- 检查Service Worker是否正确注册
- 查看浏览器控制台错误信息

## 📞 获取帮助

如遇问题，请：
1. 检查GitHub Pages部署状态
2. 查看浏览器控制台错误
3. 提交Issue到项目仓库

---

**祝您部署成功！** 🎉
"""
        
        with open(self.project_dir / "DEPLOYMENT.md", 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        print("✅ 部署说明创建完成")
    
    def run_deployment(self):
        """执行完整的部署准备"""
        print("🚀 开始准备GitHub Pages部署...")
        print("=" * 50)
        
        try:
            # 创建所有必需文件
            self.create_github_repo_files()
            self.generate_icons()
            self.create_package_json()
            self.optimize_for_github_pages()
            self.create_deployment_instructions()
            
            print("\n" + "=" * 50)
            print("🎉 GitHub Pages部署准备完成！")
            print("\n📋 接下来的步骤：")
            print("1. 修改deploy_to_github.py中的github_username")
            print("2. 创建GitHub仓库")
            print("3. 上传代码到GitHub")
            print("4. 启用GitHub Pages")
            print("5. 访问部署的网站")
            print("\n📖 详细说明请查看 DEPLOYMENT.md 文件")
            print(f"\n🌐 部署后访问地址：")
            print(f"   https://{self.github_username}.github.io/{self.app_name}/")
            
        except Exception as e:
            print(f"❌ 部署准备失败：{e}")
            return False
        
        return True

def main():
    """主函数"""
    deployer = GitHubDeployer()
    deployer.run_deployment()

if __name__ == "__main__":
    main()
