#!/usr/bin/env python3
"""
从已review的repos_xxx.md生成写作指引文档
"""
import sys
import json
import re
from pathlib import Path
from datetime import datetime, timedelta

REVIEW_SIGNATURE_KEY = 'weekly_bot_reviewed'

def calculate_week_description(start_date_str, end_date_str):
    """根据日期跨度计算周数描述"""
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        days_diff = (end_date - start_date).days + 1  # +1 包含起始日期
        
        if 7<= days_diff < 14:
            return "为单周周报"
        elif days_diff < 21:
            return "为双周周报"
        elif days_diff < 28:
            return "为三周周报"
        else:
            return f"为{days_diff}天周报"
    except:
        return "为周报"

def update_previous_weekly_embed(current_weekly_num):
    """自动更新上一周的embed格式（从[+]改为[+-]）"""
    if current_weekly_num <= 1:
        return  # 第一期周报没有上一期
    
    previous_num = current_weekly_num - 1
    index_file = Path(__file__).parent.parent.parent / 'trees' / 'weekly' / 'index.md'
    
    if not index_file.exists():
        return
    
    # 读取index.md
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 将上一周的[+]改为[+-]
    old_embed = f'[+](/weekly/weekly{previous_num}.md#:embed)'
    new_embed = f'[+-](/weekly/weekly{previous_num}.md#:embed)'
    
    if old_embed in content:
        content = content.replace(old_embed, new_embed)
        
        # 保存更新后的内容
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ 已更新 weekly{previous_num} 的embed格式：[+] → [+-]")

def parse_reviewed_md(md_file):
    """解析已review的MD文件，提取Package和Project的URL"""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取Package区的所有URL（匹配到下一个emoji section，如 ## 🚀 或 ## ⚠️）
    pkg_section = re.search(r'## 📦 Package.*?\n(.*?)(?=\n## [🚀⚠️]|\Z)', content, re.DOTALL)
    packages = re.findall(r'https://github\.com/[^/\s]+/[^\s\)]+', pkg_section.group(1)) if pkg_section else []
    
    # 提取Project区的所有URL
    proj_section = re.search(r'## 🚀 Project.*?\n(.*?)(?=\n## ⚠️|\Z)', content, re.DOTALL)
    projects = re.findall(r'https://github\.com/[^/\s]+/[^\s\)]+', proj_section.group(1)) if proj_section else []
    
    return packages, projects

def load_full_data(md_file):
    """加载完整数据JSON"""
    json_file = md_file.replace('.md', '_full_data.json')
    
    # 检查文件是否存在
    if not Path(json_file).exists():
        print(f"❌ 错误：找不到数据文件 {json_file}")
        print(f"请确保先运行 bot.py 生成完整数据")
        sys.exit(1)
    
    # 尝试加载JSON
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析失败: {e}")
        print(f"文件可能已损坏: {json_file}")
        sys.exit(1)

def detect_weekly_number():
    """自动检测weekly编号"""
    # 从脚本位置找到项目根目录
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    weekly_dir = project_root / 'trees' / 'weekly'
    
    if not weekly_dir.exists():
        return 1
    
    # 只匹配目录，不包括.md文件
    weekly_dirs = [d for d in weekly_dir.iterdir() if d.is_dir() and d.name.startswith('weekly')]
    if not weekly_dirs:
        return 1
    
    numbers = []
    for d in weekly_dirs:
        match = re.search(r'weekly(\d+)', d.name)
        if match:
            numbers.append(int(match.group(1)))
    
    return max(numbers) + 1 if numbers else 1

def format_readme(readme, max_chars=1000):
    """格式化README：概述+功能列表+用法示例"""
    if not readme:
        return "*无README*"
    
    # 截取前1000字
    snippet = readme[:max_chars]
    
    # 尝试提取结构化信息
    lines = snippet.split('\n')
    
    # 概述（前5行）
    overview = '\n'.join(lines[:5])
    
    # 功能列表（查找- 开头的行）
    features = [line for line in lines if line.strip().startswith('-')]
    
    if features:
        return f"**概述**:\n{overview}\n\n**主要功能**:\n" + '\n'.join(features[:5])
    else:
        return overview

def format_code_files(code_files):
    """格式化代码文件：路径列表 + 关键代码"""
    if not code_files:
        return "*无代码文件*"
    
    # 路径列表
    paths = [f"- `{cf['path']}`" for cf in code_files[:10]]  # 最多10个
    
    # 关键代码（main.mbt或第一个文件）
    main_file = next((cf for cf in code_files if 'main.mbt' in cf['path']), code_files[0])
    
    return f"**文件列表**:\n" + '\n'.join(paths) + f"\n\n**关键代码** (`{main_file['path']}`):\n```moonbit\n{main_file['content'][:500]}...\n```"

def extract_real_examples(weekly_num):
    """从上一期周报提取真实示例"""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    last_weekly_dir = project_root / 'trees' / 'weekly' / f'weekly{weekly_num-1}'
    
    examples = {
        'package': None,
        'project': None
    }
    
    # 提取Package示例
    pkg_file = last_weekly_dir / 'packages.md'
    if pkg_file.exists():
        try:
            content = pkg_file.read_text(encoding='utf-8')
            # 提取BEGIN和END之间的第一个条目（去掉frontmatter）
            match = re.search(r'<!-- BEGIN: packages -->(.*?)<!-- END: packages -->', content, re.DOTALL)
            if match:
                entries_text = match.group(1).strip()
                # 取第一个条目（通常以作者开头，到第一个空行结束）
                lines = [l for l in entries_text.split('\n') if l.strip()]
                if lines:
                    # 取前3行作为示例
                    examples['package'] = '\n'.join(lines[:3])
        except:
            pass
    
    # 提取Project示例
    proj_file = last_weekly_dir / 'projects.md'
    if proj_file.exists():
        try:
            content = proj_file.read_text(encoding='utf-8')
            match = re.search(r'<!-- BEGIN: projects -->(.*?)<!-- END: projects -->', content, re.DOTALL)
            if match:
                entries_text = match.group(1).strip()
                lines = [l for l in entries_text.split('\n') if l.strip()]
                if lines:
                    examples['project'] = '\n'.join(lines[:3])
        except:
            pass
    
    return examples

def generate_writing_guide(md_file):
    """生成写作指引文档"""
    
    # 解析review后的分类
    pkg_urls, proj_urls = parse_reviewed_md(md_file)
    # 校验是否已完成review（存在签名）
    with open(md_file, 'r', encoding='utf-8') as f:
        whole = f.read()
    reviewed = (REVIEW_SIGNATURE_KEY in whole)
    
    # 加载完整数据
    full_data = load_full_data(md_file)
    
    # 检测weekly编号
    weekly_num = detect_weekly_number()
    
    # 提取日期 - 从MD文件标题提取搜索日期
    with open(md_file, 'r', encoding='utf-8') as f:
        first_line = f.readline()
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', first_line)
    
    search_date = date_match.group(1) if date_match else datetime.now().strftime('%Y-%m-%d')
    
    # 计算周数描述（假设搜索日期是开始日期，结束日期是开始日期+7天）
    start_date = search_date
    end_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=6)).strftime('%Y-%m-%d')
    week_description = calculate_week_description(start_date, end_date)
    
    # 提取真实示例
    real_examples = extract_real_examples(weekly_num)
    
    # 生成指令文档
    instructions_doc = f"""# Weekly {weekly_num} 周报条目写作指引

> 📅 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
> 📦 Package: {len(pkg_urls)}个 | 🚀 Project: {len(proj_urls)}个

---

## 🚨 核心规则（违反将导致重做）

### ✅ 必须做到：
1. **仅处理数据文档中的仓库**（{len(pkg_urls) + len(proj_urls)}个），不得增删
2. **文件路径**（和weekly{weekly_num-1}同级）：
   - `trees/weekly/weekly{weekly_num}.md` ← 主文档
   - `trees/weekly/weekly{weekly_num}/packages.md` ← Package条目
   - `trees/weekly/weekly{weekly_num}/projects.md` ← Project条目
   - `trees/weekly/weekly{weekly_num}/official.md` ← 空模板（只保留frontmatter，不要添加任何锚点标记）
   - `trees/weekly/weekly{weekly_num}/community.md` ← 空模板（只保留frontmatter，不要添加任何锚点标记）

3. **格式要求**：
   - 每条2-3句（用途+功能+特性）
   - 条目间无空行
   - 直接编辑文件内容，添加Package/Project条目
   - 保持Markdown格式，不要添加任何特殊标记
   - 文件末尾恰好1个换行

### ❌ 严禁：
- 重复frontmatter（每个文件只能有一个`---`块）
- 文件尾部再次粘贴整段模板
- 添加任何特殊标记或锚点
- 臆测信息（必须基于README和提供的数据）

---

## 📖 风格参照

**请先阅读以下文件了解写作风格**：
- `trees/weekly/weekly{weekly_num-1}/packages.md` - 阅读前2条Package条目
- `trees/weekly/weekly{weekly_num-1}/projects.md` - 阅读前2条Project条目

**若无法访问历史文件，请按以下最小规范**：
- 作者：`[username 昵称](url)` 或 `[username](url)`（无昵称时）
- 类型：库/框架/绑定/工具集（Package）| 应用/游戏/CLI/示例（Project）
- 用途：一句话说清楚干什么用的
- 功能：从README提炼3-5个核心功能
- 特性：技术亮点或应用场景

---

## 📋 执行步骤

### Step 1: 访问仓库URL
访问数据文档中每个仓库的GitHub页面，了解项目整体情况

### Step 2: 结合数据编写
- 使用数据文档中的技术信息补充理解
- 参照历史风格编写条目
- 直接编辑文件内容，添加条目

### Step 3: 创建文件结构
- 创建 `trees/weekly/weekly{weekly_num}/` 目录
- 创建4个子文档：packages.md、projects.md、official.md、community.md
- 创建主文档：`trees/weekly/weekly{weekly_num}.md`
- 更新索引：在 `trees/weekly/index.md` 末尾添加embed行（使用 `[+]` 格式）

### 主文档模板：
```markdown
---
title: Weekly{weekly_num} 社区周报 {start_date} ~ {end_date}
---

这里是 {start_date} ~ {end_date} 的社区周报，{week_description}。

[+](/weekly/weekly{weekly_num}/official.md#:embed)

[+](/weekly/weekly{weekly_num}/projects.md#:embed)

[+](/weekly/weekly{weekly_num}/packages.md#:embed)

[+](/weekly/weekly{weekly_num}/community.md#:embed)
```

---

## 📋 格式要求详解

### ✅ 正确的embed格式：
```
[+](/weekly/weekly{weekly_num}/official.md#:embed)
[+](/weekly/weekly{weekly_num}/projects.md#:embed)
[+](/weekly/weekly{weekly_num}/packages.md#:embed)
[+](/weekly/weekly{weekly_num}/community.md#:embed)
```

### ❌ 错误的embed格式（禁止使用）：
```
[+-](/weekly/weekly{weekly_num}/official.md#:embed)  ← 错误：历史周报格式
[+](/weekly/weekly{weekly_num}/official.md#:embed)   ← 错误：多余空格
```

### ✅ 正确的子文档标题：
- `title: 本周官方重要动态`
- `title: 本周社区动态`
- `title: 本周社区新增优质项目`
- `title: 本周社区新增优质包`

### ❌ 错误的子文档标题（禁止使用）：
- `title: 官方动态`  ← 错误：缺少"本周"和"重要"
- `title: 社区动态`  ← 错误：缺少"本周"

### ✅ 空文档的正确格式（official.md和community.md）：
```markdown
---
title: 本周官方重要动态
---

```

### ❌ 空文档的错误格式（禁止使用）：
```markdown
---
title: 本周官方重要动态
---

<!-- 任何特殊标记 -->
```
**注意**：空文档只保留frontmatter，不要添加任何特殊标记！

## ✅ 验证清单

生成完成后检查：
- [ ] 文件数量正确（5个文件）
- [ ] 条目数量：Package {len(pkg_urls)}个，Project {len(proj_urls)}个
- [ ] 每条包含：作者+用途+功能
- [ ] 无重复frontmatter
- [ ] 无文件尾部模板粘贴
- [ ] index.md已更新
- [ ] embed格式使用 `[+]`（不是 `[+-]`）
- [ ] 子文档标题包含"本周"字样
- [ ] 文件格式正确，无特殊标记

**现在开始执行！**
"""
    
    # 生成数据文档
    data_doc = {
        'weekly_num': weekly_num,
        'start_date': start_date,
        'end_date': end_date,
        'week_description': week_description,
        'packages': [],
        'projects': []
    }
    
    # 处理Package数据
    missing_count = 0
    for i, url in enumerate(pkg_urls, 1):
        if url not in full_data:
            print(f"⚠️  警告：Package URL {url} 在数据中找不到，跳过")
            missing_count += 1
            continue
        
        repo = full_data[url]['repo']
        data = full_data[url]['full']
        
        author_info = repo.get('author_info', {})
        readme = data.get('readme', '')
        readme_brief = readme[:300] + '...' if len(readme) > 300 else readme
        
        # 提取关键代码片段
        code_files = data.get('code_files', [])
        key_code = ''
        if code_files:
            main_file = next((cf for cf in code_files if 'main.mbt' in cf.get('path', '')), code_files[0])
            key_code = main_file.get('content', '')[:300] + '...' if len(main_file.get('content', '')) > 300 else main_file.get('content', '')
        
        # 技术信号
        tech_signals = []
        if data.get('has_lib'):
            tech_signals.append('lib目录')
        if any('main.mbt' in cf.get('path', '') for cf in code_files):
            tech_signals.append('main.mbt')
        if data.get('moon_mod'):
            tech_signals.append('moon.mod.json')
        
        package_data = {
            'index': i,
            'name': repo['name'],
            'url': url,
            'category': 'Package',
            'author': {
                'username': author_info.get('username', ''),
                'nickname': author_info.get('nickname', ''),
                'profile_url': f"https://github.com/{author_info.get('username', '')}" if author_info.get('username') else '',
                'display': author_info.get('display', '')
            },
            'description': repo.get('description', ''),
            'readme_summary': readme_brief,
            'key_code': key_code,
            'tech_signals': tech_signals,
            'metadata': {
                'stars': repo.get('stars', 0),
                'created_at': repo.get('created_at', ''),
                'topics': repo.get('topics', [])
            }
        }
        data_doc['packages'].append(package_data)
    
    # 处理Project数据
    for i, url in enumerate(proj_urls, 1):
        if url not in full_data:
            print(f"⚠️  警告：Project URL {url} 在数据中找不到，跳过")
            missing_count += 1
            continue
        
        repo = full_data[url]['repo']
        data = full_data[url]['full']
        
        author_info = repo.get('author_info', {})
        readme = data.get('readme', '')
        readme_brief = readme[:300] + '...' if len(readme) > 300 else readme
        
        # 提取关键代码片段
        code_files = data.get('code_files', [])
        key_code = ''
        if code_files:
            main_file = next((cf for cf in code_files if 'main.mbt' in cf.get('path', '')), code_files[0])
            key_code = main_file.get('content', '')[:300] + '...' if len(main_file.get('content', '')) > 300 else main_file.get('content', '')
        
        # 技术信号
        tech_signals = []
        if any('cmd/main' in cf.get('path', '') for cf in code_files):
            tech_signals.append('cmd/main')
        if any('main.mbt' in cf.get('path', '') for cf in code_files):
            tech_signals.append('main.mbt')
        if data.get('moon_mod'):
            tech_signals.append('moon.mod.json')
        
        project_data = {
            'index': i,
            'name': repo['name'],
            'url': url,
            'category': 'Project',
            'author': {
                'username': author_info.get('username', ''),
                'nickname': author_info.get('nickname', ''),
                'profile_url': f"https://github.com/{author_info.get('username', '')}" if author_info.get('username') else '',
                'display': author_info.get('display', '')
            },
            'description': repo.get('description', ''),
            'readme_summary': readme_brief,
            'key_code': key_code,
            'tech_signals': tech_signals,
            'metadata': {
                'stars': repo.get('stars', 0),
                'created_at': repo.get('created_at', ''),
                'topics': repo.get('topics', [])
            }
        }
        data_doc['projects'].append(project_data)
    
    # 自动更新上一周的embed格式（从[+]改为[+-]）
    update_previous_weekly_embed(weekly_num)
    
    # 保存指令文档
    instructions_file = md_file.replace('repos_', 'writing_guide_instructions_')
    with open(instructions_file, 'w', encoding='utf-8') as f:
        f.write(instructions_doc)
    
    # 保存数据文档
    data_file = md_file.replace('repos_', 'writing_guide_data_').replace('.md', '.json')
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data_doc, f, ensure_ascii=False, indent=2)
    
    return instructions_file, data_file, weekly_num

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python generate_writing_guide.py output/repos_weekly15_2025-10-14.md")
        sys.exit(1)
    
    md_file = sys.argv[1]
    instructions_file, data_file, weekly_num = generate_writing_guide(md_file)
    
    print(f"""
{'=' * 60}
写作指引已生成
{'=' * 60}

指令文档: {instructions_file}
数据文档: {data_file}
Weekly {weekly_num}

下一步:
在Cursor里同时发送:

@{instructions_file}
@{data_file}

按照指令要求生成周报条目

{'=' * 60}
""")
