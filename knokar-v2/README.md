# KNOKAR v2 — client preview

Approved source: `../../knokar/web03`, synchronized 2026-10-20 with the supplied subpage designs.

- Czech: https://jakknaj.github.io/web-design-pres/knokar-v2/
- English: https://jakknaj.github.io/web-design-pres/knokar-v2/en/
- Deployment: `.github/workflows/deploy-pages.yml`, push to `main`.

```sh
npm ci
npm run check
ASTRO_BASE=/web-design-pres/knokar-v2 npm run build
```

Seven full-bleed hero photos with manual review arrows and shareable `?hero=` selection. Five generated scenes have expanded surroundings; the original Rolls-Royce is included with a lighter overlay. The desktop hero follows viewport height, the compact photo picker stays inside it, and the lower Bentley photo is preserved.

Static Czech and English pages include translated headlines, metadata, navigation, alt text, photo captions, vehicle specifications, references and enquiry prefill. The language switcher preserves the selected photo and section. Responsive optimized WebP images, self-hosted Hanken Grotesk, accessible navigation and native TypeScript interactions.

Forms remain explicitly disabled pending submission integration. Client quotes, showroom imagery and the map remain illustrative. Fleet availability/prices require personal confirmation. Preview requests no search indexing.

See `design-qa.md` for verification history. Generated-image prompts remain in the source project at `../../knokar/gen_photos/hero-outpaint-2026-10-17/prompts.json`.

## Subpages — 2026-10-20

Eight supplied designs implemented, with long-term rental **variant B** and a different Rolls-Royce dusk photograph on the related long-term service in Financial services. Seven vehicles have individual detail routes; Czech and English versions total 30 static pages.

Header/footer/homepage navigation now opens the corresponding pages. Fleet brand filters, six-photo AMG gallery, related-car carousel, keyboard controls and vehicle inquiry prefill work without framework hydration. News cards link to the supplied archived articles. Forms remain disabled with visible contact alternatives.

Source copied from `../../knokar/web03/src/`. GitHub Pages publishes this version through the existing `deploy-pages.yml` workflow on `main`.
