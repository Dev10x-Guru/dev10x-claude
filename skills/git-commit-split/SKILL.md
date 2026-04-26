---
name: Dev10x:git-commit-split
description: >
  Split monolithic git commits into atomic, cohesive commits following
  Clean Architecture principles. Uses interactive rebase to separate
  changes by feature dependency order (utilities → data → DTOs →
  refactoring → features → API), ensuring each commit is self-contained,
  passes tests, and maintains proper cohesion.
  TRIGGER when: a commit contains mixed concerns that should be separate
  atomic commits.
  DO NOT TRIGGER when: commits are already atomic, or grooming history
  without splitting (use Dev10x:git-groom).
user-invocable: true
invocation-name: Dev10x:git-commit-split
allowed-tools:
  - AskUserQuestion
  - mcp__plugin_Dev10x_cli__start_split_rebase
  - Bash(${CLAUDE_PLUGIN_ROOT}/skills/git-commit-split/scripts/:*)
---

# Split Commit Skill

Split monolithic git commits into atomic, cohesive commits that
follow Clean Architecture principles and dependency order. Each
resulting commit is self-contained, passes all tests, and
changes one well-scoped part of the code.

## Instructions

The full workflow — split-plan construction, interactive rebase
steps, per-commit validation, reorder rules — lives in
[`instructions.md`](instructions.md).

When this skill is invoked, Read `instructions.md` now and
follow it end-to-end. `TaskCreate` calls and the split-plan
`AskUserQuestion` gate documented there are REQUIRED.
