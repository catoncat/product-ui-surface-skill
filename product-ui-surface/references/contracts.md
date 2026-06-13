# Product UI Surface Contracts

Create these contracts before new multi-screen UI work, redesigns, or large UI edits. Keep them short enough for workers to read.

## Artifact Path Convention

For one screen, the surface contract may be inline. When artifacts are persisted, use `ui-surface/` for all of them:

- `ui-surface/page-inventory.md`
- `ui-surface/design-system-contract.md`
- `ui-surface/surface-language-contract.md`
- `ui-surface/forbidden-terms.txt`
- `ui-surface/verification-report.md`

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

brief_to_ui_translation:
- brief_phrase: 帮助用户高效管理能力
  forbidden_in_ui: true
  use_instead:
  - object: 能力
  - action: 新建能力 / 编辑能力 / 停用能力
  - state: 草稿 / 已发布 / 已停用

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

## Forbidden Terms File

Write `ui-surface/forbidden-terms.txt` with one forbidden visible-UI term per line, derived from `surface-language-contract.md`.

```text
帮助用户
提升效率
可控
低干扰
agentic workflow
这个界面旨在
管理能力
```

The audit script can also read `forbidden_brief_terms` directly with `--contract ui-surface/surface-language-contract.md`.

## Verification Report

```markdown
# Verification Report

target:
build_or_server:

screenshots:
- route:
  viewport:
  screenshot_path:
  browser_target:
  screen_region:
  designer_pass:
  - region:
    criterion:
    evidence:
    issue:
    fix_or_acceptance:
  user_pass:
  - task:
    step:
    visible_cue:
    result:
    issue:
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
