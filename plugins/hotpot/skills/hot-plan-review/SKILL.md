---
name: hot-plan-review
description: Use when hotpot business artifacts or a technical plan need review for omissions, contradictions, uncovered business entries, inconsistent shared rules, risks, unclear boundaries, missing verification, or unimplementable instructions.
---

# Hotpot Plan Review

就地审查 plan 与 canonical 业务产物，findings 优先；不做代码 review、不改代码、不重写整个计划。

开始前按需读取 `../../references/shared-conventions.md` 中的 Context、Module、Artifact Resolution 与 Business Entry Resolution，并读取 `../../references/review-checklist.md`。写入时再读取 `../../references/output-style-guide.md` 和 `../../references/artifact-templates.md` 的“计划评审”模板。

## Workflow

1. 解析 scope；读取 `requirement.md`、`plan.md`、可用的 `pre-analysis.md`，以及当前 artifact mode 的 canonical spec/use cases 或 README/shared rules/entries。
2. 对照 checklist 查遗漏、矛盾、边界泄漏、依赖风险、验证缺口和不可实施内容。整 bundle 必须覆盖每个 entry，并为每条 shared rule 提供一致实现口径。
3. 检查局部问题是否被误提升、跨 entry 契约是否遗漏、未确认项是否被静默定案。Treat any plan produced while a blocking question is unconfirmed as a blocking review finding.
4. 若临时问题区已删除，确认每个结论已带来源 Case 落到正式契约；允许共享问题保留已确认记录。
5. findings 按严重度排序，每项包含具体问题、spec/plan/code 证据和修复建议。
6. 给出 `✅ 通过 / ⚠️ 有条件通过 / ❌ 需修改`，按模板写入并更新 Metadata/指针。

无问题时也要明确结论和残余风险或验证缺口。Codex 中由当前 agent 完成，不启动 review subagent。
