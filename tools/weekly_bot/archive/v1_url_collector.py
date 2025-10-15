#!/usr/bin/env python3
"""
周报URL收集器
功能：收集上次周报之后新创建的MoonBit仓库URL
"""

import requests
import os
import re
from datetime import datetime
from typing import List, Dict, Optional

# 路径常量：以当前文件为基准，定位项目根与输出目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # tools/weekly_bot
PROJECT_ROOT = os.path.dirname(os.path.dirname(BASE_DIR))  # 项目根
WEEKLY_DIR = os.path.join(PROJECT_ROOT, "trees", "weekly")  # 周报目录
OUTPUT_DIR = os.path.join(BASE_DIR, "output")  # 输出目录
os.makedirs(OUTPUT_DIR, exist_ok=True)

class WeeklyURLCollector:
    """周报URL收集器"""
    
    def __init__(self, github_token: Optional[str] = None):
        """初始化"""
        self.github_token = github_token or os.getenv('GITHUB_TOKEN')
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Weekly-URL-Collector/1.0'
        }
        if self.github_token:
            self.headers['Authorization'] = f'token {self.github_token}'
    
    def get_last_weekly_date(self) -> datetime:
        """从最新周报文件提取结束时间"""
        weekly_dir = WEEKLY_DIR
        
        # 获取所有周报文件
        weekly_files = []
        for filename in os.listdir(weekly_dir):
            if filename.startswith('weekly') and filename.endswith('.md') and filename != 'index.md':
                weekly_files.append(filename)
        
        if not weekly_files:
            print("⚠️  未找到周报文件，使用30天前作为默认时间")
            return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # 按数字排序，获取最新的周报
        def extract_number(filename):
            match = re.search(r'weekly(\d+)', filename)
            return int(match.group(1)) if match else 0
        
        latest_weekly = sorted(weekly_files, key=extract_number)[-1]
        latest_path = os.path.join(weekly_dir, latest_weekly)
        
        print(f"📄 读取最新周报: {latest_weekly}")
        
        with open(latest_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取时间范围：2025/9/22 ~ 2025/10/8
        time_pattern = r'(\d{4}/\d{1,2}/\d{1,2})\s*~\s*(\d{4}/\d{1,2}/\d{1,2})'
        match = re.search(time_pattern, content)
        
        if match:
            end_date_str = match.group(2)  # 获取结束时间
            end_date = datetime.strptime(end_date_str, '%Y/%m/%d')
            print(f"⏰ 上次周报结束时间: {end_date.date()}")
            return end_date
        else:
            print("⚠️  无法提取时间，使用7天前作为默认时间")
            return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    def search_with_update_filter(self, query: str, since_date: datetime) -> List[Dict]:
        """搜索并按更新时间过滤"""
        print(f"\n🔍 搜索: {query}")
        results = []
        page = 1
        max_pages = 10  # 最多10页
        
        while page <= max_pages:
            url = "https://api.github.com/search/repositories"
            params = {
                'q': query,
                'sort': 'updated',
                'order': 'desc',
                'per_page': 100,
                'page': page
            }
            
            try:
                response = requests.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                
                data = response.json()
                items = data.get('items', [])
                
                if not items:
                    break
                
                # 检查每个仓库的更新时间
                for repo in items:
                    updated_at = datetime.fromisoformat(
                        repo['updated_at'].replace('Z', '+00:00')
                    ).date()
                    
                    # 如果更新时间早于或等于周报时间，停止搜索
                    if updated_at <= since_date.date():
                        print(f"   ⏹️  遇到 updated_at <= {since_date.date()}，停止搜索")
                        return results
                    
                    results.append(repo)
                
                print(f"   📄 第{page}页: {len(items)}个仓库")
                page += 1
                
            except requests.exceptions.RequestException as e:
                print(f"   ❌ API请求失败: {e}")
                break
        
        print(f"   ✅ 第一次过滤完成: {len(results)}个仓库")
        return results
    
    def deduplicate(self, repos: List[Dict]) -> List[Dict]:
        """按仓库ID去重"""
        seen = set()
        unique_repos = []
        
        for repo in repos:
            repo_id = repo['id']
            if repo_id not in seen:
                seen.add(repo_id)
                unique_repos.append(repo)
        
        return unique_repos
    
    def filter_by_created_date(self, repos: List[Dict], since_date: datetime) -> List[Dict]:
        """按创建时间过滤（第二次过滤）"""
        print(f"\n🔍 第二次过滤: created_at > {since_date.date()}")
        filtered = []
        
        for repo in repos:
            created_at = datetime.fromisoformat(
                repo['created_at'].replace('Z', '+00:00')
            ).date()
            
            # 只保留创建时间晚于周报时间的
            if created_at > since_date.date():
                filtered.append(repo)
        
        print(f"   ✅ 第二次过滤完成: {len(filtered)}个仓库")
        return filtered
    
    
    def save_results(self, repos: List[Dict]):
        """保存结果到文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 保存所有URL到单个文件
        urls_filename = os.path.join(OUTPUT_DIR, f"new_repos_urls_{timestamp}.txt")
        with open(urls_filename, 'w', encoding='utf-8') as f:
            for repo in repos:
                f.write(f"{repo['html_url']}\n")
        print(f"\n📝 所有仓库URL已保存: {urls_filename}")
        
        # 保存详细信息
        detail_filename = os.path.join(OUTPUT_DIR, f"new_repos_detail_{timestamp}.md")
        with open(detail_filename, 'w', encoding='utf-8') as f:
            f.write(f"# 新仓库收集结果\n\n")
            f.write(f"收集时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"总计: {len(repos)}个新仓库\n\n")
            
            for i, repo in enumerate(repos, 1):
                f.write(f"{i}. **{repo['full_name']}**\n")
                f.write(f"   - URL: {repo['html_url']}\n")
                f.write(f"   - 描述: {repo.get('description', '无')}\n")
                f.write(f"   - 语言: {repo.get('language', '未知')}\n")
                f.write(f"   - 创建: {repo['created_at'][:10]}\n")
                f.write(f"   - Stars: {repo['stargazers_count']}, Forks: {repo['forks_count']}\n\n")
        
        print(f"📝 详细信息已保存: {detail_filename}")
    
    def run(self):
        """主流程"""
        print("=" * 60)
        print("周报URL收集器")
        print("=" * 60)
        
        # 1. 获取上次周报时间
        since_date = self.get_last_weekly_date()
        
        # 2. 第一次过滤：搜索"moonbit"
        repos1 = self.search_with_update_filter("moonbit", since_date)
        
        # 3. 第一次过滤：搜索"language:moonbit"
        repos2 = self.search_with_update_filter("language:moonbit", since_date)
        
        # 4. 合并去重
        print(f"\n🔄 合并去重...")
        all_repos = self.deduplicate(repos1 + repos2)
        print(f"   ✅ 合并后: {len(all_repos)}个仓库")
        
        # 5. 第二次过滤：按创建时间
        new_repos = self.filter_by_created_date(all_repos, since_date)
        
        # 6. 保存结果
        self.save_results(new_repos)
        
        print("\n" + "=" * 60)
        print("✅ 收集完成！")
        print("=" * 60)
        print(f"\n📊 统计:")
        print(f"   新仓库总计: {len(new_repos)}个")
        print(f"\n💡 下一步:")
        print(f"   1. 打开生成的 new_repos_urls_*.txt 文件")
        print(f"   2. 在Cursor Chat中让AI分类为'项目'和'包'")
        print(f"   3. 分别让AI生成项目和包的周报条目")
        print(f"\n📋 Cursor分类提示词:")
        print(f"   '请将以下仓库分类为'项目'和'包'两类。")
        print(f"    分类标准：")
        print(f"    - 项目：完整应用、游戏、工具、框架实现、演示")
        print(f"    - 包：库、工具包、可被其他项目引用的模块'")
        print(f"\n   然后分别生成周报条目。")

def main():
    """主函数"""
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("⚠️  未设置GITHUB_TOKEN，API调用可能受限")
        print("   建议: export GITHUB_TOKEN=your_token\n")
    
    collector = WeeklyURLCollector(github_token)
    collector.run()

if __name__ == "__main__":
    main()

