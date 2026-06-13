# Product UI Surface Verification

Rendered verification is required when a local or browser target is available.

## Browser Preference

Prefer Codex In-App Browser for:

- `localhost`, `127.0.0.1`, `::1`
- `file://` prototypes
- no-login or test-login product pages
- screenshot-based visual inspection

Use other browser automation only when the in-app browser cannot reach the target, cannot capture the needed evidence, or the user explicitly asks for another route.

## Designer Pass

Inspect screenshots and rendered pages for:

- visual hierarchy: primary task is obvious without explanatory text
- density: operational pages are compact but readable
- alignment and spacing: repeated structures line up across pages
- component consistency: same object/action uses same component pattern
- typography: headings fit the surface; no hero-scale text inside tool panels
- state coverage: empty, loading, error, disabled, selected, hover/focus
- responsive framing: mobile and desktop do not overlap or truncate key controls
- color use: not a one-note palette; status colors have clear meaning

Do not reduce this pass to "looks modern." Name the screen region and the concrete issue or evidence.

## User Pass

Walk the task as a user:

- entry point is findable
- primary action is clear
- next step follows from visible state
- feedback arrives after actions
- errors say what happened and how to recover
- destructive actions are hard to trigger accidentally
- empty states do not lecture or expose product strategy
- visible words feel like UI, not a PRD, demo script, or AI assistant explanation

This is not an accessibility-only pass. Basic accessibility issues can be reported, but do not let WCAG-style findings replace product usability judgment.

## Visible Text Audit

Collect text from the rendered DOM, copy files, or screenshots converted to text when practical. Then scan for:

- direct brief terms
- explanatory phrases such as `用于`, `旨在`, `帮助用户`, `用户可以`
- internal implementation terms
- product strategy or pitch language
- tutorial voice in labels, actions, and statuses

Use the bundled script for a deterministic first pass:

```bash
python3 product-ui-surface/scripts/audit_visible_text.py visible-text.txt --forbidden ui-surface/forbidden-terms.txt
```

The script is a guardrail, not the final reviewer. False positives should be reviewed, not ignored blindly.

## Completion Standard

Do not mark a UI slice complete unless the closeout includes:

- focused build/test result
- screenshot or live browser evidence
- designer pass notes
- user pass notes
- visible text audit result or reason it was not possible
- remaining risks
