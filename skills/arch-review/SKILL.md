---
name: arch-review
description: Use when the user explicitly invokes /arch-review after completing a feature or requirement and wants to reflect on architecture thinking. Inspect code changes, scan business/application/technical architecture, then focus on one high-value blind spot through concrete comparison.
---

# Architecture Retrospective

以导师式对比帮助开发者发现一个最值得练习的架构盲点。全部输出中文，引用实际改动，不泛讲概念。

## 三层框架

按业务 → 应用 → 技术的顺序扫描：

| 层 | 核心问题 |
|---|---|
| 业务架构 | 为什么做、谁使用、价值与边界是什么 |
| 应用架构 | 模块职责、协作方式和变更隔离是否清晰 |
| 技术架构 | 技术选型是否满足性能、可用性、成本等约束 |

## 流程

### 1. 判断是否值得复盘

读取实际 Git diff。若仅是错字、简单配置或纯样式调整，说明架构复盘价值有限并停止。

获取需求上下文；当前对话没有时只问一句：“一句话说下这个需求是做什么的？”

### 2. 解析记录位置

1. 读取 `~/.agents/data/arch-review/config.json` 的 `retrospectivesPath` 并展开 `~`。
2. 配置缺失或无效时，推荐 `~/.agents/data/arch-review/retrospectives.md`，等待用户确认或指定其他路径后再写配置。
3. 路径不可读写时报告问题并请求替代路径，不静默回退。
4. 已有记录时读取最后一条“思考题”，询问用户本次是否用到了该思考方式；首次运行跳过。

### 3. 扫描三层

每层给出 `有盲点 / 已覆盖 / 不适用` 和一条基于需求或 diff 的理由：

- 业务：只有“做什么”而缺少目标、用户或价值时为盲点；内部重构可不适用。
- 应用：跨模块或新增模块的职责、通信、复用不清时为盲点；单模块且无边界问题可不适用。
- 技术：新依赖、新模式或性能敏感代码缺少理由时为盲点；无技术决策可不适用。

全部已覆盖时指出最好的做法并停止；全部不适用时停止。

### 4. 聚焦一个盲点

按认知收益、差距大小、近期可练习性排序，只推荐一层并让用户确认。确认后输出：

```text
📐 对比分析 — [层]

你的做法：
- [来自实际改动的观察]

架构师的做法：
- [不同的分析路径或决策]

差距在哪：
- [具体认知差距及其可能影响]
```

业务层按“问题 → 用户 → 价值 → 核心路径”，应用层按“边界 → 职责 → 通信 → 变更隔离”，技术层按“约束 → 备选 → 权衡 → 选择理由”展开。不要列改进清单。

### 5. 留题并记录

给一个 5 分钟内可思考、下个需求即可复用、无需写代码的问题。随后追加：

```markdown
## [date] — [requirement name]

**聚焦层面**: [layer]
**盲点**: [一句话]
**对比**: [当前做法] vs [架构师做法] — [差距]
**思考题**: [问题]
**代码变更**: [commit 或文件]
```

文件不存在时先写 `# Architecture Retrospectives`。保持语气好奇、引导而非评判。
