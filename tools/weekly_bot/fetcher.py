#!/usr/bin/env python3
"""
GraphQL重量级数据抓取模块
抓取仓库的README、代码结构、作者昵称等完整信息
"""

import requests
import re
from typing import Dict, List, Optional
from datetime import datetime
from config import (
    GITHUB_TOKEN,
    GITHUB_GRAPHQL_URL,
    SEARCH_QUERIES,
    README_MAX_CHARS_FOR_AI,
    MBT_FILE_MAX_CHARS,
    MAX_MBT_FILES
)

class GitHubFetcher:
    """GitHub数据抓取器"""
    
    def __init__(self):
        self.headers = {
            'Authorization': f'Bearer {GITHUB_TOKEN}',
            'Content-Type': 'application/json'
        }
    
    def search_repos(self, since_date: str) -> List[Dict]:
        """
        搜索仓库（两种策略：关键词 + 语言）
        
        Args:
            since_date: 起始日期 (YYYY-MM-DD)
        
        Returns:
            去重后的仓库列表
        """
        all_repos = {}
        
        for query_str in SEARCH_QUERIES:
            search_query = f'{query_str} created:>{since_date} sort:created-desc'
            
            repos = self._graphql_search(search_query)
            
            # 去重
            for repo in repos:
                if repo['url'] not in all_repos:
                    all_repos[repo['url']] = repo
        
        return list(all_repos.values())
    
    def _graphql_search(self, search_query: str) -> List[Dict]:
        """GraphQL搜索查询"""
        query = """
        query($searchQuery: String!, $cursor: String) {
          search(query: $searchQuery, type: REPOSITORY, first: 100, after: $cursor) {
            pageInfo {
              hasNextPage
              endCursor
            }
            edges {
              node {
                ... on Repository {
                  name
                  nameWithOwner
                  url
                  description
                  createdAt
                  stargazerCount
                  primaryLanguage { name }
                  repositoryTopics(first: 10) {
                    nodes { topic { name } }
                  }
                  isFork
                  owner {
                    login
                    ... on User { name }
                    ... on Organization { name }
                    __typename
                  }
                }
              }
            }
          }
        }
        """
        
        repos = []
        cursor = None
        has_next = True
        
        while has_next:
            try:
                response = requests.post(
                    GITHUB_GRAPHQL_URL,
                    json={
                        'query': query,
                        'variables': {
                            'searchQuery': search_query,
                            'cursor': cursor
                        }
                    },
                    headers=self.headers,
                    timeout=30
                )
                
                response.raise_for_status()
                data = response.json()
                
                if 'errors' in data:
                    print(f"\n⚠️ GraphQL错误: {data['errors']}")
                    break
                
                for edge in data['data']['search']['edges']:
                    repo = edge['node']
                    repos.append({
                        'name': repo['name'],
                        'full_name': repo['nameWithOwner'],
                        'url': repo['url'],
                        'description': repo['description'] or '',
                        'created_at': repo['createdAt'],
                        'stars': repo['stargazerCount'],
                        'language': repo['primaryLanguage']['name'] if repo['primaryLanguage'] else '',
                        'topics': [t['topic']['name'] for t in repo['repositoryTopics']['nodes']],
                        'is_fork': repo['isFork'],
                        'owner_login': repo['owner']['login'],
                        'owner_name': repo['owner'].get('name', ''),
                        'owner_type': repo['owner']['__typename']
                    })
                
                page_info = data['data']['search']['pageInfo']
                has_next = page_info['hasNextPage']
                cursor = page_info['endCursor']
                
            except requests.exceptions.RequestException as e:
                print(f"\n❌ 搜索错误: {e}")
                break
        
        return repos
    
    def fetch_full_repo_data(self, repo_url: str) -> Optional[Dict]:
        """
        抓取单个仓库的完整数据（重量级）
        
        包含: README全文、moon.mod.json、.mbt代码片段、文件结构
        
        Args:
            repo_url: 仓库URL
        
        Returns:
            完整的仓库数据，失败返回None
        """
        # 解析owner和repo名
        match = re.search(r'github\.com/([^/]+)/([^/]+)', repo_url)
        if not match:
            return None
        
        owner, name = match.groups()
        
        query = """
        query($owner: String!, $name: String!) {
          repository(owner: $owner, name: $name) {
            # README.md
            readme: object(expression: "HEAD:README.md") {
              ... on Blob {
                text
              }
            }
            
            # README.mbt.md (MoonBit优先)
            readmeMbt: object(expression: "HEAD:README.mbt.md") {
              ... on Blob {
                text
              }
            }
            
            # moon.mod.json
            moonMod: object(expression: "HEAD:moon.mod.json") {
              ... on Blob {
                text
              }
            }
            
            # 根目录文件列表
            rootTree: object(expression: "HEAD:") {
              ... on Tree {
                entries {
                  name
                  type
                  object {
                    ... on Blob {
                      text
                    }
                  }
                }
              }
            }
            
            # src目录
            srcTree: object(expression: "HEAD:src") {
              ... on Tree {
                entries {
                  name
                  type
                  object {
                    ... on Blob {
                      text
                    }
                  }
                }
              }
            }
            
            # lib目录
            libTree: object(expression: "HEAD:lib") {
              ... on Tree {
                entries {
                  name
                  type
                }
              }
            }
            
            # cmd目录 (新架构)
            cmdTree: object(expression: "HEAD:cmd/main") {
              ... on Tree {
                entries {
                  name
                  type
                  object {
                    ... on Blob {
                      text
                    }
                  }
                }
              }
            }
          }
        }
        """
        
        try:
            response = requests.post(
                GITHUB_GRAPHQL_URL,
                json={
                    'query': query,
                    'variables': {'owner': owner, 'name': name}
                },
                headers=self.headers,
                timeout=30
            )
            
            response.raise_for_status()
            data = response.json()
            
            if 'errors' in data:
                return None
            
            repo_data = data['data']['repository']
            
            # 提取数据
            result = {
                'readme': self._extract_readme(repo_data),
                'moon_mod': self._extract_moon_mod(repo_data),
                'code_files': self._extract_code_files(repo_data),
                'has_lib': bool(repo_data.get('libTree'))
            }
            
            return result
            
        except Exception as e:
            print(f"\n⚠️ 抓取失败 {repo_url}: {e}")
            return None
    
    def _extract_readme(self, repo_data: Dict) -> str:
        """提取README内容（智能匹配优先级）"""
        # 1. 优先: README.mbt.md (MoonBit新架构)
        readme_mbt = repo_data.get('readmeMbt')
        if readme_mbt and readme_mbt.get('text'):
            return readme_mbt['text'][:README_MAX_CHARS_FOR_AI]
        
        # 2. 其次: README.md (通用)
        readme_md = repo_data.get('readme')
        if readme_md and readme_md.get('text'):
            return readme_md['text'][:README_MAX_CHARS_FOR_AI]
        
        # 3. 回退: 从rootTree查找任何README文件
        root_tree = repo_data.get('rootTree') or {}
        for entry in root_tree.get('entries', []):
            if entry['name'].upper().startswith('README'):
                text = entry.get('object', {}).get('text', '')
                if text:
                    return text[:README_MAX_CHARS_FOR_AI]
        
        return ''
    
    def _extract_moon_mod(self, repo_data: Dict) -> str:
        """提取moon.mod.json内容"""
        moon_mod_obj = repo_data.get('moonMod')
        if not moon_mod_obj:
            return ''
        
        return moon_mod_obj.get('text', '')
    
    def _extract_code_files(self, repo_data: Dict) -> List[Dict]:
        """提取.mbt代码文件片段（统一500字符）"""
        code_files = []
        
        # 根目录.mbt文件
        root_tree = repo_data.get('rootTree') or {}
        for entry in root_tree.get('entries', []):
            if entry['name'].endswith('.mbt') and entry['type'] == 'blob':
                text = entry.get('object', {}).get('text', '')
                code_files.append({
                    'path': entry['name'],
                    'content': text[:500] if text else ''
                })
        
        # src目录.mbt文件
        src_tree = repo_data.get('srcTree') or {}
        for entry in src_tree.get('entries', []):
            if entry['name'].endswith('.mbt') and entry['type'] == 'blob':
                text = entry.get('object', {}).get('text', '')
                code_files.append({
                    'path': f"src/{entry['name']}",
                    'content': text[:500] if text else ''
                })
        
        # cmd目录.mbt文件 (新架构)
        cmd_tree = repo_data.get('cmdTree') or {}
        for entry in cmd_tree.get('entries', []):
            if entry['name'].endswith('.mbt') and entry['type'] == 'blob':
                text = entry.get('object', {}).get('text', '')
                code_files.append({
                    'path': f"cmd/main/{entry['name']}",
                    'content': text[:500] if text else ''
                })
        
        # 限制文件数量
        return code_files[:MAX_MBT_FILES]
    
    def identify_author(self, repo: Dict, full_data: Optional[Dict] = None) -> Dict:
        """
        识别作者信息
        
        Args:
            repo: 基础仓库信息
            full_data: 完整仓库数据（可选）
        
        Returns:
            作者信息字典
        """
        owner_login = repo['owner_login']
        owner_name = repo.get('owner_name', '')
        owner_type = repo.get('owner_type', 'User')
        is_fork = repo['is_fork']
        
        # 情况1: 组织仓库（优先判断）
        if owner_type == 'Organization':
            return {
                'type': 'organization',
                'username': owner_login,
                'nickname': owner_name,
                'display': None,
                'confidence': 'low',
                'review_reason': '组织仓库'
            }
        
        # 情况2: Fork仓库
        if is_fork:
            return {
                'type': 'fork',
                'username': owner_login,
                'nickname': owner_name,
                'display': None,
                'confidence': 'low',
                'review_reason': 'Fork仓库'
            }
        
        # 情况3: 个人仓库（有昵称）
        if owner_name:
            return {
                'type': 'individual',
                'username': owner_login,
                'nickname': owner_name,
                'display': f"[{owner_login} {owner_name}](https://github.com/{owner_login})",
                'confidence': 'high'
            }
        
        # 情况4: 个人仓库（无昵称）
        return {
            'type': 'individual',
            'username': owner_login,
            'nickname': None,
            'display': f"[{owner_login}](https://github.com/{owner_login})",
            'confidence': 'high'
        }


if __name__ == "__main__":
    # 测试
    fetcher = GitHubFetcher()
    
    print("测试搜索...")
    repos = fetcher.search_repos('2025-10-01')
    print(f"找到 {len(repos)} 个仓库")
    
    if repos:
        print("\n测试抓取第一个仓库详情...")
        full_data = fetcher.fetch_full_repo_data(repos[0]['url'])
        if full_data:
            print(f"README长度: {len(full_data['readme'])}")
            print(f"代码文件: {len(full_data['code_files'])}")
            print(f"有moon.mod.json: {bool(full_data['moon_mod'])}")

