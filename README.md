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

Current approved version from `knokar/web03`, synchronized 2026-10-17. Czech preview: https://jakknaj.github.io/web-design-pres/knokar-v2/; English: https://jakknaj.github.io/web-design-pres/knokar-v2/en/. Workflow builds with `ASTRO_BASE=/web-design-pres/knokar-v2`. Includes the seven-photo hero comparison, expanded generated scenes, compact laptop hero, full CZ/EN copy and language switching, responsive images, self-hosted fonts, mobile navigation, inline vehicle details, inquiry prefill and illustrative references. Contact/newsletter integrations remain pending.
