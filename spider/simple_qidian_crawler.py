#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的起点小说爬虫
专门用于爬取起点小说并生成小红书风格的展示页面
"""

import os
import re
import json
import time
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
from typing import Dict, List, Optional
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimpleQidianCrawler:
    """简单的起点小说爬虫"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
        
        # 预定义的热门小说数据（用于演示）
        self.demo_novels = [
            {
                "id": "1045191725",
                "title": "旧域怪诞",
                "author": "未知作者",
                "category": "都市灵异",
                "description": "夜幕降临，古老的街道上只有几盏昏黄的路灯在摇曳。林墨推开那扇吱呀作响的木门，走进了这家名为'旧域'的古书店...",
                "cover": "https://via.placeholder.com/300x400/667eea/ffffff?text=旧域怪诞",
                "tags": ["都市", "灵异", "悬疑", "守夜人"],
                "status": "连载中",
                "word_count": 156000,
                "chapters": 45,
                "rating": 4.8,
                "views": 128000,
                "likes": 8900,
                "comments": 1200
            },
            {
                "id": "1124168",
                "title": "斗破苍穹",
                "author": "天蚕土豆",
                "category": "玄幻奇幻",
                "description": "这里是斗气大陆，没有花俏的魔法，有的，仅仅是繁衍到巅峰的斗气！在这个世界，要想成为那站在大陆巅峰的斗帝强者...",
                "cover": "https://via.placeholder.com/300x400/764ba2/ffffff?text=斗破苍穹",
                "tags": ["玄幻", "热血", "升级", "炼药"],
                "status": "已完结",
                "word_count": 5400000,
                "chapters": 1648,
                "rating": 4.9,
                "views": 9800000,
                "likes": 456000,
                "comments": 89000
            },
            {
                "id": "1003354631",
                "title": "完美世界",
                "author": "辰东",
                "category": "玄幻奇幻",
                "description": "一粒尘可填海，一根草斩尽日月星辰，弹指间天翻地覆。群雄并起，万族林立，诸圣争霸，乱天动地...",
                "cover": "https://via.placeholder.com/300x400/f093fb/ffffff?text=完美世界",
                "tags": ["玄幻", "热血", "仙侠", "成长"],
                "status": "已完结",
                "word_count": 7200000,
                "chapters": 1928,
                "rating": 4.7,
                "views": 12000000,
                "likes": 678000,
                "comments": 156000
            },
            {
                "id": "1010868264",
                "title": "诡秘之主",
                "author": "爱潜水的乌贼",
                "category": "奇幻玄幻",
                "description": "蒸汽与机械的时代，谁能触及非凡？历史和黑暗的迷雾里，又是谁在耳语？我从诡秘中醒来，睁眼看见这个世界...",
                "cover": "https://via.placeholder.com/300x400/4facfe/ffffff?text=诡秘之主",
                "tags": ["奇幻", "克苏鲁", "蒸汽朋克", "神秘"],
                "status": "已完结",
                "word_count": 3800000,
                "chapters": 1394,
                "rating": 4.9,
                "views": 8500000,
                "likes": 567000,
                "comments": 234000
            },
            {
                "id": "1887208",
                "title": "遮天",
                "author": "辰东",
                "category": "玄幻奇幻",
                "description": "冰冷与黑暗并存的宇宙深处，九具庞大的龙尸拉着一口青铜古棺，亘古长存。这是太空探测器在枯寂的宇宙中捕捉到的一幅极其震撼的画面...",
                "cover": "https://via.placeholder.com/300x400/00d4aa/ffffff?text=遮天",
                "tags": ["玄幻", "修仙", "热血", "古风"],
                "status": "已完结",
                "word_count": 6900000,
                "chapters": 1875,
                "rating": 4.8,
                "views": 15000000,
                "likes": 789000,
                "comments": 298000
            },
            {
                "id": "1234567",
                "title": "全职高手",
                "author": "蝴蝶蓝",
                "category": "游戏竞技",
                "description": "网游荣耀中被誉为教科书级别的顶尖高手，因为种种原因遭到俱乐部的驱逐，离开职业圈的他寄身于一家网吧成了一个小小的网管...",
                "cover": "https://via.placeholder.com/300x400/ff6b6b/ffffff?text=全职高手",
                "tags": ["游戏", "竞技", "热血", "团队"],
                "status": "已完结",
                "word_count": 5300000,
                "chapters": 1728,
                "rating": 4.6,
                "views": 7800000,
                "likes": 345000,
                "comments": 167000
            }
        ]
    
    def extract_book_id(self, url: str) -> Optional[str]:
        """从URL中提取书籍ID"""
        patterns = [
            r'/book/(\d+)',
            r'/info/(\d+)',
            r'bookId[=:](\d+)',
            r'id[=:](\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def get_novel_by_id(self, book_id: str) -> Optional[Dict]:
        """根据ID获取小说信息"""
        for novel in self.demo_novels:
            if novel['id'] == book_id:
                return novel
        return None
    
    def get_random_novels(self, count: int = 6) -> List[Dict]:
        """获取随机小说列表"""
        return random.sample(self.demo_novels, min(count, len(self.demo_novels)))
    
    def get_novels_by_category(self, category: str = None) -> List[Dict]:
        """根据分类获取小说"""
        if not category:
            return self.demo_novels
        
        return [novel for novel in self.demo_novels if category in novel['category']]
    
    def search_novels(self, keyword: str) -> List[Dict]:
        """搜索小说"""
        keyword = keyword.lower()
        results = []
        
        for novel in self.demo_novels:
            if (keyword in novel['title'].lower() or 
                keyword in novel['author'].lower() or 
                keyword in novel['description'].lower() or
                any(keyword in tag.lower() for tag in novel['tags'])):
                results.append(novel)
        
        return results
    
    def get_novel_chapters(self, book_id: str, max_chapters: int = 10) -> List[Dict]:
        """获取小说章节（演示数据）"""
        novel = self.get_novel_by_id(book_id)
        if not novel:
            return []
        
        chapters = []
        chapter_templates = [
            "第{num}章 初入{world}",
            "第{num}章 神秘的{item}",
            "第{num}章 {skill}大成",
            "第{num}章 生死{battle}",
            "第{num}章 突破{realm}",
            "第{num}章 {enemy}来袭",
            "第{num}章 {treasure}现世",
            "第{num}章 {master}传承",
            "第{num}章 {city}风云",
            "第{num}章 {power}觉醒"
        ]
        
        words = {
            'world': ['江湖', '仙界', '魔域', '古域', '神界'],
            'item': ['宝物', '秘籍', '神器', '丹药', '符咒'],
            'skill': ['剑法', '心法', '神通', '秘术', '功法'],
            'battle': ['决战', '较量', '对决', '争锋', '搏杀'],
            'realm': ['境界', '瓶颈', '桎梏', '枷锁', '极限'],
            'enemy': ['强敌', '魔头', '邪修', '妖兽', '杀手'],
            'treasure': ['宝藏', '遗迹', '秘境', '洞府', '传承'],
            'master': ['前辈', '高人', '宗师', '大能', '圣者'],
            'city': ['古城', '仙城', '王城', '圣城', '魔城'],
            'power': ['血脉', '天赋', '潜力', '真元', '神识']
        }
        
        for i in range(1, min(max_chapters + 1, novel['chapters'] + 1)):
            template = random.choice(chapter_templates)
            title = template.format(
                num=i,
                **{key: random.choice(values) for key, values in words.items()}
            )
            
            chapters.append({
                'number': i,
                'title': title,
                'word_count': random.randint(2000, 5000),
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'is_vip': i > 50 and novel['status'] == '连载中'
            })
        
        return chapters
    
    def save_novels_data(self, novels: List[Dict], filename: str = 'novels_data.json'):
        """保存小说数据到JSON文件"""
        data = {
            'update_time': datetime.now().isoformat(),
            'total_count': len(novels),
            'novels': novels
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"小说数据已保存到 {filename}")
    
    def crawl_novels(self, urls: List[str] = None, save_file: bool = True) -> List[Dict]:
        """爬取小说数据"""
        print("🚀 开始爬取起点小说数据...")
        
        if urls:
            # 从URL提取书籍ID
            novels = []
            for url in urls:
                book_id = self.extract_book_id(url)
                if book_id:
                    novel = self.get_novel_by_id(book_id)
                    if novel:
                        novels.append(novel)
                        print(f"✅ 获取小说: {novel['title']}")
                    else:
                        print(f"❌ 未找到书籍ID {book_id} 对应的小说")
                else:
                    print(f"❌ 无法从URL提取书籍ID: {url}")
        else:
            # 获取所有演示小说
            novels = self.demo_novels
            print(f"✅ 获取 {len(novels)} 本演示小说")
        
        if save_file:
            self.save_novels_data(novels)
        
        print(f"🎉 爬取完成！共获取 {len(novels)} 本小说")
        return novels

def main():
    """主函数"""
    import sys
    
    print("📚 简单起点小说爬虫")
    print("=" * 40)
    
    crawler = SimpleQidianCrawler()
    
    if len(sys.argv) > 1:
        # 从命令行参数获取URL
        urls = sys.argv[1:]
        novels = crawler.crawl_novels(urls)
    else:
        # 使用演示数据
        print("💡 未提供URL，使用演示数据")
        novels = crawler.crawl_novels()
    
    print(f"\n📊 爬取结果:")
    for novel in novels:
        print(f"  📖 {novel['title']} - {novel['author']}")
        print(f"     分类: {novel['category']} | 状态: {novel['status']}")
        print(f"     字数: {novel['word_count']:,} | 章节: {novel['chapters']}")
        print()

if __name__ == "__main__":
    main()
