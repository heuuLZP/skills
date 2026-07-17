---
name: hot-requirement-analysis
description: Use when a raw product request, ticket, PRD, bug report, or conversation needs requirement understanding before hotpot pre-analysis, module split, use cases, spec, plan, or coding.
---

# Hotpot Requirement Analysis

**Required reading:** `../../references/output-style-guide.md`, `../../references/shared-conventions.md`, `../../references/artifact-templates.md`.

This skill is part of the `hotpot` package. Install the whole package so shared references at `../../references/` are available.

## Purpose

Understand a raw requirement before downstream hotpot work. Produce a short requirement card that captures source, goal, scope, constraints, ambiguities, and the safest next hotpot step.

## Boundaries

Do:

- Resolve the hotpot requirement context before writing.
- Resolve the raw requirement source before analysis.
- Extract goal, motivation, explicit in/out scope, constraints, assumptions, and ambiguous key terms.
- Mark open questions as blocking or non-blocking.
- Produce one triage verdict and save `.hotpot/[req]/requirement.md`.

Do not:

- Guess requirement content from a branch name, requirement slug, or existing spec/plan.
- Write behavior contracts, business rules, state machines, or acceptance criteria; use `hot-spec`.
- Inspect code; use `hot-pre-analysis`.
- Split modules; use `hot-module-split`.
- Enumerate full scenarios; use `hot-use-cases`.
- Trigger the next skill automatically.

## Workflow

1. Resolve or create the requirement using `../../references/shared-conventions.md` Context Resolution; do not silently create or select context.
2. Resolve the raw requirement source:
   - Use the user's current message when it contains the requirement.
   - Use a provided local file path, PRD, ticket, bug report, or pasted conversation when supplied.
   - For updates, read existing `.hotpot/[req]/requirement.md` only as prior context, not as the original source.
   - If no raw source is available, STOP and ask for the requirement source before writing.
3. Quote or precisely paraphrase the core ask; keep source attribution explicit.
4. Extract goal, scope, constraints, assumptions, and ambiguous key terms.
5. List open questions; mark each question's downstream impact and whether it blocks progress.
6. Choose exactly one verdict using this priority:
   - `clarify-first`: blocking ambiguity prevents safe downstream work.
   - `hot-module-split`: multiple responsibilities, modules, ownership boundaries, or dependency order are unclear.
   - `hot-pre-analysis`: existing system behavior, code location, data flow, or reuse risk must be known first.
   - `hot-use-cases`: branches, failures, races, or acceptance boundaries are the main risk.
   - `hot-spec`: requirement is small and clear enough to write a behavior contract.
7. Write the requirement card using the `Requirement` template from `../../references/artifact-templates.md`.
8. Include `Metadata` and update `.hotpot/[req]/_meta.md` `Updated`.

## Output Requirements

- Put `Summary` and verdict before details.
- Keep it short and scannable; this is a card, not a full spec.
- Include source locator, even when the source is the current conversation.
- Use `clarify-first` when a missing decision could change scope, user-visible behavior, or module ownership.
- If the source is vague but work can continue safely, list the default assumption in `Open Questions / Ambiguities`.

## Red Flags

| Red flag | Correction |
|---|---|
| Requirement content inferred from slug or branch | Ask for or read the raw source |
| No source locator | Add conversation/file/ticket attribution |
| Acceptance criteria or state machines appear | Move that work to `hot-spec` |
| File paths or code structure appear | Move that work to `hot-pre-analysis` |
| Multiple modules are designed in detail | Move that work to `hot-module-split` |
| Open questions are empty while the source is vague | Record ambiguity or stop for clarification |

## Suggested Next Steps

- `clarify-first`: ask the blocking questions before another hotpot skill.
- `hot-module-split`: split modules or sub-tasks.
- `hot-pre-analysis`: inspect existing implementation and risks.
- `hot-use-cases`: enumerate scenarios and acceptance boundaries.
- `hot-spec`: write the behavior contract.
