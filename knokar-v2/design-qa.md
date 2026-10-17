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

## Feedback update — 2026-10-17

- `npm run check`: 0 errors, warnings, hints. `npm run build`: passed.
- Rendered desktop and 390px mobile hero inspected; responsive geometry at 320, 390, 768, 1024, 1440 and 1920px: no horizontal overflow, unbroken “in Motion”, copy and photo controls fit.
- All six hero images decode; next/previous wrap and update the name, count and shareable URL. Direct variant URLs restore the selection. Switching preserves scroll position.
- Services Mercedes and references Range Rover inspected in browser; original lower Bentley retained. Mission emblem and its mobile reserved space removed.
- Native preview resize timed out; mobile/responsive checks used same-origin iframes in the T3 preview.
- Local source updated only; published client presentation remains unchanged.

### Full-background correction — 2026-10-17

All six hero photographs now cover the complete banner on desktop and mobile (`inset: 0`, `object-fit: cover`, `sizes="100vw"`). Removed inset composition, image masks and edge fades. Retained a translucent contrast overlay and per-image mobile focal positions; restored the shorter mobile banner height. Browser geometry verified full coverage for all six variants at desktop and 390px mobile. `npm run check`: no diagnostics; `npm run build`: passed. No generated extensions needed.

### Expanded scenes and original hero — 2026-10-17

- Built-in Imagegen: five scene extensions inspected and saved as `src/assets/{porsche-profile,porsche-rear,mercedes-amg-studio,range-rover-alps,range-rover-road}-wide.png`; exact prompts/output manifest preserved in `../gen_photos/hero-outpaint-2026-10-17/prompts.json`.
- Original Rolls-Royce restored as `original-rolls`, with original image and crop settings. Real CLA photo unchanged; service/reference photos still use their prior source images.
- Browser: seven variants decode and cycle with accurate names/counts, wrapping and URL selection on desktop and 390px mobile. Full banner coverage retained; default Porsche and original Rolls inspected visually. Direct original variant URL restores correctly.
- `npm run check`: 0 errors, warnings, hints. `npm run build`: passed. Local preview only, no deployment.

### Czech / English — 2026-10-17

- `npm run check`: no diagnostics. Static build with `ASTRO_BASE=/web-design-pres/knokar-v2`: both language pages generated; locale and nested switcher URLs verified in output.
- T3 preview: CZ → EN → CZ switching preserves `?hero=original-rolls#sluzby`; correct claim, HTML language, page title and current-language state.
- English content/alternative-text audit: remaining Czech diacritics belong only to proper names, postal addresses and the native language label.
- English car details/specifications and enquiry prefill, menu Close state, all three testimonial quotes/roles and translated photo captions verified.
- Both languages at 320, 390, 768, 1024, 1440 and 1920px: no document overflow, hero heading/header fit. Language controls have 44×44px targets; English desktop/mobile and Czech desktop inspected visually.
- Seven photo variants and full-bleed treatment preserved. Local preview only; no deployment.

### Original photo exposure — 2026-10-17

Original Rolls-Royce now uses 20% of the shared overlay strength; other slides retain their prior overlays. CSS follows the visible slide without changing photo files. Desktop/mobile original inspected for legibility; switching restores normal opacity for the next slide. Static build passed.

### Laptop hero height — 2026-10-17

Desktop hero now uses `clamp(560px, 80svh, 780px)` instead of its width-driven aspect ratio. Photo comparison control stays absolutely positioned; reduced padding, label size and arrow icons make its pill smaller while retaining 44px button targets. Desktop intro top padding reduced to 48–80px; mobile hero height preserved.

Browser geometry in both languages at 1280×720, 1366×768, 1440×900, 1920×1080 and 390×844: heading and controls fit, no horizontal overflow. Hiding/showing the comparison control produces exactly the same hero height. At 1366×768, hero is 614px high and intro content begins at 662px. `npm run check`: no diagnostics. Static build passed. T3 screenshot capture failed/timed out; geometry inspection succeeded in a new preview tab.
