# Skills 工作流提示词

> 按使用频率排序，高频场景简洁，复杂场景详细。直接复制即可使用。

---

## 一、高频场景（简洁版）

### 1. 新功能开发

**标准开发**
```text
请按标准开发流程执行：using-superpowers → brainstorming → writing-plans → 对应领域技能 → requesting-code-review。
```

**快速开发（轻量改动）**
```text
请按快速开发流程执行：using-superpowers → search-first → 对应领域技能。
```

**重型项目**
```text
请按重型项目流程执行：using-superpowers → brainstorming → planning-with-files → using-git-worktrees → executing-plans。
```

**重型项目（高能动性版）**
```text
请按重型项目高能动性流程执行：using-superpowers → high-agency → brainstorming → planning-with-files → using-git-worktrees → executing-plans。
```

---

### 2. Bug 修复

**标准 Bug**
```text
请按 Bug 修复流程执行：systematic-debugging → 最小修复 → 反思总结。
```

**疑难 Bug**
```text
请按疑难 Bug 流程执行：systematic-debugging → planning-with-files（记录假设与实验）→ 反思总结。
```

**收到评审意见后**
```text
请按评审修复流程执行：receiving-code-review → systematic-debugging → 修复问题。
```

**需要驱动力时**
```text
请按高能动性流程执行：high-agency → systematic-debugging → verification-before-completion。
```

**需要压力激励时**
```text
请按 PUA 激励流程执行：pua → systematic-debugging → verification-before-completion。
```

---

### 3. 前端开发

**React / Next.js 新页面**
```text
请按前端开发流程执行：using-superpowers → brainstorming → writing-plans → react-best-practices → react-doctor → webapp-testing。
```

**视觉设计 / 创意界面**
```text
请按前端视觉流程执行：using-superpowers → brainstorming → frontend-design → ui-ux-pro-max → theme-factory → webapp-testing。
```

**前端 Bug**
```text
请按前端 Bug 流程执行：systematic-debugging → webapp-testing → react-doctor。
```

---

### 4. Python 开发

**标准 Python 功能**
```text
请按 Python 开发流程执行：using-superpowers → brainstorming → writing-plans → python-patterns → python-design-patterns → python-testing。
```

**Python 性能优化**
```text
请按 Python 优化流程执行：systematic-debugging → python-performance-optimization → python-patterns。
```

**数据分析 / CSV 处理**
```text
请按数据分析流程执行：using-superpowers → brainstorming → csv-data-summarizer → xlsx（如需表格输出）。
```

---

### 5. 文档处理

**通用文件处理**
```text
请按文件处理流程执行：using-superpowers → 按文件类型选择 pdf/docx/xlsx/pptx → file-to-markdown（如需提取）。
```

**PDF 处理**
```text
请按 PDF 流程执行：using-superpowers → pdf → nutrient-document-processing（如需 OCR/签名）。
```

**Word / Excel / PPT**
```text
请按 Office 流程执行：using-superpowers → docx/xlsx/pptx → doc-coauthoring（如需说明文档）。
```

---

## 二、中频场景（简洁版）

### 6. 后端 API 开发

**标准 API**
```text
请按后端 API 流程执行：using-superpowers → brainstorming → writing-plans → api-design → backend-patterns → error-handling-patterns。
```

**安全敏感接口**
```text
请按安全接口流程执行：using-superpowers → brainstorming → api-design → backend-patterns → error-handling-patterns。
```

---

### 7. 数据库操作

**表结构变更**
```text
请按数据库变更流程执行：using-superpowers → brainstorming → writing-plans → database-migrations。
```

---

### 8. 测试与审查

**代码评审**
```text
请按代码评审流程执行：using-superpowers → requesting-code-review。
```

---

### 9. 文档写作

**PRD / 技术方案**
```text
请按文档协作流程执行：using-superpowers → doc-coauthoring → brainstorming → writing-plans（如需后续实施）。
```

**长文 / 博客**
```text
请按内容写作流程执行：using-superpowers → brainstorming → article-writing。
```

---

## 三、复杂场景（详细版）

### 10. AI / Agent 项目

**AI 项目启动**
```text
请按 AI 项目流程执行：
1. using-superpowers - 检查可用技能
2. brainstorming - 明确项目目标、数据来源、模型选择
3. project-development - 规划整体方案
4. writing-plans - 制定实施计划
5. python-patterns + python-testing - 实现阶段
```

**MCP 工具开发**
```text
请按 MCP 开发流程执行：
1. using-superpowers - 检查可用技能
2. search-first - 查找现有方案
3. brainstorming - 明确工具接口与功能
4. mcp-builder - 构建 MCP 服务器
```

**多智能体系统**
```text
请按多智能体流程执行：
1. using-superpowers - 检查可用技能
2. brainstorming - 明确各 Agent 职责与协作方式
3. writing-plans - 制定架构方案
4. dispatching-parallel-agents - 并行任务分发
5. filesystem-context - 如需持久化上下文
```

---

### 11. 代码重构

**代码重构**
```text
请按重构流程执行：
1. using-superpowers - 检查可用技能
2. brainstorming - 明确重构目标与边界
3. writing-plans - 制定重构计划
4. code-simplifier + coding-standards - 代码优化
5. requesting-code-review - 如需评审
```

---

### 12. 大型项目规划

**项目启动**
```text
请按项目规划流程执行：
1. using-superpowers - 检查可用技能
2. brainstorming - 明确项目目标、范围、约束
3. planning-with-files - 创建任务计划文件
4. writing-plans - 制定详细实施计划
5. using-git-worktrees - 如需并行开发
6. executing-plans - 按计划执行
```

---

## 四、技术栈专项

### Django 开发
```text
using-superpowers → brainstorming → writing-plans → django-patterns → django-security → django-tdd → django-verification。
```

### C++ 开发
```text
using-superpowers → brainstorming → writing-plans → cpp-coding-standards → cpp-testing。
```

### React Native / Expo
```text
using-superpowers → brainstorming → react-native-skills → building-native-ui。
```

### Hugging Face 平台
```text
using-superpowers → hf-mcp → hugging-face-cli/hugging-face-datasets/hugging-face-jobs（按需选择）。
```

---

## 五、快速选择指南

| 场景 | 推荐工作流 |
|------|-----------|
| 还没想清楚要做什么 | brainstorming → writing-plans |
| 正在写代码 | python-patterns / react-best-practices |
| 遇到 Bug | systematic-debugging |
| 做前端项目 | frontend-design → ui-ux-pro-max |
| 做 Python/AI 项目 | python-patterns → python-testing |
| 写文档 | doc-coauthoring → article-writing |
| 处理文件 | pdf/docx/xlsx/pptx |
| 集成外部平台 | mcp-builder → hf-mcp |
| 代码评审 | requesting-code-review |
| 重构代码 | code-simplifier → coding-standards |
| 需要驱动力/主动性 | high-agency → systematic-debugging |
| 需要压力激励/穷尽方案 | pua → systematic-debugging |
| 复杂调试/卡壳多次 | pua/high-agency → systematic-debugging → verification-before-completion |
