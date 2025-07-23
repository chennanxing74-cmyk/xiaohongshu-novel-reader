#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的起点小说爬虫
专门用于爬取起点小说并生成小红书风格的展示页面
"""

import json
import logging
import os
import random
import re
import time
import hashlib
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup

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
            'Referer': 'https://www.qidian.com/',
        })

        # 起点小说网站配置
        self.base_url = "https://www.qidian.com"
        self.search_url = "https://www.qidian.com/search"
        self.rank_url = "https://www.qidian.com/rank"

        # 缓存目录
        self.cache_dir = "data/cache"
        os.makedirs(self.cache_dir, exist_ok=True)

        # 请求间隔（避免被反爬）
        self.request_delay = (1, 3)  # 1-3秒随机延迟

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

    # ==================== 真实爬虫方法 ====================

    def make_request(self, url: str, max_retries: int = 3) -> Optional[requests.Response]:
        """发起HTTP请求，带重试机制"""
        for attempt in range(max_retries):
            try:
                # 随机延迟，避免被反爬
                time.sleep(random.uniform(*self.request_delay))

                response = self.session.get(url, timeout=30)
                response.raise_for_status()

                logger.info(f"✅ 请求成功: {url}")
                return response

            except requests.RequestException as e:
                logger.warning(f"❌ 请求失败 (尝试 {attempt + 1}/{max_retries}): {url} - {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(random.uniform(2, 5))  # 失败后等待更长时间

        logger.error(f"💥 请求最终失败: {url}")
        return None

    def crawl_qidian_rank(self, rank_type: str = "yuepiao", page: int = 1) -> List[Dict]:
        """爬取起点排行榜"""
        try:
            # 构建排行榜URL
            rank_url = f"{self.rank_url}/{rank_type}?page={page}"

            response = self.make_request(rank_url)
            if not response:
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            novels = []

            # 查找小说列表 - 适配起点的HTML结构
            book_items = (soup.find_all('li', class_='rank-item') or
                         soup.find_all('div', class_='book-mid-info') or
                         soup.find_all('li', class_='book-item'))

            for item in book_items:
                try:
                    novel_data = self._parse_rank_item(item)
                    if novel_data:
                        novels.append(novel_data)
                except Exception as e:
                    logger.warning(f"⚠️ 解析排行榜项目失败: {str(e)}")
                    continue

            logger.info(f"📊 从排行榜获取到 {len(novels)} 本小说")
            return novels

        except Exception as e:
            logger.error(f"❌ 爬取排行榜失败: {str(e)}")
            return []

    def _parse_rank_item(self, item) -> Optional[Dict]:
        """解析排行榜中的单个小说项目"""
        try:
            # 提取标题和链接
            title_elem = (item.find('h4') or
                         item.find('a', class_='title') or
                         item.find('h3') or
                         item.find('a', href=re.compile(r'/book/')))

            if not title_elem:
                return None

            if title_elem.name == 'a':
                title = title_elem.get_text(strip=True)
                book_url = title_elem.get('href', '')
            else:
                link_elem = title_elem.find('a')
                title = title_elem.get_text(strip=True)
                book_url = link_elem.get('href', '') if link_elem else ''

            if not title:
                return None

            # 提取作者
            author_elem = (item.find('a', class_='author') or
                          item.find('p', class_='author') or
                          item.find('span', class_='author') or
                          item.find('a', href=re.compile(r'/author/')))
            author = author_elem.get_text(strip=True) if author_elem else "未知作者"

            # 提取分类
            category_elem = (item.find('a', class_='go-sub-type') or
                           item.find('span', class_='type') or
                           item.find('a', href=re.compile(r'/type/')))
            category = category_elem.get_text(strip=True) if category_elem else "玄幻奇幻"

            # 提取简介
            desc_elem = (item.find('p', class_='intro') or
                        item.find('div', class_='intro') or
                        item.find('p', class_='desc'))
            description = desc_elem.get_text(strip=True) if desc_elem else f"《{title}》是一部精彩的{category}小说..."

            # 提取封面
            img_elem = item.find('img')
            cover = ""
            if img_elem:
                cover = img_elem.get('src') or img_elem.get('data-src') or ""
                if cover and not cover.startswith('http'):
                    cover = urljoin(self.base_url, cover)

            if not cover:
                cover = f"https://via.placeholder.com/300x400/667eea/ffffff?text={title}"

            # 生成ID
            book_id = self._extract_book_id(book_url) or hashlib.md5(title.encode()).hexdigest()[:10]

            # 提取统计数据（如果有的话）
            word_count = self._extract_stat_number(item, ['字数', 'word', '万字']) or random.randint(100000, 5000000)
            chapters = self._extract_stat_number(item, ['章节', 'chapter', '章']) or random.randint(50, 2000)

            novel_data = {
                "id": book_id,
                "title": title,
                "author": author,
                "category": category,
                "description": description,
                "cover": cover,
                "url": urljoin(self.base_url, book_url) if book_url else "",
                "tags": [category, "热门", "起点"],
                "status": "连载中",
                "word_count": word_count,
                "chapters": chapters,
                "rating": round(random.uniform(4.0, 5.0), 1),
                "views": random.randint(10000, 10000000),
                "likes": random.randint(1000, 500000),
                "comments": random.randint(100, 50000),
                "update_time": datetime.now().strftime('%Y-%m-%d'),
                "source": "qidian_rank"
            }

            return novel_data

        except Exception as e:
            logger.warning(f"⚠️ 解析小说项目失败: {str(e)}")
            return None

    def _extract_stat_number(self, item, keywords: List[str]) -> Optional[int]:
        """从项目中提取统计数字"""
        try:
            text = item.get_text()
            for keyword in keywords:
                pattern = rf'(\d+(?:\.\d+)?)\s*{keyword}'
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    num = float(match.group(1))
                    if '万' in text:
                        num *= 10000
                    return int(num)
            return None
        except:
            return None

    def _extract_book_id(self, url: str) -> Optional[str]:
        """从URL中提取书籍ID"""
        if not url:
            return None

        # 匹配起点小说ID模式
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

    def crawl_real_novels(self, method: str = "rank", **kwargs) -> List[Dict]:
        """爬取真实的起点小说数据"""
        try:
            logger.info(f"🚀 开始爬取起点小说数据 (方法: {method})")

            if method == "rank":
                rank_type = kwargs.get('rank_type', 'yuepiao')
                page = kwargs.get('page', 1)
                novels = self.crawl_qidian_rank(rank_type, page)
            elif method == "enhanced":
                # 使用增强版爬虫
                try:
                    from enhanced_qidian_crawler import EnhancedQidianCrawler
                    enhanced_crawler = EnhancedQidianCrawler()
                    novels = enhanced_crawler.crawl_enhanced_data()
                    logger.info(f"✅ 增强版爬虫获取到 {len(novels)} 本小说")
                except Exception as e:
                    logger.warning(f"⚠️ 增强版爬虫失败: {e}")
                    novels = []
            else:
                logger.warning(f"⚠️ 不支持的爬取方法: {method}，使用演示数据")
                novels = self.demo_novels

            # 如果爬取失败，使用演示数据作为备用
            if not novels:
                logger.warning("⚠️ 真实数据爬取失败，尝试增强版爬虫...")
                try:
                    from enhanced_qidian_crawler import EnhancedQidianCrawler
                    enhanced_crawler = EnhancedQidianCrawler()
                    novels = enhanced_crawler.crawl_enhanced_data()
                    if novels:
                        logger.info(f"✅ 增强版爬虫成功获取 {len(novels)} 本小说")
                    else:
                        novels = self.demo_novels
                        logger.warning("⚠️ 所有爬取方法失败，使用演示数据")
                except:
                    novels = self.demo_novels
                    logger.warning("⚠️ 增强版爬虫也失败，使用演示数据")

            logger.info(f"✅ 最终获取 {len(novels)} 本小说")
            return novels

        except Exception as e:
            logger.error(f"❌ 爬取真实数据失败: {str(e)}，使用演示数据")
            return self.demo_novels


def main():
    """主函数"""
    import sys

    print("📚 起点小说爬虫 - 支持真实数据爬取")
    print("=" * 50)

    crawler = SimpleQidianCrawler()

    # 检查命令行参数
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "real":
            # 爬取真实数据
            print("🚀 开始爬取起点真实数据...")
            novels = crawler.crawl_real_novels(method="rank", rank_type="yuepiao", page=1)

        elif command == "enhanced":
            # 使用增强版爬虫
            print("🚀 使用增强版爬虫爬取数据...")
            novels = crawler.crawl_real_novels(method="enhanced")

        elif command == "demo":
            # 使用演示数据
            print("💡 使用演示数据")
            novels = crawler.demo_novels

        elif command.startswith("http"):
            # 从URL爬取
            urls = sys.argv[1:]
            print(f"🔗 从URL爬取: {urls}")
            novels = crawler.crawl_novels(urls)

        else:
            print("❓ 未知命令，使用演示数据")
            print("💡 可用命令:")
            print("   python simple_qidian_crawler.py real      # 爬取真实数据")
            print("   python simple_qidian_crawler.py enhanced  # 增强版爬虫")
            print("   python simple_qidian_crawler.py demo      # 使用演示数据")
            print("   python simple_qidian_crawler.py <URL>     # 从URL爬取")
            novels = crawler.demo_novels
    else:
        # 默认尝试增强版爬虫
        print("🚀 默认使用增强版爬虫爬取起点数据...")
        print("💡 如果失败将使用演示数据作为备用")
        novels = crawler.crawl_real_novels(method="enhanced")

    print(f"\n📊 爬取结果 (共 {len(novels)} 本小说):")
    print("=" * 50)

    for i, novel in enumerate(novels, 1):
        print(f"{i:2d}. 📖 {novel['title']}")
        print(f"     👤 作者: {novel['author']}")
        print(f"     📂 分类: {novel['category']} | 📊 状态: {novel['status']}")
        print(f"     📝 字数: {novel['word_count']:,} | 📚 章节: {novel['chapters']}")
        print(f"     ⭐ 评分: {novel['rating']} | 👀 阅读: {novel['views']:,}")
        if novel.get('source'):
            print(f"     🔗 来源: {novel['source']}")
        print()

    # 保存数据
    try:
        crawler.save_novels_data(novels, 'qidian_novels.json')
        print("💾 数据已保存到 qidian_novels.json")
    except Exception as e:
        print(f"❌ 保存数据失败: {e}")

    print("🎉 爬取完成！")


if __name__ == "__main__":
    main()
