#!/usr/bin/env python3
"""Verify archive completeness, source coverage, file checksums and catalogue links."""
import hashlib
import json
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit
from bs4 import BeautifulSoup

R = Path(__file__).resolve().parents[1] / 'content' / 'wordpress'
load = lambda name: json.loads((R / name).read_text())
records, media, galleries = [load('data/' + name + '.json') for name in ('records', 'media', 'galleries')]
errors = []
for m in media:
    if not m.get('local_path'):
        errors.append({'kind': 'missing_media', 'url': m['source_url']})
        continue
    path = R / m['local_path']
    if not path.exists():
        errors.append({'kind': 'missing_file', 'path': m['local_path']})
    elif path.stat().st_size != m['bytes'] or hashlib.sha256(path.read_bytes()).hexdigest() != m['sha256']:
        errors.append({'kind': 'checksum', 'path': m['local_path']})

for kind in ('posts', 'pages'):
    raw_ids = {x['id'] for x in load('raw/' + kind + '.json')}
    archived_ids = {x.get('id') for x in records if x['type'] == kind[:-1]}
    if raw_ids != archived_ids:
        errors.append({'kind': 'rest_coverage', 'collection': kind, 'missing': list(raw_ids - archived_ids)})

for sitemap, urls in load('data/sitemaps.json').items():
    if any(k in sitemap for k in ('-posts-post-', '-posts-page-', '-posts-event-', '-posts-location-')):
        missing = set(urls) - {r['source_url'] for r in records}
        # The home page is a post index, archived as HTML plus its individual posts.
        if 'https://www.golmansketreninky.cz/' in missing:
            for meta in (R / 'raw/http').glob('*.json'):
                cached = json.loads(meta.read_text())
                if cached['url'] == 'https://www.golmansketreninky.cz/' and cached['ok'] and (R / cached['raw_file']).exists():
                    missing.remove(cached['url'])
                    break
        if missing:
            errors.append({'kind': 'sitemap_coverage', 'sitemap': sitemap, 'missing': sorted(missing)})

gallery_photos = 0
for g in galleries:
    urls = [x['source_url'] for x in g['images']]
    if len(urls) != len(set(urls)):
        errors.append({'kind': 'duplicate_gallery_photo', 'gallery': g['id']})
    for image in g['images']:
        if not image.get('local_path') or not (R / image['local_path']).exists():
            errors.append({'kind': 'missing_gallery_photo', 'gallery': g['id'], 'url': image['source_url']})
        else:
            gallery_photos += 1

for r in records:
    if not (R / r['markdown_path']).exists():
        errors.append({'kind': 'missing_markdown', 'path': r['markdown_path']})

# Check generated static catalogue links as a browser resolves them (percent decoding).
for path in [R / 'index.html', R / 'media.html', *sorted((R / 'galerie').glob('*.html'))]:
    doc = BeautifulSoup(path.read_text(), 'html.parser')
    for el in doc.select('[href], img[src]'):
        value = el.get('href', el.get('src', ''))
        p = urlsplit(value)
        if p.scheme or p.netloc or not p.path:
            continue
        target = (path.parent / unquote(p.path)).resolve()
        if not target.exists():
            errors.append({'kind': 'broken_catalogue_link', 'file': str(path.relative_to(R)), 'target': value})

report = {'result': 'pass' if not errors else 'incomplete', 'record_counts': dict(Counter(r['type'] for r in records)),
    'media_files_verified': sum(bool(m.get('local_path')) for m in media), 'media_bytes': sum(m.get('bytes', 0) for m in media),
    'gallery_count': len(galleries), 'gallery_photos_verified': gallery_photos, 'checks': ['REST IDs', 'all content sitemap URLs',
    'all file sizes and SHA-256', 'gallery photo membership and local files', 'Markdown files', 'catalogue local links'], 'errors': errors}
(R / 'data/validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: v for k, v in report.items() if k != 'errors'}, ensure_ascii=False, indent=2))
print('Errors:', len(errors), errors[:8])
raise SystemExit(bool(errors))
