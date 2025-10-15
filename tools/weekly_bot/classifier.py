#!/usr/bin/env python3
"""
AI分类模块
使用DeepSeek-V3对仓库进行智能分类
"""

import json
import requests
import time
from typing import Dict, List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import (
    SILICONFLOW_API_KEY,
    SILICONFLOW_API_URL,
    MODEL_NAME,
    TEMPERATURE,
    MAX_TOKENS,
    TOP_P,
    TOP_K,
    MAX_CONCURRENCY,
    AI_TIMEOUT,
    AI_RETRIES
)

class RepoClassifier:
    """仓库分类器（基于DeepSeek-V3）"""
    
    def __init__(self):
        self.headers = {
            'Authorization': f'Bearer {SILICONFLOW_API_KEY}',
            'Content-Type': 'application/json'
        }
        self.total_input_tokens = 0
        self.total_output_tokens = 0
    
    def classify_repos(self, repos_with_data: List[Tuple[Dict, Dict]]) -> Dict:
        """
        批量分类仓库
        
        Args:
            repos_with_data: [(repo_basic, repo_full_data), ...]
        
        Returns:
            {
                'project': [repo1, repo2, ...],
                'package': [repo3, repo4, ...],
                'review': [repo5, ...]
            }
        """
        results = {
            'project': [],
            'package': [],
            'review': []
        }
        
        # 硬规则预分流
        to_classify = []
        for repo, full in repos_with_data:
            # 信息不足
            if not full or (not repo.get('description') and not full.get('readme')):
                repo['review_reason'] = '信息不足'
                results['review'].append(repo)
                continue
                
            # 组织/Fork（依赖bot中的author_info）
            author_type = (repo.get('author_info') or {}).get('type')
            if author_type in ['organization', 'fork'] or repo.get('is_fork'):
                repo['review_reason'] = '组织/或Fork仓库'
                results['review'].append(repo)
                continue
                
            to_classify.append((repo, full))
        
        if not to_classify:
            return results
        
        # 单仓库并发调用AI
        def worker(args):
            repo, full = args
            prompt = self._build_single_prompt(repo, full)
            
            # 简单重试
            last_err = None
            for attempt in range(AI_RETRIES + 1):
                try:
                    response = self._call_api(prompt)
                    return repo, self._parse_single_response(response)
                except Exception as e:
                    last_err = e
                    if attempt < AI_RETRIES:
                        time.sleep(1)  # 简单延迟
                        
            return repo, {'label': 'review', 'reason': f'API调用失败: {str(last_err)[:50]}'}
        
        # 并发执行
        with ThreadPoolExecutor(max_workers=MAX_CONCURRENCY) as executor:
            futures = [executor.submit(worker, item) for item in to_classify]
            
            for i, future in enumerate(as_completed(futures), 1):
                repo, result = future.result()
                label = (result.get('label') or '').lower()
                reason = result.get('reason') or 'AI未分类（模型不确定）'
                
                if label in ['project', 'package']:
                    results[label].append(repo)
                else:
                    repo['review_reason'] = reason
                    results['review'].append(repo)
        
        return results
    
    def _build_single_prompt(self, repo: Dict, full_data: Dict) -> str:
        """构建单仓库AI提示词"""
        
        # 组装结构信号
        cf = full_data.get('code_files') or []
        paths = [c.get('path') or '' for c in cf]
        has_main = any(p.endswith('main.mbt') for p in paths)
        has_cmd_main = any('cmd/main/main.mbt' in p for p in paths)
        
        data = {
            'url': repo['url'],
            'name': repo['name'],
            'description': repo.get('description') or '',
            'topics': repo.get('topics') or [],
            'structure': {
                'has_lib_dir': bool(full_data.get('has_lib')),
                'has_main': has_main,
                'has_cmd_main': has_cmd_main,
                'has_moon_mod': bool(full_data.get('moon_mod'))
            },
            'readme_snippet': (full_data.get('readme') or '')[:2000]  # 限制长度
        }
        
        prompt = f"""你是MoonBit周报的分类专家。请判断下面这个GitHub仓库是 project、package，或者 review（不确定时）：

定义：
- package: 面向其他项目复用的库/框架/绑定/工具集
- project: 面向用户使用的应用/游戏/CLI/工具/示例成品

规则：
- 不确定时，一定返回 review，并简要说明原因（1句话）

仓库数据：
{json.dumps(data, ensure_ascii=False, indent=2)}

只返回一个JSON对象，不要markdown代码块，也不要多余文本：
{{
  "url": "{repo['url']}",
  "label": "project|package|review",
  "reason": "一句话原因"
}}"""
        
        return prompt
    
    def _parse_single_response(self, response: Dict) -> Dict:
        """解析单仓库AI响应"""
        content = response['choices'][0]['message']['content'].strip()
        
        # 去除可能的```包裹或json前缀
        if '```json' in content:
            content = content.split('```json')[1].split('```')[0].strip()
        elif '```' in content:
            content = content.split('```')[1].split('```')[0].strip()
        elif content.startswith('json'):
            content = content[4:].strip()
        
        try:
            obj = json.loads(content)
            label = (obj.get('label') or '').lower()
            reason = obj.get('reason') or 'AI未分类（模型不确定）'
            return {'label': label, 'reason': reason}
        except Exception as e:
            return {'label': 'review', 'reason': 'AI未分类（解析失败）'}
    
    
    def _call_api(self, prompt: str) -> Dict:
        """调用DeepSeek-V3 API"""
        payload = {
            'model': MODEL_NAME,
            'messages': [
                {
                    'role': 'system',
                    'content': '你是一个专业的代码分类专家，擅长分析GitHub仓库的类型。只返回JSON格式的分类结果。'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'stream': False,
            'max_tokens': MAX_TOKENS,
            'temperature': TEMPERATURE,
            'top_p': TOP_P,
            'top_k': TOP_K
        }
        
        response = requests.post(
            SILICONFLOW_API_URL,
            headers=self.headers,
            json=payload,
            timeout=AI_TIMEOUT
        )
        
        response.raise_for_status()
        result = response.json()
        
        # 统计token使用
        if 'usage' in result:
            self.total_input_tokens += result['usage'].get('prompt_tokens', 0)
            self.total_output_tokens += result['usage'].get('completion_tokens', 0)
        
        return result
    
    
    def get_usage_stats(self) -> Dict:
        """获取token使用统计"""
        from config import estimate_cost
        
        cost = estimate_cost(self.total_input_tokens, self.total_output_tokens)
        
        return {
            'input_tokens': self.total_input_tokens,
            'output_tokens': self.total_output_tokens,
            'total_tokens': self.total_input_tokens + self.total_output_tokens,
            'estimated_cost': cost
        }


if __name__ == "__main__":
    # 测试
    classifier = RepoClassifier()
    
    # 模拟数据
    test_data = [
        (
            {
                'url': 'https://github.com/test/lib',
                'name': 'lib',
                'description': 'A utility library',
                'topics': ['library', 'moonbit']
            },
            {
                'readme': '# Utility Library\nThis is a library...',
                'moon_mod': '{"name": "@test/lib"}',
                'code_files': [{'path': 'lib.mbt', 'content': 'pub fn add() {}'}],
                'has_lib': True
            }
        )
    ]
    
    print("测试分类...")
    result = classifier.classify_repos(test_data)
    print(f"结果: {result}")
    print(f"Token统计: {classifier.get_usage_stats()}")

