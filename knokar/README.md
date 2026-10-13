# KNOKAR web02

Customer preview copied from `knokar/web02`, based on Knokar design prototype variant D. Source brief and originals remain in the original Knokar project.

```sh
npm install
npm run dev -- --port 4325
npm run check
npm run build
npm run preview
```

Requires Node 22.12+ (or a newer supported Node release). Deploy the generated `dist/` folder.

- `src/pages/index.astro`: homepage composition.
- `src/layouts/SiteLayout.astro`: Czech document, metadata, local fonts and global styling.
- `src/components/`: individual homepage sections and reusable vehicle cards.
- `src/content/vehicles/*.json`: fleet cards, validated with Astro Content Layer and an image schema in `src/content.config.ts`.
- `src/assets/`: production copies of supplied photographs and logo artwork. Astro generates responsive WebP assets at build time.
- `src/styles/global.css`: variant D tokens, grid, responsive layouts and accessibility corrections.

No React runtime, backend, adapter or external font request. Only the mobile navigation and inquiry prefilling ship browser JavaScript.

## Design decisions

The explicit variant D reference takes precedence over the older homepage direction: Hanken Grotesk, pill buttons, glass header, variant D section order and all four selected vehicles are retained. Original prototype, `web/`, brief and archived material remain unchanged. Corrected the introduction's grammatical error and removed the unverified “current inventory” claim. Fixed clipped mobile philosophy text and mobile emblem placement.

## Before publication

Contact submission has no configured external service. The submit button is disabled and the form clearly directs visitors to working phone/email links; it never claims to send a message. Vehicle CTAs prefill the message without discarding the visitor's added text. Connect a submission service and provide the approved privacy information before enabling submission.

Confirm archived fleet specifications/availability, the supplied 19 years / 800+ claims, and the prototype's business address before publication. No testimonials, live availability or pricing were invented.

Section and header containers are fluid up to 1920px, then centered at that maximum width, with responsive 20–56px side gutters. Section backgrounds and hero photography remain full-width. Individual paragraph measures remain bounded for readability.

## GitHub Pages

Public preview: https://jakknaj.github.io/web-design-pres/knokar/

Build for the nested URL with `ASTRO_BASE=/web-design-pres/knokar npm run build`. The repository workflow builds and publishes this folder automatically on pushes to `main`.
