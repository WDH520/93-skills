# /plan Command

Initialize planning files for a new complex task.

## Usage

Type `/plan` or `/start` to invoke this skill.

## What It Does

1. Creates `task_plan.md` — Your roadmap with phases and goals
2. Creates `findings.md` — Storage for research and discoveries
3. Creates `progress.md` — Session log and test results
4. Optionally runs session catchup to recover previous context

## When to Use

Use this command when:
- Starting a multi-step task (3+ steps)
- Beginning a research project
- Building/creating a new project
- Task will span many tool calls
- Anything requiring organization
- Resuming work after a break

## Skip When

Don't use for:
- Simple questions
- Single-file edits
- Quick lookups

## After Initialization

1. Fill in the **Goal** section in `task_plan.md`
2. Update **Current Phase** to "Phase 1"
3. Start working through the phases
4. Update status after each phase: `pending` → `in_progress` → `complete`
5. Log findings immediately after discoveries

## Files Created

| File | Purpose |
|------|---------|
| `task_plan.md` | Task roadmap with phases |
| `findings.md` | Research and discoveries |
| `progress.md` | Session log and test results |

## Quick Start Workflow

```bash
# 1. Initialize planning files
/plan

# 2. Check for previous session context
python .trae/skills/planning-with-files/scripts/session-catchup.py

# 3. Start working on Phase 1
# ... work ...

# 4. Update phase status in task_plan.md after completion

# 5. Continue to next phase
```
