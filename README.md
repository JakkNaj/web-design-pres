# Web Design Presentations

Static client design previews deployed with GitHub Pages.

## Deployment

The repository uses `.github/workflows/deploy-pages.yml`.

- Pushing to `main` builds each Astro preview.
- The workflow assembles the output into `_site`.
- `actions/deploy-pages@v4` publishes `_site` to GitHub Pages.

Expected production URL:

```text
https://jakknaj.github.io/web-design-pres/
```

## Gólmanské tréninky — koncept 03

Tmavá varianta v Lumos pro Astro, dostupná z přehledu návrhů: https://jakknaj.github.io/web-design-pres/golmansketreninky-v3/. Workflow ji sestavuje se správnou vnořenou cestou a ověřuje místní odkazy i média.

## KNOKAR — první pracovní verze

Astro homepage based on variant D, copied from `knokar/web02` on 2026-10-13. Preview: https://jakknaj.github.io/web-design-pres/knokar/. The workflow builds with `ASTRO_BASE=/web-design-pres/knokar`. Contact submission remains disabled pending integration; telephone/email links work.

## KNOKAR v2 — finální design

Astro implementation of `knokar/design-prototype/Final.dc.html`, source in `knokar/web03`, copied 2026-10-15. Preview: https://jakknaj.github.io/web-design-pres/knokar-v2/. Workflow builds with `ASTRO_BASE=/web-design-pres/knokar-v2`. Includes responsive optimized images, self-hosted fonts, mobile navigation, inline vehicle details, inquiry prefill and an explicitly illustrative reference carousel. Contact/newsletter integrations and English translation remain pending.
