# Product UI Surface Skill

Codex skill for creating, redesigning, and refactoring product UI as a real product surface.

It is not a microcopy-only skill and not an accessibility-only checklist. It guides agents to work through UI surface contracts, component consistency, interaction quality, rendered screenshot verification, and visible text leakage checks.

## Install

Copy the skill folder into a Codex skill directory:

```bash
cp -R product-ui-surface ~/.agents/skills/
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

## Audit Script

```bash
python3 product-ui-surface/scripts/audit_visible_text.py visible-text.txt --contract ui-surface/surface-language-contract.md
```

Use `--help` for allowlists, excludes, JSON output, and project-specific terms.
