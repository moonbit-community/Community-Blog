import os
import json
import requests
from pathlib import Path
from typing import Dict, List, Optional
import logging
from tenacity import retry, stop_after_attempt, wait_exponential
import hashlib

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TranslationError(Exception):
    """翻译失败的自定义异常"""
    pass

class MarkdownTranslator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.siliconflow.cn/v1/chat/completions"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })
        self.glossary = self.load_glossary()
        self.cache_dir = Path(".translation_cache")
        self.cache_dir.mkdir(exist_ok=True)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def translate_text(self, text: str, file_path: str) -> str:
        """使用技术内容保留进行翻译"""
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
                        "你是一位专业的技术文档翻译助手。\n"
                        "规则:\n"
                        "1. 完全保留所有 Markdown 格式\n"
                        "2. 绝不修改代码块或行内代码\n"
                        "3. 保留 URL 和 YAML front matter 不变\n"
                        f"4. 使用以下术语表:\n{self.format_glossary()}\n"
                        "5. 保持技术术语一致\n"
                        f"6. 正在翻译的文件路径：{file_path}"
                    )
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            "temperature": 0.3,
            "max_tokens": 4000,
            "top_p": 0.9
        }

        try:
            response = self.session.post(
                self.base_url,
                json=payload,
                timeout=60  # 增加超时时间
            )
            response.raise_for_status()
            result = response.json()['choices'][0]['message']['content']
            
            # 保存缓存
            try:
                with open(cache_file, 'w', encoding='utf-8') as f:
                    f.write(result)
            except Exception as e:
                logger.warning(f"Cache write failed: {str(e)}")
                
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API 请求失败：{str(e)}")
            raise TranslationError("翻译服务不可用")
        except Exception as e:
            logger.error(f"意外错误：{str(e)}")
            raise TranslationError("处理翻译失败")

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
            return "（空术语表）"
        return "\n".join(f"{k} → {v}" for k, v in self.glossary.items())

    def translate_file(self, input_path: str, output_path: str) -> bool:
        """处理单个文件，使用原子写入"""
        # 确保 rel_path 始终有值
        rel_path = input_path  # 默认值
        
        try:
            input_file = Path(input_path)
            # 使用更健壮的路径处理方法
            try:
                # 尝试获取相对于源目录的路径
                source_path = Path.cwd() / "trees"
                rel_path = input_file.relative_to(source_path)
            except ValueError:
                # 如果失败，尝试获取相对于当前工作目录的路径
                try:
                    rel_path = input_file.relative_to(Path.cwd())
                except ValueError:
                    # 如果都失败，使用绝对路径
                    rel_path = input_file.absolute()
            
            # 读取文件，明确处理编码
            with open(input_path, 'r', encoding='utf-8', newline='') as f:
                content = f.read()

            if not content.strip():
                logger.warning(f"跳过空文件：{rel_path}")
                return False

            # 创建输出目录结构
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # 修复：直接使用输出路径字符串，避免相对路径计算
            logger.info(f"Translating {rel_path} → {output_path}")
            
            # 原子写入模式
            temp_path = output_file.with_suffix('.tmp')
            translated = self.translate_text(content, str(rel_path))
            
            with open(temp_path, 'w', encoding='utf-8', newline='') as f:
                f.write(translated)
            
            # 成功后原子重命名
            temp_path.replace(output_file)
            return True

        except TranslationError as e:
            logger.error(f"翻译失败 {rel_path}: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"处理 {rel_path} 失败：{str(e)}", exc_info=True)
            return False

    def batch_translate(self, 
                      input_dir: str, 
                      output_dir: str, 
                      specific_files: Optional[List[str]] = None) -> Dict[str, int]:
        """
        批量翻译，保留目录结构
        
        参数：
            input_dir: 源目录路径
            output_dir: 目标目录路径
            specific_files: 要处理的相对路径的可选列表
            
        返回：
            包含成功/失败计数的字典
        """
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        
        # 解析文件列表
        if specific_files:
            md_files = [input_path / f for f in specific_files]
        else:
            md_files = list(input_path.rglob('*.md'))
        
        logger.info(f"Found {len(md_files)} files for translation")
        
        stats = {'success': 0, 'failed': 0}
        for md_file in md_files:
            # 维护相对路径结构
            rel_path = md_file.relative_to(input_path)
            output_file = output_path / rel_path
            
            if self.translate_file(str(md_file), str(output_file)):
                stats['success'] += 1
            else:
                stats['failed'] += 1
        
        logger.info(f"翻译完成：✅ {stats['success']} 个成功，❌ {stats['failed']} 个失败")
        return stats