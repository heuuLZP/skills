---
name: hot-spec
description: Use when a requirement or module needs a business specification or behavior contract before technical planning, including rules, boundaries, states, acceptance criteria, and verification expectations.
---

# Hotpot Spec

**Required reading:** `../../references/output-style-guide.md`, `../../references/shared-conventions.md`, `../../references/artifact-templates.md`.

This skill is part of the `hotpot` package. Install the whole package so shared references at `../../references/` are available.

## Purpose

Create the business specification or behavior contract. The spec answers what must be true, not how the code is organized.

## Boundaries

Do:

- Define behavior contract, business rules, boundaries, state/flow, acceptance criteria, and verification expectations.
- Use existing `requirement.md`, `use-cases.md`, `module-split.md`, and `pre-analysis.md` when available.
- Explicitly state whether new unit tests are required.
- Save to the fixed `.hotpot` path when useful:
  - requirement scope: `.hotpot/[req]/spec.md`
  - module scope: `.hotpot/[req]/modules/[mod]/spec.md`

Do not:

- Choose directories, components, hooks, services, or file responsibilities.
- Write implementation code.
- Default to “需单测”.

## Workflow

1. Resolve requirement and scope using `../../references/shared-conventions.md` Context Resolution and Module Resolution; do not silently create or select context.
2. Read `.hotpot/[req]/requirement.md` and same-scope scenario inputs when present. If no use cases exist, enumerate only the minimum scenarios needed for this spec; do not pretend a full `hot-use-cases` pass was done.
3. Write the behavior contract as user/system observable outcomes.
4. Capture business rules and exceptions.
5. Define state or flow with Mermaid when relevant.
6. State in-scope and out-of-scope boundaries.
7. Fill `Verification`:
   - Default: run app, walk scenarios, run existing tests.
   - Write `需单测：是` only when the requirement explicitly needs new unit tests, such as pure logic, complex state machines, or regression-sensitive rules.
8. Include `Metadata`; for module scope, update `.last-module`.

## Output Requirements

Use the `Spec` template from `../../references/artifact-templates.md`.

The spec must let `hot-plan` answer:

- Which behavior must be implemented?
- Which rules must not be violated?
- Which states and boundaries matter?
- How should completion be verified?

## Red Flags

- File paths or import statements appear in spec.
- Business rules are mixed with implementation preferences.
- Verification says “test it” without a concrete method.
- “需单测：是” appears without a reason.

## Suggested Next Steps

- If technical design is needed: `hot-plan`.
- If the spec feels risky or incomplete: `hot-plan-review` after plan, or revise spec first.
