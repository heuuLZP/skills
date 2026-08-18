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

## Verification Rule

默认运行应用/相关命令、走查场景、运行已有测试。只有 `hot-spec` 明确 `需单测：是` 时才规划新增单测及其覆盖行为。

若 `requirement.md` 与 canonical 业务产物冲突，停止并先修订 `hot-spec`。计划应足以实施而无需重做架构决策，但不得变成代码、spec 复述或执行 checklist。
