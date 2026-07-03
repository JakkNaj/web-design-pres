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
