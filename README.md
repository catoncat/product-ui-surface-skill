# Product UI Surface Skill

Codex skill for creating, redesigning, and refactoring product UI as a real product surface.

It is not a microcopy-only skill and not an accessibility-only checklist. It guides agents to work through UI surface contracts, component consistency, interaction quality, rendered screenshot verification, and visible text leakage checks.

## Install

Install from GitHub with `npx skills`:

```bash
npx skills add catoncat/product-ui-surface-skill -g -a codex -y
```

Then invoke it explicitly:

```text
Use $product-ui-surface to create/redesign/refactor this product UI.
```

## What It Enforces

- Build from a compact UI surface contract before meaningful UI work.
- For multi-page work, persist contracts under `ui-surface/`.
- Treat Codex In-App Browser screenshots as the default local visual evidence.
- Review from both designer and user perspectives.
- Do not let product brief or PRD language leak into visible UI.
- Escalate whole-product work to a `codex-conductor` workflow/runtime when available.

## Optional Companion: Codex Conductor

For whole-product UI work with many routes, workers, waves, or durable state, install the companion conductor skill from its GitHub repository:

```bash
npx skills add catoncat/codex-conductor -g -a codex -y
```

`product-ui-surface` is the UI surface skill. `codex-conductor` is the orchestration skill that coordinates controller, builder, and verifier sessions for large scopes.

## Audit Script

```bash
python3 product-ui-surface/scripts/audit_visible_text.py visible-text.txt --contract ui-surface/surface-language-contract.md
```

Use `--help` for allowlists, excludes, JSON output, and project-specific terms.
