---
name: hot-requirement-analysis
description: Use when a raw product request, ticket, PRD, bug report, or conversation needs requirement understanding before hotpot pre-analysis, module split, use cases, spec, plan, or coding.
---

# Hotpot Requirement Analysis

将原始输入整理成简短的需求卡片并给出一个路由结论。不检查代码，不写业务契约、完整场景、模块设计或技术方案。

开始前读取 `../../references/shared-conventions.md` 的 `Context Resolution` 与读写规则。写入时再读取 `../../references/output-style-guide.md` 和 `../../references/artifact-templates.md` 的“需求分析”模板。

## Workflow

1. 解析或创建 requirement，不静默选择上下文。
2. 确定原始来源：当前消息、用户提供的文件/PRD/工单/缺陷/对话。更新任务可把现有 `requirement.md` 当历史背景，但不能当原始来源；没有来源就停止询问。
3. 引用或精确转述核心诉求，提取目标、动机、范围内/外、约束、假设和歧义术语。
4. 列出问题及下游影响，标记是否阻断。
5. 按优先级选择且只选择一个结论：
   - `clarify-first`：缺失决定会改变范围、用户行为或模块归属。
   - `hot-module-split`：多个职责、边界、归属或依赖顺序不清。
   - `hot-pre-analysis`：必须先确认现有行为、代码、数据流或复用风险。
   - `hot-use-cases`：主要风险是分支、失败、竞态或验收边界。
   - `hot-spec`：需求小且清晰，可直接定义行为契约。
6. 原始输入已有多个独立入口或主流程时优先 `hot-module-split`，但本阶段不创建 entry 文件。
7. 按模板写 `requirement.md`，包含 source locator 与 Metadata，并更新 `_meta.md`。

## Quality Bar

- 摘要和结论先行；保持卡片化，不扩写成 spec。
- 模糊但可安全继续时明确默认假设；会影响关键决策时使用 `clarify-first`。
- 不从 branch、slug 或已有计划反推需求；不出现文件设计、状态机或验收契约。
