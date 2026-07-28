---
name: hot-use-cases
description: Use when a requirement or module needs scenario enumeration before spec or implementation, including main flows, branches, failures, races, non-goals, and acceptance scenarios; supports both single-file artifacts and selecting or updating one or more business entries in an entry-bundle.
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
- Save to the resolved `.hotpot` artifact path when useful:
  - requirement scope: `.hotpot/[req]/use-cases.md`
  - module single-file: `.hotpot/[req]/modules/[mod]/use-cases.md`
  - module entry-bundle: `.hotpot/[req]/modules/[mod]/README.md` and selected `entries/*.md`

Do not:

- Write the business contract; use `hot-spec`.
- Choose implementation files or libraries; use `hot-plan`.
- Add tests by default.

## Workflow

1. Resolve requirement and scope using `../../references/shared-conventions.md` Context Resolution and Module Resolution; do not silently create or select context.
2. For module scope, perform Artifact Resolution and Business Entry Resolution before reading or writing business artifacts.
3. If no module business artifacts exist, apply the mode-selection rules: use single-file for a simple module; propose `entry-bundle` for strong complexity signals and wait for confirmation unless the user already requested entry-based organization.
4. Read `requirement.md`, `module-split.md`, and relevant `pre-analysis.md` content when present.
5. In single-file mode, keep the existing workflow and `Use Cases` template.
6. In entry-bundle mode:
   - read `README.md`, `shared-rules.md`, and only the selected entries unless the user requested the whole module,
   - create or update the `Entry` template sections from “入口与目标” through “验收场景”,
   - preserve every section owned by `hot-spec`, including rules, questions, interface dependencies, verification, and business boundaries,
   - maintain the README entry index and summary without duplicating entry details.
7. Start with primary flows, then add branches, boundaries, failures, races, non-goals, and checkable acceptance scenarios.
8. Read the complete existing file before updating it; report conflicts instead of overwriting another skill's content.
9. Include `Metadata`; for module scope, update `.last-module`, and update `.last-entry` only for a selected entry.
10. For entry-bundle writes, run `../../scripts/validate_artifacts.py` against the module directory when the script is available.

## Output Requirements

Use the `Use Cases` template for single-file mode. Use the module README and Entry templates for entry-bundle mode.

Every acceptance scenario should be checkable later by `hot-check`.

## Common Mistakes

| Mistake | Correction |
|---|---|
| Only listing happy paths | Include branch, failure, and race cases |
| Writing implementation decisions | Stop at observable behavior |
| Treating scenarios as mandatory unit tests | Verification method is decided later in spec/plan |
| Reading or rewriting every entry for a single-entry request | Resolve and update only the selected entry plus shared context |
| Creating a navigation-only `use-cases.md` | In entry-bundle mode, do not create compatibility single files |

## Suggested Next Steps

- If behavior should be locked: `hot-spec`.
- If the scenario list exposes unclear ownership: `hot-module-split`.
