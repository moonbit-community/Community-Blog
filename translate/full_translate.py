#!/usr/bin/env python3
import sys
import argparse
import logging
import time
import asyncio
import aiohttp
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AsyncTranslationError(Exception):
    """异步翻译失败的自定义异常"""
    pass

class AsyncMarkdownTranslator:
    def __init__(self, api_key: str, max_concurrent: int = 20):
        self.api_key = api_key
        self.base_url = "https://api.siliconflow.cn/v1/chat/completions"
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.glossary = self.load_glossary()
        self.cache_dir = Path(".translation_cache")
        self.cache_dir.mkdir(exist_ok=True)

    @retry(
        stop=stop_after_attempt(10), 
        wait=wait_exponential(multiplier=2, min=5, max=120),
        reraise=True,
        retry=retry_if_exception_type((aiohttp.ClientError, asyncio.TimeoutError, TimeoutError))
    )
    async def translate_text_async(self, session: aiohttp.ClientSession, text: str, file_path: str) -> str:
        """异步翻译文本"""
        # 检查缓存
        cache_key = hashlib.md5(text.encode('utf-8')).hexdigest()
        cache_file = self.cache_dir / f"{cache_key}.cache"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                logger.warning(f"Cache read failed: {str(e)}")
        
        payload = {
            "model": "Pro/deepseek-ai/DeepSeek-R1",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "你是一位专业的计算机科学和技术文档翻译专家，专门负责将中文技术文档翻译成英文。\n\n"
                        "翻译任务：将以下中文 Markdown 文档翻译成英文，保持技术准确性和可读性。\n\n"
                        "核心要求：\n"
                        "1. 目标语言：英语（美式英语）\n"
                        "2. 完全保留所有 Markdown 格式、语法和结构\n"
                        "3. 绝不修改任何代码块（```...```）或行内代码（`...`）\n"
                        "4. 保留所有 URL、链接和 YAML front matter 完全不变\n"
                        "5. 保持技术术语的一致性和准确性\n"
                        "6. 使用专业、清晰、自然的英文表达\n"
                        "7. 保持原文的逻辑结构和段落组织\n"
                        "8. 对于数学公式、算法描述等保持精确性\n"
                        "9. 请检查翻译内容的头尾是否符合原文件的格式\n\n"
                        f"技术术语表（必须遵循）：\n{self.format_glossary()}\n\n"
                        f"当前翻译文件：{file_path}\n\n"
                        "请直接输出翻译后的英文内容，不要添加任何解释或注释。"
                    )
                },
                {
                    "role": "user",
                    "content": f"请将以下中文技术文档翻译成英文：\n\n{text}"
                }
            ],
            "temperature": 0.2,
            "max_tokens": 4000,
            "top_p": 0.9
        }

        async with self.semaphore:  # 限制并发数
            try:
                async with session.post(
                    self.base_url,
                    json=payload,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    timeout=aiohttp.ClientTimeout(total=180, connect=30)
                ) as response:
                    response.raise_for_status()
                    result = await response.json()
                    translated_text = result['choices'][0]['message']['content']
                    
                    # 保存缓存
                    try:
                        with open(cache_file, 'w', encoding='utf-8') as f:
                            f.write(translated_text)
                    except Exception as e:
                        logger.warning(f"Cache write failed: {str(e)}")
                    
                    return translated_text
                    
            except aiohttp.ClientError as e:
                logger.error(f"API 请求失败：{str(e)}")
                raise AsyncTranslationError(f"翻译服务不可用： {str(e)}")
            except asyncio.TimeoutError as e:
                logger.error(f"请求超时：{str(e)}")
                raise AsyncTranslationError(f"请求超时： {str(e)}")
            except Exception as e:
                logger.error(f"意外错误：{str(e)}", exc_info=True)
                raise AsyncTranslationError(f"处理翻译失败： {str(e)}")

    def load_glossary(self) -> Dict[str, str]:
        """加载技术术语表"""
        glossary_paths = [
            Path("translate/glossary.json"),
            Path("./glossary.json")
        ]
        
        for glossary_path in glossary_paths:
            if glossary_path.exists():
                try:
                    with open(glossary_path, 'r', encoding='utf-8') as f:
                        logger.info(f"Loaded glossary from {glossary_path}")
                        return json.load(f)
                except Exception as e:
                    logger.warning(f"术语表加载失败 ({glossary_path}): {str(e)}")
        
        logger.warning("No glossary found, using empty glossary")
        return {}

    def format_glossary(self) -> str:
        """为 API 提示格式化术语表"""
        if not self.glossary:
            return "（无特定术语表，请使用标准计算机科学术语）"
        
        formatted_terms = []
        for chinese, english in self.glossary.items():
            formatted_terms.append(f"  • {chinese} → {english}")
        
        return "术语对照表：\n" + "\n".join(formatted_terms)

    async def translate_file_async(self, session: aiohttp.ClientSession, input_path: str, output_path: str) -> Tuple[str, bool]:
        """异步处理单个文件"""
        rel_path = input_path  # 默认值
        
        try:
            input_file = Path(input_path)
            # 获取相对路径
            try:
                source_path = Path.cwd() / "trees"
                rel_path = input_file.relative_to(source_path)
            except ValueError:
                try:
                    rel_path = input_file.relative_to(Path.cwd())
                except ValueError:
                    rel_path = input_file.absolute()
            
            # 读取文件
            with open(input_path, 'r', encoding='utf-8', newline='') as f:
                content = f.read()

            if not content.strip():
                logger.warning(f"跳过空文件：{rel_path}")
                return (str(rel_path), False)

            # 创建输出目录
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"开始翻译：{rel_path}")
            
            # 异步翻译
            translated = await self.translate_text_async(session, content, str(rel_path))
            
            # 原子写入
            temp_path = output_file.with_suffix('.tmp')
            with open(temp_path, 'w', encoding='utf-8', newline='') as f:
                f.write(translated)
            
            temp_path.replace(output_file)
            return (str(rel_path), True)

        except AsyncTranslationError as e:
            logger.error(f"翻译失败 {rel_path}: {str(e)}", exc_info=True)
            return (str(rel_path), False)
        except Exception as e:
            logger.error(f"处理 {rel_path} 失败：{str(e)}", exc_info=True)
            return (str(rel_path), False)

    async def batch_translate_async(self, 
                                  input_dir: str, 
                                  output_dir: str, 
                                  specific_files: Optional[List[str]] = None,
                                  max_retries: int = 5) -> Dict[str, int]:
        """异步批量翻译，支持失败重试"""
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        
        # 获取文件列表
        if specific_files:
            md_files = [input_path / f for f in specific_files]
        else:
            md_files = list(input_path.rglob('*.md'))
        
        logger.info(f"找到 {len(md_files)} 个文件进行翻译")
        logger.info(f"最大并发数：{self.max_concurrent}")
        logger.info(f"最大重试次数：{max_retries}")
        
        # 准备翻译任务
        translation_tasks = []
        for md_file in md_files:
            rel_path = md_file.relative_to(input_path)
            output_file = output_path / rel_path
            translation_tasks.append((str(md_file), str(output_file)))
        
        stats = {'success': 0, 'failed': 0, 'retries': 0}
        failed_files = translation_tasks.copy()  # 初始所有文件都标记为需要处理
        successful_files = []
        
        start_time = time.time()
        
        # 创建 HTTP 会话
        connector = aiohttp.TCPConnector(limit=0, limit_per_host=0)  # 无限制连接
        timeout = aiohttp.ClientTimeout(total=600)  # 10 分钟超时
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            retry_count = 0
            
            while failed_files and retry_count < max_retries:
                if retry_count > 0:
                    logger.info(f"第 {retry_count} 次重试，剩余 {len(failed_files)} 个失败文件")
                    # 重试间隔
                    await asyncio.sleep(5)
                
                current_batch = failed_files.copy()
                failed_files.clear()
                
                # 创建当前批次的翻译任务
                tasks = [
                    self.translate_file_async(session, input_file, output_file)
                    for input_file, output_file in current_batch
                ]
                
                # 并发执行当前批次任务
                logger.info(f"开始翻译 {len(tasks)} 个文件...")
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # 处理结果
                for i, result in enumerate(results):
                    input_file, output_file = current_batch[i]
                    rel_path = Path(input_file).relative_to(input_path)
                    
                    if isinstance(result, Exception):
                        logger.error(f"任务异常 {rel_path}：{str(result)}", exc_info=True)
                        failed_files.append((input_file, output_file))
                        stats['retries'] += 1
                    else:
                        rel_path_str, success = result
                        if success:
                            stats['success'] += 1
                            successful_files.append((input_file, output_file))
                            logger.info(f"✅ 翻译成功：{rel_path}")
                        else:
                            failed_files.append((input_file, output_file))
                            stats['retries'] += 1
                            logger.error(f"❌ 翻译失败：{rel_path}")
                
                retry_count += 1
                
                # 如果还有失败文件，输出进度
                if failed_files:
                    logger.warning(f"第 {retry_count} 轮完成，还有 {len(failed_files)} 个文件失败")
                else:
                    logger.info(f"所有文件翻译成功！")
                    break
        
        # 最终统计
        stats['failed'] = len(failed_files)
        elapsed_time = time.time() - start_time
        
        # 输出最终统计
        logger.info(f"翻译完成：✅ {stats['success']} 个成功，❌ {stats['failed']} 个失败")
        logger.info(f"总重试次数：{stats['retries']}")
        logger.info(f"总耗时：{elapsed_time:.2f} 秒")
        if elapsed_time > 0:
            logger.info(f"平均速度：{stats['success']/elapsed_time:.2f} 文件/秒")
        
        # 如果还有失败文件，输出详细信息
        if failed_files:
            logger.error("最终失败的文件：")
            for input_file, output_file in failed_files:
                rel_path = Path(input_file).relative_to(input_path)
                logger.error(f"  - {rel_path}")
        
        return stats

async def full_translate(source_dir: str, target_dir: str, api_key: str, max_concurrent: int = 20, max_retries: int = 5):
    """异步全量翻译"""
    # 确保目录存在
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    
    if not source_path.exists():
        logger.error(f"源目录不存在：{source_dir}")
        return
    
    # 创建目标目录
    target_path.mkdir(parents=True, exist_ok=True)
    
    # 初始化异步翻译器
    translator = AsyncMarkdownTranslator(api_key, max_concurrent)
    
    # 执行异步批量翻译
    stats = await translator.batch_translate_async(
        input_dir=source_dir,
        output_dir=target_dir,
        max_retries=max_retries
    )
    
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
    parser = argparse.ArgumentParser(description='全量翻译 Markdown 文件（高并发异步版本）')
    parser.add_argument("--source-dir", default="trees", help="源目录路径 (默认：trees)")
    parser.add_argument("--target-dir", default="tree_en", help="目标目录路径 (默认：tree_en)")
    parser.add_argument("--api-key", required=True, help="翻译 API 密钥")
    parser.add_argument("--max-concurrent", type=int, default=20, help="最大并发请求数 (默认：20)")
    parser.add_argument("--max-retries", type=int, default=5, help="最大重试次数 (默认：5)")
    
    args = parser.parse_args()
    
    try:
        logger.info("开始全量翻译（高并发异步版本）...")
        logger.info(f"源目录：{args.source_dir}")
        logger.info(f"目标目录：{args.target_dir}")
        logger.info(f"最大并发数：{args.max_concurrent}")
        logger.info(f"最大重试次数：{args.max_retries}")
        
        # 运行翻译
        asyncio.run(full_translate(
            source_dir=args.source_dir,
            target_dir=args.target_dir,
            api_key=args.api_key,
            max_concurrent=args.max_concurrent,
            max_retries=args.max_retries
        ))
        
        logger.info("全量翻译完成")
    except Exception as e:
        logger.error(f"全量翻译失败：{str(e)}", exc_info=True)
        sys.exit(1)
