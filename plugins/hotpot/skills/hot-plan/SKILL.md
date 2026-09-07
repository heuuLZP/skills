---
name: hot-plan
description: Use when canonical hotpot business artifacts are ready and the work needs a technical implementation plan covering directories, components, state, data flow, file responsibilities, business-entry coverage, comments, and verification points.
---

# Hotpot Plan

把 canonical 业务契约映射为可执行的技术设计，供 `/goal` 或编码 agent 实现。只做架构落点，不写代码，也不拆成微任务清单。

开始前按需读取 `../../references/shared-conventions.md` 中的 Context、Module、Artifact Resolution、Business Entry Resolution 和验证规则。写入时再读取 `../../references/output-style-guide.md` 和 `../../references/artifact-templates.md` 的“计划”模板。

## Workflow

1. 解析 requirement 与 scope；模块 scope 先做 Artifact Resolution 和 Business Entry Resolution。
2. 读取 `pre-analysis.md`、相关代码与 canonical business artifacts：single-file 读 spec/相关 use cases；entry-bundle 读 README、shared rules 和目标或全部相关 entries。`requirement.md` 只作范围背景。
3. 检查所有 canonical 问题区：
   - 若存在标记为 `是否阻断：是` and is not `已确认` 的问题，停止并返回 `hot-spec`。
   - 未确认的非阻断问题保留为依赖或风险，不替用户选择口径。
   - 临时问题区已删除表示完成沉淀；共享问题的确认记录可继续保留。
4. 检查相关代码以避免发明新架构，优先复用项目惯例。
5. 设计目录/文件职责、组件/钩子/服务、状态与数据流、请求/缓存/竞态处理；每项标注覆盖的 spec/rule/entry。
6. 拖拽、虚拟滚动、表单、数据请求、缓存和并发优先使用成熟库或现有 wrapper，除非 spec 要求自研。
7. 只对非显然逻辑要求注释/JSDoc；从 canonical 场景和共享规则定义验证点。
8. 按模板写 plan 与 Metadata，更新 module 指针。

## 架构决策门禁

在设计技术计划前，读取 `module-split.md` 的架构决策信号、`pre-analysis.md` 的架构事实和用户提供的上下文。

若命中以下任一高影响变更：系统边界、跨项目依赖、共享基础能力、数据 / 状态 / 业务规则所有权、构建 / 发布 / 部署 / 运行拓扑，或重要性能 / 可用性 / 安全 / 兼容性约束，则必须存在用户确认的“架构决策摘要”。摘要至少包含：决策、当前约束、比较过的方案、明确放弃、演进 / 兼容方式和验证指标。

若缺少摘要，停止生成 `plan.md`，明确提示用户显式运行 `$arch-coach decide`，再带回摘要继续；不自动调用 skill，不读取固定文件，也不把未确认的推断当作摘要。

存在摘要时，在计划中加入 `## 架构决策依据`，并将边界、约束、取舍、演进方式映射到架构、文件职责、组件、状态、数据流和验证计划。没有命中高影响条件时写“不适用”，保持现有流程。

## Verification Rule

默认运行应用/相关命令、走查场景、运行已有测试。只有 `hot-spec` 明确 `需单测：是` 时才规划新增单测及其覆盖行为。

若 `requirement.md` 与 canonical 业务产物冲突，停止并先修订 `hot-spec`。计划应足以实施而无需重做架构决策，但不得变成代码、spec 复述或执行 checklist。
