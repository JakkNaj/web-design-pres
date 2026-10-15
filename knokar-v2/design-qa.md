# Final design QA — 2026-10-15

Source: `../design-prototype/Final.dc.html` and `Final-Mobile.dc.html`. Preserved final section sequence, photography/crops, Hanken Grotesk, brand palette, glass header, service icons/cards, fleet, reference carousel and showroom composition. Implementation differences and pending integrations are recorded in README.

- `npm ci`, `npm run check`: 0 errors, warnings or hints.
- `ASTRO_BASE=/web-design-pres/knokar-v2 npm run build`: passed in both source and presentation copy.
- Production HTML/CSS audit: all 72 local asset references and 43 internal anchors resolve; IDs unique; no canvas bindings/blob URLs/runtime dependencies.
- T3 collaborative browser: desktop visual inspection and mobile rendering via same-origin 390px iframe (native preview resizing timed out). Services, hero and philosophy inspected visually.
- Geometry at 320, 390, 768, 1024, 1440 and 1920px: no horizontal document overflow; hero content and philosophy heading fit.
- Desktop service dropdown: click, Escape, expanded state and focus return passed.
- Mobile navigation: opens, closes with Escape/focus return, closes on section selection; header remains sticky.
- All four inline vehicle panels show correct model and eight specifications; selecting an inquiry closes the panel, fills the selected model and focuses the message field.
- Reference carousel next/previous wraps correctly: 02 / 03 → 03 / 03 → 01 / 03 → 03 / 03.
- All production images decode successfully. Self-hosted Czech fonts and nested asset URLs verified.

Forms remain explicitly disabled pending integration; client references/showroom visuals remain illustrative; English translation remains pending.
