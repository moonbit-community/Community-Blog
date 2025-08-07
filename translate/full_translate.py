#!/usr/bin/env python3
import os
import sys
import json
import argparse
import logging
from pathlib import Path
from typing import Dict, List
from translator import MarkdownTranslator

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def full_translate(source_dir: str, target_dir: str, api_key: str):
    """
    全量翻译指定目录中的所有 Markdown 文件
    
    参数：
        source_dir: 源目录路径
        target_dir: 目标目录路径
        api_key: 翻译 API 密钥
    """
    # 确保目录存在
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    
    if not source_path.exists():
        logger.error(f"源目录不存在：{source_dir}")
        return
    
    # 创建目标目录
    target_path.mkdir(parents=True, exist_ok=True)
    
    # 初始化翻译器
    translator = MarkdownTranslator(api_key)
    
    # 获取所有 Markdown 文件
    md_files = list(source_path.rglob('*.md'))
    
    if not md_files:
        logger.warning(f"在 {source_dir} 中没有找到 Markdown 文件")
        return
    
    logger.info(f"找到 {len(md_files)} 个 Markdown 文件进行翻译")
    
    # 执行全量翻译
    stats = translator.batch_translate(
        input_dir=source_dir,
        output_dir=target_dir
    )
    
    # 输出结果统计
    logger.info(f"翻译完成：✅ {stats['success']} 个成功，❌ {stats['failed']} 个失败")
    
    # 生成目录结构报告
    tree_report = generate_directory_tree(target_path)
    logger.info(f"输出目录结构：\n{tree_report}")

def generate_directory_tree(path: Path, max_depth: int = 3) -> str:
    """生成目录结构文本表示"""
    try:
        lines = []
        prefix = ""
        
        for entry in path.iterdir():
            if entry.is_dir():
                lines.append(f"{prefix}├── {entry.name}/")
                walk_directory(entry, lines, prefix + "│   ", max_depth-1)
            else:
                lines.append(f"{prefix}├── {entry.name}")
        
        return "\n".join(lines)
    except Exception as e:
        logger.warning(f"生成目录树失败：{str(e)}")
        return "无法生成目录树"

def walk_directory(path: Path, lines: list, prefix: str, depth: int):
    """递归遍历目录"""
    if depth <= 0:
        return
        
    entries = list(path.iterdir())
    for i, entry in enumerate(entries):
        is_last = i == len(entries) - 1
        new_prefix = prefix + ("    " if is_last else "│   ")
        
        if entry.is_dir():
            lines.append(f"{prefix}{'└──' if is_last else '├──'} {entry.name}/")
            if depth > 1:
                walk_directory(entry, lines, new_prefix, depth-1)
        else:
            lines.append(f"{prefix}{'└──' if is_last else '├──'} {entry.name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='全量翻译 Markdown 文件')
    parser.add_argument("--source-dir", default="trees", help="源目录路径 (默认：trees)")
    parser.add_argument("--target-dir", default="tree_en", help="目标目录路径 (默认：tree_en)")
    parser.add_argument("--api-key", required=True, help="翻译 API 密钥")
    
    args = parser.parse_args()
    
    try:
        logger.info("开始全量翻译...")
        logger.info(f"源目录：{args.source_dir}")
        logger.info(f"目标目录：{args.target_dir}")
        
        full_translate(
            source_dir=args.source_dir,
            target_dir=args.target_dir,
            api_key=args.api_key
        )
        
        logger.info("全量翻译完成")
    except Exception as e:
        logger.error(f"全量翻译失败：{str(e)}", exc_info=True)
        sys.exit(1)