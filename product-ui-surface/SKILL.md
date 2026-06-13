---
name: product-ui-surface
description: Use when creating, redesigning, or refactoring product UI across one page, a module, or a whole app; when the user asks for visual polish, component consistency, interaction quality, designer/user-perspective screenshot review, or preventing product-brief language from leaking into visible UI.
---

# Product UI Surface

## Overview

Create or improve product UI as a product surface, not as a PRD, accessibility-only audit, or marketing rewrite. Optimize the rendered experience: visual hierarchy, component consistency, interaction paths, states, and visible text.

Core rule: separate `why this product exists` from `what the user sees`. Raw strategy, implementation details, and design intent may inform the work, but they must not leak into screen text, page structure, or review notes as if they were UI.

## Scope Router

Classify the request before editing.

| User request | Mode |
| --- | --- |
| New product UI, app screen, dashboard, or tool surface | Greenfield product UI |
| Existing component, small page, or focused state | Single-session improvement |
| Existing module or several related pages | Page-group redesign/refactor |
| Whole product, many routes, many workers, durable state, waves, or handoffs | Escalate to a `codex-conductor` workflow/runtime when available: controller owns contracts/state/waves; builders edit UI from filtered context; verifiers inspect rendered output |
| Only labels/buttons/errors/toasts, no layout or interaction work | Use `ui-microcopy` instead, or only for the text subtask |

Do not treat "from the user's perspective" as "do an accessibility checklist." Accessibility is a baseline guard when visible risk appears; this skill's main lens is product usability, visual design quality, and interaction reasonableness.

## Required Artifacts

For any meaningful UI creation, redesign, or refactor, create a compact UI surface contract before editing. For one screen, the contract may be inline in the plan. For new multi-screen UI, page-group redesign, or whole-product work, persist these artifacts under `ui-surface/`:

- `page-inventory.md`: routes, screens, dialogs, empty/error/loading states, critical flows.
- `design-system-contract.md`: layout, density, spacing, typography, components, interaction patterns, responsive rules.
- `surface-language-contract.md`: allowed UI terms, forbidden brief terms, visible text constraints.
- `forbidden-terms.txt`: one forbidden visible-UI term per line, derived from `surface-language-contract.md`, for mechanical scans.
- `verification-report.md`: screenshots reviewed, designer pass, user pass, regressions, remaining risks.

For whole-product work, let the conductor own `ui-surface/workflow-state.md`.

## Workflow

1. Inventory the existing UI or target product surface from routes, components, screenshots, domain objects, user tasks, and live app behavior when available.
2. Compile contracts before large edits. See `references/contracts.md`.
3. Slice the work by repeated screen pattern: app shell, navigation, list pages, detail pages, forms, settings, states, then sweep.
4. Build or improve toward the contract. Prefer existing design-system primitives and shared components over one-off styling.
5. Verify rendered UI with screenshots. Prefer Codex In-App Browser for local targets (`localhost`, `127.0.0.1`, `file://`) and no-login pages.
6. Run visible text leakage checks. Use `scripts/audit_visible_text.py` on extracted visible text or UI copy files.
7. Close each slice only after designer pass, user pass, and focused functional checks are recorded.

Read `references/workflow.md` for multi-page orchestration and role boundaries. Read `references/verification.md` before declaring visual work complete.

## Designer And User Pass

Every meaningful UI change needs both lenses:

- Designer pass: hierarchy, rhythm, alignment, density, component reuse, typography, contrast, responsive framing, state coverage.
- User pass: task path, affordance, decision load, feedback timing, error recovery, empty-state usefulness, whether visible words sound like product UI rather than a product brief.

Report these as evidence, not taste. Cite screenshot path or browser target, viewport, and the specific screen region reviewed.

## Hard Boundaries

- Do not change backend APIs, data models, auth, persistence, pricing, or business rules unless the user explicitly includes them.
- Do not turn operational tools into marketing pages. Admin/SaaS/productivity tools should stay dense, scannable, and task-focused.
- Do not introduce a new component system when the repo already has one unless the existing system cannot support the contract.
- Do not let raw prompt words such as `帮助用户`, `提升效率`, `可控`, `低干扰`, `agentic workflow`, or `这个界面旨在` appear in visible UI unless they are true product terminology.
- Do not call the work complete from code inspection alone; rendered screenshot verification is required when a local/browser target is available.

## Resources

- `references/workflow.md`: full-product and multi-page workflow, including conductor role boundaries.
- `references/contracts.md`: artifact templates and worker prompt shape.
- `references/verification.md`: visual, interaction, screenshot, and text-leak verification checklist.
- `references/examples.md`: short greenfield, conductor, worker, and verifier examples.
- `scripts/audit_visible_text.py`: deterministic scan for brief leakage and explanatory UI phrases.
