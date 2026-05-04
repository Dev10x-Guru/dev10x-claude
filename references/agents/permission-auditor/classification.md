# Allow Rule Classification & Toxicity Patterns

Reference material for the `permission-auditor` agent — Phases 3
and 4. The agent spec links here for the full category table,
the HOOK_ENABLED vs DEAD_RULE distinction, structural toxicity
patterns, and known-safe patterns.

## Phase 3: Allow Rule Classification

Classify every allow rule into risk categories:

| Category | Criteria | Example |
|----------|----------|---------|
| **DESTRUCTIVE** | Permits irreversible operations with no skill coverage | `Bash(rm -rf:*)` allows recursive deletion |
| **OVERLY_BROAD** | Single rule covers destructive + safe operations | `Bash(gh:*)` covers `gh repo delete` |
| **CONTRADICTS_POLICY** | Rule conflicts with CLAUDE.md instructions | `git config:*` when CLAUDE.md says "NEVER update git config" |
| **SKILL_REQUIRED** | Rule enables skill/worktree workflows — must not be removed | `Bash(git reset:*)` for rebase recovery in worktrees |
| **HOOK_ENABLED** | Allow rule exists so a PreToolUse hook can fire its redirect message | `Bash(git push:*)` enabled for SkillRedirectValidator |
| **DEAD_RULE** | Rule is overridden by a hook AND the hook does not depend on the allow rule to fire | `python3 -c "import json:*"` blocked by `block-python3-inline.py` |
| **WILDCARD_ESCAPE** | Variable prefix acts as wildcard for any command | `Bash(VARNAME=:*)` matches `VARNAME=x; rm -rf /` |
| **PRIVILEGE_ESCALATION** | Rule allows modifying permission settings themselves | `Write(~/.claude/**)` covers `settings.local.json` |
| **REDUNDANT** | Duplicate of another rule | Two identical `curl -sI` entries |
| **SAFE** | Appropriately scoped for its purpose | `Bash(git log:*)` |

### HOOK_ENABLED vs DEAD_RULE distinction

The permission layer runs before hooks. If a hook's redirect
message depends on the allow rule passing silently (e.g.,
SkillRedirectValidator), the rule is `HOOK_ENABLED` — removing
it replaces the educational redirect with a generic permission
prompt. Only classify as `DEAD_RULE` when the hook blocks
unconditionally regardless of whether the allow rule exists
(e.g., `block-python3-inline.py`). See ADR-0003 for the full
rationale.

For each non-SAFE rule, note:
- The specific dangerous command it permits
- Whether a deny rule could narrow it
- Whether the rule should be replaced with granular alternatives

## Phase 4: Toxicity Pattern Detection

For each allow rule classified as non-SAFE, determine if the
issue is **structural** (no allow rule can fix it) or
**rule-based** (fixable with rule changes).

### Structural patterns (require skill/hook updates, not rule changes)

- `PREFIX_POISONED_SUBSHELL`: `VAR=$(cmd) && script` — `$()`
  shifts prefix
- `PREFIX_POISONED_CHAIN`: `mkdir -p /tmp && script` — `&&`
  shifts prefix
- `PREFIX_POISONED_ENVVAR`: `ENV=val command` — env prefix
  breaks matching
- `PREFIX_POISONED_COMMENT`: `# comment\ncommand` — `#` breaks
  all matching
- `HOOK_BLOCKED_RETRY`: Pattern already blocked by hook, should
  never be attempted

### Rule-based patterns (fixable with allow/deny rule changes)

- `MISSING_DENY`: Destructive variant lacks a deny override
- `NEEDS_GRANULAR`: Broad rule should be split into safe
  subcommands
- `DEAD_RULE`: Hook blocks what the rule permits (hook does not
  depend on the allow rule)
- `HOOK_ENABLED`: Allow rule enables a hook's redirect message —
  do NOT recommend removal

## Known-Safe Patterns (Skip List)

These allow rules are legitimate and must NOT be flagged as
DESTRUCTIVE, OVERLY_BROAD, or CONTRADICTS_POLICY:

| Pattern | Classification | Rationale |
|---------|---------------|-----------|
| `Bash(git reset:*)` | SKILL_REQUIRED | Worktree rebase recovery needs `--hard`; skills gate destructive usage |
| `Bash(git reset --hard:*)` | SKILL_REQUIRED | Explicit variant of above — same rationale |
| `Bash(git reset --soft:*)` | SAFE | Non-destructive; moves HEAD only |
| `Bash(git -C:*)` | SKILL_REQUIRED | Cross-repo targeting when CWD is a different worktree; CLAUDE.md forbids redundant `-C` (when CWD matches), not all `-C` usage |

When encountering these patterns during Phase 3, classify them
per the table above — do not escalate to HIGH/CRITICAL.
