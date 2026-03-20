---
name: file-to-markdown
description: >
  将各种文件格式（PDF、DOCX、PPTX、XLSX、HTML、Images、Audio、CSV、JSON、XML、EPUB 等）
  转换为 Markdown 格式。使用多工具组合策略（MarkItDown + Docling + Marker + PyMuPDF4LLM + Pandoc），
  根据文件类型自动选择最优转换工具。支持单文件转换、批量目录扫描、转换质量检查。
  当用户要求"转换文件为 markdown"、"文件转 md"、"批量转换文档"、"PDF 转 markdown"、
  "文档转文本"、"convert to markdown"、"file to md"、"batch convert documents"时使用此技能。
  也适用于 LLM/RAG 数据预处理管道中的文档提取环节。
---

# 文件转 Markdown

将任意文件转换为结构化 Markdown，多工具自动选优。所有脚本使用 PEP 723 inline metadata，通过 `uv run` 自动解析依赖，无需手动安装。

## 前置条件

需要 [uv](https://docs.astral.sh/uv/) 包管理器：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

检查环境状态：

```bash
uv run scripts/setup.py status
```

## 快速开始

### 单文件转换

```bash
uv run scripts/convert.py input.pdf -o output.md
```

指定工具：

```bash
uv run scripts/convert.py input.pdf --tool docling -o output.md
```

强制使用某工具（不回退）：

```bash
uv run scripts/convert.py input.pdf --force-tool marker -o output.md
```

### 批量转换

```bash
uv run scripts/batch_convert.py /path/to/docs/ -o /path/to/output/
```

带过滤和并行：

```bash
uv run scripts/batch_convert.py /path/to/docs/ -o output/ --extensions .pdf .docx --workers 4
```

### 质量检查

```bash
uv run scripts/quality_check.py output.md
uv run scripts/quality_check.py /path/to/output/  # 批量检查
```

## 工具选择策略

系统根据文件格式自动选择最优工具链：

| 文件类型 | 首选 → 备选 |
|----------|-------------|
| PDF (简单) | Docling → Marker → PyMuPDF4LLM → MarkItDown |
| DOCX/DOC | MarkItDown → Docling → Pandoc |
| PPTX | MarkItDown → Marker |
| XLSX/CSV | MarkItDown |
| HTML | MarkItDown → Docling |
| Images | MarkItDown(+LLM) → Docling |
| EPUB | MarkItDown → Marker |
| Audio | MarkItDown(+LLM) |
| RST/LaTeX/RTF | Pandoc |

若首选工具失败或未安装，自动回退到下一个可用工具。

**工具详细对比**: 见 [references/tool-comparison.md](references/tool-comparison.md)

## Python API 调用

在其他脚本中直接调用：

```python
import sys
sys.path.insert(0, 'scripts')
from convert import convert_file

result = convert_file('document.pdf', output_path='output.md')
if result.success:
    print(f"转换成功，使用工具: {result.tool_used}, 耗时: {result.elapsed_seconds:.1f}s")
    print(result.content[:500])
```

批量转换：

```python
from batch_convert import batch_convert

batch_result = batch_convert(
    '/path/to/docs',
    output_dir='/path/to/output',
    extensions={'.pdf', '.docx'},
    max_workers=4
)
print(f"成功: {batch_result.succeeded}/{batch_result.total}")
```

质量检查：

```python
from quality_check import check_quality

report = check_quality(md_content, source_path='original.pdf')
print(f"质量评分: {report.score}/100 ({report.grade})")
```

## 特殊场景指南

### PDF 含复杂表格

优先 Docling（IBM AI 表格识别）：

```bash
uv run scripts/convert.py report.pdf --tool docling
```

### PDF 含数学公式

优先 Marker（LaTeX 公式提取）：

```bash
uv run scripts/convert.py paper.pdf --tool marker
```

### 需要最快速度

优先 PyMuPDF4LLM：

```bash
uv run scripts/convert.py large.pdf --tool pymupdf4llm
```

### LLM 增强图像描述

MarkItDown 可集成 OpenAI/Azure LLM 进行图像内容描述（需在 convert.py 中配置 llm_client）。

## 注意事项

- **依赖管理**: 所有脚本使用 PEP 723 inline metadata，`uv run` 自动解析依赖，无需手动 `pip install`
- **许可证**: MarkItDown 和 Docling 为 MIT（自由商用）；Marker 为 GPL-3.0，PyMuPDF4LLM 为 AGPL-3.0（商用需注意）
- **GPU**: Marker 和 Docling 在有 GPU 时表现更好，CPU 也可运行但较慢
- **大文件**: 超过 100MB 的文件建议使用 PyMuPDF4LLM（内存效率最高）
- **中文 PDF**: Docling 和 Marker 对中文支持较好
