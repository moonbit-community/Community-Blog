#!/usr/bin/env python3
"""
发布前校验脚本（强约束）
检查：
1) 重复 frontmatter/标题模板
2) 条目空行、结尾换行
3) 不可打印字符（如 U+007F）
4) 主文档与子文档路径、索引 embed
5) 空文档格式正确
"""

import sys
import re
from pathlib import Path

def read(p: Path):
    return p.read_text(encoding='utf-8') if p.exists() else ''

def has_dup_frontmatter(text: str) -> bool:
    return len(re.findall(r'^---\n.*?\n---\n', text, re.DOTALL | re.MULTILINE)) > 1

def has_dup_template(text: str) -> bool:
    # 简单检测：同一文件出现两次 title: 行
    return len(re.findall(r'^title:\s', text, re.MULTILINE)) > 1

def has_unprintable(text: str) -> bool:
    # 检测常见不可打印字符（DEL, 控制符），允许常规换行和制表
    return re.search(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', text) is not None

def has_anchor_markers(text: str) -> bool:
    """检查是否包含锚点标记"""
    return bool(re.search(r'<!--\s*(BEGIN|END):?\s*\w*\s*-->', text))

def has_empty_document_format(text: str) -> bool:
    """检查空文档格式是否正确（只有frontmatter）"""
    # 移除frontmatter后应该只有空白
    content_without_frontmatter = re.sub(r'^---\n.*?\n---\n', '', text, flags=re.DOTALL)
    return not content_without_frontmatter.strip()

def has_extra_blank_between_items(text: str) -> bool:
    # 检查列表项之间是否存在空行（- 开头）
    lines = text.splitlines()
    for i in range(len(lines) - 1):
        if lines[i].startswith('- ') and lines[i+1].strip() == '':
            return True
    return False

def ends_with_single_nl(text: str) -> bool:
    return text.endswith('\n') and not text.endswith('\n\n')

def main():
    if len(sys.argv) < 2:
        print('用法: python postcheck.py trees/weekly/weekly15')
        sys.exit(1)
    base = Path(sys.argv[1])
    weekly_num = re.search(r'weekly(\d+)$', base.name)
    if not weekly_num:
        print('❌ 路径应为 trees/weekly/weeklyN')
        sys.exit(1)
    n = weekly_num.group(1)

    # 文件路径
    main_md = base.parent / f'weekly{n}.md'
    pkg = base / 'packages.md'
    proj = base / 'projects.md'
    off = base / 'official.md'
    com = base / 'community.md'
    idx = base.parent / 'index.md'

    problems = []

    # 存在性
    for p in [main_md, pkg, proj, off, com, idx]:
        if not p.exists():
            problems.append(f'缺失文件: {p}')

    # 内容检查
    for p in [pkg, proj, off, com, main_md]:
        t = read(p)
        if has_dup_frontmatter(t):
            problems.append(f'重复 frontmatter: {p}')
        if has_dup_template(t):
            problems.append(f'重复模板块/标题: {p}')
        if has_unprintable(t):
            problems.append(f'包含不可打印字符: {p}')
        if p in [pkg, proj] and has_extra_blank_between_items(t):
            problems.append(f'条目之间存在空行: {p}')
        if not ends_with_single_nl(t):
            problems.append(f'结尾换行不规范（应恰好一个）: {p}')
    # 检查是否包含锚点标记（应该没有）
    for p in [pkg, proj, off, com]:
        t = read(p)
        if has_anchor_markers(t):
            problems.append(f'包含锚点标记: {p}')
    
    # 检查空文档格式（official.md 和 community.md）
    for p, name in [(off, 'official'), (com, 'community')]:
        if p.exists():
            t = read(p)
            if not has_empty_document_format(t):
                problems.append(f'{name}.md 格式错误：应只包含frontmatter，无其他内容')

    # 索引 embed 格式检查
    idx_t = read(idx)
    if f'[+](/weekly/weekly{n}.md#:embed)' not in idx_t:
        problems.append('索引未追加 weeklyN 的 embed 行')
    
    # 检查embed格式是否正确（当前周报应该使用 [+] 格式）
    if f'[+-](/weekly/weekly{n}.md#:embed)' in idx_t:
        problems.append(f'索引embed格式错误：当前周报应使用 [+] 格式，不是 [+-]')
    
    # 检查主文档embed格式
    main_t = read(main_md)
    if '[+-]' in main_t:
        problems.append(f'主文档embed格式错误：应使用 [+] 格式，不是 [+-]')
    
    # 检查子文档标题格式
    for p, expected_title in [(off, '本周官方重要动态'), (com, '本周社区动态')]:
        if p.exists():
            t = read(p)
            if 'title:' in t:
                if expected_title not in t:
                    problems.append(f'{p.name} 标题格式错误：应包含"{expected_title}"')

    if problems:
        print('❌ 检查未通过：')
        for s in problems:
            print('-', s)
        sys.exit(2)
    else:
        print('✅ 检查通过')

if __name__ == '__main__':
    main()


