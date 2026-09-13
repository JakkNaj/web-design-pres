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
