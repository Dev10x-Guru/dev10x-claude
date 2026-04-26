---
name: Dev10x:ticket-scope
description: >
  Scope Linear tickets with technical research and architecture design.
  Extends the base scope skill with Linear ticket integration, story
  point estimation, and acceptance criteria formatting.
  TRIGGER when: preparing to implement a Linear ticket — scoping
  technical approach, estimating story points, or writing acceptance
  criteria.
  DO NOT TRIGGER when: scoping non-Linear tickets, multi-ticket
  projects (use Dev10x:project-scope), or new domain areas (use
  Dev10x:ddd first).
user-invocable: true
invocation-name: Dev10x:ticket-scope
allowed-tools:
  - mcp__claude_ai_Linear__get_issue
  - mcp__claude_ai_Linear__list_issues
  - mcp__claude_ai_Linear__list_comments
  - mcp__claude_ai_Linear__save_comment
  - Skill(Dev10x:jtbd)
  - Agent
  - WebFetch
  - Grep
  - Glob
  - Read
  - Bash(mkdir -p:*)
---

# Ticket Scope — Linear Ticket Scoping Skill

Create comprehensive technical scoping documents for Linear
tickets. Extends the base `Dev10x:scope` skill with Linear-
specific workflows (ticket fetch, comment back, story point
estimation, acceptance criteria).

## Instructions

The full workflow — ticket fetch, context gathering, research
loop, story point sizing, AC generation, comment writeback —
lives in [`instructions.md`](instructions.md).

When this skill is invoked, Read `instructions.md` now and
follow it end-to-end. `TaskCreate` calls and `AskUserQuestion`
gates documented there are REQUIRED.
