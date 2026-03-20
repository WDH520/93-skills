#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
文件转 Markdown 工具环境配置脚本。
使用 uv 管理依赖，检测工具安装状态，提供 uv run 命令建议。
"""

import argparse
import importlib.util
import shutil
import subprocess
import sys
from typing import Dict, List

# 工具配置信息
TOOL_CONFIGS = {
    "markitdown": {
        "pip_package": "markitdown[all]",
        "import_name": "markitdown",
        "description": "通用多格式转换 (PDF/DOCX/PPTX/XLSX/HTML/Images/Audio/CSV/JSON/XML/ZIP/EPUB)",
        "license": "MIT",
        "priority": 1,
    },
    "docling": {
        "pip_package": "docling",
        "import_name": "docling",
        "description": "AI驱动高精度文档转换 (PDF/DOCX/HTML, IBM Research, 表格识别极强)",
        "license": "MIT",
        "priority": 2,
    },
    "marker": {
        "pip_package": "marker-pdf",
        "import_name": "marker",
        "description": "深度学习PDF转换 (公式/学术论文, 需GPU最佳)",
        "license": "GPL-3.0",
        "priority": 3,
    },
    "pymupdf4llm": {
        "pip_package": "pymupdf4llm",
        "import_name": "pymupdf4llm",
        "description": "LLM专用PDF提取 (速度最快, 语义结构保持)",
        "license": "AGPL-3.0",
        "priority": 4,
    },
    "pandoc": {
        "pip_package": None,  # 系统软件包
        "import_name": None,
        "description": "通用格式互转 (50+格式, 需系统安装)",
        "license": "GPL-2.0",
        "priority": 5,
    },
}


def check_uv_installed() -> bool:
    """检查 uv 是否已安装"""
    return shutil.which("uv") is not None


def check_tool_installed(tool_name: str) -> bool:
    """检查工具是否已安装（当前环境）"""
    config = TOOL_CONFIGS.get(tool_name)
    if not config:
        return False

    if tool_name == "pandoc":
        return shutil.which("pandoc") is not None

    import_name = config.get("import_name")
    if import_name:
        return importlib.util.find_spec(import_name) is not None
    return False


def get_status() -> Dict[str, bool]:
    """获取所有工具的安装状态"""
    return {name: check_tool_installed(name) for name in TOOL_CONFIGS}


def install_uv() -> bool:
    """安装 uv"""
    if check_uv_installed():
        print("✅ uv 已安装。")
        return True
    print("正在安装 uv...")
    try:
        subprocess.check_call(
            ["curl", "-LsSf", "https://astral.sh/uv/install.sh"],
            stdout=subprocess.PIPE,
        )
        print("✅ uv 安装成功。")
        return True
    except Exception:
        print(
            "❌ 自动安装 uv 失败。请手动安装: https://docs.astral.sh/uv/getting-started/installation/"
        )
        return False


def install_tool(tool_name: str) -> bool:
    """使用 uv pip 安装指定工具"""
    config = TOOL_CONFIGS.get(tool_name)
    if not config:
        print(f"❌ 找不到工具配置: {tool_name}")
        return False

    pip_package = config.get("pip_package")
    if not pip_package:
        if tool_name == "pandoc":
            print("ℹ️  Pandoc 需系统安装: brew install pandoc 或 apt install pandoc")
        else:
            print(f"❌ 工具 {tool_name} 没有对应的 pip 软件包。")
        return False

    if not check_uv_installed():
        print(
            "❌ 未检测到 uv。请先运行: curl -LsSf https://astral.sh/uv/install.sh | sh"
        )
        return False

    print(f"正在安装 {tool_name} ({pip_package})...")
    try:
        subprocess.check_call(["uv", "pip", "install", pip_package])
        print(f"✅ {tool_name} 安装成功。")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 安装 {tool_name} 失败: {e}")
        return False


def install_by_license(license_filter: str = "MIT") -> List[str]:
    """按许可证过滤安装工具"""
    installed = []
    for name, config in TOOL_CONFIGS.items():
        if config["license"] == license_filter and config["pip_package"]:
            if install_tool(name):
                installed.append(name)
    return installed


def install_all() -> List[str]:
    """安装所有可 pip 安装的工具"""
    installed = []
    for name, config in TOOL_CONFIGS.items():
        if config["pip_package"]:
            if install_tool(name):
                installed.append(name)
    return installed


def print_status():
    """打印工具状态表格"""
    # uv 状态
    uv_ok = check_uv_installed()
    print(
        f"\n🔧 uv: {'✅ 已安装' if uv_ok else '❌ 未安装 — 运行: curl -LsSf https://astral.sh/uv/install.sh | sh'}"
    )
    print()

    status = get_status()
    print(f"{'工具':<15} | {'状态':<10} | {'许可证':<10} | {'描述'}")
    print("-" * 100)

    sorted_tools = sorted(TOOL_CONFIGS.items(), key=lambda x: x[1]["priority"])
    for name, config in sorted_tools:
        is_installed = status.get(name, False)
        status_str = "✅ 已安装" if is_installed else "❌ 未安装"
        print(
            f"{name:<15} | {status_str:<10} | {config['license']:<10} | {config['description']}"
        )

    print("-" * 100)
    print()
    print("💡 提示: 脚本使用 PEP 723 inline metadata，uv run 会自动解析依赖。")
    print("   直接运行: uv run scripts/convert.py input.pdf -o output.md")
    print("   无需手动 pip install。")
    print()
    if not uv_ok:
        print("⚠️  请先安装 uv: curl -LsSf https://astral.sh/uv/install.sh | sh")


def main():
    parser = argparse.ArgumentParser(
        description="文件转 Markdown 工具环境配置脚本 (uv)"
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    subparsers.add_parser("status", help="查看所有工具的安装状态")

    install_parser = subparsers.add_parser("install", help="安装指定工具 (uv pip)")
    install_parser.add_argument(
        "tool", choices=list(TOOL_CONFIGS.keys()), help="要安装的工具名称"
    )

    subparsers.add_parser("install-all", help="安装所有可用的 pip 工具")
    subparsers.add_parser("install-mit", help="仅安装 MIT 许可证的工具 (推荐)")
    subparsers.add_parser("install-uv", help="安装 uv 包管理器")

    args = parser.parse_args()

    if args.command == "status":
        print_status()
    elif args.command == "install":
        install_tool(args.tool)
    elif args.command == "install-all":
        install_all()
    elif args.command == "install-mit":
        install_by_license("MIT")
    elif args.command == "install-uv":
        install_uv()
    else:
        print_status()


if __name__ == "__main__":
    main()
