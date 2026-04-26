---
name: Dev10x:gh-pr-merge
description: >
  Validate all pre-merge conditions and execute PR merge.
  Checks unresolved threads, CI status, draft state, mergeability,
  working copy, fixup commits, and review approval before merging.
  TRIGGER when: PR is ready to merge and needs pre-merge validation.
  DO NOT TRIGGER when: PR is still draft, CI is failing, or review
  comments are unaddressed.
user-invocable: true
invocation-name: Dev10x:gh-pr-merge
allowed-tools:
  - AskUserQuestion
  - Bash(gh pr view:*)
  - Bash(gh pr merge:*)
  - Bash(gh pr checks:*)
  - Bash(gh api graphql:*)
  - Bash(${CLAUDE_PLUGIN_ROOT}/skills/gh-pr-merge/scripts/:*)
  - mcp__plugin_Dev10x_cli__check_top_level_comments
  - Bash(gh repo view:*)
  - Bash(git status:*)
  - Bash(git log:*)
---

# Merge PR

Pre-merge validation gate that checks 8 conditions before
executing `gh pr merge`. Prevents premature merges by verifying
unresolved threads, CI, draft state, mergeability, working copy,
fixup commits, and review approval.

## Instructions

The full workflow — 8 pre-merge checks, strategy selection from
project settings, merge execution, post-merge verification —
lives in [`instructions.md`](instructions.md).

When this skill is invoked, Read `instructions.md` now and
follow it end-to-end. `TaskCreate` and `AskUserQuestion` calls
documented there are REQUIRED.
