---
name: hot-module-split
description: Use when a requirement needs decomposition into modules, responsibility boundaries, dependencies, execution order, or when a resulting module may still contain multiple independently understandable business entries that need an artifact-mode recommendation before specs or plans.
---

# Hotpot Module Split

**Required reading:** `../../references/output-style-guide.md`, `../../references/shared-conventions.md`, `../../references/artifact-templates.md`.

This skill is part of the `hotpot` package. Install the whole package so shared references at `../../references/` are available.

## Purpose

Split a requirement into modules with clear ownership, boundaries, dependencies, recommended order, and a lightweight complexity check for business entries inside each module.

## Boundaries

Do:

- Define each module by responsibility, inputs, outputs, dependencies, and non-goals.
- Resolve ownership of shared concepts.
- Identify dependency order and parallelizable work.
- Identify business entry boundaries and recommend `single-file` or `entry-bundle` for each module.
- Save to `.hotpot/[req]/module-split.md` when useful.

Do not:

- Expand detailed flows, rules, interfaces, or implementation inside a business entry.
- Choose files, components, hooks, or services.
- Enumerate detailed use cases; use `hot-use-cases`.
- Execute code changes.

## Workflow

1. Resolve or create the requirement using `../../references/shared-conventions.md` Context Resolution; do not silently create or select context.
2. Read `.hotpot/[req]/requirement.md` if present; otherwise read the raw request. Also read any existing `.hotpot/[req]/pre-analysis.md`.
3. Identify candidate modules by business responsibility first, not by file names.
4. Check for ambiguous ownership: shared state, shared validation, cross-module data, UI vs service responsibilities.
5. Produce 2-7 modules. If there are more, split the requirement into separate requirements.
6. For each module, check the business-entry complexity signals in `../../references/shared-conventions.md` Artifact Resolution.
7. When `entry-bundle` is recommended, list only each entry ID, entry or main-flow name, independent responsibility, boundary, and shared-rule candidates.
8. Draw a dependency graph and suggest execution order. Business entries remain inside their module and do not enter the requirement dependency graph.
9. Include `Metadata` and update `.hotpot/[req]/_meta.md`.

## Boundary Rules

- One concept has one owner.
- A module should be explainable in one sentence.
- Avoid circular dependencies. If one appears, propose a boundary change.
- Use negative boundaries: explicitly state what a module does not do.
- Treat buttons, fields, API methods, and implementation files as insufficient business-entry boundaries by themselves.

## Output Requirements

Use the `Module Split` template from `../../references/artifact-templates.md`.

Include:

- Summary table.
- Mermaid dependency graph.
- Module details.
- Artifact mode recommendation and a lightweight business-entry index for complex modules.
- Boundary decisions.
- Suggested order.

## Suggested Next Steps

- For each module or for the full requirement: `hot-use-cases`.
- If implementation details are still unknown: `hot-pre-analysis` for a specific module.
