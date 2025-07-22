#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化Git部署脚本
初始化Git仓库并推送到GitHub
"""

import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """运行命令并处理结果"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True, encoding='utf-8')
        print(f"✅ {description}完成")
        if result.stdout.strip():
            print(f"   输出: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description}失败")
        if e.stderr:
            print(f"   错误: {e.stderr.strip()}")
        if e.stdout:
            print(f"   输出: {e.stdout.strip()}")
        return False

def main():
    """主函数"""
    print("🚀 Spider项目Git自动部署")
    print("=" * 40)
    
    # 确认当前目录
    current_dir = Path.cwd()
    print(f"📁 当前目录: {current_dir}")
    
    # 检查是否有必要文件
    if not (current_dir / "README.md").exists():
        print("❌ 未找到README.md，请先运行deploy_spider_to_github.py")
        return
    
    # 获取仓库信息
    repo_name = "spider-novel-reader"
    github_username = "chennanxing74-cmyk"
    
    print(f"📦 仓库名称: {repo_name}")
    print(f"👤 GitHub用户: {github_username}")
    
    # 初始化Git仓库
    if not (current_dir / ".git").exists():
        if not run_command("git init", "初始化Git仓库"):
            return
        
        if not run_command("git branch -M main", "设置主分支为main"):
            return
    else:
        print("✅ Git仓库已存在")
    
    # 添加所有文件
    if not run_command("git add .", "添加所有文件"):
        return
    
    # 检查是否有更改
    result = subprocess.run("git status --porcelain", shell=True, 
                          capture_output=True, text=True)
    if not result.stdout.strip():
        print("ℹ️  没有新的更改需要提交")
    else:
        # 提交更改
        commit_msg = "Deploy Spider Novel Reader Project to GitHub Pages"
        if not run_command(f'git commit -m "{commit_msg}"', "提交更改"):
            return
    
    # 添加远程仓库
    remote_url = f"https://github.com/{github_username}/{repo_name}.git"
    
    # 检查远程仓库是否已存在
    result = subprocess.run("git remote get-url origin", shell=True, 
                          capture_output=True, text=True)
    if result.returncode != 0:
        if not run_command(f"git remote add origin {remote_url}", "添加远程仓库"):
            return
    else:
        print("✅ 远程仓库已存在")
    
    print("\n" + "=" * 50)
    print("🎉 Git仓库准备完成！")
    print("=" * 50)
    
    print(f"\n📋 现在请按以下步骤操作：")
    print(f"\n1️⃣  创建GitHub仓库:")
    print(f"   - 访问: https://github.com/new")
    print(f"   - 仓库名称: {repo_name}")
    print(f"   - 设置为Public")
    print(f"   - 不要初始化README、.gitignore或license")
    
    print(f"\n2️⃣  推送代码:")
    print(f"   git push -u origin main")
    
    print(f"\n3️⃣  启用GitHub Pages:")
    print(f"   - 进入仓库设置 → Pages")
    print(f"   - Source: Deploy from a branch")
    print(f"   - Branch: main")
    print(f"   - 点击Save")
    
    print(f"\n4️⃣  访问网站:")
    print(f"   主页: https://{github_username}.github.io/{repo_name}/")
    print(f"   阅读器: https://{github_username}.github.io/{repo_name}/xiaohongshu_app/")
    
    # 询问是否立即推送
    try:
        push_now = input("\n❓ 是否现在推送到GitHub? (y/N): ").strip().lower()
        if push_now in ['y', 'yes']:
            print("\n🚀 正在推送到GitHub...")
            if run_command("git push -u origin main", "推送到GitHub"):
                print("\n🎉 推送成功！")
                print("⏳ 请等待几分钟让GitHub Pages部署完成")
                print(f"🌐 然后访问: https://{github_username}.github.io/{repo_name}/")
            else:
                print("\n❌ 推送失败，请检查:")
                print("   1. GitHub仓库是否已创建")
                print("   2. 网络连接是否正常")
                print("   3. Git凭据是否正确")
        else:
            print("\n💡 稍后手动推送:")
            print("   git push -u origin main")
    
    except KeyboardInterrupt:
        print("\n\n🛑 操作已取消")

if __name__ == "__main__":
    main()
