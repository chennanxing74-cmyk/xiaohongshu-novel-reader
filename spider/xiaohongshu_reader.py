#!/usr/bin/env python3
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

"""
小红书风格的小说展示页面
基于Flask的小红书风格小说阅读界面
"""

import os
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for
from simple_qidian_crawler import SimpleQidianCrawler
import random
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'xiaohongshu_novel_reader'

# 全局爬虫实例
crawler = SimpleQidianCrawler()

@app.route('/')
def index():
    """首页 - 小红书风格的瀑布流布局"""
    # 获取筛选参数
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    
    # 获取小说数据
    if search:
        novels = crawler.search_novels(search)
    elif category:
        novels = crawler.get_novels_by_category(category)
    else:
        novels = crawler.demo_novels
    
    # 为每本小说添加随机的小红书风格数据
    for novel in novels:
        novel['random_likes'] = random.randint(100, 10000)
        novel['random_comments'] = random.randint(10, 1000)
        novel['random_shares'] = random.randint(5, 500)
        novel['random_collections'] = random.randint(50, 5000)
        novel['hot_tags'] = random.sample(novel['tags'], min(3, len(novel['tags'])))
        novel['update_days_ago'] = random.randint(1, 30)
    
    # 获取分类列表
    categories = list(set(novel['category'] for novel in crawler.demo_novels))
    
    return render_template('xiaohongshu_index.html', 
                         novels=novels, 
                         categories=categories,
                         current_category=category,
                         current_search=search)

@app.route('/novel/<novel_id>')
def novel_detail(novel_id):
    """小说详情页 - 小红书风格的详情展示"""
    novel = crawler.get_novel_by_id(novel_id)
    if not novel:
        return "小说不存在", 404
    
    # 获取章节列表
    chapters = crawler.get_novel_chapters(novel_id, 20)
    
    # 生成小红书风格的评论数据
    comments = generate_fake_comments(novel['title'])
    
    # 推荐相关小说
    related_novels = [n for n in crawler.demo_novels if n['id'] != novel_id and n['category'] == novel['category']][:4]
    
    return render_template('xiaohongshu_detail.html', 
                         novel=novel, 
                         chapters=chapters,
                         comments=comments,
                         related_novels=related_novels)

@app.route('/read/<novel_id>/<int:chapter_num>')
def read_chapter(novel_id, chapter_num):
    """阅读页面 - 小红书风格的阅读界面"""
    novel = crawler.get_novel_by_id(novel_id)
    if not novel:
        return "小说不存在", 404
    
    chapters = crawler.get_novel_chapters(novel_id, 100)
    
    # 找到当前章节
    current_chapter = None
    for chapter in chapters:
        if chapter['number'] == chapter_num:
            current_chapter = chapter
            break
    
    if not current_chapter:
        return "章节不存在", 404
    
    # 生成章节内容
    content = generate_chapter_content(novel, current_chapter)
    
    # 上一章和下一章
    prev_chapter = next((c for c in chapters if c['number'] == chapter_num - 1), None)
    next_chapter = next((c for c in chapters if c['number'] == chapter_num + 1), None)
    
    return render_template('xiaohongshu_read.html',
                         novel=novel,
                         chapter=current_chapter,
                         content=content,
                         prev_chapter=prev_chapter,
                         next_chapter=next_chapter,
                         total_chapters=len(chapters))

@app.route('/api/like/<novel_id>')
def like_novel(novel_id):
    """点赞小说"""
    novel = crawler.get_novel_by_id(novel_id)
    if novel:
        novel['likes'] = novel.get('likes', 0) + 1
        return jsonify({'success': True, 'likes': novel['likes']})
    return jsonify({'success': False})

@app.route('/api/collect/<novel_id>')
def collect_novel(novel_id):
    """收藏小说"""
    novel = crawler.get_novel_by_id(novel_id)
    if novel:
        return jsonify({'success': True, 'message': '收藏成功！'})
    return jsonify({'success': False})

def generate_fake_comments(novel_title):
    """生成虚拟评论数据"""
    comment_templates = [
        "这本《{title}》真的太好看了！强烈推荐！",
        "作者的文笔真的很棒，情节紧凑，停不下来",
        "已经熬夜看到凌晨3点了，明天还要上班😭",
        "这个设定太有创意了，期待后续更新",
        "男主角太帅了，女主角也很有个性",
        "剧情反转太精彩了，完全猜不到结局",
        "这本书让我重新爱上了{category}类小说",
        "文字功底很深厚，描写很细腻",
        "更新速度能再快点就好了，等得好着急",
        "已经推荐给好几个朋友了，都说很好看"
    ]
    
    usernames = [
        "书虫小仙女", "夜读者", "文字控", "小说迷", "阅读狂魔",
        "书海遨游", "文学青年", "故事收集者", "字里行间", "书香墨韵"
    ]
    
    comments = []
    for i in range(random.randint(5, 15)):
        template = random.choice(comment_templates)
        comment_text = template.format(title=novel_title, category="玄幻")
        
        comments.append({
            'username': random.choice(usernames),
            'avatar': f"https://via.placeholder.com/40x40/ff{random.randint(1000,9999)}/ffffff?text={random.choice(usernames)[0]}",
            'content': comment_text,
            'likes': random.randint(0, 100),
            'time_ago': f"{random.randint(1, 24)}小时前",
            'level': random.randint(1, 10)
        })
    
    return comments

def generate_chapter_content(novel, chapter):
    """生成章节内容"""
    content_templates = [
        f"在{novel['title']}的世界里，主角面临着前所未有的挑战。",
        "夜幕降临，古老的传说即将揭开神秘的面纱。",
        "力量的觉醒往往伴随着巨大的代价，这是亘古不变的真理。",
        "在这个充满奇迹与危险的世界中，每一个选择都可能改变命运的轨迹。",
        "古老的预言正在一步步应验，而真正的考验才刚刚开始。"
    ]
    
    paragraphs = []
    for i in range(random.randint(8, 15)):
        if i == 0:
            paragraphs.append(f"    {chapter['title']}讲述了一个扣人心弦的故事。")
        else:
            paragraphs.append(f"    {random.choice(content_templates)}")
    
    return "\n\n".join(paragraphs)

def create_templates():
    """创建HTML模板文件"""
    templates_dir = "templates"
    os.makedirs(templates_dir, exist_ok=True)
    
    # 这里会创建小红书风格的模板
    print("✅ 模板目录已创建")

def main():
    """主函数"""
    print("🌸 小红书风格小说阅读器")
    print("=" * 40)
    
    # 先运行爬虫获取数据
    print("📚 准备小说数据...")
    crawler.crawl_novels()
    
    # 创建模板目录
    create_templates()
    
    print("🚀 启动小红书风格Web服务器...")
    print("📱 访问地址: http://localhost:5000")
    print("🎨 小红书风格界面已就绪")
    print("=" * 40)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n⏹️ 服务器已停止")

if __name__ == "__main__":
    main()
