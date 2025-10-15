#!/usr/bin/env python3
"""
输出格式化模块
生成分区Markdown输出
"""

from datetime import datetime
from typing import Dict, List
from config import README_MAX_CHARS_FOR_OUTPUT

class MarkdownFormatter:
    """Markdown格式化器"""
    
    def format_output(self, classified: Dict, since_date: str, weekly_num: int) -> str:
        """
        生成最终的Markdown输出
        
        Args:
            classified: 分类结果
            since_date: 起始日期
            weekly_num: 周报编号
        
        Returns:
            完整的Markdown内容
        """
        projects = classified.get('project', [])
        packages = classified.get('package', [])
        reviews = classified.get('review', [])
        
        total = len(projects) + len(packages) + len(reviews)
        now = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        # 开始构建
        output = f"# MoonBit 新仓库 ({since_date} 之后)\n\n"
        output += f"共 {total} 个仓库 | 生成时间: {now}\n\n"
        output += "---\n\n"
        
        # Package区
        output += f"## 📦 Package ({len(packages)}个)\n\n"
        if packages:
            for idx, pkg in enumerate(packages, 1):
                output += self._format_repo_detail(pkg, idx)
        else:
            output += "*暂无新包*\n\n"
        
        output += "---\n\n"
        
        # Project区
        output += f"## 🚀 Project ({len(projects)}个)\n\n"
        if projects:
            for idx, proj in enumerate(projects, 1):
                output += self._format_repo_detail(proj, idx)
        else:
            output += "*暂无新项目*\n\n"
        
        output += "---\n\n"
        
        # Review区
        output += f"## ⚠️ 需要Review ({len(reviews)}个)\n\n"
        
        if reviews:
            # 按类型分组
            org_repos = []
            fork_repos = []
            classify_fail = []
            fetch_fail = []
            
            for repo in reviews:
                author_type = repo.get('author_info', {}).get('type')
                reason = repo.get('review_reason', '未知原因')
                
                if author_type == 'organization':
                    org_repos.append(repo)
                elif author_type == 'fork':
                    fork_repos.append(repo)
                elif '抓取失败' in reason or '数据抓取失败' in reason:
                    fetch_fail.append(repo)
                else:
                    classify_fail.append(repo)
            
            # 输出分区（组织仓库用详细格式+README）
            if org_repos:
                output += f"### 🏢 组织仓库 ({len(org_repos)}个)\n\n"
                for idx, repo in enumerate(org_repos, 1):
                    output += self._format_repo_detail(repo, idx)
                output += "\n"
            
            if fork_repos:
                output += f"### 🔀 Fork仓库 ({len(fork_repos)}个)\n\n"
                for idx, repo in enumerate(fork_repos, 1):
                    output += self._format_repo_simple(repo, idx)
                output += "\n"
            
            if classify_fail:
                output += f"### 🤔 分类存疑 ({len(classify_fail)}个)\n\n"
                for idx, repo in enumerate(classify_fail, 1):
                    output += self._format_repo_simple(repo, idx)
                output += "\n"
            
            if fetch_fail:
                output += f"### ❌ 抓取失败 ({len(fetch_fail)}个)\n\n"
                for idx, repo in enumerate(fetch_fail, 1):
                    output += self._format_repo_simple(repo, idx)
                output += "\n"
        else:
            output += "*全部仓库已成功分类*\n\n"
        
        return output
    
    def _format_repo_detail(self, repo: Dict, idx: int) -> str:
        """详细格式（带README）"""
        
        # 作者信息
        author_info = repo.get('author_info', {})
        
        # 基础信息
        stars = repo['stars'] if repo['stars'] > 0 else 0
        created = repo['created_at'][:10]  # 只要日期
        language = repo['language'] or '未知'
        topics_str = ', '.join(repo['topics'][:5]) if repo['topics'] else '无'
        desc = repo['description'] or '无描述'
        
        # README
        readme_full = repo.get('full_data', {}).get('readme', '')
        readme_display = readme_full[:README_MAX_CHARS_FOR_OUTPUT]
        if len(readme_full) > README_MAX_CHARS_FOR_OUTPUT:
            readme_display += '...'
        
        output = f"### {idx}. [{repo['full_name']}]({repo['url']})\n"
        
        # 作者（只在有display时显示）
        if author_info.get('display'):
            output += f"**作者**: {author_info['display']}\n"
        
        output += f"**Stars**: {stars} | **创建**: {created} | **语言**: {language}\n"
        output += f"**Topics**: {topics_str}\n"
        output += f"**描述**: {desc}\n\n"
        
        if readme_display:
            output += f"**README**:\n```\n{readme_display}\n```\n\n"
        else:
            output += f"**README**: *无*\n\n"
        
        output += "---\n\n"
        
        return output
    
    def _format_repo_simple(self, repo: Dict, idx: int) -> str:
        """简单格式（仅标题和原因）"""
        reason = repo.get('review_reason', '未知原因')
        return f"{idx}. [{repo['full_name']}]({repo['url']}) - {reason}\n"


if __name__ == "__main__":
    # 测试
    formatter = MarkdownFormatter()
    
    test_data = {
        'project': [
            {
                'url': 'https://github.com/test/game',
                'full_name': 'test/game',
                'owner_login': 'test',
                'description': 'A game',
                'created_at': '2025-10-10T00:00:00Z',
                'stars': 10,
                'language': 'MoonBit',
                'topics': ['game', 'moonbit'],
                'author_info': {
                    'display': '[test Zhang San](https://github.com/test)'
                },
                'full_data': {
                    'readme': '# Game\nThis is a game...'
                }
            }
        ],
        'package': [],
        'review': [
            {
                'url': 'https://github.com/org/lib',
                'full_name': 'org/lib',
                'owner_login': 'org',
                'review_reason': '组织仓库，需确认主要作者'
            }
        ]
    }
    
    output = formatter.format_output(test_data, '2025-10-08', 15)
    print(output[:500])

