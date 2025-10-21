#!/usr/bin/env python3
"""
MoonBit 周报仓库收集器 v3.0
使用 DeepSeek-V3 AI 分类，重量级数据抓取
"""

import sys
import re
import logging
import subprocess
from datetime import datetime
from pathlib import Path

from config import (
    WEEKLY_DIR,
    OUTPUT_DIR,
    OUTPUT_FILENAME_FORMAT,
    get_weekly_number
)
from fetcher import GitHubFetcher
from classifier import RepoClassifier
from formatter import MarkdownFormatter
import json

# ============ 日志配置 ============

def setup_logging():
    """设置日志（仅终端输出）"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )

# ============ 日期处理 ============

def auto_detect_date():
    """从最新周报提取截止日期"""
    try:
        weekly_files = list(WEEKLY_DIR.glob("weekly*.md"))
        if not weekly_files:
            return None
        
        # 按数字排序
        latest = max(weekly_files, 
                     key=lambda p: int(re.search(r'\d+', p.stem).group()))
        
        # 读取 frontmatter
        content = latest.read_text(encoding='utf-8')
        
        # 提取：title: Weekly14 社区周报 2025/9/22 ~ 2025/10/8
        match = re.search(r'~\s*(\d{4}/\d{1,2}/\d{1,2})', content)
        
        if match:
            date_str = match.group(1)
            parts = date_str.split('/')
            return f"{parts[0]}-{parts[1]:0>2}-{parts[2]:0>2}"
        
    except Exception as e:
        logging.warning(f"自动检测日期失败：{e}")
    
    return None

def get_search_date():
    """获取搜索日期（智能：自动检测或手动输入）"""
    # 支持命令行参数
    if len(sys.argv) > 1:
        date_arg = sys.argv[1]
        if re.match(r'\d{4}-\d{2}-\d{2}', date_arg):
            return date_arg
        else:
            print(f"❌ 日期格式错误：{date_arg}")
            sys.exit(1)
    
    auto_date = auto_detect_date()
    
    if auto_date:
        print(f"📅 检测到上次周报日期：{auto_date}")
        try:
            confirm = input("确认使用？(y/n): ").strip().lower()
            if confirm == 'y':
                return auto_date
        except EOFError:
            # 非交互式环境，自动使用
            print("(非交互式环境，自动使用检测到的日期)")
            return auto_date
    
    # 手动输入
    while True:
        try:
            date_input = input("\n请输入起始日期 (格式：2025-10-08): ").strip()
            if re.match(r'\d{4}-\d{2}-\d{2}', date_input):
                return date_input
            print("❌ 格式错误，请重新输入")
        except EOFError:
            print("\n❌ 无法获取输入，请使用命令行参数：python bot.py 2025-10-08")
            sys.exit(1)

def save_full_data(output_file, repos_with_data):
    """保存所有仓库的完整数据，供后续生成写作指引使用"""
    full_data = {}
    for repo, data in repos_with_data:
        full_data[repo['url']] = {
            'repo': repo,
            'full': data
        }
    
    json_file = str(output_file).replace('.md', '_full_data.json')
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(full_data, f, ensure_ascii=False, indent=2)
    
    return json_file

# ============ 主流程 ============

def main():
    print("🤖 MoonBit 周报仓库收集器 v3.0 (DeepSeek-V3)")
    print("─" * 60)
    
    # 设置日志
    setup_logging()
    
    # 获取日期
    since_date = get_search_date()
    print(f"📅 搜索日期：{since_date}")
    
    # 初始化
    fetcher = GitHubFetcher()
    classifier = RepoClassifier()
    formatter = MarkdownFormatter()
    
    # 步骤 1: 搜索仓库
    print(f"\n🔍 搜索...", end=' ', flush=True)
    repos = fetcher.search_repos(since_date)
    print(f"找到 {len(repos)} 个仓库")
    
    if not repos:
        print("✅ 没有新仓库，退出")
        return
    
    # 步骤 2: 抓取完整数据
    print(f"\n📥 抓取完整数据...", end=' ', flush=True)
    repos_with_data = []
    fetch_success = 0
    fetch_failed = 0
    
    for idx, repo in enumerate(repos, 1):
        full_data = fetcher.fetch_full_repo_data(repo['url'])
        
        if full_data:
            repo['full_data'] = full_data
            
            # 识别作者
            author_info = fetcher.identify_author(repo, full_data)
            repo['author_info'] = author_info
            
            repos_with_data.append((repo, full_data))
            fetch_success += 1
        else:
            repo['review_reason'] = '数据抓取失败'
            repos_with_data.append((repo, None))
            fetch_failed += 1
    
    print(f"{fetch_success}/{len(repos)} 成功")
    
    # 步骤 3: AI 分类
    print(f"\n🤖 AI 分类...", end=' ', flush=True)
    classified = classifier.classify_repos(repos_with_data)
    
    # 处理需要 Review 的仓库（组织/Fork 必须 Review）
    for repo, _ in repos_with_data:
        author_info = repo.get('author_info', {})
        
        # 组织仓库或 Fork 仓库必须进入 Review 区
        if author_info.get('type') in ['organization', 'fork']:
            if repo not in classified['review']:
                repo['review_reason'] = author_info.get('review_reason', '需要人工确认')
                classified['review'].append(repo)
                
                # 从 project/package 中移除
                for category in ['project', 'package']:
                    if repo in classified.get(category, []):
                        classified[category].remove(repo)
    
    # 显示分类结果
    print(f"📦 {len(classified['package'])} Package | 🚀 {len(classified['project'])} Project | ⚠️  {len(classified['review'])} Review")
    
    # 步骤 4: 生成输出
    weekly_num = get_weekly_number()
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    output_content = formatter.format_output(classified, since_date, weekly_num)
    
    # 覆盖防护：若文件存在且含有 review 签名，除非--force，否则拒绝覆盖
    output_filename = OUTPUT_FILENAME_FORMAT.format(
        weekly_num=weekly_num,
        date=date_str
    )
    output_file = OUTPUT_DIR / output_filename
    if output_file.exists():
        try:
            existing = output_file.read_text(encoding='utf-8')
            if 'weekly_bot_reviewed' in existing and '--force' not in sys.argv:
                print(f"\n⚠️  文件已被 review，阻止覆盖：{output_file.name}")
                print(f"如需覆盖请添加 --force 参数")
                return
        except Exception:
            pass
    output_file.write_text(output_content, encoding='utf-8')
    
    # 保存完整数据 JSON
    json_file = save_full_data(output_file, repos_with_data)
    
    # 显示成本
    ai_stats = classifier.get_usage_stats()
    print(f"💰 成本：¥{ai_stats['estimated_cost']:.4f}")
    
    # 保存信息
    print(f"\n📄 输出：{output_file.name}")
    
    # 根据是否有 Review 仓库，给出不同的下一步指引
    review_count = len(classified['review'])
    
    if review_count > 0:
        print(f"\n⚠️  发现 {review_count} 个待 Review 仓库")
        print("\n👉 按回车进入交互式 Review，或 Ctrl+C 退出")
        try:
            input()
        except (EOFError, KeyboardInterrupt):
            print("\n已退出")
            return
        
        # 自动调用 review.py（失败则中止）
        result = subprocess.run(['python', 'review.py', str(output_file)])
        if result.returncode != 0:
            print("\n❌ Review 失败，已停止。请修复后重试：")
            print(f"python review.py {output_file}")
            return
        
        # Review 完成后，提示生成写作指引
        print("\n👉 按回车生成写作指引，或 Ctrl+C 退出")
        try:
            input()
        except (EOFError, KeyboardInterrupt):
            print("\n已退出")
            return
        
        result = subprocess.run(['python', 'generate_writing_guide.py', str(output_file)])
        if result.returncode != 0:
            print("\n❌ 写作指引生成失败，请检查错误信息")
            return
        
        # 提示运行 postcheck
        print(f"\n📋 建议运行发布前检查：")
        print(f"python tools/weekly_bot/postcheck.py trees/weekly/weekly{get_weekly_number()}")
    else:
        print("\n👉 按回车生成写作指引，或 Ctrl+C 退出")
        try:
            input()
        except (EOFError, KeyboardInterrupt):
            print("\n已退出")
            return
        
        result = subprocess.run(['python', 'generate_writing_guide.py', str(output_file)])
        if result.returncode != 0:
            print("\n❌ 写作指引生成失败，请检查错误信息")
            return
        
        # 提示运行 postcheck
        print(f"\n📋 建议运行发布前检查：")
        print(f"python tools/weekly_bot/postcheck.py trees/weekly/weekly{get_weekly_number()}")
    
    print("\n✅ 周报自动化完成！")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断")
        sys.exit(0)
    except Exception as e:
        logging.error(f"运行错误：{e}", exc_info=True)
        print(f"\n❌ 错误：{e}")
        sys.exit(1)

