---
name: human-review
description: AI-assisted human review of many pending Git changes before commit. Use when the user asks to review, inspect, stage, or commit changes interactively in small batches, especially when they want at most three files per batch, an explanation of what and why, and explicit human approval before every commit. Supports Codex and Claude Code.
---

# Human Review

Help the human understand and approve pending changes. Analyze and organize the work, but leave every commit decision to the human.

## Safety Contract

- Never commit without explicit approval for the currently displayed batch.
- Never use `git add .`, `git add -A`, `git commit -a`, or another broad staging command.
- Never discard file contents. Do not use `git reset --hard`, `git checkout --`, `git restore <path>`, or destructive equivalents.
- Keep each batch to at most three files. Prefer a smaller coherent batch over filling all three slots.
- Treat approval as single-use. Approval for one batch does not authorize later batches.
- Do not edit code as part of this workflow. If review finds a problem, report it and let the human decide what happens next.
- Do not start subagents for this review unless the human explicitly requests them.

## Workflow

### 1. Establish repository state

1. Confirm the working directory is inside a Git repository.
2. Read `git status --short`, unstaged changes, staged changes, untracked files, renames, and deletions.
3. If nothing is pending, say so and stop.
4. Record which paths or hunks were already staged before this skill started.

If the index already contains changes, preserve that boundary:

- Review the pre-existing staged set before staging anything new.
- If it contains at most three files and forms a coherent change, use it as the first batch.
- If it contains more than three files or mixes unrelated work, do not silently unstage or regroup it. Explain the conflict and ask the human how to split it.
- Never mix newly staged changes into a pre-existing staged batch without explicit approval.

### 2. Plan batches

Inspect the actual diffs and group the remaining paths by one coherent purpose, dependency, or behavior. Do not group mechanically by filename or merely to reach three files.

Apply these rules:

- Maximum three files per batch.
- Keep implementation and its directly coupled types or tests together when possible.
- Separate unrelated features, fixes, documentation, generated files, and configuration changes.
- Call out deletions, renames, dependency files, lockfiles, CI files, environment files, and generated artifacts.
- Keep one file in one batch by default. If a file contains unrelated changes that require hunk-level splitting, ask for permission before using patch staging.
- The batch plan is provisional. Re-read repository state after every commit because hooks or human edits may change it.

Briefly tell the human how many batches are currently expected and which files are in the first batch. Do not dump the entire diff.

### 3. Stage only the current batch

Stage only the exact paths in the current batch using path-scoped commands such as `git add -- <path>...`. Handle deletions with an exact path-scoped command. Quote unusual paths safely.

For tracked files that contain both intended and unrelated hunks, do not stage the whole path. Ask the human before using interactive or patch staging.

After staging:

1. Verify the index with `git diff --cached --name-status`.
2. Verify the staged diff with `git diff --cached`.
3. Confirm no path outside the approved current batch entered the index.
4. If the staged result is wrong, repair only staging state and explain what happened. Never discard working-tree content.

### 4. Present the batch

Summarize from the staged diff, not from filenames or assumptions. Use this compact structure:

```text
Batch 1 / about 4

Files
- path/to/file-a
  - Main change: ...
  - Why: ...
  - Review focus: ...
- path/to/file-b
  - Main change: ...
  - Why: ...
  - Review focus: ...

Cross-file behavior: ...
Suggested commit: fix: ...
Verification: ...
```

For each file, explain:

- the main behavioral or structural change,
- why the change appears necessary, grounded in code, nearby context, specs, plans, or tests,
- risks, uncertainty, or the exact area worth human attention.

Say when the reason is inferred rather than documented. Report review findings before the summary, ordered by severity and linked to exact files and lines when possible. Do not claim tests passed unless evidence exists.

### 5. Ask for the human decision

Use the host's structured question tool when available. In Claude Code, use its interactive question mechanism; in Codex, use the available user-input or structured-choice mechanism. Present exactly these three decisions, with wording adjusted naturally to the host:

1. `Approve and commit` - Commit only the currently staged batch with the suggested message, then continue to the next batch.
2. `Reject and stop` - Do not commit. Unstage only changes added to the index by this skill for the current batch, preserve all working-tree content, and end the workflow.
3. `Request changes` - Collect the human's free-form feedback about grouping, analysis, exclusions, review concerns, or commit message; apply it and present the batch again without committing.

The prompt must include the suggested commit message and make clear that the decision applies only to the current batch.

If the host cannot show structured choices, use the same three numbered choices in plain text and wait. Do not interpret vague replies such as `looks okay`, silence, or approval from an earlier batch as authorization to commit.

### 6. Apply the decision

For `Approve and commit`:

1. Recheck that the staged path list still matches the displayed batch.
2. Commit with the approved message.
3. Report the commit hash and subject.
4. Re-read Git status and diffs.
5. Continue with the next coherent batch, returning to staging and explanation.

For `Reject and stop`:

1. Unstage only paths or hunks newly staged by this skill for the current batch.
2. Preserve anything that was staged before the skill started.
3. Verify and report the resulting Git state, then stop.

For `Request changes`:

1. Collect the free-form opinion if it was not included with the choice.
2. Restate the requested adjustment briefly.
3. Change only staging state, grouping, explanation, or proposed commit message as requested.
4. Re-verify and re-present the batch.
5. Ask the same three-way question again.

### 7. Finish

After the last approved commit, verify the repository status and summarize the commits created. Clearly identify any remaining unstaged, staged, untracked, skipped, or conflicted changes.

## Stop Conditions

Stop without committing when:

- the repository has unresolved conflicts,
- safe batch boundaries cannot be determined without splitting a file and permission is absent,
- hooks or external edits change the staged content after it was presented,
- a commit fails,
- the human rejects the batch or asks to pause.

Explain the exact state and retain all work so the workflow can resume safely.
