---
name: hot-use-cases
description: Use when a requirement needs scenario enumeration before spec or implementation, especially main flows, branches, edge cases, failures, race conditions, non-goals, and acceptance scenarios.
---

# Hotpot Use Cases

**Required reading:** `../../references/output-style-guide.md`, `../../references/shared-conventions.md`, `../../references/artifact-templates.md`.

This skill is part of the `hotpot` package. Install the whole package so shared references at `../../references/` are available.

## Purpose

Enumerate the scenarios a requirement must satisfy. This is the place where P19 gets its value: scenario discovery before implementation, without defaulting to new unit test files.

## Boundaries

Do:

- Capture primary flows, branches, edge cases, failure cases, race conditions, non-goals, and acceptance scenarios.
- Include user-visible behavior and system behavior.
- Save to the fixed `.hotpot` path when useful:
  - requirement scope: `.hotpot/[req]/use-cases.md`
  - module scope: `.hotpot/[req]/modules/[mod]/use-cases.md`

Do not:

- Write the business contract; use `hot-spec`.
- Choose implementation files or libraries; use `hot-plan`.
- Add tests by default.

## Workflow

1. Resolve requirement and scope using `../../references/shared-conventions.md` Context Resolution and Module Resolution; do not silently create or select context.
2. Read existing requirement-level `requirement.md`, `module-split.md`, and same-scope `pre-analysis.md` if present.
3. Start with primary user flows.
4. Add branches and boundaries: empty state, invalid input, permission, loading, cancellation, retry, offline, partial failure.
5. Add race cases when async work exists: old response after new request, double submit, rapid navigation, stale cache, concurrent writes.
6. Mark non-goals to prevent scope drift.
7. Convert the list into acceptance scenarios.
8. Include `Metadata`; for module scope, update `.last-module`.

## Output Requirements

Use the `Use Cases` template from `../../references/artifact-templates.md`.

Every acceptance scenario should be checkable later by `hot-check`.

## Common Mistakes

| Mistake | Correction |
|---|---|
| Only listing happy paths | Include branch, failure, and race cases |
| Writing implementation decisions | Stop at observable behavior |
| Treating scenarios as mandatory unit tests | Verification method is decided later in spec/plan |

## Suggested Next Steps

- If behavior should be locked: `hot-spec`.
- If the scenario list exposes unclear ownership: `hot-module-split`.
