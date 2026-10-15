# KNOKAR — web03

Static Astro implementation of `../design-prototype/Final.dc.html` (2026-10-15). The selected final design supersedes the earlier homepage layout: Hanken Grotesk, Rolls-Royce dusk hero, glass navigation, service tiles and emblem card, brand portfolio, four vehicles with inline details, historical news, illustrative reference carousel, philosophy, contact/showroom and footer.

```sh
npm ci
npm run dev
npm run check
npm run build
```

Images are imported and optimized with responsive WebP variants. Fonts include Czech glyphs and are self-hosted. Native TypeScript handles navigation, Escape/focus return, vehicle details, inquiry prefill and reference cycling. No framework hydration or backend required.

Client presentation copy lives in `../../web-design-pres/knokar-v2/`, labeled **KNOKAR v2**. Build with `ASTRO_BASE=/web-design-pres/knokar-v2`. Public URL: https://jakknaj.github.io/web-design-pres/knokar-v2/ . The preview requests no search indexing.

## Pending real content/integrations

- Inquiry and newsletter submissions are disabled with visible explanations; no data is sent or saved. Telephone and email work.
- Client references are explicit design placeholders, not real endorsements. Showroom photography and the map are illustrative.
- English translation was not supplied; EN is disabled and labeled as forthcoming.
- Fleet images/specifications and news retain the supplied design's archived content; availability/prices require personal confirmation.

Original design, brand documents, photos and previous website versions are preserved. Small implementation adjustments: corrected introductory grammar, removed unverified current-inventory wording, mobile hero height and philosophy text overflow, scrollable mobile navigation, native hidden states and focus handling.
