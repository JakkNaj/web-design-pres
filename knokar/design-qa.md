# Variant D implementation QA

Reference: `../design-prototype/VariantD.dc.html` and its supplied assets; mobile reference imports the same design at 390px.

Compared full-page reference and implementation captures at 1440px and 390px. Preserved section sequence, images/crops, Hanken Grotesk hierarchy, glass header, ruled grids, palette and pill controls. Intentional differences: unavailable-form notice and disabled submit, corrected intro grammar, removal of unverified current inventory wording, mobile philosophy clipping fix and emblem positioning fix.

Browser checks: 1440, 1024, 768, 390 and 320px widths; no horizontal document overflow or broken visible images. Mobile navigation opens/closes, closes on section selection, and Escape restores trigger focus. All four vehicle CTAs prefill the correct model. All internal anchors resolve. No page JavaScript errors. Reduced-motion rendering checked.

Desktop initially inspected in the T3 shared browser. After it reported no available automation host during resizing, remaining checks ran with local Chromium/Playwright.

`npm run check` and `npm run build` pass. Submission integration remains explicitly unavailable, as documented in README.

Final result: passed.

## Fluid-width update

Removed the 1360px maximum width from shared section containers and the header. Gutters remain responsive (20–56px); edge-extending images now offset only those gutters. Browser geometry checks passed at 320, 390, 768, 1440, 1920, 2560 and 3440px with no horizontal overflow. Desktop containers occupy the full viewport; introduction content begins 56px from the left on wide screens. Paragraph measures remain constrained for readability. Production build passes.

## 1920px content cap

Supersedes the uncapped fluid-width update: shared section and header containers now use a centered 1920px maximum. Section backgrounds and hero photography remain viewport-wide. Verified centered container geometry, full-width hero and no horizontal overflow at 390, 1440, 1920, 2560 and 3440px; visually inspected the 2560px capture. Production build passes.

## Services spacing refinement

Replaced the bordered Services heading cells with an open responsive heading layout. Removed the service section's outer rules and image/list divider; retained only separators within the service list. Desktop visually verified in the shared browser; 390px layout verified in a same-origin iframe because preview resizing timed out. Heading stacks cleanly with no horizontal overflow. Production build passes.

## Wide-screen philosophy height

Capped the philosophy photo band at 720px on desktop (above 1100px), retaining its full-width image and existing text. At 2560px, the band is 720px tall instead of approximately 1097px. Verified the crop and heading fit in a 2560px browser iframe. Notebook widths below the cap and mobile retain their existing sizing. Production build passes.
