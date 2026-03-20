#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
# -*- coding: utf-8 -*-
"""
Markdown 转换质量评估工具。纯 stdlib 实现，无外部依赖。

使用方式:
  uv run quality_check.py output.md
  uv run quality_check.py /path/to/output/ --recursive
"""

import os
import re
import sys
import argparse
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class QualityReport:
    file_path: str
    md_path: str
    file_size_bytes: int
    md_size_bytes: int
    md_line_count: int
    md_word_count: int
    has_headings: bool
    heading_count: int
    has_tables: bool
    table_count: int
    has_code_blocks: bool
    has_images: bool
    image_ref_count: int
    has_links: bool
    link_count: int
    has_lists: bool
    empty_ratio: float
    avg_line_length: float
    score: int
    warnings: List[str] = field(default_factory=list)
    grade: str = "F"


def check_quality(
    md_content: str, source_path: str = "", md_path: str = ""
) -> QualityReport:
    """分析 Markdown 内容并计算质量指标。"""
    lines = md_content.splitlines()
    line_count = len(lines)
    md_size = len(md_content.encode("utf-8"))

    # 基础统计
    words = re.findall(r"\w+", md_content)
    word_count = len(words)

    # 标题计数 (以 # 开头的行)
    headings = [l for l in lines if l.strip().startswith("#")]
    heading_count = len(headings)

    # 表格计数 (包含 | 的行)
    # 简单启发式：连续的有 | 的行可能构成表格
    table_lines = [l for l in lines if "|" in l]
    table_count = 0
    if table_lines:
        # 统计表格数量（通过检查 | --- | 这种分隔线）
        table_count = len(re.findall(r"\|?\s*:?-+:?\s*\|", md_content))

    # 代码块计数 (```)
    code_blocks = re.findall(r"```", md_content)
    code_block_count = len(code_blocks) // 2

    # 图片计数 (![)
    image_refs = re.findall(r"!\[.*?\]\(.*?\)", md_content)
    image_ref_count = len(image_refs)

    # 链接计数 ([...](...)
    links = re.findall(r"\[.*?\]\(.*?\)", md_content)
    # 排除图片
    links = [l for l in links if not any(img in l for img in image_refs)]
    link_count = len(links)

    # 列表项计数 (以 -, *, 1. 开头的行)
    list_items = [l for l in lines if re.match(r"^\s*([-*]|\d+\.)\s+", l)]
    list_count = len(list_items)

    # 空行率
    empty_lines = [l for l in lines if not l.strip()]
    empty_ratio = len(empty_lines) / line_count if line_count > 0 else 0

    # 平均行长
    total_len = sum(len(l) for l in lines)
    avg_line_length = total_len / line_count if line_count > 0 else 0

    # 评分逻辑
    score = 0
    warnings = []

    # 1. 基础分: 内容存在且字数 > 10
    if word_count > 10:
        score += 50
    else:
        warnings.append("内容过少或字数不足。")

    # 2. 结构分: 有标题
    if heading_count > 0:
        score += 10
    else:
        warnings.append("缺少标题结构。")

    # 3. 可读性: 平均行长 20-200
    if 20 <= avg_line_length <= 200:
        score += 10
    elif avg_line_length > 200:
        warnings.append(
            f"平均行长过大 ({avg_line_length:.1f})，可能包含未换行的长文本。"
        )

    # 4. 密度分: 空行率 < 0.5
    if empty_ratio < 0.5:
        score += 10
    else:
        warnings.append(f"空行率过高 ({empty_ratio:.1%})。")

    # 5. 格式分: 有表格或列表
    if table_count > 0 or list_count > 0:
        score += 10
    else:
        warnings.append("缺少表格或列表等格式化内容。")

    # 6. 效率分: 字数/文件大小比例合理
    # 如果 source_path 为空，无法准确判断，但我们可以根据 md_size 估算
    # 这里我们用 md_size 作为参考
    if md_size > 0:
        ratio = word_count / md_size
        if ratio > 0.1:
            score += 10
        else:
            warnings.append(f"信息密度较低 (字数/字节比: {ratio:.2f})。")

    # 惩罚项
    # 内容过短 (针对非琐碎文件)
    if len(md_content) < 50:
        score -= 20
        warnings.append("内容极短，可能转换失败。")

    # 过长行
    long_lines = [l for l in lines if len(l) > 500]
    if len(long_lines) > 0:
        score -= 10
        warnings.append(
            f"发现 {len(long_lines)} 行超长文本 (>500字符)，可能包含未解析的二进制数据或长 URL。"
        )

    # 限制分数范围
    score = max(0, min(100, score))

    # 评级
    if score >= 80:
        grade = "A"
    elif score >= 60:
        grade = "B"
    elif score >= 40:
        grade = "C"
    elif score >= 20:
        grade = "D"
    else:
        grade = "F"

    source_size = 0
    if source_path and os.path.exists(source_path):
        source_size = os.path.getsize(source_path)

    return QualityReport(
        file_path=source_path,
        md_path=md_path,
        file_size_bytes=source_size,
        md_size_bytes=md_size,
        md_line_count=line_count,
        md_word_count=word_count,
        has_headings=heading_count > 0,
        heading_count=heading_count,
        has_tables=table_count > 0,
        table_count=table_count,
        has_code_blocks=code_block_count > 0,
        has_images=image_ref_count > 0,
        image_ref_count=image_ref_count,
        has_links=link_count > 0,
        link_count=link_count,
        has_lists=list_count > 0,
        empty_ratio=empty_ratio,
        avg_line_length=avg_line_length,
        score=score,
        warnings=warnings,
        grade=grade,
    )


def check_file(
    md_file_path: str, source_file_path: Optional[str] = None
) -> QualityReport:
    """读取 Markdown 文件并运行质量检查。"""
    try:
        with open(md_file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"读取文件失败: {md_file_path}, 错误: {e}")
        return QualityReport(
            file_path=source_file_path or "",
            md_path=md_file_path,
            file_size_bytes=0,
            md_size_bytes=0,
            md_line_count=0,
            md_word_count=0,
            has_headings=False,
            heading_count=0,
            has_tables=False,
            table_count=0,
            has_code_blocks=False,
            has_images=False,
            image_ref_count=0,
            has_links=False,
            link_count=0,
            has_lists=False,
            empty_ratio=0,
            avg_line_length=0,
            score=0,
            warnings=[f"读取文件失败: {e}"],
            grade="F",
        )

    return check_quality(content, source_file_path or "", md_file_path)


def check_directory(dir_path: str, recursive: bool = True) -> List[QualityReport]:
    """查找所有 .md 文件，运行质量检查，并按分数升序排序。"""
    reports = []
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".md"):
                md_path = os.path.join(root, file)
                reports.append(check_file(md_path))
        if not recursive:
            break

    # 按分数升序排序（最差的在前）
    reports.sort(key=lambda x: x.score)
    return reports


def print_report(report: QualityReport):
    """打印单份报告，带有表情指示符。"""
    emoji = "✅" if report.score >= 80 else "⚠️" if report.score >= 40 else "❌"

    print(f"\n{emoji} 质量报告: {os.path.basename(report.md_path)}")
    print("-" * 40)
    print(f"文件路径: {report.md_path}")
    print(f"源文件:   {report.file_path or '未知'}")
    print(f"质量评分: {report.score} ({report.grade})")
    print(f"字数统计: {report.md_word_count}")
    print(f"行数统计: {report.md_line_count}")
    print(f"空行比例: {report.empty_ratio:.1%}")
    print(f"平均行长: {report.avg_line_length:.1f}")

    stats = []
    if report.heading_count:
        stats.append(f"标题({report.heading_count})")
    if report.table_count:
        stats.append(f"表格({report.table_count})")
    if report.image_ref_count:
        stats.append(f"图片({report.image_ref_count})")
    if report.link_count:
        stats.append(f"链接({report.link_count})")

    if stats:
        print(f"内容结构: {', '.join(stats)}")

    if report.warnings:
        print("\n警告事项:")
        for w in report.warnings:
            print(f"  - {w}")
    print("-" * 40)


def print_summary(reports: List[QualityReport]):
    """打印所有报告的摘要表格、平均分和等级分布。"""
    if not reports:
        print("未发现可检查的文件。")
        return

    print(f"\n{'文件名':<30} | {'分数':<5} | {'等级':<4} | {'字数':<6} | {'警告':<4}")
    print("-" * 60)

    total_score = 0
    grades = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}

    for r in reports:
        name = os.path.basename(r.md_path)
        if len(name) > 27:
            name = name[:24] + "..."
        warn_count = len(r.warnings)
        print(
            f"{name:<30} | {r.score:<5} | {r.grade:<4} | {r.md_word_count:<6} | {warn_count:<4}"
        )

        total_score += r.score
        grades[r.grade] += 1

    avg_score = total_score / len(reports)
    print("-" * 60)
    print(f"平均分: {avg_score:.1f}")
    print(f"等级分布: " + ", ".join([f"{k}: {v}" for k, v in grades.items() if v > 0]))


def main():
    parser = argparse.ArgumentParser(description="Markdown 转换质量评估工具")
    parser.add_argument("path", help="Markdown 文件或目录路径")
    parser.add_argument("--source", help="对应的源文件路径（仅在检查单个文件时有效）")
    parser.add_argument("--recursive", action="store_true", help="是否递归检查目录")

    args = parser.parse_args()

    if os.path.isfile(args.path):
        report = check_file(args.path, args.source)
        print_report(report)
    elif os.path.isdir(args.path):
        reports = check_directory(args.path, args.recursive)
        print_summary(reports)
    else:
        print(f"路径不存在: {args.path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
