#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地开发服务器
用于测试小红书风格小说阅读器
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """自定义HTTP请求处理器"""
    
    def end_headers(self):
        # 添加CORS头
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        # 添加缓存控制
        if self.path.endswith(('.html', '.js', '.css')):
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
        
        super().end_headers()
    
    def do_OPTIONS(self):
        """处理OPTIONS请求"""
        self.send_response(200)
        self.end_headers()
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[{self.log_date_time_string()}] {format % args}")

def find_free_port(start_port=8000, max_attempts=10):
    """查找可用端口"""
    import socket
    
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    
    raise RuntimeError(f"无法找到可用端口 (尝试了 {start_port}-{start_port + max_attempts - 1})")

def start_server():
    """启动开发服务器"""
    # 切换到应用目录
    app_dir = Path(__file__).parent
    os.chdir(app_dir)
    
    # 查找可用端口
    try:
        port = find_free_port()
    except RuntimeError as e:
        print(f"❌ {e}")
        return
    
    # 创建服务器
    try:
        with socketserver.TCPServer(("", port), CustomHTTPRequestHandler) as httpd:
            server_url = f"http://localhost:{port}"
            
            print("🚀 小红书风格小说阅读器 - 开发服务器")
            print("=" * 50)
            print(f"📱 服务器地址: {server_url}")
            print(f"📁 服务目录: {app_dir}")
            print("🔧 开发模式: 已启用")
            print("=" * 50)
            print("💡 提示:")
            print("  - 修改文件后刷新浏览器即可看到更改")
            print("  - 按 Ctrl+C 停止服务器")
            print("  - 在移动设备上测试请使用局域网IP")
            print("=" * 50)
            
            # 自动打开浏览器
            try:
                webbrowser.open(server_url)
                print("🌐 已自动打开浏览器")
            except Exception:
                print("⚠️  无法自动打开浏览器，请手动访问上述地址")
            
            print("\n⏳ 服务器运行中...")
            print("   访问应用请打开:", server_url)
            
            # 启动服务器
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n🛑 服务器已停止")
    except Exception as e:
        print(f"❌ 服务器启动失败: {e}")

def show_network_info():
    """显示网络信息"""
    import socket
    
    try:
        # 获取本机IP
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        print(f"\n🌐 网络信息:")
        print(f"   主机名: {hostname}")
        print(f"   本机IP: {local_ip}")
        print(f"   局域网访问: http://{local_ip}:端口号")
        print("   (可用于手机等设备测试)")
        
    except Exception:
        print("\n⚠️  无法获取网络信息")

def main():
    """主函数"""
    print("🎯 小红书风格小说阅读器 - 本地开发服务器")
    
    # 检查是否在正确目录
    if not Path("index.html").exists():
        print("❌ 错误: 未找到 index.html 文件")
        print("   请确保在应用根目录运行此脚本")
        return
    
    # 显示网络信息
    show_network_info()
    
    # 启动服务器
    try:
        start_server()
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == "__main__":
    main()
