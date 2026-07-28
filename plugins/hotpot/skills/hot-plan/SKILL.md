---
name: hot-plan
description: Use when canonical hotpot business artifacts are ready and the work needs a technical implementation plan covering directories, components, state, data flow, file responsibilities, business-entry coverage, comments, and verification points.
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
2. For module scope, perform Artifact Resolution and Business Entry Resolution before reading business artifacts.
3. Read `pre-analysis.md` and canonical business artifacts:
   - single-file: `spec.md` and relevant `use-cases.md`,
   - entry-bundle: `README.md`, `shared-rules.md`, and the selected or all relevant entries.
   Read `.hotpot/[req]/requirement.md` only as scope/constraint background.
4. Inspect code paths needed to avoid inventing architecture.
5. Design files and responsibilities. Prefer existing project patterns and mark every responsibility and verification point with the business entries it covers.
6. Design state and data flow, including request/cache/race handling and contracts shared across entries.
7. Decide interaction infrastructure:
   - Use mature libraries or existing wrappers for drag/drop, virtual scroll, forms, data fetching, caching, and concurrency.
   - Do not hand-roll well-established infrastructure unless the spec requires it.
8. Add comment/JSDoc requirements only where logic is non-obvious.
9. Define verification points from canonical scenarios and shared rules.
10. Include `Metadata`; for module scope, update `.last-module`.

## P19 Verification Rule

Default verification is:

- run the app or relevant command,
- walk the enumerated scenarios,
- run existing tests.

Only require new unit tests when `hot-spec` explicitly says `需单测：是`. If it does, say where the tests belong and which behavior they cover.

If `requirement.md` conflicts with the canonical business artifacts, stop and recommend revising `hot-spec`; do not bypass confirmed decisions in the technical plan.

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
| Requiring `spec.md` in an entry-bundle | Resolve and read README, shared rules, and relevant entries |
| Creating one plan per entry mechanically | Organize by code architecture, but label business-entry coverage |

## Suggested Next Steps

- If risk is non-trivial: `hot-plan-review`.
- To implement: ask `/goal` to execute using the spec and plan.
