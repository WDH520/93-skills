# 文件转 Markdown 工具对比参考

## 工具矩阵

| 工具 | Stars | 许可证 | 支持格式 | 核心技术 | 最佳场景 |
|------|-------|--------|----------|----------|----------|
| **MarkItDown** | ⭐86.8k | MIT | PDF/DOCX/PPTX/XLSX/Images/Audio/HTML/CSV/JSON/XML/ZIP/EPUB | 基础提取 + 可选LLM | 通用多格式轻量转换 |
| **Docling** | ⭐~53k | MIT | PDF/DOCX/PPTX/HTML/XLSX/Images | DocLayNet + TableFormer AI | 高精度表格/布局保持 |
| **Marker** | ⭐31.5k | GPL-3.0 | PDF/Image/PPTX/DOCX/XLSX/HTML/EPUB | Surya OCR + Texify | 学术论文/公式密集 |
| **MinerU** | ⭐~54k | — | PDF | 专用AI模型链 | 科学文献/教科书 |
| **PyMuPDF4LLM** | ⭐1.3k | AGPL-3.0 | PDF | PyMuPDF引擎 | LLM/RAG专用PDF快速提取 |
| **E2M** | ⭐1.2k | MIT | DOC/DOCX/EPUB/HTML/URL/PDF/PPT/MP3 | 解析器+转换器 | 轻量多格式 |
| **Pandoc** | 经典 | GPL-2.0 | 50+格式互转 | Haskell语法解析 | 格式互转 (非AI) |

## 格式 → 推荐工具

| 文件格式 | 首选工具 | 备选工具 | 说明 |
|----------|----------|----------|------|
| PDF (简单) | MarkItDown | PyMuPDF4LLM | 文本为主的PDF |
| PDF (复杂表格) | Docling | Marker | 含大量表格的PDF |
| PDF (学术/公式) | Marker | MinerU | 含LaTeX公式 |
| DOCX | MarkItDown | Docling, Pandoc | Word文档 |
| PPTX | MarkItDown | Marker | PowerPoint |
| XLSX/CSV | MarkItDown | — | 电子表格 |
| HTML | MarkItDown | Docling | 网页 |
| Images | MarkItDown(+LLM) | Docling | 需OCR |
| EPUB | MarkItDown | Marker | 电子书 |
| Audio | MarkItDown(+LLM) | — | 需语音转写 |
| RST/LaTeX/RTF | Pandoc | — | 标记语言互转 |

## 安装指南

### MarkItDown (推荐首装)
```bash
pip install 'markitdown[all]'
# 或按需安装: pip install 'markitdown[pdf,docx,pptx]'
```

### Docling
```bash
pip install docling
```

### Marker
```bash
pip install marker-pdf
# 注意: GPL-3.0 许可证，商用需注意
```

### PyMuPDF4LLM
```bash
pip install pymupdf4llm
# 注意: AGPL-3.0 许可证
```

### Pandoc
```bash
# macOS
brew install pandoc
# Ubuntu/Debian
sudo apt install pandoc
# Windows
choco install pandoc
```

## 许可证注意事项

| 许可证 | 工具 | 商用限制 |
|--------|------|----------|
| MIT | MarkItDown, Docling | ✅ 自由商用 |
| GPL-3.0 | Marker | ⚠️ 衍生作品需开源 |
| AGPL-3.0 | PyMuPDF4LLM | ⚠️ 网络服务也需开源 |
| GPL-2.0 | Pandoc | ⚠️ 衍生作品需开源 |

## 性能参考

- **速度**: PyMuPDF4LLM > MarkItDown > Docling > Marker
- **精度(表格)**: Docling > Marker > MarkItDown > PyMuPDF4LLM
- **精度(公式)**: Marker ≈ MinerU > Docling > MarkItDown
- **格式覆盖**: MarkItDown > Marker > Docling > PyMuPDF4LLM
- **资源占用**: PyMuPDF4LLM < MarkItDown < Docling < Marker
