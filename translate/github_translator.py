#!/usr/bin/env python3
import argparse
import os
import sys
import json
from pathlib import Path
from typing import List, Dict
from translator import MarkdownTranslator
from github import Github
from git import Repo
import logging

sys.path.append(str(Path(__file__).parent.resolve()))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TranslationBot:
    def __init__(self):
        self.args = self.parse_args()
        self.api_key = os.getenv("API_KEY")
        if not self.api_key:
            logger.error("Missing API_KEY environment variable")
            sys.exit(1)
        self.translator = MarkdownTranslator(self.api_key)
        self.run_id = os.getenv("GITHUB_RUN_ID", "manual-run")
        
        # 初始化 Git 仓库
        try:
            self.repo = Repo(".")
            logger.info(f"Initialized Git repo at {self.repo.working_dir}")
        except Exception as e:
            logger.error(f"Failed to initialize Git repo: {str(e)}")
            if self.args.dry_run:
                logger.warning("Continuing in dry-run mode without Git")
            else:
                sys.exit(1)

    def parse_args(self):
        parser = argparse.ArgumentParser(description='Automated Markdown Translation Bot')
        parser.add_argument("--source-dir", default="trees", help="Source directory with Chinese markdown")
        parser.add_argument("--target-dir", default="tree_en", help="Target directory for English translations")
        parser.add_argument("--pr-reviewers", default="", help="Comma-separated GitHub reviewers")
        parser.add_argument("--dry-run", action="store_true", help="Run without pushing changes")
        return parser.parse_args()

    def run(self):
        try:
            logger.info(f"Starting translation run {self.run_id}")
            
            # 阶段 1：检测和验证变更
            changed_files = self.get_changed_files()
            if not changed_files:
                logger.info("No changed Markdown files detected")
                return
            
            # 阶段 2：执行翻译
            stats = self.execute_translation(changed_files)
            
            # 阶段 3：提交和创建 PR
            if self.args.dry_run:
                logger.info("⚠️ Dry run mode activated. No changes will be committed.")
                logger.info(f"Would create PR for {len(changed_files)} files")
            else:
                self.create_versioned_pr(changed_files, stats)
            
            logger.info(f"Translation completed successfully")
            
        except Exception as e:
            logger.error(f"Translation pipeline failed: {str(e)}", exc_info=True)
            sys.exit(1)

    def get_changed_files(self) -> List[str]:
        """识别已修改/添加的 markdown 文件"""
        changed = []
        source_path = Path(self.args.source_dir).absolute()
        
        try:
            # 方法 1: 使用 GitPython 的 diff
            try:
                # 获取当前 HEAD 与上一次提交的差异
                if self.repo.head.is_valid() and len(self.repo.head.commit.parents) > 0:
                    diff = self.repo.head.commit.parents[0].diff(self.repo.head.commit)
                    for diff_item in diff:
                        if diff_item.change_type in ('A', 'M') and diff_item.a_path.endswith('.md'):
                            abs_path = (Path(self.repo.working_dir) / diff_item.a_path).absolute()
                            try:
                                rel_path = abs_path.relative_to(source_path)
                                if not str(rel_path).startswith('..'):
                                    changed.append(str(abs_path))
                            except ValueError:
                                continue
            except Exception as e:
                logger.warning(f"GitPython diff failed: {str(e)}")
            
            # 方法 2: 如果方法 1 失败，使用环境变量
            if not changed:
                logger.info("Trying alternative method using GitHub event payload")
                event_path = os.getenv("GITHUB_EVENT_PATH")
                if event_path and Path(event_path).exists():
                    with open(event_path, 'r') as f:
                        event_data = json.load(f)
                    
                    # 获取提交中修改的文件
                    for commit in event_data.get('commits', []):
                        for file_path in commit.get('modified', []) + commit.get('added', []):
                            if file_path.endswith('.md') and file_path.startswith(self.args.source_dir):
                                abs_path = (Path(self.repo.working_dir) / file_path).absolute()
                                changed.append(str(abs_path))
            
            # 方法 3: 作为最后手段，处理所有文件
            if not changed:
                logger.warning("No changes detected, processing all files")
                for file_path in Path(self.args.source_dir).rglob('*.md'):
                    changed.append(str(file_path.absolute()))
            
        except Exception as e:
            logger.error(f"Failed to detect changed files: {str(e)}")
        
        if changed:
            logger.info(f"Detected {len(changed)} changed files")
            # 使用绝对路径的源目录来计算相对路径
            source_abs = Path(self.args.source_dir).absolute()
            sample_files = "\n".join([f"  - {Path(f).relative_to(source_abs)}" for f in changed[:3]])
            if len(changed) > 3:
                sample_files += f"\n  - ...(+{len(changed)-3} more)"
            logger.info(f"Changed files:\n{sample_files}")
        else:
            logger.warning("No valid markdown changes detected")
        return changed

    def execute_translation(self, files: List[str]) -> Dict[str, int]:
        """使用结构保留执行批量翻译"""
        # 确保输出目录存在
        output_dir = Path(self.args.target_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 获取相对路径用于处理 - 使用绝对路径的源目录
        source_abs = Path(self.args.source_dir).absolute()
        rel_files = [str(Path(f).relative_to(source_abs)) for f in files]
        
        logger.info(f"Starting translation of {len(files)} files to {output_dir}...")
        logger.info(f"Files to translate: {rel_files[:3]}... (total: {len(rel_files)})")
        
        # 调用翻译器
        stats = self.translator.batch_translate(
            input_dir=self.args.source_dir,
            output_dir=self.args.target_dir,
            specific_files=rel_files
        )
        
        if stats['success'] == 0:
            raise Exception("All translations failed")
            
        logger.info(f"Translation results: ✅ {stats['success']} succeeded, ❌ {stats['failed']} failed")
        return stats

    def create_versioned_pr(self, changed_files: List[str], stats: Dict[str, int]):
        """提交变更并创建带版本的 PR"""
        # 配置 Git 身份
        self.repo.git.config("user.name", "Translation Bot")
        self.repo.git.config("user.email", "translation-bot@users.noreply.github.com")
        
        # 创建带版本的 branch
        branch_name = f"translation-{self.run_id}"
        logger.info(f"Creating branch {branch_name}")
        
        # 添加所有更改
        self.repo.git.add(A=True)
        
        # 创建提交
        commit_msg = f"""feat(translation): batch update {self.run_id}

Files processed:
- Success: {stats['success']}
- Failed: {stats['failed']}
"""
        self.repo.index.commit(commit_msg)
        logger.info("Changes committed")
        
        # 推送到 branch
        origin = self.repo.remote(name='origin')
        origin.push(refspec=f"HEAD:{branch_name}", force=True)
        logger.info(f"Pushed to {branch_name}")
        
        # 创建 PR
        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            raise Exception("Missing GITHUB_TOKEN")
            
        g = Github(github_token)
        repo_name = os.getenv("GITHUB_REPOSITORY")
        if not repo_name:
            raise Exception("Missing GITHUB_REPOSITORY")
            
        repo = g.get_repo(repo_name)
        
        pr_title = f"[Bot] Translation Updates ({self.run_id})"
        pr_body = self.generate_pr_body(changed_files, stats)
        
        # 创建 PR（不使用 labels 参数）
        pr = repo.create_pull(
            title=pr_title,
            body=pr_body,
            head=branch_name,
            base="main"
        )
        
        # 单独添加标签
        pr.add_to_labels("translation", "needs-review")
        
        # 设置审阅者
        if self.args.pr_reviewers:
            reviewers = [r.strip() for r in self.args.pr_reviewers.split(",") if r.strip()]
            logger.info(f"Adding reviewers: {', '.join(reviewers)}")
            pr.create_review_request(reviewers=reviewers)
        
        logger.info(f"Created PR #{pr.number}: {pr.html_url}")

    def generate_pr_body(self, files: List[str], stats: Dict[str, int]) -> str:
        """生成完整的 PR 描述"""
        # 使用绝对路径的源目录来计算相对路径
        source_abs = Path(self.args.source_dir).absolute()
        sample_files = "\n".join(f"- `{Path(f).relative_to(source_abs)}`" for f in files[:5])
        if len(files) > 5:
            sample_files += f"\n- ...(+{len(files)-5} more files)"
        
        return f"""
## Translation Report (Run {self.run_id})

### Statistics
✅ Successfully translated: **{stats['success']} files**  
❌ Failed translations: **{stats['failed']} files**

### Changed Files
{sample_files}

### Verification Checklist
1. [ ] Markdown formatting preserved
2. [ ] Code blocks unchanged
3. [ ] Technical terms accurate
4. [ ] URLs functional

### Output Structure
> Automatically generated by translation pipeline
"""

    def get_directory_tree(self, path: Path, max_depth: int = 3) -> str:
        """获取目录结构文本表示"""
        try:
            lines = []
            prefix = ""
            
            for entry in path.iterdir():
                if entry.is_dir():
                    lines.append(f"{prefix}├── {entry.name}/")
                    self.walk_directory(entry, lines, prefix + "│   ", max_depth-1)
                else:
                    lines.append(f"{prefix}├── {entry.name}")
            
            return "\n".join(lines)
        except Exception as e:
            logger.warning(f"Failed to generate tree: {str(e)}")
            return "Could not generate directory tree"
    
    def walk_directory(self, path: Path, lines: list, prefix: str, depth: int):
        if depth <= 0:
            return
            
        entries = list(path.iterdir())
        for i, entry in enumerate(entries):
            is_last = i == len(entries) - 1
            new_prefix = prefix + ("    " if is_last else "│   ")
            
            if entry.is_dir():
                lines.append(f"{prefix}{'└──' if is_last else '├──'} {entry.name}/")
                if depth > 1:
                    self.walk_directory(entry, lines, new_prefix, depth-1)
            else:
                lines.append(f"{prefix}{'└──' if is_last else '├──'} {entry.name}")

if __name__ == "__main__":
    try:
        TranslationBot().run()
    except Exception as e:
        logger.error(f"Fatal error in translation bot: {str(e)}", exc_info=True)
        sys.exit(1)