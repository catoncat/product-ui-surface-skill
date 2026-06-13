# Product UI Surface Workflow

Use this reference when creating, redesigning, or refactoring product UI across a module, many pages, or an entire product.

## Workflow Modes

### Single-session surface work

Use for one new screen, small existing page, or component. The same session may inventory, edit, and verify, but it still needs a compact contract and rendered verification.

### Page-group surface work

Use for several related screens. Create shared contracts, then build or improve repeated patterns together so lists, details, forms, dialogs, and states converge.

### Whole-product surface work

Use `codex-conductor`. The current controller owns state, contracts, prompts, wave slicing, evidence reconciliation, and final closeout. Execution sessions own product edits. Verifier sessions own rendered evidence.

The controller should not edit product UI in conductor mode unless explicitly assigned a small implementation slice.

## Recommended Waves

1. App shell, navigation, page frame, global spacing, responsive frame.
2. Design-system primitives and shared component wrappers.
3. List/table/index pages.
4. Detail/record pages.
5. Forms, settings, create/edit flows.
6. Empty, loading, error, disabled, permission, and destructive states.
7. Final sweep for visual consistency, interaction regressions, and visible text leakage.

Adjust waves to match the product. Do not split by arbitrary file count when screen patterns are more meaningful.

## Context Permissions

Use context isolation to reduce brief leakage.

### Controller may see

- Raw product brief and goals.
- Repo rules and project constraints.
- Existing UI, screenshots, route inventory, design notes.
- User preferences and risk boundaries.

### UI builder should see

- The slice assignment.
- Relevant files/routes/screenshots.
- `design-system-contract.md`.
- `surface-language-contract.md`.
- Required behavior to preserve.
- Verification commands and browser target.

The builder should not receive long raw strategy text, product-market framing, or phrases that should be forbidden in UI.

### Verifier should see

- Browser target and routes.
- Contract files.
- Expected critical flows.
- Built artifacts or branch/worktree details.

The verifier should inspect rendered output rather than trusting implementation notes.

## Slice Prompt Shape

Use this shape when assigning a UI worker:

```markdown
Goal:
Create or improve [routes/screens/components] to match the UI contracts.

Write scope:
- [files or folders]

Read first:
- AGENTS.md and project rules
- ui-surface/design-system-contract.md
- ui-surface/surface-language-contract.md
- relevant component and route files

Preserve:
- existing APIs
- existing data model
- current business flow
- critical interactions listed below

Do not:
- add marketing copy
- expose brief/internal terms
- make accessibility the only optimization lens
- change backend contracts

Verification:
- run focused tests/build checks
- verify rendered page in Codex In-App Browser when target is local
- record designer pass and user pass evidence
```

## Controller Closeout

Before moving to the next wave, reconcile:

- changed files and ownership
- screenshots or browser observations
- visible text audit result
- known regressions
- follow-up fixes

Do not batch unresolved visual issues into the final sweep if they affect shared components; fix shared component drift early.
