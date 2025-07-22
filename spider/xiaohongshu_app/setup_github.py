#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub仓库设置和部署脚本
自动化设置GitHub仓库并部署到GitHub Pages
"""

import os
import subprocess
import sys
from pathlib import Path

class GitHubSetup:
    """GitHub设置助手"""
    
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.repo_name = "xiaohongshu-novel-reader"
        self.github_username = None
        
    def check_git_installed(self):
        """检查Git是否已安装"""
        try:
            result = subprocess.run(['git', '--version'], 
                                  capture_output=True, text=True, check=True)
            print(f"✅ Git已安装: {result.stdout.strip()}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Git未安装或不在PATH中")
            print("   请先安装Git: https://git-scm.com/downloads")
            return False
    
    def get_github_username(self):
        """获取GitHub用户名"""
        while True:
            username = input("请输入您的GitHub用户名: ").strip()
            if username:
                self.github_username = username
                break
            print("❌ 用户名不能为空")
    
    def init_git_repo(self):
        """初始化Git仓库"""
        print("\n📁 初始化Git仓库...")
        
        os.chdir(self.project_dir)
        
        try:
            # 检查是否已经是Git仓库
            if (self.project_dir / ".git").exists():
                print("⚠️  已存在Git仓库，跳过初始化")
                return True
            
            # 初始化仓库
            subprocess.run(['git', 'init'], check=True)
            print("✅ Git仓库初始化完成")
            
            # 设置默认分支为main
            subprocess.run(['git', 'branch', '-M', 'main'], check=True)
            print("✅ 默认分支设置为main")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Git仓库初始化失败: {e}")
            return False
    
    def update_config_files(self):
        """更新配置文件中的用户名"""
        print(f"\n📝 更新配置文件 (用户名: {self.github_username})...")
        
        # 更新README.md
        readme_file = self.project_dir / "README.md"
        if readme_file.exists():
            content = readme_file.read_text(encoding='utf-8')
            content = content.replace("your-username", self.github_username)
            readme_file.write_text(content, encoding='utf-8')
            print("✅ README.md已更新")
        
        # 更新package.json
        package_file = self.project_dir / "package.json"
        if package_file.exists():
            content = package_file.read_text(encoding='utf-8')
            content = content.replace("your-username", self.github_username)
            package_file.write_text(content, encoding='utf-8')
            print("✅ package.json已更新")
        
        # 更新DEPLOYMENT.md
        deployment_file = self.project_dir / "DEPLOYMENT.md"
        if deployment_file.exists():
            content = deployment_file.read_text(encoding='utf-8')
            content = content.replace("your-username", self.github_username)
            deployment_file.write_text(content, encoding='utf-8')
            print("✅ DEPLOYMENT.md已更新")
    
    def add_and_commit_files(self):
        """添加文件并提交"""
        print("\n📦 添加文件到Git...")
        
        try:
            # 添加所有文件
            subprocess.run(['git', 'add', '.'], check=True)
            print("✅ 文件已添加到暂存区")
            
            # 提交
            commit_message = "Initial commit: 小红书风格小说阅读器"
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            print("✅ 文件已提交")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ 文件提交失败: {e}")
            return False
    
    def add_remote_origin(self):
        """添加远程仓库"""
        print(f"\n🔗 添加远程仓库...")
        
        remote_url = f"https://github.com/{self.github_username}/{self.repo_name}.git"
        
        try:
            # 检查是否已有远程仓库
            result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("⚠️  远程仓库已存在，跳过添加")
                return True
            
            # 添加远程仓库
            subprocess.run(['git', 'remote', 'add', 'origin', remote_url], check=True)
            print(f"✅ 远程仓库已添加: {remote_url}")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ 添加远程仓库失败: {e}")
            return False
    
    def show_next_steps(self):
        """显示后续步骤"""
        print("\n" + "=" * 60)
        print("🎉 本地Git仓库设置完成！")
        print("=" * 60)
        
        print(f"\n📋 接下来请按以下步骤操作：")
        print(f"\n1️⃣  创建GitHub仓库:")
        print(f"   - 访问: https://github.com/new")
        print(f"   - 仓库名称: {self.repo_name}")
        print(f"   - 设置为Public")
        print(f"   - 不要初始化README、.gitignore或license")
        
        print(f"\n2️⃣  推送代码到GitHub:")
        print(f"   git push -u origin main")
        
        print(f"\n3️⃣  启用GitHub Pages:")
        print(f"   - 进入仓库设置页面")
        print(f"   - 找到'Pages'部分")
        print(f"   - Source选择'Deploy from a branch'")
        print(f"   - Branch选择'main'")
        print(f"   - 点击Save")
        
        print(f"\n4️⃣  访问部署的网站:")
        print(f"   https://{self.github_username}.github.io/{self.repo_name}/")
        
        print(f"\n💡 提示:")
        print(f"   - 推送代码后等待几分钟让GitHub Pages部署完成")
        print(f"   - 可以在仓库的Actions标签页查看部署状态")
        print(f"   - 详细说明请查看DEPLOYMENT.md文件")
        
        print(f"\n🚀 快速推送命令:")
        print(f"   cd {self.project_dir}")
        print(f"   git push -u origin main")
    
    def run_setup(self):
        """运行完整设置流程"""
        print("🚀 GitHub仓库设置助手")
        print("=" * 40)
        
        # 检查Git
        if not self.check_git_installed():
            return False
        
        # 获取用户名
        self.get_github_username()
        
        # 初始化Git仓库
        if not self.init_git_repo():
            return False
        
        # 更新配置文件
        self.update_config_files()
        
        # 添加和提交文件
        if not self.add_and_commit_files():
            return False
        
        # 添加远程仓库
        if not self.add_remote_origin():
            return False
        
        # 显示后续步骤
        self.show_next_steps()
        
        return True

def main():
    """主函数"""
    setup = GitHubSetup()
    
    try:
        success = setup.run_setup()
        if success:
            print("\n✅ 设置完成！请按照上述步骤继续操作。")
        else:
            print("\n❌ 设置过程中出现错误，请检查并重试。")
    except KeyboardInterrupt:
        print("\n\n🛑 用户取消操作")
    except Exception as e:
        print(f"\n❌ 意外错误: {e}")

if __name__ == "__main__":
    main()
