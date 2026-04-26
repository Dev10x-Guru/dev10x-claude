---
name: Dev10x:gh-pr-monitor
description: >
  Launch a background agent to monitor PR CI checks and review comments,
  automatically address issues with fixup commits, and notify team when
  ready. Use after creating a PR to automate the entire review cycle.
  TRIGGER when: PR has been created and needs CI/review monitoring.
  DO NOT TRIGGER when: PR does not exist yet (use Dev10x:gh-pr-create
  first), or user wants to manually handle review comments.
user-invocable: true
invocation-name: Dev10x:gh-pr-monitor
allowed-tools:
  - Agent
  - AskUserQuestion
  - mcp__plugin_Dev10x_cli__pr_notify
  - mcp__plugin_Dev10x_cli__detect_tracker
  - mcp__plugin_Dev10x_cli__pr_detect
  - Bash(${CLAUDE_PLUGIN_ROOT}/skills/gh-context/scripts/:*)
  - Bash(${CLAUDE_PLUGIN_ROOT}/skills/gh-pr-monitor/scripts/:*)
  - Bash(${CLAUDE_PLUGIN_ROOT}/skills/gh-pr-merge/scripts/:*)
  - mcp__plugin_Dev10x_cli__ci_check_status
  - mcp__plugin_Dev10x_cli__check_top_level_comments
  - Bash(gh:*)
  - Skill(Dev10x:qa-scope)
  - Skill(Dev10x:request-review)
  - Skill(Dev10x:verify-acc-dod)
---

# PR Review Monitor (Background Agent)

Launch a background agent that monitors a PR through its full
lifecycle — CI checks, review comments, team notification — so
the user can keep working.

## Instructions

The full workflow — background dispatch, polling loop, fixup
handling, team notification, verification — lives in
[`instructions.md`](instructions.md).

When this skill is invoked, Read `instructions.md` now and
follow it end-to-end. `TaskCreate` and `AskUserQuestion` calls
documented there are REQUIRED.
