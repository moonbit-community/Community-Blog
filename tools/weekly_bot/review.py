#!/usr/bin/env python3
"""
交互式Review工具
帮助快速处理Review区的仓库，标注贡献者和分类
"""

import sys
import json
import re
import signal
import termios
import tty
import requests
import readline
from pathlib import Path
from datetime import datetime
from config import GITHUB_TOKEN, GITHUB_GRAPHQL_URL

def fetch_contributors_from_github(repo_url: str, limit: int = 5) -> list:
    """
    从GitHub API获取仓库的主要贡献者
    
    Args:
        repo_url: 仓库URL
        limit: 返回的贡献者数量限制
    
    Returns:
        贡献者列表，每个元素包含name, login, url, contributions
    """
    try:
        # 提取owner和repo名称
        match = re.search(r'github\.com/([^/]+)/([^/]+)', repo_url)
        if not match:
            print(f"    ⚠️ 无法解析仓库URL: {repo_url}")
            return []
        
        owner, repo = match.groups()
        
        # 验证token
        if not GITHUB_TOKEN:
            print(f"    ⚠️ GitHub Token未配置，跳过API获取")
            return []
        
        # GitHub REST API获取contributors
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
        headers = {
            'Authorization': f'Bearer {GITHUB_TOKEN}',
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'MoonBit-Weekly-Bot/3.3'
        }
        
        response = requests.get(api_url, headers=headers, timeout=15)
        
        # 处理不同的HTTP状态码
        if response.status_code == 404:
            print(f"    ⚠️ 仓库不存在或无权访问: {repo_url}")
            return []
        elif response.status_code == 403:
            print(f"    ⚠️ API限制或权限不足: {repo_url}")
            return []
        elif response.status_code != 200:
            print(f"    ⚠️ API请求失败 ({response.status_code}): {repo_url}")
            return []
        
        contributors = response.json()
        
        if not isinstance(contributors, list):
            print(f"    ⚠️ API返回格式异常: {repo_url}")
            return []
        
        # 格式化返回数据
        result = []
        for i, contrib in enumerate(contributors[:limit]):
            try:
                # 获取用户详细信息
                user_url = contrib.get('url', '')
                if not user_url:
                    continue
                    
                user_response = requests.get(user_url, headers=headers, timeout=10)
                if user_response.status_code == 200:
                    user_data = user_response.json()
                    name = user_data.get('name', '').strip()
                    login = contrib.get('login', '').strip()
                    
                    if not login:
                        continue
                    
                    result.append({
                        'name': name or login,  # 如果没有真实姓名，使用用户名
                        'login': login,
                        'url': f"https://github.com/{login}",
                        'contributions': contrib.get('contributions', 0),
                        'display': f"[{login} {name}](https://github.com/{login})" if name else f"[{login}](https://github.com/{login})"
                    })
            except Exception as user_e:
                print(f"    ⚠️ 获取用户信息失败: {user_e}")
                continue
        
        return result
        
    except requests.exceptions.Timeout:
        print(f"    ⚠️ 请求超时: {repo_url}")
        return []
    except requests.exceptions.ConnectionError:
        print(f"    ⚠️ 网络连接失败: {repo_url}")
        return []
    except Exception as e:
        print(f"    ⚠️ 获取贡献者失败: {e}")
        return []

def validate_github_url(url: str) -> bool:
    """验证GitHub URL格式"""
    pattern = r'^https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/?$'
    return bool(re.match(pattern, url.strip()))

def safe_input(prompt: str = "", timeout: int = 600) -> str:
    """
    基于readline的安全输入函数，支持完整的光标操作和signal处理
    
    Args:
        prompt: 提示信息
        timeout: 超时时间（秒）
    
    Returns:
        用户输入的字符串
    """
    # 检查是否在交互式环境中
    if not sys.stdin.isatty():
        print(f"    ⚠️ 非交互式环境，无法获取用户输入")
        return "NON_INTERACTIVE"
    
    # 配置readline以支持更好的编辑体验
    try:
        # 启用历史记录和自动补全
        readline.parse_and_bind("tab: complete")
        readline.parse_and_bind("set editing-mode emacs")
        
        # 设置readline的signal处理
        readline.parse_and_bind("set convert-meta off")
        readline.parse_and_bind("set input-meta on")
        readline.parse_and_bind("set output-meta on")
    except Exception:
        # 如果readline配置失败，继续使用基本功能
        pass
    
    # 保存原始signal处理
    original_handlers = {}
    signals_to_handle = [signal.SIGINT, signal.SIGTERM, signal.SIGQUIT]
    
    for sig in signals_to_handle:
        try:
            original_handlers[sig] = signal.signal(sig, signal.SIG_IGN)
        except (OSError, ValueError):
            # 某些signal在某些系统上不可用
            pass
    
    try:
        # 设置超时处理
        def timeout_handler(signum, frame):
            raise TimeoutError("输入超时")
        
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)
        
        # 使用readline增强的input
        try:
            result = input(prompt)
            return result
        except (EOFError, KeyboardInterrupt):
            # 用户按Ctrl+C或Ctrl+D
            return ""
        
    except TimeoutError:
        print(f"\n⚠️ 输入超时（{timeout}秒）")
        return ""
    except Exception as e:
        print(f"    ⚠️ 输入错误: {e}")
        return ""
    finally:
        # 恢复所有signal处理
        for sig, handler in original_handlers.items():
            try:
                signal.signal(sig, handler)
            except (OSError, ValueError):
                pass
        signal.alarm(0)

def safe_input_with_validation(prompt: str, valid_choices: list = None, default: str = None) -> str:
    """
    带验证的安全输入函数
    
    Args:
        prompt: 提示信息
        valid_choices: 有效选择列表
        default: 默认值
    
    Returns:
        验证后的输入
    """
    max_attempts = 5  # 最大重试次数
    attempt_count = 0
    
    while attempt_count < max_attempts:
        attempt_count += 1
        
        try:
            user_input = safe_input(prompt).strip()
            
            # 处理非交互式环境
            if user_input == "NON_INTERACTIVE":
                print("    ⚠️ 非交互式环境，使用默认值")
                return default if default else ""
            
            # 如果输入为空且有默认值，返回默认值
            if not user_input and default:
                return default
            
            # 如果没有有效选择限制，直接返回
            if not valid_choices:
                return user_input
            
            # 验证选择
            if user_input in valid_choices:
                return user_input
            
            # 如果是数字选择
            if user_input.isdigit():
                idx = int(user_input)
                if 0 <= idx <= len(valid_choices):
                    return user_input
            
            print(f"    ❌ 无效输入，请选择: {', '.join(map(str, valid_choices))}")
            
            if attempt_count >= max_attempts:
                print(f"    ⚠️ 达到最大重试次数({max_attempts})，使用默认值")
                return default if default else ""
            
        except Exception as e:
            print(f"    ❌ 输入错误: {e}")
            if attempt_count >= max_attempts:
                print(f"    ⚠️ 达到最大重试次数({max_attempts})，使用默认值")
                return default if default else ""
    
    # 如果达到最大重试次数，返回默认值
    return default if default else ""

def interactive_multi_choice(prompt: str, options: list, allow_multiple: bool = True) -> list:
    """
    交互式多选功能
    
    Args:
        prompt: 提示信息
        options: 选项列表，每个元素包含name, display等
        allow_multiple: 是否允许多选
    
    Returns:
        选中的选项列表
    """
    max_attempts = 5  # 最大重试次数
    attempt_count = 0
    
    while attempt_count < max_attempts:
        attempt_count += 1
        
        print(f"\n    {prompt}")
        print("    选项:")
        
        for i, option in enumerate(options, 1):
            print(f"    □ {i}) {option.get('display', option.get('name', str(option)))}")
        
        if allow_multiple:
            print(f"    □ {len(options)+1}) 手动输入贡献者URL")
            print(f"    □ 0) 跳过")
            choice_prompt = f"    选择 (可多选，用空格分隔，如: 1 3 {len(options)+1}): "
        else:
            choice_prompt = f"    选择 (1-{len(options)}): "
        
        # 添加调试信息
        if not sys.stdin.isatty():
            print("    ⚠️ 检测到非交互式环境，自动选择跳过")
            return []
        
        user_input = safe_input(choice_prompt, timeout=600).strip()
        
        # 处理非交互式环境
        if user_input == "NON_INTERACTIVE":
            print("    ⚠️ 非交互式环境，自动跳过")
            return []
        
        # 改进空输入处理
        if not user_input:
            if attempt_count >= max_attempts:
                print(f"    ⚠️ 连续{max_attempts}次空输入，自动跳过")
                return []
            print("    💡 请输入选择或按Ctrl+C退出")
            continue
        
        # 解析多选输入
        if allow_multiple:
            choices = user_input.split()
            selected = []
            manual_input_needed = False
            
            for choice in choices:
                if choice == '0':
                    return []  # 跳过
                elif choice.isdigit():
                    idx = int(choice)
                    if 1 <= idx <= len(options):
                        selected.append(options[idx-1])
                    elif idx == len(options) + 1:
                        manual_input_needed = True
                else:
                    print(f"    ❌ 无效选择: {choice}")
                    continue
            
            # 处理手动输入
            if manual_input_needed:
                manual_contributor = interactive_contributor_input("手动输入贡献者（支持：[name](url) | @username | url）")
                if manual_contributor:
                    # 将单个贡献者字符串转换为期望的格式
                    selected.append({
                        'name': manual_contributor,
                        'login': manual_contributor,
                        'url': manual_contributor,
                        'display': manual_contributor
                    })
            
            if selected:
                return selected
            else:
                print("    ❌ 请至少选择一个选项")
                if attempt_count >= max_attempts:
                    print(f"    ⚠️ 达到最大重试次数({max_attempts})，自动跳过")
                    return []
        else:
            # 单选
            if user_input.isdigit():
                idx = int(user_input)
                if 1 <= idx <= len(options):
                    return [options[idx-1]]
            
            print(f"    ❌ 无效选择，请输入 1-{len(options)}")
            if attempt_count >= max_attempts:
                print(f"    ⚠️ 达到最大重试次数({max_attempts})，自动跳过")
                return []
    
    # 如果达到最大重试次数，返回空列表
    print(f"    ⚠️ 达到最大重试次数({max_attempts})，自动跳过")
    return []


def confirm_with_retry(prompt: str, selected_items: list, item_type: str = "选项") -> list:
    """
    确认选择，支持返回重新更改
    
    Args:
        prompt: 确认提示
        selected_items: 已选择的项目列表
        item_type: 项目类型（用于显示）
    
    Returns:
        确认后的选择列表，如果用户选择重新更改则返回None
    """
    while True:
        print(f"\n    {prompt}")
        print(f"    已选择的{item_type}:")
        
        for item in selected_items:
            display = item.get('display', item.get('name', str(item)))
            print(f"    ✓ {display}")
        
        choice = safe_input_with_validation(
            f"    确认这些{item_type}? (y=确认 / e=重新选择): ",
            valid_choices=['y', 'e'],
            default='y'
        )
        
        if choice == 'y':
            return selected_items
        elif choice == 'e':
            return None  # 表示需要重新选择

def format_multiple_contributors(contributors: list) -> str:
    """
    格式化多个贡献者显示
    
    Args:
        contributors: 贡献者列表
    
    Returns:
        格式化后的贡献者字符串
    """
    if not contributors:
        return ""
    
    if len(contributors) == 1:
        return contributors[0]['display']
    
    if len(contributors) == 2:
        return f"{contributors[0]['display']} 和 {contributors[1]['display']}"
    
    # 多个贡献者
    displays = [c['display'] for c in contributors]
    return "、".join(displays)

def normalize_contributor(raw: str) -> str:
    """标准化贡献者输入格式"""
    s = ' '.join(raw.split())
    if not s:
        return ''
    # 已是 [name](url)
    if '[' in s and '](' in s and s.endswith(')'):
        return s
    # 仅URL → 提取用户名
    if s.startswith('http'):
        m = re.search(r'github\.com/([^/\s\)]{1,40})', s)
        if m:
            u = m.group(1)
            return f"[{u}](https://github.com/{u})"
        return ''
    # @username 或 username → 自动补全URL
    u = s.lstrip('@').strip()
    if re.match(r'^[A-Za-z0-9-]{1,40}$', u):
        return f"[{u}](https://github.com/{u})"
    return ''

def interactive_contributor_input(prompt: str) -> str:
    """交互式贡献者输入，支持多步确认和自动补全"""
    # 检查是否在交互式环境
    if not sys.stdin.isatty():
        print("    ⚠️ 非交互式环境，无法输入贡献者")
        return None
    
    print(f"\n    {prompt}")
    print("    格式: https://github.com/username")
    print("    输入 'done' 完成，输入 'cancel' 取消")
    
    contributors = []
    empty_input_count = 0
    max_empty_attempts = 3
    
    while True:
        try:
            url_input = safe_input("    URL: ", timeout=600).strip()
        except Exception as e:
            print(f"    ❌ 输入错误: {e}")
            continue
        
        # 处理特殊命令
        if url_input.lower() == 'done':
            break
        elif url_input.lower() == 'cancel':
            return None
        elif not url_input:
            # 空输入，提示用户
            empty_input_count += 1
            if empty_input_count >= max_empty_attempts:
                print(f"    ⚠️ 连续{max_empty_attempts}次空输入，退出输入")
                break
            print("    💡 请输入URL、'done' 或 'cancel'")
            continue
        
        # 重置空输入计数
        empty_input_count = 0
        
        # 验证URL格式
        if not validate_github_url(url_input):
            print("    ❌ 无效的GitHub URL格式")
            print("    💡 正确格式: https://github.com/username")
            continue
        
        # 提取用户名
        match = re.search(r'github\.com/([^/]+)', url_input)
        if not match:
            print("    ❌ 无法解析用户名")
            continue
            
        username = match.group(1)
        
        # 检查是否重复
        if any(c['login'] == username for c in contributors):
            print(f"    ⚠️ 贡献者 {username} 已存在")
            continue
        
        contributors.append({
            'name': username,
            'login': username,
            'url': url_input,
            'display': f"[{username}]({url_input})"
        })
        print(f"    ✓ 已添加: [{username}]({url_input})")
    
    if contributors:
        # 显示所有贡献者并确认
        print(f"\n    已添加的贡献者:")
        for i, c in enumerate(contributors, 1):
            print(f"    {i}) {c['display']}")
        
        confirm = safe_input_with_validation(
            "    确认这些贡献者? (y=确认 / e=重新选择 / s=跳过仓库): ",
            valid_choices=['y', 'e', 's'],
            default='y'
        )
        
        if confirm == 'y':
            return contributors[0]['display']  # 返回第一个贡献者的显示格式
        elif confirm == 'e':
            return interactive_contributor_input(prompt)  # 递归重新选择
        else:
            return None
    
    return None

def load_data(md_file):
    """加载MD文件和JSON数据"""
    # 读取MD文件
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # 读取JSON数据
    json_file = md_file.replace('.md', '_full_data.json')
    with open(json_file, 'r', encoding='utf-8') as f:
        full_data = json.load(f)
    
    return md_content, full_data

def extract_review_repos(md_content):
    """提取Review区的所有仓库（支持详细格式和简单列表格式）"""
    review_repos = []
    
    # 匹配Review区
    review_section = re.search(r'## ⚠️ 需要Review.*?\n(.*?)(?=\n## |\Z)', md_content, re.DOTALL)
    if not review_section:
        return []
    
    section_content = review_section.group(1)
    
    # 格式1: 详细格式 ### 数字. [name](url) （组织仓库、Fork仓库）
    detailed_pattern = r'### (\d+)\. \[([^\]]+)\]\((https://github\.com/[^\)]+)\)(.*?)(?=\n###|\n\d+\.|\Z)'
    detailed_matches = re.findall(detailed_pattern, section_content, re.DOTALL)
    
    for idx, name, url, details in detailed_matches:
        # 提取描述、作者等信息
        desc_match = re.search(r'\*\*描述\*\*: (.+)', details)
        author_match = re.search(r'\*\*作者\*\*: (.+)', details)
        readme_match = re.search(r'\*\*README\*\*:(.*?)(?=\n\*\*|\n---|\Z)', details, re.DOTALL)
        
        review_repos.append({
            'index': int(idx),
            'name': name,
            'url': url,
            'description': desc_match.group(1).strip() if desc_match else '无',
            'author': author_match.group(1).strip() if author_match else None,
            'readme_snippet': readme_match.group(1).strip() if readme_match else '',
            'is_detailed': True
        })
    
    # 格式2: 简单列表 数字. [name](url) - reason （分类存疑、抓取失败）
    simple_pattern = r'^(\d+)\. \[([^\]]+)\]\((https://github\.com/[^\)]+)\)\s*-\s*(.+)$'
    simple_matches = re.findall(simple_pattern, section_content, re.MULTILINE)
    
    for idx, name, url, reason in simple_matches:
        review_repos.append({
            'index': int(idx),
            'name': name,
            'url': url,
            'description': reason.strip(),
            'author': None,
            'readme_snippet': '',
            'is_detailed': False
        })
    
    # 按index排序
    review_repos.sort(key=lambda x: x['index'])
    
    return review_repos

def extract_contributors(readme, url, moon_mod=None):
    """从README和moon_mod.json提取可能的贡献者"""
    candidates = []
    
    # Pattern 0: 从 moon_mod.json 的 name 字段提取（优先级最高）
    if moon_mod:
        try:
            import json
            mod_data = json.loads(moon_mod)
            mod_name = mod_data.get('name', '')
            # 提取 username/package 格式
            if '/' in mod_name:
                username = mod_name.split('/')[0]
                if username.lower() not in ['moonbit-community', 'moonbit', 'moonbitlang']:
                    candidates.append({'name': username, 'url': f'https://github.com/{username}'})
        except:
            pass
    
    if not readme:
        return candidates[:5] if candidates else []
    
    # Pattern 1: Markdown链接 [name](url)
    matches = re.findall(r'\[([^\]]+)\]\((https://github\.com/[^)]+)\)', readme)
    for name, link in matches:
        # 过滤掉非人名的链接
        if not any(kw in name.lower() for kw in ['github', 'license', 'badge', 'build', 'npm', 'crate']):
            if 'github.com' in link and link != url:  # 不包括仓库自己的URL
                candidates.append({'name': name, 'url': link})
    
    # Pattern 2: @username 提及
    matches = re.findall(r'@(\w+)', readme)
    for username in matches:
        if len(username) > 2:  # 过滤太短的
            candidates.append({'name': username, 'url': f'https://github.com/{username}'})
    
    # Pattern 3: 从标题提取 username/repo 格式（如 # Yoorkin/splice）
    title_match = re.search(r'^#+ ([a-zA-Z0-9-_]+)/[a-zA-Z0-9-_]+', readme, re.MULTILINE)
    if title_match:
        username = title_match.group(1)
        # 排除组织名本身
        if username.lower() not in ['moonbit-community', 'moonbit', 'moonbitlang']:
            candidates.append({'name': username, 'url': f'https://github.com/{username}'})
    
    # Pattern 4: 从URL推断（organization名）
    org_match = re.match(r'https://github\.com/([^/]+)/', url)
    if org_match:
        org_name = org_match.group(1)
        # 如果是moonbit-community等，可能在README里有维护者
        if 'community' in org_name.lower() or 'moonbit' in org_name.lower():
            # 查找"by XXX"或"author: XXX"
            author_pattern = r'(?:by|author|maintainer|contributor)[\s:]+[@\[]?([^\]\n,]+)'
            author_matches = re.findall(author_pattern, readme, re.IGNORECASE)
            for author in author_matches[:2]:
                author = author.strip()
                if author and not author.startswith('http'):
                    candidates.append({'name': author, 'url': f'https://github.com/{author}'})
    
    # 去重
    seen = set()
    unique = []
    for c in candidates:
        key = c['url'].lower()
        if key not in seen and c['name'].strip():
            seen.add(key)
            unique.append(c)
    
    return unique[:5]  # 最多5个候选

def review_repo(repo, full_data, is_org=False):
    """Review单个仓库"""
    print("\n" + "─" * 60)
    print(f"📦 [{repo['index']}] {repo['name']}")
    print(f"    URL: {repo['url']}")
    print(f"    描述: {repo['description']}")
    
    if repo['author']:
        print(f"    作者: {repo['author']}")
    
    # 获取完整README和moon_mod
    repo_data = full_data.get(repo['url'])
    if repo_data is None:
        print("    ⚠️ 仓库数据缺失，跳过")
        return {'repo': repo, 'category': 'review', 'contributors': []}
    
    data = repo_data.get('full_data', {})
    readme = data.get('readme', '')
    moon_mod = data.get('moon_mod', '')
    
    result = {'repo': repo}
    
    # 如果是组织仓库，需要标注贡献者
    if is_org:
        print(f"\n    🏢 组织仓库 - 需要标注主要贡献者")
        
        # 获取GitHub API贡献者 + 静态提取的贡献者
        github_contributors = fetch_contributors_from_github(repo['url'])
        static_contributors = extract_contributors(readme, repo['url'], moon_mod)
        
        # 合并贡献者列表，去重
        all_contributors = []
        seen_urls = set()
        
        # 优先使用GitHub API的贡献者
        for contrib in github_contributors:
            if contrib['url'] not in seen_urls:
                all_contributors.append(contrib)
                seen_urls.add(contrib['url'])
        
        # 添加静态提取的贡献者
        for contrib in static_contributors:
            if contrib['url'] not in seen_urls:
                all_contributors.append({
                    'name': contrib['name'],
                    'login': contrib['name'],
                    'url': contrib['url'],
                    'display': f"[{contrib['name']}]({contrib['url']})"
                })
                seen_urls.add(contrib['url'])
        
        # 交互式选择贡献者
        selected_contributors = None
        while selected_contributors is None:
            if all_contributors:
                selected_contributors = interactive_multi_choice(
                    "选择主要贡献者:",
                    all_contributors,
                    allow_multiple=True
                )
            else:
                print(f"\n    未找到贡献者候选，需要手动输入")
                manual_contributor = interactive_contributor_input("手动输入贡献者（支持：[name](url) | @username | url）")
                if manual_contributor:
                    # 将单个贡献者字符串转换为期望的格式
                    selected_contributors = [{
                        'name': manual_contributor,
                        'login': manual_contributor,
                        'url': manual_contributor,
                        'display': manual_contributor
                    }]
                else:
                    selected_contributors = []
            
            if selected_contributors is not None:
                # 确认选择
                confirmed = confirm_with_retry(
                    "确认贡献者选择:",
                    selected_contributors,
                    "贡献者"
                )
                if confirmed is None:
                    selected_contributors = None  # 重新选择
        
        if selected_contributors:
            result['contributor'] = format_multiple_contributors(selected_contributors)
            print(f"    ✓ 已选择贡献者: {result['contributor']}")
        else:
            print(f"    ↷ 跳过此仓库")
            result['category'] = 'skip'
            return result
    
    # 显示README摘要（如果有）
    if readme:
        snippet = readme[:200].replace('\n', ' ')
        print(f"\n    README: {snippet}...")
    
    # 分类选择
    print(f"\n    分配类别:")
    print(f"      1) Package  2) Project  3) 丢弃（不进入周报）")
    
    category_options = [
        {'name': 'Package', 'display': '📦 Package'},
        {'name': 'Project', 'display': '🚀 Project'},
        {'name': 'Discard', 'display': '🗑️ 丢弃（不进入周报）'}
    ]
    
    selected_category = None
    while selected_category is None:
        selected_category = interactive_multi_choice(
            "选择类别:",
            category_options,
            allow_multiple=False
        )
        
        if selected_category:
            # 确认选择
            confirmed = confirm_with_retry(
                "确认类别选择:",
                selected_category,
                "类别"
            )
            if confirmed is None:
                selected_category = None  # 重新选择
    
    if selected_category:
        category_name = selected_category[0]['name']
        if category_name == 'Discard':
            result['category'] = 'skip'
            print(f"    🗑️ 已丢弃")
        else:
            result['category'] = category_name.lower()
            emoji = '📦' if category_name == 'Package' else '🚀'
            print(f"    ✓ 已分配到 {emoji} {category_name}")
    else:
        # 非交互式环境或用户取消，默认跳过
        result['category'] = 'skip'
        print(f"    ↷ 跳过此仓库")
    
    return result

def update_md_file(md_file, md_content, results):
    """更新MD文件"""
    
    # 提取Package和Project区的当前内容
    pkg_section = re.search(r'(## 📦 Package.*?\n)(.*?)(?=\n## )', md_content, re.DOTALL)
    proj_section = re.search(r'(## 🚀 Project.*?\n)(.*?)(?=\n## )', md_content, re.DOTALL)
    
    pkg_header = pkg_section.group(1) if pkg_section else "## 📦 Package (0个)\n\n"
    pkg_content = pkg_section.group(2) if pkg_section else ""
    proj_header = proj_section.group(1) if proj_section else "## 🚀 Project (0个)\n\n"
    proj_content = proj_section.group(2) if proj_section else ""
    
    # 统计当前数量
    pkg_count = len(re.findall(r'^### \d+\.', pkg_content, re.MULTILINE))
    proj_count = len(re.findall(r'^### \d+\.', proj_content, re.MULTILINE))
    
    # 构建新增条目
    new_pkg_entries = []
    new_proj_entries = []
    
    for result in results:
        if result['category'] == 'skip':
            continue
        
        repo = result['repo']
        
        # 构建条目
        entry = f"### {repo['index']}. [{repo['name']}]({repo['url']})\n"
        
        # 如果有贡献者信息，替换作者
        if result.get('contributor'):
            entry += f"**作者**: {result['contributor']}\n"
        elif repo.get('author'):
            entry += f"**作者**: {repo['author']}\n"
        
        entry += f"**描述**: {repo['description']}\n"
        
        if result['category'] == 'package':
            new_pkg_entries.append(entry)
        else:
            new_proj_entries.append(entry)
    
    # 更新Package区
    if new_pkg_entries:
        pkg_count += len(new_pkg_entries)
        pkg_header = f"## 📦 Package ({pkg_count}个)\n\n"
        pkg_content += "\n" + "\n---\n\n".join(new_pkg_entries) + "\n\n---\n\n"
    
    # 更新Project区
    if new_proj_entries:
        proj_count += len(new_proj_entries)
        proj_header = f"## 🚀 Project ({proj_count}个)\n\n"
        proj_content += "\n" + "\n---\n\n".join(new_proj_entries) + "\n\n---\n\n"
    
    # 移除已处理的仓库从Review区
    processed_urls = {r['repo']['url'] for r in results if r['category'] != 'skip'}
    
    # 处理详细格式：### 数字. [name](url)
    def remove_processed_detailed(match):
        url = match.group(1)  # 修复：正则只有1个捕获组
        if url in processed_urls:
            return ''
        return match.group(0)
    
    md_content = re.sub(
        r'### \d+\. \[[^\]]+\]\((https://github\.com/[^\)]+)\).*?(?=\n###|\n\d+\.|\n## |\Z)',
        remove_processed_detailed,
        md_content,
        flags=re.DOTALL
    )
    
    # 处理简单列表格式：数字. [name](url) - reason
    def remove_processed_simple(match):
        url = match.group(1)
        if url in processed_urls:
            return ''
        return match.group(0)
    
    md_content = re.sub(
        r'^\d+\. \[[^\]]+\]\((https://github\.com/[^\)]+)\)\s*-\s*.+$',
        remove_processed_simple,
        md_content,
        flags=re.MULTILINE
    )
    
    # 重建文件（保持分区间最小空行）
    md_content = re.sub(r'## 📦 Package.*?\n.*?(?=\n## )', pkg_header + pkg_content, md_content, count=1, flags=re.DOTALL)
    md_content = re.sub(r'## 🚀 Project.*?\n.*?(?=\n## )', proj_header + proj_content, md_content, count=1, flags=re.DOTALL)

    # 清理多余分隔符与空行
    # 1) 连续 --- 合并为单个
    md_content = re.sub(r'(\n---\n){2,}', '\n---\n', md_content)
    # 2) 去掉分区内多余空行
    md_content = re.sub(r'\n{3,}', '\n\n', md_content)
    
    # 更新Review区标题（统计剩余）
    review_count = len(re.findall(r'^### \d+\.', re.search(r'## ⚠️ 需要Review.*', md_content, re.DOTALL).group(0), re.MULTILINE)) if re.search(r'## ⚠️ 需要Review', md_content) else 0
    md_content = re.sub(r'## ⚠️ 需要Review \(\d+个\)', f'## ⚠️ 需要Review ({review_count}个)', md_content)
    
    # 结尾仅保留一个换行
    if not md_content.endswith('\n'):
        md_content += '\n'
    md_content = re.sub(r'\n+$', '\n', md_content)

    # 保存
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    # 写入review签名（用于后续防覆盖与校验）
    signature = f"<!-- weekly_bot_reviewed: {datetime.now().isoformat(timespec='seconds')} -->\n"
    try:
        if 'weekly_bot_reviewed' not in md_content:
            with open(md_file, 'a', encoding='utf-8') as f:
                f.write(signature)
    except Exception:
        pass
    
    return pkg_count, proj_count, review_count

def main():
    try:
        if len(sys.argv) < 2:
            print("用法: python review.py output/repos_weekly15_2025-10-14.md")
            sys.exit(1)
        
        md_file = sys.argv[1]
        
        # 验证文件存在
        if not Path(md_file).exists():
            print(f"❌ 文件不存在: {md_file}")
            sys.exit(1)
        
        print("\n" + "=" * 60)
        print("📋 交互式 Review 工具")
        print("=" * 60)
        
        # 加载数据
        print("\n⏳ 加载数据...")
        try:
            md_content, full_data = load_data(md_file)
            review_repos = extract_review_repos(md_content)
        except Exception as e:
            print(f"❌ 数据加载失败: {e}")
            sys.exit(1)
        
        if not review_repos:
            print("\n✅ 没有需要Review的仓库！")
            sys.exit(0)
        
        print(f"✓ 找到 {len(review_repos)} 个需要Review的仓库")
        
        # 分类：详细格式（组织/Fork）vs 简单列表（分类存疑/抓取失败）
        detailed_repos = []  # 需要标注贡献者的详细格式仓库
        simple_repos = []    # 只需分类的简单列表仓库
        
        for repo in review_repos:
            if repo.get('is_detailed', False):
                detailed_repos.append(repo)
            else:
                simple_repos.append(repo)
        
        results = []
        
        # 处理详细格式仓库（组织/Fork，需要标注贡献者）
        if detailed_repos:
            print(f"\n" + "=" * 60)
            print(f"🏢 组织/Fork仓库 ({len(detailed_repos)}个) - 需要标注贡献者")
            print("=" * 60)
            
            for repo in detailed_repos:
                result = review_repo(repo, full_data, is_org=True)
                results.append(result)
        
        # 处理简单列表仓库（分类存疑/抓取失败，只需分类）
        if simple_repos:
            print(f"\n" + "=" * 60)
            print(f"🤔 其他Review仓库 ({len(simple_repos)}个) - 只需分类")
            print("=" * 60)
            
            for repo in simple_repos:
                result = review_repo(repo, full_data, is_org=False)
                results.append(result)
        
        # 统计
        pkg_count = sum(1 for r in results if r['category'] == 'package')
        proj_count = sum(1 for r in results if r['category'] == 'project')
        skip_count = sum(1 for r in results if r['category'] == 'skip')
        
        print("\n" + "=" * 60)
        print("📊 Review 汇总")
        print("=" * 60)
        print(f"✓ Package: {pkg_count} 个")
        print(f"✓ Project: {proj_count} 个")
        print(f"↷ 跳过: {skip_count} 个")
        
        # 确认保存
        if pkg_count + proj_count > 0:
            confirm = safe_input_with_validation(
                f"\n保存修改? (y/n): ",
                valid_choices=['y', 'n'],
                default='y'
        ).lower()
        
            if confirm == 'y':
                print("\n⏳ 更新MD文件...")
                total_pkg, total_proj, remain = update_md_file(md_file, md_content, results)
                
                print("\n" + "=" * 60)
                print("✅ Review 完成！")
                print("=" * 60)
                print(f"📦 Package: 现在共 {total_pkg} 个")
                print(f"🚀 Project: 现在共 {total_proj} 个")
                print(f"⚠️  Review: 剩余 {remain} 个")
                print(f"\n✓ 已更新: {md_file}")
                print(f"\n📝 下一步: python generate_writing_guide.py {md_file}")
                print("=" * 60)
            else:
                print("\n❌ 已取消，未保存修改")
        else:
            print("\n✓ 没有更改")
    
    except Exception as e:
        print(f"\n❌ Review过程出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    # 设置全局signal处理
    def signal_handler(signum, frame):
        print(f"\n\n⚠️ 收到信号 {signum}，正在安全退出...")
        sys.exit(0)
    
    # 注册signal处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

