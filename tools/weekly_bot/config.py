#!/usr/bin/env python3
"""
周报机配置模块
管理API Keys、常量、模型配置等
"""

import os
import sys
from pathlib import Path

# ============ 项目路径 ============

PROJECT_ROOT = Path("../../")
WEEKLY_DIR = PROJECT_ROOT / "trees" / "weekly"
OUTPUT_DIR = Path(__file__).parent / "output"

# 确保目录存在
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ============ API配置 ============

# GitHub Token
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    print("❌ 错误: 未找到 GITHUB_TOKEN")
    print("\n设置方法:")
    print("  export GITHUB_TOKEN='ghp_your_token_here'")
    print("\n获取Token: https://github.com/settings/tokens")
    print("  权限需要: public_repo (或 repo)")
    sys.exit(1)

# 硅基流动 API Key
SILICONFLOW_API_KEY = os.getenv('SILICONFLOW_API_KEY')
if not SILICONFLOW_API_KEY:
    print("❌ 错误: 未找到 SILICONFLOW_API_KEY")
    print("\n设置方法:")
    print("  export SILICONFLOW_API_KEY='sk-your_token_here'")
    print("\n获取Key: https://cloud.siliconflow.cn/account/ak")
    sys.exit(1)

# ============ 硅基流动配置 ============

SILICONFLOW_API_URL = "https://api.siliconflow.cn/v1/chat/completions"
MODEL_NAME = "deepseek-ai/DeepSeek-V3"  # 使用最强的DeepSeek-V3

# API请求参数
TEMPERATURE = 0.1        # 低温度保证分类稳定
MAX_TOKENS = 1500        # DeepSeek-V3输出长度
TOP_P = 0.7             
TOP_K = 50              
STREAM = False           # 不使用流式输出

# ============ 数据抓取配置 ============

# README抓取
README_MAX_CHARS_FOR_AI = 2000      # 喂给AI的README长度
README_MAX_CHARS_FOR_OUTPUT = 500   # 输出展示的README长度

# 代码抓取
MBT_FILE_MAX_CHARS = 300            # 单个.mbt文件抓取长度
MAX_MBT_FILES = 10                  # 最多抓取的.mbt文件数

# ============ 并发与AI配置 ============

MAX_CONCURRENCY = 6  # 最大并发数
AI_TIMEOUT = 60      # AI请求超时（秒）
AI_RETRIES = 2       # AI请求重试次数

# ============ GitHub GraphQL配置 ============

GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

# 搜索策略
SEARCH_QUERIES = [
    "moonbit",           # 关键词搜索
    "language:moonbit"   # 语言过滤
]

# ============ 输出配置 ============

# 文件命名格式
OUTPUT_FILENAME_FORMAT = "repos_weekly{weekly_num}_{date}.md"

# ============ 成本配置 ============

# DeepSeek-V3价格（估算）
PRICE_INPUT_PER_1K = 0.001   # ¥0.001/1K tokens
PRICE_OUTPUT_PER_1K = 0.002  # ¥0.002/1K tokens

# ============ 工具函数 ============

def get_weekly_number():
    """获取当前周报编号（从最新周报中提取）"""
    import re
    
    weekly_files = list(WEEKLY_DIR.glob("weekly*.md"))
    if not weekly_files:
        return 1
    
    # 按数字排序，取最大值
    latest = max(weekly_files, 
                 key=lambda p: int(re.search(r'\d+', p.stem).group()))
    
    current_num = int(re.search(r'\d+', latest.stem).group())
    return current_num + 1  # 下一期周报编号

def estimate_cost(input_tokens, output_tokens):
    """估算API成本"""
    input_cost = (input_tokens / 1000) * PRICE_INPUT_PER_1K
    output_cost = (output_tokens / 1000) * PRICE_OUTPUT_PER_1K
    return input_cost + output_cost

# ============ 配置验证 ============

def validate_config():
    """验证配置是否正确"""
    checks = []
    
    # 检查API Keys
    checks.append(("GITHUB_TOKEN", bool(GITHUB_TOKEN)))
    checks.append(("SILICONFLOW_API_KEY", bool(SILICONFLOW_API_KEY)))
    
    # 检查目录
    checks.append(("WEEKLY_DIR", WEEKLY_DIR.exists()))
    checks.append(("OUTPUT_DIR", OUTPUT_DIR.exists()))
    
    all_ok = all(check[1] for check in checks)
    
    if not all_ok:
        print("\n⚠️ 配置检查失败:")
        for name, status in checks:
            symbol = "✅" if status else "❌"
            print(f"  {symbol} {name}")
    
    return all_ok

if __name__ == "__main__":
    print("配置检查:")
    print("=" * 50)
    validate_config()
    print(f"\n模型: {MODEL_NAME}")
    print(f"批量大小: {BATCH_SIZE}")
    print(f"周报目录: {WEEKLY_DIR}")
    print(f"输出目录: {OUTPUT_DIR}")
    print(f"下一期周报: weekly{get_weekly_number()}")

