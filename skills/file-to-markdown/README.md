# file-to-markdown: 多格式文件转 Markdown 引擎

![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)
![License MIT](https://img.shields.io/badge/license-MIT-green.svg)
![uv](https://img.shields.io/badge/manager-uv-purple.svg)

> **一句话描述**：基于多工具组合策略（MarkItDown + Docling + Marker + PyMuPDF4LLM + Pandoc）的智能文件转换引擎，支持 PDF、DOCX、PPTX、XLSX 等多种格式一键转为高质量 Markdown。

---

## ✨ 功能特性

- 🧩 **多工具组合**：集成 5 大主流转换工具，取长补短，覆盖最全格式。
- 🔄 **自动回退**：首选工具失败时，自动尝试备选工具，确保转换成功率。
- ⚡ **零配置运行**：使用 `uv` 包管理器，依赖自动解析，无需手动 `pip install`。
- 📦 **批量处理**：支持目录递归扫描、并行转换（多 Worker 支持）。
- ✅ **质量检查**：内置转换质量评分工具，快速定位转换异常。

## 📂 支持格式

系统根据文件后缀自动选择最优工具链：

| 格式 | 首选工具 | 备选工具链 | 说明 |
| :--- | :--- | :--- | :--- |
| **PDF** | Docling / Marker | PyMuPDF4LLM → MarkItDown | 智能识别表格/公式 |
| **DOCX** | MarkItDown | Docling → Pandoc | Word 文档 |
| **PPTX** | MarkItDown | Marker | 演示文稿 |
| **XLSX** | MarkItDown | — | 电子表格 |
| **HTML** | MarkItDown | Docling | 网页内容 |
| **Images** | MarkItDown | Docling | 图片 OCR |
| **EPUB** | MarkItDown | Marker | 电子书 |
| **Audio** | MarkItDown | — | 音频转写 |

## 🚀 快速开始

### 前提条件

本技能依赖 **[uv](https://docs.astral.sh/uv/)** 进行依赖管理和脚本运行。

```bash
# 安装 uv (macOS/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 安装为 Claude Code Skill

将本项目克隆到 Claude Code 的技能目录：

```bash
# 创建技能目录
mkdir -p ~/.claude/skills

# 克隆仓库
git clone https://github.com/your-repo/file-to-markdown.git ~/.claude/skills/file-to-markdown
```

### 独立使用

也可以直接下载源码并在本地运行：

```bash
git clone https://github.com/your-repo/file-to-markdown.git
cd file-to-markdown
```

## 🛠️ 使用方法

### 1. 环境检查

查看当前环境工具支持状态：

```bash
uv run scripts/setup.py status
```

### 2. 单文件转换

最基础的用法，自动选择最佳工具：

```bash
uv run scripts/convert.py input.pdf -o output.md
```

指定特定工具（例如处理带表格的 PDF 推荐用 docling）：

```bash
uv run scripts/convert.py report.pdf --tool docling -o report.md
```

### 3. 批量转换

扫描目录并转换所有支持的文件：

```bash
uv run scripts/batch_convert.py /path/to/docs -o /path/to/output
```

**高级选项**：指定扩展名和并行进程数：

```bash
uv run scripts/batch_convert.py /docs -o /output --extensions .pdf .docx --workers 4
```

### 4. 质量检查

对转换后的 Markdown 文件进行质量评分（0-100分）：

```bash
uv run scripts/quality_check.py output.md
```

批量检查目录：

```bash
uv run scripts/quality_check.py /path/to/output
```

## 🧠 工具优先级策略

本技能采用 **"最优匹配 + 自动降级"** 策略：

1. **Format Matching**: 根据文件扩展名查找 `FORMAT_TOOL_PRIORITY` 列表。
2. **Priority Execution**: 尝试列表中的第一个工具（Priority 1）。
3. **Automatic Fallback**: 
   - 如果首选工具未安装或运行报错，系统捕获异常。
   - 自动切换到下一个优先级的工具。
   - 只有当所有可用工具都失败时，才返回转换错误。

例如 PDF 转换链：`Docling` (擅长表格) ❌ 失败 → `Marker` (擅长公式) ❌ 失败 → `PyMuPDF4LLM` (速度快) ✅ 成功。

## 🧰 集成的转换工具

| 工具 | 许可证 | 擅长领域 |
| :--- | :--- | :--- |
| **[MarkItDown](https://github.com/microsoft/markitdown)** | MIT | **通用全能王**。支持 Office 全家桶、图片、音频、HTML 等，微软出品。 |
| **[Docling](https://github.com/DS4SD/docling)** | MIT | **文档布局分析**。IBM 出品，对复杂 PDF 表格和多栏布局还原度极高。 |
| **[Marker](https://github.com/VikParuchuri/marker)** | GPL-3.0 | **学术/公式**。擅长处理包含大量数学公式的 PDF 和书籍。 |
| **[PyMuPDF4LLM](https://github.com/pymupdf/PyMuPDF)** | AGPL-3.0 | **极速转换**。专为 LLM 设计，速度极快，适合纯文本 PDF 提取。 |
| **[Pandoc](https://pandoc.org/)** | GPL-2.0 | **文档互转**。格式转换界的瑞士军刀，主要作为兜底方案。 |

## 📂 项目结构

```text
file-to-markdown/
├── README.md               # 项目说明
├── SKILL.md                # Claude Code 技能定义
├── scripts/
│   ├── convert.py          # 核心转换脚本 (单文件)
│   ├── batch_convert.py    # 批量转换脚本 (多进程)
│   ├── quality_check.py    # 质量检查脚本
│   └── setup.py            # 环境检查与设置
└── references/
    └── tool-comparison.md  # 详细的工具对比评测
```

## ⚖️ 许可证

本项目代码使用 **MIT License**。

> **注意**：集成的第三方工具（Marker, PyMuPDF4LLM, Pandoc）可能采用 GPL 或 AGPL 协议，在商业产品中使用时请查阅对应工具的许可证条款。
