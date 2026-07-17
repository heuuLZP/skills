---
name: hot-plan
description: Use when a behavior spec is ready and the work needs a technical implementation plan covering directory organization, components, state, data flow, file responsibilities, comments, and verification points.
---

# Hotpot Plan

**Required reading:** `../../references/output-style-guide.md`, `../../references/shared-conventions.md`, `../../references/artifact-templates.md`.

This skill is part of the `hotpot` package. Install the whole package so shared references at `../../references/` are available.

## Purpose

Produce a technical landing plan for `/goal` or a coding agent. This plan describes how the code should be organized and verified, but it does not write code and does not split work into an execution checklist.

## Boundaries

Do:

- Map spec behavior to directories, files, components, hooks, services, utils, state, and data flow.
- Choose interaction infrastructure and reuse existing project patterns.
- Identify key exported functions, complex logic, and places needing comments or JSDoc.
- Define verification points.
- Save to the fixed `.hotpot` path when useful:
  - requirement scope: `.hotpot/[req]/plan.md`
  - module scope: `.hotpot/[req]/modules/[mod]/plan.md`

Do not:

- Write code.
- Break the work into atomic execution tasks.
- Execute changes.
- Add new unit tests unless spec `Verification` explicitly says “需单测：是”.

## Workflow

1. Resolve requirement and scope using `../../references/shared-conventions.md` Context Resolution and Module Resolution; do not silently create or select context.
2. Read same-scope `spec.md` and `pre-analysis.md`; read `.hotpot/[req]/requirement.md` only as scope/constraint background.
3. Inspect code paths needed to avoid inventing architecture.
4. Design files and responsibilities. Prefer existing project patterns.
5. Design state and data flow, including request/cache/race handling.
6. Decide interaction infrastructure:
   - Use mature libraries or existing wrappers for drag/drop, virtual scroll, forms, data fetching, caching, and concurrency.
   - Do not hand-roll well-established infrastructure unless the spec requires it.
7. Add comment/JSDoc requirements only where logic is non-obvious.
8. Define verification points from spec scenarios.
9. Include `Metadata`; for module scope, update `.last-module`.

## P19 Verification Rule

Default verification is:

- run the app or relevant command,
- walk the enumerated scenarios,
- run existing tests.

Only require new unit tests when `hot-spec` explicitly says `需单测：是`. If it does, say where the tests belong and which behavior they cover.

If `requirement.md` appears to conflict with `spec.md`, stop and recommend revising `hot-spec`; do not bypass spec decisions in the technical plan.

## Output Requirements

Use the `Plan` template from `../../references/artifact-templates.md`.

The plan must be enough for `/goal` to implement without re-deciding architecture, but it must not become code or a micro-task checklist.

## Common Mistakes

| Mistake | Correction |
|---|---|
| Rewriting the spec in technical words | Map behavior to concrete code responsibilities |
| Listing “implement X” tasks | Keep to technical design, not execution checklist |
| Defaulting to new unit tests | Follow spec Verification |
| Ignoring existing patterns | Inspect and reuse project conventions |

## Suggested Next Steps

- If risk is non-trivial: `hot-plan-review`.
- To implement: ask `/goal` to execute using the spec and plan.
