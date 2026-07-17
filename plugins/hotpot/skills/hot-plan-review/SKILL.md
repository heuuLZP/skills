---
name: hot-plan-review
description: Use when a hotpot spec or technical plan needs review for omissions, contradictions, risks, unclear boundaries, missing verification, or parts that cannot be implemented as written.
---

# Hotpot Plan Review

**Required reading:** `../../references/output-style-guide.md`, `../../references/shared-conventions.md`, `../../references/artifact-templates.md`, `../../references/review-checklist.md`.

This skill is part of the `hotpot` package. Install the whole package so shared references at `../../references/` are available.

## Purpose

Review the spec and plan before execution. Findings lead. This is a design/plan review, not a code review and not an implementation step.

## Boundaries

Do:

- Compare plan against spec, use cases, and known code constraints.
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
2. Read `.hotpot/[req]/requirement.md` if present, then same-scope `spec.md` and `plan.md`; read same-scope `use-cases.md` and `pre-analysis.md` if present.
3. Use `../../references/review-checklist.md`.
4. Lead with findings ordered by severity.
5. For each finding, include:
   - severity,
   - concrete issue,
   - evidence from spec/plan/code,
   - recommended fix.
6. Give a verdict:
   - ✅ 通过,
   - ⚠️ 有条件通过,
   - ❌ 需修改.
7. Include `Metadata`; for module scope, update `.last-module`.

## P20 Rule

In Codex, complete this review in place. Do not start a review subagent. If independent review is needed, the human decides manually.

## Output Requirements

Use the `Plan Review` template from `../../references/artifact-templates.md`.

If there are no issues, say that clearly and list residual risk or verification gaps.

## Suggested Next Steps

- If findings exist: revise `hot-spec` or `hot-plan`.
- If approved: use `/goal` to execute from the spec and plan.
