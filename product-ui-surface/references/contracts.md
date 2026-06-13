# Product UI Surface Contracts

Create these contracts before new multi-screen UI work, redesigns, or large UI edits. Keep them short enough for workers to read.

## Page Inventory

```markdown
# Page Inventory

entry:
- local_target:
- auth_state:
- viewport_targets:

routes:
- route:
  screen_name:
  pattern: shell | list | detail | form | settings | dialog | state
  priority: high | medium | low
  critical_actions:
  states:
  current_issues:
  verification:
```

For greenfield UI, use planned routes and screen names instead of discovered routes.

## Design System Contract

```markdown
# Design System Contract

product_type:
visual_direction:
- dense task surface, not marketing page
- [project-specific direction]

layout:
- page frame:
- navigation:
- content width:
- responsive rules:

components:
- buttons:
- inputs:
- tables/lists:
- cards/panels:
- dialogs:
- alerts/toasts:
- empty states:

interaction:
- primary action placement:
- destructive action pattern:
- loading/disabled behavior:
- validation feedback:
- keyboard/focus expectations:

avoid:
- one-off component styling
- nested decorative cards
- oversized hero/marketing sections for operational tools
```

## Surface Language Contract

```markdown
# Surface Language Contract

allowed_ui_terms:
- [real product nouns]
- [real actions]
- [real statuses]

forbidden_brief_terms:
- 帮助用户
- 提升效率
- 可控
- 低干扰
- agentic workflow
- 这个界面旨在
- 管理能力

copy_rules:
- Titles name objects or places.
- Buttons name actions.
- Status text names current state.
- Empty states describe state and one next action.
- Helper text may state format, limit, or immediate consequence.
- Do not explain product strategy, implementation details, or why the feature exists.

tone:
- product surface, not PRD
- concise, concrete, no tutorial voice
```

## Verification Report

```markdown
# Verification Report

target:
build_or_server:

screenshots:
- route:
  viewport:
  evidence:
  designer_pass:
  user_pass:
  issues:

interaction_checks:
- flow:
  result:
  evidence:

visible_text_audit:
- command:
- result:
- findings:

remaining_risks:
- ...
```

## Builder Input Filter

Before giving a worker a slice, remove or summarize:

- market positioning
- internal design rationale
- feature pitch language
- implementation architecture not needed for the slice
- phrases listed in `forbidden_brief_terms`

If a worker needs domain context, translate it into object/action/state language.
