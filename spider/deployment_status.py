#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
部署状态检查脚本
检查所有文件是否准备就绪
"""

import os
from pathlib import Path

def check_file_exists(file_path, description):
    """检查文件是否存在"""
    if Path(file_path).exists():
        print(f"✅ {description}")
        return True
    else:
        print(f"❌ {description} - 文件不存在: {file_path}")
        return False

def check_directory_exists(dir_path, description):
    """检查目录是否存在"""
    if Path(dir_path).exists() and Path(dir_path).is_dir():
        print(f"✅ {description}")
        return True
    else:
        print(f"❌ {description} - 目录不存在: {dir_path}")
        return False

def main():
    """主检查函数"""
    print("🔍 Spider项目部署状态检查")
    print("=" * 50)
    
    all_good = True
    
    # 检查核心文件
    print("\n📋 核心文件检查:")
    files_to_check = [
        ("README.md", "项目说明文件"),
        ("index.html", "主页面文件"),
        ("xiaohongshu_reader.py", "Python阅读器"),
        ("simple_qidian_crawler.py", "爬虫脚本"),
        ("novel_generator.py", "小说生成器"),
        ("novels_data.json", "小说数据"),
        ("requirements.txt", "Python依赖"),
        ("package.json", "项目配置"),
        (".gitignore", "Git忽略文件"),
        ("GITHUB_DEPLOYMENT_GUIDE.md", "部署指南"),
        ("push_to_github.bat", "推送脚本")
    ]
    
    for file_path, description in files_to_check:
        if not check_file_exists(file_path, description):
            all_good = False
    
    # 检查目录
    print("\n📁 目录结构检查:")
    dirs_to_check = [
        ("xiaohongshu_app", "小红书风格阅读器"),
        ("templates", "HTML模板"),
        (".github/workflows", "GitHub Actions工作流")
    ]
    
    for dir_path, description in dirs_to_check:
        if not check_directory_exists(dir_path, description):
            all_good = False
    
    # 检查小红书应用文件
    print("\n📱 小红书应用文件检查:")
    app_files = [
        ("xiaohongshu_app/index.html", "应用主页"),
        ("xiaohongshu_app/app.js", "应用逻辑"),
        ("xiaohongshu_app/styles.css", "样式文件"),
        ("xiaohongshu_app/data.js", "小说数据"),
        ("xiaohongshu_app/manifest.json", "PWA配置"),
        ("xiaohongshu_app/sw.js", "Service Worker"),
        ("xiaohongshu_app/server.py", "本地服务器")
    ]
    
    for file_path, description in app_files:
        if not check_file_exists(file_path, description):
            all_good = False
    
    # 检查Git状态
    print("\n🔧 Git状态检查:")
    if Path(".git").exists():
        print("✅ Git仓库已初始化")
        
        # 检查是否有提交
        import subprocess
        try:
            result = subprocess.run(["git", "log", "--oneline", "-1"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ 代码已提交")
                print(f"   最新提交: {result.stdout.strip()}")
            else:
                print("❌ 没有提交记录")
                all_good = False
        except:
            print("⚠️  无法检查Git提交状态")
        
        # 检查远程仓库
        try:
            result = subprocess.run(["git", "remote", "get-url", "origin"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ 远程仓库已配置")
                print(f"   远程地址: {result.stdout.strip()}")
            else:
                print("❌ 远程仓库未配置")
                all_good = False
        except:
            print("⚠️  无法检查远程仓库")
    else:
        print("❌ Git仓库未初始化")
        all_good = False
    
    # 总结
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 所有检查通过！项目已准备好部署")
        print("\n📋 下一步操作:")
        print("1. 在GitHub创建仓库: spider-novel-reader")
        print("2. 运行: push_to_github.bat")
        print("3. 启用GitHub Pages")
        print("4. 访问部署的网站")
        
        print("\n🌐 预期访问地址:")
        print("   主页: https://chennanxing74-cmyk.github.io/spider-novel-reader/")
        print("   阅读器: https://chennanxing74-cmyk.github.io/spider-novel-reader/xiaohongshu_app/")
    else:
        print("❌ 发现问题，请检查上述错误并修复")
    
    print("\n📖 详细部署指南请查看: GITHUB_DEPLOYMENT_GUIDE.md")

if __name__ == "__main__":
    main()
