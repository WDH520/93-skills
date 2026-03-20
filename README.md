# Skills - 智能体技能集合

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/WDH520/93-skills)](https://github.com/WDH520/93-skills/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/WDH520/93-skills)](https://github.com/WDH520/93-skills/network)
[![GitHub issues](https://img.shields.io/github/issues/WDH520/93-skills)](https://github.com/WDH520/93-skills/issues)

**93 个强大的智能体技能，助你高效完成编程开发、AI 辅助、文档处理等各类任务**

</div>

## 📖 简介

这是一个为 Trae IDE 设计的智能体技能集合，包含 **93 个实用技能**，涵盖：
- 🚀 **任务规划与执行** - 让工作更有条理
- 🤖 **AI 与智能体管理** - 高效使用 AI 辅助开发
- 💻 **前后端开发** - React、Python、Django、C++ 等
- 🎨 **设计与可视化** - 前端界面、算法艺术、数据可视化
- 📄 **文档处理** - Markdown、PDF、Office 文档处理
- 🧪 **测试与调试** - 自动化测试、系统化调试
- 📊 **数据分析** - CSV 处理、数据可视化
- 🎓 **学习与成长** - 知识管理、技能创建

## ✨ 核心特性

- **93+ 实用技能** - 覆盖开发全流程
- **标准化工作流** - 内置最佳实践流程
- **多语言支持** - TypeScript、Python、Java、C++ 等
- **AI 优先** - 专为 AI 辅助开发设计
- **易于扩展** - 提供技能创建模板和指南
- **中文友好** - 完整中文文档和说明

## 🚀 快速开始

### 前置要求

- Trae IDE 或支持智能体的开发环境
- Node.js 18+（部分技能需要）
- Python 3.8+（部分技能需要）

### 安装技能

1. 克隆本仓库到本地
```bash
git clone https://github.com/WDH520/skills.git
```

2. 将技能文件复制到你的技能目录
```bash
cp -r skills/* $CODEX_HOME/skills/
```

3. 重启 IDE 或重新加载窗口

### 使用技能

在对话中直接使用技能名称，例如：
```
使用 python-testing 技能为我的函数编写测试
```

或使用工作流提示词：
```
请按标准开发流程执行：using-superpowers → brainstorming → writing-plans → 对应领域技能
```

## 📚 技能分类

### 流程与方法类（25+ 技能）
| 技能 | 用途 |
|------|------|
| `brainstorming` | 开始任何新任务前的构思 |
| `writing-plans` | 制定详细实施计划 |
| `planning-with-files` | 复杂任务分解与跟踪 |
| `systematic-debugging` | 科学方法定位问题 |
| `requesting-code-review` | 主动请求代码评审 |
| `receiving-code-review` | 分析评审意见 |
| `high-agency` | 高能动性工作模式 |
| `pua` | 压力激励模式 |

### AI 与智能体类（10+ 技能）
| 技能 | 用途 |
|------|------|
| `agent-dispatcher` | 自动选择合适智能体 |
| `agent-coordinator` | 显式指定智能体 |
| `agentic-engineering` | AI 主导工作流程设计 |
| `project-development` | AI 项目规划 |

### 后端与数据类（15+ 技能）
| 技能 | 用途 |
|------|------|
| `api-design` | RESTful API 设计 |
| `backend-patterns` | 后端架构模式 |
| `database-migrations` | 数据库 schema 变更 |
| `python-patterns` | Python 最佳实践 |
| `django-patterns` | Django 开发模式 |
| `csv-data-summarizer` | CSV 数据分析 |

### 前端与设计类（20+ 技能）
| 技能 | 用途 |
|------|------|
| `react-best-practices` | React/Next.js 最佳实践 |
| `frontend-design` | 创意前端界面设计 |
| `ui-ux-pro-max` | UI/UX 设计规范 |
| `web-artifacts-builder` | 单文件 HTML 打包 |
| `algorithmic-art` | 算法艺术创作 |
| `canvas-design` | 静态设计作品 |

### 文档处理类（15+ 技能）
| 技能 | 用途 |
|------|------|
| `pdf` | PDF 文件处理 |
| `docx` | Word 文档处理 |
| `pptx` | PowerPoint 处理 |
| `xlsx` | Excel 表格处理 |
| `file-to-markdown` | 文档转 Markdown |
| `baoyu-markdown-to-html` | Markdown 转 HTML |

### 测试与质量类（10+ 技能）
| 技能 | 用途 |
|------|------|
| `python-testing` | Python 单元测试 |
| `cpp-testing` | C++ 测试 |
| `webapp-testing` | Web 应用测试 |
| `react-doctor` | React 代码质量检查 |
| `code-review-optimizer` | 代码审查优化 |

## 📋 完整技能列表

详见 [skills-manual.md](skills-manual.md)

## 🔧 常用工作流

### 标准开发流程
```
using-superpowers → brainstorming → writing-plans → 对应领域技能 → requesting-code-review
```

### Bug 修复流程
```
systematic-debugging → 最小修复 → 反思总结
```

### 重型项目流程
```
using-superpowers → high-agency → brainstorming → planning-with-files → using-git-worktrees → executing-plans
```

### 前端开发流程
```
using-superpowers → brainstorming → writing-plans → react-best-practices → react-doctor → webapp-testing
```

完整工作流提示词见 [skills-prompts.md](skills-prompts.md)

## 📁 项目结构

```
skills/
├── skills/                    # 技能目录
│   ├── brainstorming/         # 单个技能
│   │   ├── SKILL.md          # 技能定义
│   │   └── agents/           # 智能体配置
│   ├── python-testing/
│   ├── react-best-practices/
│   └── ...                   # 93 个技能
├── skills-manual.md          # 技能使用手册
├── skills-prompts.md         # 工作流提示词
└── README.md                 # 本文件
```

## 🎯 使用示例

### 示例 1：开发新功能
```text
我想添加用户认证功能，请按标准流程执行
```

### 示例 2：修复 Bug
```text
我的 API 接口返回 500 错误，请帮我调试
```

### 示例 3：代码优化
```text
请帮我优化这段 Python 代码的性能
```

### 示例 4：文档处理
```text
请帮我把这个 PDF 文件转换成 Markdown 格式
```

## 🤝 贡献指南

欢迎贡献新的技能！请参考以下步骤：

1. Fork 本仓库
2. 创建新分支 `git checkout -b feature/new-skill`
3. 创建技能文件（参考现有技能结构）
4. 提交更改 `git commit -m 'Add new skill: xxx'`
5. 推送到分支 `git push origin feature/new-skill`
6. 创建 Pull Request

### 技能创建模板

使用 `skill-creator` 技能获取详细的技能创建指南。

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 🙏 致谢

- 基于 Trae IDE 智能体系统构建
- 灵感来源于实际开发中的高频需求
- 感谢所有贡献者

## 📬 联系方式

- GitHub: [@WDH520](https://github.com/WDH520)
- Issues: [问题反馈](https://github.com/WDH520/skills/issues)

---

<div align="center">

**如果这个项目对你有帮助，请给一个 ⭐️ Star！**

Made with ❤️ by WDH520

</div>
