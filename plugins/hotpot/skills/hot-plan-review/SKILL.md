---
name: hot-plan-review
description: Use when hotpot business artifacts or a technical plan need review for omissions, contradictions, uncovered business entries, inconsistent shared rules, risks, unclear boundaries, missing verification, or unimplementable instructions.
---

# Hotpot Plan Review

**Required reading:** `../../references/output-style-guide.md`, `../../references/shared-conventions.md`, `../../references/artifact-templates.md`, `../../references/review-checklist.md`.

This skill is part of the `hotpot` package. Install the whole package so shared references at `../../references/` are available.

## Purpose

Review the canonical business artifacts and plan before execution. Findings lead. This is a design/plan review, not a code review and not an implementation step.

## Boundaries

Do:

- Compare plan against canonical business artifacts and known code constraints.
- Find omissions, contradictions, boundary leaks, dependency risks, verification gaps, and unimplementable instructions.
- Save to the fixed `.hotpot` path when useful:
  - requirement scope: `.hotpot/[req]/plan-review.md`
  - module scope: `.hotpot/[req]/modules/[mod]/plan-review.md`

Do not:

- Modify code.
- Rewrite the whole plan unless the user asks.
- Dispatch review subagents in Codex.

## Workflow

1. Resolve requirement and scope using `../../references/shared-conventions.md` Context Resolution and Module Resolution; do not silently create or select context.
2. For module scope, perform Artifact Resolution and Business Entry Resolution.
3. Read `.hotpot/[req]/requirement.md`, `plan.md`, and `pre-analysis.md` when present. Read `spec.md` / `use-cases.md` in single-file mode or README, shared rules, and relevant entries in entry-bundle mode.
4. Use `../../references/review-checklist.md`. For an entire entry-bundle, verify every entry has a plan landing point and every shared rule has one consistent implementation approach.
5. Check that entry-local questions were not promoted to module-wide behavior, cross-entry contracts were not omitted, and unresolved questions were not silently decided.
   - Treat any plan produced while a blocking question is unconfirmed as a blocking review finding.
   - Verify that deleted single-file or entry-local question sections have source-Case-backed conclusions in canonical rules, interface dependencies, extra code-external work, or another formal contract section.
   - Allow confirmed shared-question records to remain in `共享待确认项`.
6. Lead with findings ordered by severity.
7. For each finding, include:
   - severity,
   - concrete issue,
   - evidence from spec/plan/code,
   - recommended fix.
8. Give a verdict:
   - ✅ 通过,
   - ⚠️ 有条件通过,
   - ❌ 需修改.
9. Include `Metadata`; for module scope, update `.last-module`.

## P20 Rule

In Codex, complete this review in place. Do not start a review subagent. If independent review is needed, the human decides manually.

## Output Requirements

Use the `Plan Review` template from `../../references/artifact-templates.md`.

If there are no issues, say that clearly and list residual risk or verification gaps.

## Suggested Next Steps

- If findings exist: revise `hot-spec` or `hot-plan`.
- If approved: use `/goal` to execute from the spec and plan.
