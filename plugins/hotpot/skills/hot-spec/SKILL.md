---
name: hot-spec
description: Use when a requirement or module needs a business specification or behavior contract before technical planning, including shared and entry-local rules, boundaries, states, interface dependencies, acceptance criteria, and verification; supports both single-file artifacts and business-entry bundles.
---

# Hotpot Spec

**Required reading:** `../../references/output-style-guide.md`, `../../references/shared-conventions.md`, `../../references/artifact-templates.md`.

This skill is part of the `hotpot` package. Install the whole package so shared references at `../../references/` are available.

## Purpose

Create the business specification or behavior contract. The spec answers what must be true, not how the code is organized.

## Boundaries

Do:

- Define behavior contract, business rules, boundaries, state/flow, acceptance criteria, and verification expectations.
- Use existing canonical business artifacts, `requirement.md`, `module-split.md`, and `pre-analysis.md` when available.
- Explicitly state whether new unit tests are required.
- Save to the resolved `.hotpot` artifact path when useful:
  - requirement scope: `.hotpot/[req]/spec.md`
  - module single-file: `.hotpot/[req]/modules/[mod]/spec.md`
  - module entry-bundle: `.hotpot/[req]/modules/[mod]/shared-rules.md` and selected `entries/*.md`

Do not:

- Choose directories, components, hooks, services, or file responsibilities.
- Write implementation code.
- Default to “需单测”.

## Workflow

1. Resolve requirement and scope using `../../references/shared-conventions.md` Context Resolution and Module Resolution; do not silently create or select context.
2. For module scope, perform Artifact Resolution and Business Entry Resolution before reading or writing business artifacts.
3. If no module business artifacts exist, follow the same mode-selection rules as `hot-use-cases`; do not create an entry-bundle without explicit user direction or confirmation.
4. Read `.hotpot/[req]/requirement.md` and canonical scenario inputs when present. If no use cases exist, enumerate only the minimum scenarios needed; do not pretend a full `hot-use-cases` pass was done.
5. In single-file mode, keep the existing `Spec` workflow and template.
6. In entry-bundle mode:
   - place rules or questions used by two or more entries in `shared-rules.md`,
   - place entry-local behavior, rules, questions, interface dependencies, verification, and business boundaries in the selected entry,
   - preserve the entry goal, flows, branches, failures, races, non-goals, and acceptance scenarios owned by `hot-use-cases`,
   - keep cross-Case information in README boundaries and never use it as confirmation evidence for the current Case.
7. Record each open question's type, source Case, affected entries, current wording, and confirmation status. Do not label an inference as PRD-confirmed.
8. Check for duplicated shared rules, entry-local interface questions detached from their entry, and a rules-by-type layout that hides entry context.
9. Fill `Verification`:
   - Default: run app, walk scenarios, run existing tests.
   - Write `需单测：是` only when the requirement explicitly needs new unit tests, such as pure logic, complex state machines, or regression-sensitive rules.
10. Read the complete existing file before updating it; report conflicts instead of overwriting another skill's content.
11. Include `Metadata`; for module scope, update `.last-module`, and update `.last-entry` only for a selected entry.
12. For entry-bundle writes, run `../../scripts/validate_artifacts.py` against the module directory when the script is available.

## Output Requirements

Use the `Spec` template for single-file mode. Use the module README, Shared Rules, and Entry templates for entry-bundle mode.

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
- A module has multiple independent entries but rules are still flattened by rule type.
- The same detailed rule appears in multiple entries instead of `shared-rules.md`.
- An entry-local interface question is moved into a context-free module summary.
- A navigation-only `spec.md` is created for entry-bundle compatibility.

## Suggested Next Steps

- If technical design is needed: `hot-plan`.
- If the spec feels risky or incomplete: `hot-plan-review` after plan, or revise spec first.
