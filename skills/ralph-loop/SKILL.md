---
name: ralph-loop
description: |
  实现 Ralph Wiggum 技术的迭代开发循环插件。当用户需要：(1) 启动自引用 AI 循环进行迭代开发，(2) 让 Claude 持续迭代直到任务完成，(3) 使用 /ralph-loop 命令，(4) 需要自动化的迭代改进工作流时触发。适用于定义明确的任务、需要迭代完善的开发工作、有自动验证机制的任务（测试、lint）。
---

# Ralph Loop 技能

实现 Ralph Wiggum 技术的自引用 AI 迭代开发循环。

## 核心概念

Ralph Loop 通过 Stop hook 拦截 Claude 的退出尝试，将相同的提示词重新喂给 AI，让它持续迭代改进直到任务完成：

```
/ralph-loop "任务描述" --completion-promise "COMPLETE" --max-iterations 50
```

每次迭代：
1. Claude 收到相同的提示词
2. 执行任务，修改文件
3. 尝试退出
4. Stop hook 拦截并重新喂入提示词
5. Claude 看到之前的工作成果
6. 持续改进直到完成

## 命令

### /ralph-loop

启动 Ralph 循环。

**用法：**
```
/ralph-loop "<提示词>" --max-iterations <n> --completion-promise "<文本>"
```

**参数：**
- `--max-iterations <n>` - 最大迭代次数（安全网）
- `--completion-promise <text>` - 完成信号短语

### /cancel-ralph

取消当前活动的 Ralph 循环。

**用法：**
```
/cancel-ralph
```

## 提示词编写最佳实践

### 1. 明确的完成条件

```markdown
构建 REST API。

完成时：
- 所有 CRUD 端点正常工作
- 输入验证到位
- 测试通过（覆盖率 > 80%）
- 输出: <promise>COMPLETE</promise>
```

### 2. 分阶段目标

```markdown
阶段 1: 用户认证（JWT, 测试）
阶段 2: 产品目录（列表/搜索, 测试）
阶段 3: 购物车（添加/删除, 测试）

所有阶段完成后输出 <promise>COMPLETE</promise>
```

### 3. 自我修正机制

```markdown
按 TDD 实现：
1. 编写失败的测试
2. 实现功能
3. 运行测试
4. 如有失败，调试修复
5. 重构
6. 重复直到全部通过
7. 输出: <promise>COMPLETE</promise>
```

### 4. 安全网

始终使用 `--max-iterations` 防止无限循环：

```bash
/ralph-loop "实现功能 X" --max-iterations 20
```

## 关键规则

**完成承诺（Completion Promise）只能在实际完成时输出。** 不要为了逃避循环而输出虚假承诺。循环设计为持续到真正完成为止。

## 适用场景

**适合：**
- 定义明确、有清晰成功标准的任务
- 需要迭代完善的开发工作
- 有自动验证的任务（测试、lint）
- 全新项目开发

**不适合：**
- 需要人工判断或设计决策的任务
- 一次性操作
- 成功标准不明确的任务
- 生产环境调试

## 工作原理

状态文件：`.claude/ralph-loop.local.md`

```yaml
---
iteration: 1
max_iterations: 50
completion_promise: "COMPLETE"
---
[提示词内容]
```

Stop hook 检查：
1. 是否达到最大迭代次数
2. 是否检测到完成承诺
3. 否则继续循环

## 参考资源

- 原始技术：https://ghuntley.com/ralph/
- Ralph Orchestrator：https://github.com/mikeyobrien/ralph-orchestrator
