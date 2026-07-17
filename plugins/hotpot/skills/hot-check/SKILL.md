---
name: hot-check
description: Use after implementation to check completed work against hotpot use cases, spec, and plan, focusing on scenario closure, behavior contract, verification evidence, gaps, and change summary.
---

# Hotpot Check

**Required reading:** `../../references/output-style-guide.md`, `../../references/shared-conventions.md`, `../../references/artifact-templates.md`, `../../references/review-checklist.md`.

This skill is part of the `hotpot` package. Install the whole package so shared references at `../../references/` are available.

## Purpose

Check whether completed work satisfies the use cases, spec, and plan. This is completion checking, not generic code review and not bug debugging.

## Boundaries

Do:

- Compare actual changes and verification evidence against `use-cases.md`, `spec.md`, and `plan.md`.
- Walk primary, edge, failure, and race scenarios.
- Record gaps, deviations, and a concise change summary.
- Save to the fixed `.hotpot` path when useful:
  - requirement scope: `.hotpot/[req]/check.md`
  - module scope: `.hotpot/[req]/modules/[mod]/check.md`

Do not:

- Do broad code quality review.
- Debug failures deeply; if a bug appears, recommend `superpowers:systematic-debugging`.
- Start review subagents in Codex.

## Workflow

1. Resolve requirement and scope using `../../references/shared-conventions.md` Context Resolution and Module Resolution; do not silently create or select context.
2. Identify changed files from the workspace and read relevant diffs.
3. Read same-scope hotpot artifacts in this order when present:
   - `requirement.md`
   - `use-cases.md`
   - `spec.md`
   - `plan.md`
4. Run or inspect verification evidence requested by spec/plan when feasible.
5. Check:
   - scenarios close,
   - behavior contract holds,
   - plan responsibilities landed,
   - verification evidence supports the claim,
   - deviations are explained.
6. Produce a verdict:
   - ✅ 通过,
   - ⚠️ 有条件通过,
   - ❌ 未通过.
7. Include `Metadata`; for module scope, update `.last-module`.

## Output Requirements

Use the `Check` template from `../../references/artifact-templates.md`.

Lead with verdict and gaps. Put change summary near the end. Do not paste long diffs.

## Failure Handling

When check fails:

- Say exactly which scenario, spec rule, or plan responsibility failed.
- Point to the file or evidence that shows it.
- Suggest the next action:
  - revise spec,
  - revise plan,
  - ask `/goal` to fix,
  - or use `superpowers:systematic-debugging`.

## Suggested Next Steps

- If passed: human can review the summary and proceed with normal merge/commit flow.
- If conditional: address listed gaps or accept them as known follow-up.
- If failed: fix and rerun `hot-check`.
