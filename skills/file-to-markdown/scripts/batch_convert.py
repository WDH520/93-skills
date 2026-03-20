#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "markitdown[all]",
#     "docling",
#     "pymupdf4llm",
# ]
# ///
# -*- coding: utf-8 -*-
"""
批量转换目录中的文件为 Markdown。

遍历指定目录，查找所有支持的文件格式，并调用 convert 模块进行转换。
支持多线程并发转换、增量转换（跳过已存在且较新的文件）以及保持目录结构。

使用方式:
  uv run batch_convert.py /path/to/docs/ -o /path/to/output/
  uv run batch_convert.py /path/to/docs/ --extensions .pdf .docx --workers 4
"""

import argparse
import logging
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Set

# 导入 convert 模块中的核心功能
from convert import ConversionResult, FORMAT_TOOL_PRIORITY, convert_file

# 配置日志
logger = logging.getLogger(__name__)

# 所有支持的扩展名集合
SUPPORTED_EXTENSIONS: Set[str] = set(FORMAT_TOOL_PRIORITY.keys())


@dataclass
class BatchResult:
    """批量转换结果摘要。"""

    total: int
    succeeded: int
    failed: int
    skipped: int
    results: List[ConversionResult]
    elapsed_seconds: float


def scan_directory(
    dir_path: str, recursive: bool = True, extensions: Optional[Set[str]] = None
) -> List[str]:
    """
    扫描目录，查找符合条件的文件。

    参数:
        dir_path: 目录路径
        recursive: 是否递归扫描子目录
        extensions: 过滤的扩展名集合（不指定则使用所有支持的格式）

    返回:
        排序后的绝对路径列表
    """
    base_dir = Path(dir_path).resolve()
    if not base_dir.is_dir():
        logger.error(f"路径不是目录: {dir_path}")
        return []

    target_exts = extensions if extensions else SUPPORTED_EXTENSIONS
    # 统一转换为带点的后缀且小写
    target_exts = {ext if ext.startswith(".") else f".{ext}" for ext in target_exts}
    target_exts = {ext.lower() for ext in target_exts}

    found_files: List[Path] = []

    # 使用 Path.rglob 或 glob
    pattern = "**/*" if recursive else "*"
    for path in base_dir.glob(pattern):
        # 跳过隐藏文件/目录（以 . 开头）
        if any(part.startswith(".") for part in path.relative_to(base_dir).parts):
            continue

        if path.is_file() and path.suffix.lower() in target_exts:
            found_files.append(path)

    # 排序：先按扩展名排序，再按文件名排序
    found_files.sort(key=lambda x: (x.suffix.lower(), x.name.lower()))

    return [str(f.resolve()) for f in found_files]


def batch_convert(
    dir_path: str,
    output_dir: Optional[str] = None,
    recursive: bool = True,
    extensions: Optional[Set[str]] = None,
    preferred_tool: Optional[str] = None,
    skip_existing: bool = True,
    max_workers: int = 1,
) -> BatchResult:
    """
    主批量转换逻辑。
    """
    start_time = time.time()

    # 扫描文件
    files_to_convert = scan_directory(dir_path, recursive, extensions)
    total_files = len(files_to_convert)

    if total_files == 0:
        return BatchResult(0, 0, 0, 0, [], 0.0)

    input_base = Path(dir_path).resolve()
    output_base = Path(output_dir).resolve() if output_dir else None

    results: List[ConversionResult] = []
    succeeded = 0
    failed = 0
    skipped = 0

    def process_single_file(index: int, file_path: str) -> ConversionResult:
        src_path = Path(file_path)

        # 确定输出路径
        if output_base:
            # 保持相对结构
            rel_path = src_path.relative_to(input_base)
            out_md_path = output_base / rel_path.with_suffix(".md")
        else:
            # 同级目录
            out_md_path = src_path.with_suffix(".md")

        # 检查是否跳过
        if skip_existing and out_md_path.exists():
            # 如果输出文件比源文件新，则跳过
            if out_md_path.stat().st_mtime > src_path.stat().st_mtime:
                return ConversionResult(
                    success=True,
                    content="",
                    tool_used="skip",
                    file_path=file_path,
                    output_path=str(out_md_path),
                    elapsed_seconds=0.0,
                )

        print(
            f"[{index + 1}/{total_files}] 转换中: {os.path.relpath(file_path, dir_path)} ..."
        )

        return convert_file(
            file_path=file_path,
            output_path=str(out_md_path),
            preferred_tool=preferred_tool,
        )

    # 执行转换
    if max_workers > 1:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_file = {
                executor.submit(process_single_file, i, f): f
                for i, f in enumerate(files_to_convert)
            }
            try:
                for future in as_completed(future_to_file):
                    res = future.result()
                    results.append(res)
                    if res.tool_used == "skip":
                        skipped += 1
                    elif res.success:
                        succeeded += 1
                    else:
                        failed += 1
            except KeyboardInterrupt:
                executor.shutdown(wait=False, cancel_futures=True)
                raise
    else:
        for i, f in enumerate(files_to_convert):
            try:
                res = process_single_file(i, f)
                results.append(res)
                if res.tool_used == "skip":
                    skipped += 1
                elif res.success:
                    succeeded += 1
                else:
                    failed += 1
            except KeyboardInterrupt:
                print("\n用户中断转换任务。")
                break

    elapsed = time.time() - start_time
    return BatchResult(
        total=total_files,
        succeeded=succeeded,
        failed=failed,
        skipped=skipped,
        results=results,
        elapsed_seconds=elapsed,
    )


def print_summary(result: BatchResult):
    """打印转换结果摘要。"""
    print("\n" + "=" * 50)
    print("批量转换总结")
    print("-" * 50)
    print(f"总文件数:    {result.total}")
    print(f"成功:        {result.succeeded}")
    print(f"失败:        {result.failed}")
    print(f"跳过:        {result.skipped}")
    print(f"总耗时:      {result.elapsed_seconds:.2f} 秒")
    print("=" * 50)

    if result.failed > 0:
        print("\n失败详情:")
        for res in result.results:
            if not res.success and res.tool_used != "skip":
                print(f"  - {os.path.basename(res.file_path)}: {res.error}")
        print("-" * 50)


def main():
    parser = argparse.ArgumentParser(description="批量将目录中的文件转换为 Markdown")
    parser.add_argument("directory", help="待扫描的目录路径")
    parser.add_argument("-o", "--output-dir", help="输出根目录（可选）")
    parser.add_argument(
        "--no-recursive",
        action="store_false",
        dest="recursive",
        help="不递归扫描子目录",
    )
    parser.add_argument(
        "--extensions", nargs="+", help="限制转换的扩展名 (例如 .pdf .docx)"
    )
    parser.add_argument("--tool", help="优先使用的转换工具")
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        default=True,
        help="跳过已存在且较新的输出文件 (默认开启)",
    )
    parser.add_argument(
        "--no-skip",
        action="store_false",
        dest="skip_existing",
        help="不跳过已存在的文件",
    )
    parser.add_argument(
        "--workers", type=int, default=1, help="并行工作线程数 (默认 1)"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="显示调试日志")

    args = parser.parse_args()

    # 配置日志
    log_level = logging.DEBUG if args.verbose else logging.WARNING
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )

    if not os.path.isdir(args.directory):
        print(f"错误: 路径不是目录 - {args.directory}", file=sys.stderr)
        sys.exit(1)

    ext_set = set(args.extensions) if args.extensions else None

    try:
        result = batch_convert(
            dir_path=args.directory,
            output_dir=args.output_dir,
            recursive=args.recursive,
            extensions=ext_set,
            preferred_tool=args.tool,
            skip_existing=args.skip_existing,
            max_workers=args.workers,
        )
        print_summary(result)
    except KeyboardInterrupt:
        print("\n\n转换已停止。")
        sys.exit(1)


if __name__ == "__main__":
    main()
