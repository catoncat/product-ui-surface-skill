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

## Visible Text Review

Review text from the rendered DOM, copy files, or screenshots converted to text when practical. Judge it against `surface-language-contract.md`:

- Does the text speak as the product surface, or as a designer/PM explaining the surface?
- Does it name concrete objects, actions, states, limits, or recovery paths?
- Does it smuggle in strategy, implementation, orchestration, or marketing language?
- Does helper/error text clarify the current task without teaching the whole workflow?
- Would this wording still make sense if the original prompt were hidden?

This is an agent judgment pass. Do not claim the UI is good or bad because a phrase appears or does not appear. Explain the perspective problem, cite the screen region, and rewrite toward product-surface language when needed.

## Completion Standard

Do not mark a UI slice complete unless the closeout includes:

- focused build/test result
- screenshot evidence for each changed route/state/viewport, unless impossible
- if screenshot capture is impossible, browser target, viewport, exact reason, and live-observation notes
- designer pass notes
- user pass notes
- visible text review notes tied to `surface-language-contract.md`
- remaining risks
