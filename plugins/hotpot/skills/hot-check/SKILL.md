---
name: hot-check
description: Use after implementation to check completed work against canonical hotpot business artifacts and plan, including whole-module or single-business-entry closure, shared-rule consistency, verification evidence, gaps, and change summary.
---

# Hotpot Check

核对实现是否闭合 canonical 业务产物和 plan。只检查约定范围，不做泛化代码质量 review 或深度调试。

开始前按需读取 `../../references/shared-conventions.md` 中的 Context、Module、Artifact Resolution、Business Entry Resolution 与验证规则，并读取 `../../references/review-checklist.md`。写入时再读取 `../../references/output-style-guide.md` 和 `../../references/artifact-templates.md` 的“检查”模板。

## Workflow

1. 解析 scope，识别实际改动并读取相关 diff。
2. 读取 `requirement.md`、`plan.md` 和 canonical business artifacts：single-file 使用 use cases/spec；entry-bundle 使用 README/shared rules/目标或全部相关 entries。
3. 在可行范围内运行或检查产物与 plan 要求的验证证据。
4. 核对场景闭环、行为契约、plan 职责、验证证据和偏离说明；每个选中 entry 独立闭环，shared rules 使用一致实现和验证结果。
5. 整 bundle 先按 entry 报告，再给 shared-rule 结论；单入口不加载或报告无关 entry。
6. 结论使用 `✅ 通过 / ⚠️ 有条件通过 / ❌ 未通过`。按模板写 Metadata；结论和缺口先行，变更摘要靠后，不粘贴长 diff。

## 架构决策闭环

若 `plan.md` 存在“架构决策依据”，核对实现是否遵守其中的边界、约束、取舍和演进 / 兼容方式；同时检查实际改动是否新增跨边界依赖、共享能力或运行风险。偏离时报告原因和影响，不重新设计架构、不自动调用 `$arch-coach`。

失败时指出具体 scenario、spec rule 或 plan responsibility，附文件/证据，并建议修订 spec、修订 plan、让 `/goal` 修复或进入常规系统化调试。Codex 中不启动 review subagent。
