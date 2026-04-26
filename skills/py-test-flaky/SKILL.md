---
name: Dev10x:py-test-flaky
description: >
  Fix a flaky Python test end-to-end — investigate, reproduce, patch
  the root cause, and ship the fix with a tracker ticket, branch, and
  PR. Orchestrates Dev10x ticket, branch, commit, and PR skills so
  fixes follow project conventions without per-step coaching.
  TRIGGER when: user reports a flaky pytest test, a test is marked
  `@pytest.mark.flaky`, or a pytest case fails intermittently in CI.
  DO NOT TRIGGER when: test failure is deterministic, a non-pytest
  framework is in use, or the fix is already committed.
user-invocable: true
invocation-name: Dev10x:py-test-flaky
allowed-tools:
  - AskUserQuestion
  - Bash(pytest:*)
  - Bash(uv:*)
  - Skill(skill="Dev10x:ticket-create")
  - Skill(skill="Dev10x:ticket-branch")
  - Skill(skill="Dev10x:git-commit")
  - Skill(skill="Dev10x:gh-pr-create")
  - Skill(skill="Dev10x:gh-pr-monitor")
---

# Fix Flaky Python Test

Fix a flaky pytest test through the full shipping pipeline:
reproduce, root-cause, patch, file a tracker ticket, branch,
commit, and open a PR. Delegates tracker/git/PR operations to
sibling Dev10x skills so conventions stay consistent.

## Instructions

The full workflow — 8 steps covering reproduction, root-cause
analysis, fix patterns, verification, ticket, branch, commit,
and PR creation — lives in [`instructions.md`](instructions.md).

When this skill is invoked, Read `instructions.md` now and
follow it end-to-end. `AskUserQuestion` gates documented there
are REQUIRED.
