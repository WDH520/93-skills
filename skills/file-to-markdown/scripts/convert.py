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
多工具文件转 Markdown 引擎。

策略模式 + 回退链：根据文件格式选择最优转换工具，
若首选工具失败则自动尝试下一个。

使用方式:
  uv run convert.py input.pdf -o output.md
  uv run convert.py input.pdf --tool docling -o output.md
  uv run convert.py --list-tools

注意: marker-pdf (GPL-3.0) 和 pandoc (系统包) 未列入自动依赖，
需要时可手动 `uv pip install marker-pdf` 或 `brew install pandoc`。
"""

import argparse
import logging
import os
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# 格式 → 工具优先级映射
# ---------------------------------------------------------------------------
FORMAT_TOOL_PRIORITY: Dict[str, List[str]] = {
    ".pdf": ["docling", "marker", "pymupdf4llm", "markitdown"],
    ".docx": ["markitdown", "docling", "pandoc"],
    ".doc": ["markitdown", "pandoc"],
    ".pptx": ["markitdown", "marker"],
    ".ppt": ["markitdown"],
    ".xlsx": ["markitdown", "marker"],
    ".xls": ["markitdown"],
    ".csv": ["markitdown"],
    ".tsv": ["markitdown"],
    ".html": ["markitdown", "docling"],
    ".htm": ["markitdown", "docling"],
    ".xml": ["markitdown"],
    ".json": ["markitdown"],
    ".jpg": ["markitdown", "docling"],
    ".jpeg": ["markitdown", "docling"],
    ".png": ["markitdown", "docling"],
    ".gif": ["markitdown"],
    ".bmp": ["markitdown"],
    ".tiff": ["markitdown"],
    ".tif": ["markitdown"],
    ".epub": ["markitdown", "marker"],
    ".mp3": ["markitdown"],
    ".m4a": ["markitdown"],
    ".wav": ["markitdown"],
    ".zip": ["markitdown"],
    ".rst": ["pandoc"],
    ".tex": ["pandoc"],
    ".rtf": ["pandoc"],
}

# ---------------------------------------------------------------------------
# 转换结果数据类
# ---------------------------------------------------------------------------


@dataclass
class ConversionResult:
    """转换结果。"""

    success: bool
    content: str
    tool_used: str
    file_path: str
    output_path: Optional[str] = None
    error: Optional[str] = None
    elapsed_seconds: float = 0.0


# ---------------------------------------------------------------------------
# 各工具转换函数（惰性导入）
# ---------------------------------------------------------------------------


def convert_with_markitdown(file_path: str) -> Optional[str]:
    """使用 markitdown 转换文件。"""
    try:
        from markitdown import MarkItDown  # type: ignore

        md = MarkItDown()
        result = md.convert(file_path)
        return result.text_content
    except Exception as e:
        logger.debug("markitdown 转换失败: %s", e)
        return None


def convert_with_docling(file_path: str) -> Optional[str]:
    """使用 docling 转换文件。"""
    try:
        from docling.document_converter import DocumentConverter  # type: ignore

        converter = DocumentConverter()
        result = converter.convert(file_path)
        return result.document.export_to_markdown()
    except Exception as e:
        logger.debug("docling 转换失败: %s", e)
        return None


def convert_with_marker(file_path: str) -> Optional[str]:
    """使用 marker 转换文件。优先尝试 Python API，失败则回退到 CLI。"""
    # 尝试 Python API
    try:
        from marker.converters.pdf import PdfConverter  # type: ignore

        converter = PdfConverter()
        rendered = converter(file_path)
        # marker 返回的对象结构可能因版本而异
        if hasattr(rendered, "markdown"):
            return rendered.markdown
        if isinstance(rendered, tuple) and len(rendered) > 0:
            return str(rendered[0])
        return str(rendered)
    except Exception as e:
        logger.debug("marker Python API 失败: %s，尝试 CLI 回退", e)

    # CLI 回退
    try:
        marker_bin = shutil.which("marker_single")
        if not marker_bin:
            logger.debug("未找到 marker_single 命令")
            return None

        import tempfile

        with tempfile.TemporaryDirectory() as tmp_dir:
            cmd = [marker_bin, file_path, tmp_dir]
            subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=300)

            # 查找输出的 .md 文件
            for f in Path(tmp_dir).rglob("*.md"):
                return f.read_text(encoding="utf-8")

        logger.debug("marker CLI 未生成输出文件")
        return None
    except Exception as e:
        logger.debug("marker CLI 转换失败: %s", e)
        return None


def convert_with_pymupdf4llm(file_path: str) -> Optional[str]:
    """使用 pymupdf4llm 转换 PDF 文件。"""
    try:
        import pymupdf4llm  # type: ignore

        return pymupdf4llm.to_markdown(file_path)
    except Exception as e:
        logger.debug("pymupdf4llm 转换失败: %s", e)
        return None


def convert_with_pandoc(file_path: str) -> Optional[str]:
    """使用 pandoc 命令行工具转换文件。"""
    try:
        pandoc_bin = shutil.which("pandoc")
        if not pandoc_bin:
            logger.debug("未找到 pandoc 命令")
            return None

        result = subprocess.run(
            [pandoc_bin, "-t", "markdown", file_path],
            capture_output=True,
            text=True,
            check=True,
            timeout=120,
        )
        return result.stdout
    except Exception as e:
        logger.debug("pandoc 转换失败: %s", e)
        return None


# ---------------------------------------------------------------------------
# 工具名 → 转换函数映射
# ---------------------------------------------------------------------------
CONVERTER_MAP: Dict[str, Callable[[str], Optional[str]]] = {
    "markitdown": convert_with_markitdown,
    "docling": convert_with_docling,
    "marker": convert_with_marker,
    "pymupdf4llm": convert_with_pymupdf4llm,
    "pandoc": convert_with_pandoc,
}

# ---------------------------------------------------------------------------
# 辅助函数
# ---------------------------------------------------------------------------


def detect_file_type(file_path: str) -> str:
    """检测文件类型，返回小写扩展名。优先尝试 magika 内容检测，回退到扩展名。"""
    # 尝试使用 magika 进行基于内容的检测
    try:
        from magika import Magika  # type: ignore

        m = Magika()
        result = m.identify_path(Path(file_path))
        mime = result.output.mime_type

        # MIME 到扩展名的常见映射
        mime_to_ext = {
            "application/pdf": ".pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
            "application/msword": ".doc",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation": ".pptx",
            "application/vnd.ms-powerpoint": ".ppt",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
            "application/vnd.ms-excel": ".xls",
            "text/csv": ".csv",
            "text/tab-separated-values": ".tsv",
            "text/html": ".html",
            "application/xml": ".xml",
            "text/xml": ".xml",
            "application/json": ".json",
            "image/jpeg": ".jpg",
            "image/png": ".png",
            "image/gif": ".gif",
            "image/bmp": ".bmp",
            "image/tiff": ".tiff",
            "application/epub+zip": ".epub",
            "audio/mpeg": ".mp3",
            "audio/mp4": ".m4a",
            "audio/wav": ".wav",
            "application/zip": ".zip",
            "text/x-rst": ".rst",
            "application/x-tex": ".tex",
            "application/rtf": ".rtf",
        }
        ext = mime_to_ext.get(mime)
        if ext:
            logger.debug("magika 检测到类型: %s -> %s", mime, ext)
            return ext
    except Exception as e:
        logger.debug("magika 检测失败，回退到扩展名: %s", e)

    # 回退：使用文件扩展名
    return Path(file_path).suffix.lower()


def check_tool_available(tool_name: str) -> bool:
    """检查指定工具是否可用。"""
    if tool_name == "pandoc":
        return shutil.which("pandoc") is not None

    # Python 包检测
    import_map = {
        "markitdown": "markitdown",
        "docling": "docling",
        "marker": "marker",
        "pymupdf4llm": "pymupdf4llm",
    }

    package = import_map.get(tool_name)
    if not package:
        return False

    try:
        __import__(package)
        return True
    except ImportError:
        return False


# ---------------------------------------------------------------------------
# 核心转换入口
# ---------------------------------------------------------------------------


def convert_file(
    file_path: str,
    output_path: Optional[str] = None,
    preferred_tool: Optional[str] = None,
    force_tool: Optional[str] = None,
) -> ConversionResult:
    """
    将文件转换为 Markdown。

    参数:
        file_path: 输入文件路径
        output_path: 输出文件路径（可选，不指定则仅返回内容）
        preferred_tool: 优先使用的工具（仍会回退到其他工具）
        force_tool: 强制使用的工具（不回退）

    返回:
        ConversionResult 数据类实例
    """
    file_path = os.path.abspath(file_path)

    if not os.path.isfile(file_path):
        return ConversionResult(
            success=False,
            content="",
            tool_used="",
            file_path=file_path,
            output_path=output_path,
            error=f"文件不存在: {file_path}",
        )

    ext = detect_file_type(file_path)

    # 构建工具尝试列表
    if force_tool:
        if force_tool not in CONVERTER_MAP:
            return ConversionResult(
                success=False,
                content="",
                tool_used="",
                file_path=file_path,
                output_path=output_path,
                error=f"未知工具: {force_tool}",
            )
        tools_to_try = [force_tool]
    elif preferred_tool and preferred_tool in CONVERTER_MAP:
        # 优先工具 + 回退链
        fallback = FORMAT_TOOL_PRIORITY.get(ext, list(CONVERTER_MAP.keys()))
        tools_to_try = [preferred_tool] + [t for t in fallback if t != preferred_tool]
    else:
        tools_to_try = FORMAT_TOOL_PRIORITY.get(ext, list(CONVERTER_MAP.keys()))

    # 依次尝试各工具
    errors: List[str] = []
    start = time.time()

    for tool_name in tools_to_try:
        converter = CONVERTER_MAP.get(tool_name)
        if not converter:
            continue

        logger.info("尝试使用 %s 转换 %s ...", tool_name, os.path.basename(file_path))
        try:
            content = converter(file_path)
        except Exception as e:
            msg = f"{tool_name} 异常: {e}"
            logger.debug(msg)
            errors.append(msg)
            continue

        if content is not None and content.strip():
            elapsed = time.time() - start

            # 写入输出文件
            if output_path:
                out = Path(output_path)
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(content, encoding="utf-8")

            return ConversionResult(
                success=True,
                content=content,
                tool_used=tool_name,
                file_path=file_path,
                output_path=output_path,
                elapsed_seconds=elapsed,
            )
        else:
            errors.append(f"{tool_name} 返回空内容")

    elapsed = time.time() - start
    all_errors = "; ".join(errors) if errors else "所有工具均不可用或不支持此格式"
    return ConversionResult(
        success=False,
        content="",
        tool_used="",
        file_path=file_path,
        output_path=output_path,
        error=f"所有工具均失败 ({ext}): {all_errors}",
        elapsed_seconds=elapsed,
    )


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------


def main() -> None:
    """命令行入口。"""
    parser = argparse.ArgumentParser(
        description="多工具文件转 Markdown 引擎",
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        default=None,
        help="待转换的输入文件路径",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="输出 Markdown 文件路径（不指定则输出到标准输出）",
    )
    parser.add_argument(
        "--tool",
        default=None,
        help="优先使用的转换工具（仍会回退）",
    )
    parser.add_argument(
        "--force-tool",
        default=None,
        help="强制使用指定工具（不回退）",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="显示详细调试信息",
    )
    parser.add_argument(
        "--list-tools",
        action="store_true",
        help="列出所有支持的工具及其可用状态",
    )
    args = parser.parse_args()

    # 配置日志
    log_level = logging.DEBUG if args.verbose else logging.WARNING
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )

    # 列出工具
    if args.list_tools:
        print("可用转换工具:")
        print("-" * 40)
        for name in CONVERTER_MAP:
            available = check_tool_available(name)
            status = "✓ 已安装" if available else "✗ 未安装"
            print(f"  {name:15s} {status}")
        sys.exit(0)

    # 校验输入文件
    if not args.input_file:
        parser.error("必须指定输入文件路径")
    if not os.path.isfile(args.input_file):
        print(f"错误: 文件不存在 - {args.input_file}", file=sys.stderr)
        sys.exit(1)

    # 执行转换
    result = convert_file(
        file_path=args.input_file,
        output_path=args.output,
        preferred_tool=args.tool,
        force_tool=args.force_tool,
    )

    # 输出结果摘要
    if result.success:
        print(f"转换成功!", file=sys.stderr)
        print(f"  使用工具: {result.tool_used}", file=sys.stderr)
        print(f"  耗时: {result.elapsed_seconds:.2f} 秒", file=sys.stderr)
        print(f"  内容长度: {len(result.content)} 字符", file=sys.stderr)
        if result.output_path:
            print(f"  输出文件: {result.output_path}", file=sys.stderr)
        else:
            # 未指定输出文件时，将内容输出到标准输出
            print(result.content)
        sys.exit(0)
    else:
        print(f"转换失败!", file=sys.stderr)
        print(f"  文件: {result.file_path}", file=sys.stderr)
        print(f"  错误: {result.error}", file=sys.stderr)
        print(f"  耗时: {result.elapsed_seconds:.2f} 秒", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
