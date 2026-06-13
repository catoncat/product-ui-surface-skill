# Product UI Surface Examples

Keep examples short. They show shape, not a full tutorial.

## Greenfield One Screen

Raw brief:

```text
Build a skill toggle dashboard that helps developers efficiently manage agent capabilities with low-friction control.
```

Compact surface contract:

```markdown
object/action/state:
- object: Skill
- actions: 启用 / 停用 / 查看详情
- states: 已启用 / 已停用 / 不可用

forbidden_brief_terms:
- helps developers
- efficiently manage
- agent capabilities
- low-friction control
- 帮助开发者
- 高效管理

brief_to_ui_translation:
- brief_phrase: efficiently manage agent capabilities
  forbidden_in_ui: true
  use_instead:
  - object: Skill
  - action: 启用 / 停用
  - state: 已启用 / 已停用
```

## Whole-Product Conductor Shape

```markdown
controller:
- reads raw brief and repo rules
- writes ui-surface/page-inventory.md
- writes ui-surface/design-system-contract.md
- writes ui-surface/surface-language-contract.md
- slices waves by screen pattern

builder:
- reads only assigned routes, files, screenshots, and contracts
- does not receive raw product pitch language
- edits UI and records focused checks

verifier:
- opens rendered pages in Codex In-App Browser
- captures screenshots or records why capture failed
- writes designer/user findings into ui-surface/verification-report.md
```

## Worker Prompt

```markdown
Goal:
Create or improve `/settings/skills` to match the UI surface contracts.

Write scope:
- app/settings/skills/**
- components/skills/**

Read first:
- ui-surface/design-system-contract.md
- ui-surface/surface-language-contract.md
- relevant route and component files

Preserve:
- current API calls
- current auth behavior
- enable/disable flow

Do not:
- expose brief terms
- add marketing copy
- make accessibility the only optimization lens

Verification:
- run focused tests/build
- inspect with Codex In-App Browser
- run visible text audit
```

## Verifier Report

```markdown
screenshots:
- route: /settings/skills
  viewport: 1440x900
  screenshot_path: ui-surface/screenshots/settings-skills-1440.png
  browser_target: http://localhost:3000/settings/skills
  screen_region: skills table and toolbar
  designer_pass:
  - region: toolbar
    criterion: hierarchy
    evidence: primary action is visually distinct and aligned with filters
    issue: none
    fix_or_acceptance: accepted
  user_pass:
  - task: disable a skill
    step: locate current state and disable action
    visible_cue: row status uses 已启用 and action uses 停用
    result: action is discoverable without explanatory copy
    issue: none

visible_text_audit:
- command: python3 product-ui-surface/scripts/audit_visible_text.py visible-text.txt --contract ui-surface/surface-language-contract.md
- result: pass
```
