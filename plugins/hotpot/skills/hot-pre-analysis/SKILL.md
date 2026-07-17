---
name: hot-pre-analysis
description: Use when a requirement needs codebase reconnaissance before use cases, specs, or planning, especially when existing implementation, data flow, dependencies, reuse points, or risks are unclear.
---

# Hotpot Pre Analysis

**Required reading:** `../../references/output-style-guide.md`, `../../references/shared-conventions.md`, `../../references/artifact-templates.md`.

This skill is part of the `hotpot` package. Install the whole package so shared references at `../../references/` are available.

## Purpose

Produce a factual snapshot of the current system around a requirement. This skill answers “what already exists, where is it, how does it work, what can be reused, and what risks are visible?”

## Boundaries

Do:

- Inspect relevant files, docs, routes, APIs, data models, tests, and config.
- Separate verified facts from assumptions.
- Map code structure, data flow, dependencies, reuse points, and risks.
- Save to the fixed `.hotpot` path when the result will feed later work:
  - requirement scope: `.hotpot/[req]/pre-analysis.md`
  - module scope: `.hotpot/[req]/modules/[mod]/pre-analysis.md`

Do not:

- Enumerate user scenarios; use `hot-use-cases`.
- Split modules; use `hot-module-split`.
- Propose business spec or technical solution.
- Start implementation.

## Workflow

1. Resolve requirement and optional module scope using `../../references/shared-conventions.md` Context Resolution; do not silently create or select context.
2. Read `.hotpot/[req]/requirement.md` if present; use it to focus the code search, not as a substitute for verified code facts.
3. Search the codebase with fast text/file search before drawing conclusions.
4. Read the smallest useful set of files that establish current behavior.
5. Produce a structured `Pre Analysis` artifact using `../../references/artifact-templates.md`.
6. Include `Metadata` with requirement, scope, module, skill, created date, and updated date.
7. List open questions only when they affect later spec or plan decisions.

## Output Requirements

- Put `Summary` first.
- Every factual claim should cite a file path, doc path, or observed command.
- Use Mermaid for structure, dependency, or data-flow relationships.
- Mark assumptions explicitly as assumptions.

## Completion Criteria

- A reader can find the relevant code areas without repeating the search.
- Existing behavior and reuse points are clear.
- Risks and unknowns are concrete enough to guide the next skill.

## Suggested Next Steps

- If the scope is too broad: `hot-module-split`.
- If behavior boundaries are the main risk: `hot-use-cases`.
- If behavior is already clear: `hot-spec`.
