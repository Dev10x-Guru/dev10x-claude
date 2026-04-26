---
name: Dev10x:fanout
description: >
  Close multiple open loops in parallel — PRs waiting for review,
  issues ready for implementation, tickets needing attention. Honors
  dependencies, minimizes conflict risk, auto-advances by default.
  TRIGGER when: 2+ independent work items need parallel processing
  (PRs, issues, tickets).
  DO NOT TRIGGER when: single task or sequential dependency chain
  (use Dev10x:work-on).
user-invocable: true
invocation-name: Dev10x:fanout
allowed-tools:
  - AskUserQuestion
  - Skill(skill="Dev10x:work-on")
  - Skill(skill="Dev10x:gh-pr-respond")
  - Skill(skill="Dev10x:gh-pr-monitor")
  - Skill(skill="Dev10x:git-groom")
  - Skill(skill="Dev10x:git-commit")
  - Skill(skill="Dev10x:gh-pr-create")
  - Skill(skill="Dev10x:ticket-branch")
  - Skill(skill="Dev10x:gh-pr-merge")
  - Skill(skill="Dev10x:session-wrap-up")
  - Skill(skill="Dev10x:skill-audit")
  - Write(~/.claude/Dev10x/**)
  - mcp__plugin_Dev10x_cli__*
---

# Dev10x:fanout — Parallel Work Stream Orchestrator

Close multiple open loops in parallel while honoring
dependencies and minimizing conflicts. Each item runs its full
pipeline — no collapsed shipping sequence.

## Instructions

The full workflow — 6-phase execution model, permission-aware
dispatch, parallel group management, completion gate — lives in
[`instructions.md`](instructions.md).

When this skill is invoked, Read `instructions.md` now and
follow it end-to-end. `TaskCreate` calls and the Strategy
`AskUserQuestion` gate documented there are REQUIRED.
