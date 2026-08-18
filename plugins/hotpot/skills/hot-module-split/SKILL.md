---
name: hot-module-split
description: Use when a requirement needs decomposition into modules, responsibility boundaries, dependencies, execution order, or when a resulting module may still contain multiple independently understandable business entries that need an artifact-mode recommendation before specs or plans.
---

# Hotpot Module Split

按业务职责拆分模块，明确归属、依赖、顺序和每个模块的 artifact mode 建议。不展开 entry 内部规则，不选择文件/组件，不写实现。

开始前读取 `../../references/shared-conventions.md` 的 Context Resolution，以及 Artifact Resolution 中的模式选择信号。写入时再读取 `../../references/output-style-guide.md` 和 `../../references/artifact-templates.md` 的“模块拆分”模板。

## Workflow

1. 解析 requirement；读取现有 `requirement.md`、`pre-analysis.md`，缺失时使用原始需求。
2. 按业务责任识别 2–7 个模块，而不是按文件名拆分；更多时建议拆成多个 requirement。
3. 为每个模块定义一句话职责、输入、输出、依赖和不做什么；解决共享状态、校验、跨模块数据及 UI/服务的归属。
4. 一个概念只设一个 owner；避免循环依赖，出现时调整边界。
5. 用 Artifact Resolution 的复杂度信号推荐 `single-file` 或 `entry-bundle`。复杂模块只列 entry ID/名称、独立职责、边界和共享规则候选，不展开流程与规则。
6. 画模块依赖图，标注顺序和可并行项；entry 保持在所属模块内。
7. 按模板写 `module-split.md`，包含 Metadata 并更新 `_meta.md`。

按钮、字段、API 方法或实现文件本身不足以成为模块或业务入口边界。
