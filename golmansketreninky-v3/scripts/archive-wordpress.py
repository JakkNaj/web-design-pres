#!/usr/bin/env python3
"""Read-only archive of the public legacy site. Requires Python 3, bs4 and curl.

Responses are cached under content/wordpress/raw; reruns resume interrupted work.
Only public GET requests are used. No login, forms or administrative endpoints.
"""
import concurrent.futures as cf
import hashlib
import html
import json
import re
import subprocess
import threading
import time
import unicodedata
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit, urlunsplit

from bs4 import BeautifulSoup, NavigableString

ROOT = Path(__file__).resolve().parents[1] / 'content' / 'wordpress'
BASE = 'https://www.golmansketreninky.cz/'
STAMP = datetime.now(timezone.utc).isoformat()
WORKERS = 2
REQUEST_LOCK = threading.Lock()
LAST_REQUEST = 0.0
for folder in ('raw/http', 'data', 'stranky', 'aktuality', 'udalosti', 'mista', 'galerie', 'treneri', 'partneri', 'kontakt', 'media'):
    (ROOT / folder).mkdir(parents=True, exist_ok=True)


def dump(path, data):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def clean(text):
    return re.sub(r'\s+', ' ', html.unescape(text or '').replace('\ufeff', '')).strip()


def slug(text):
    text = unicodedata.normalize('NFKD', clean(text)).encode('ascii', 'ignore').decode().lower()
    return re.sub('[^a-z0-9]+', '-', text).strip('-')[:150] or 'bez-nazvu'


def norm(url, base=BASE, asset=False):
    p = urlsplit(urljoin(base, html.unescape(url)))
    if p.scheme not in ('http', 'https'):
        return ''
    if p.hostname in ('www.golmansketreninky.cz', 'golmansketreninky.cz'):
        p = p._replace(scheme='https', netloc='www.golmansketreninky.cz')
    return urlunsplit(p._replace(fragment='', query='' if asset else p.query))


def internal(url):
    return urlsplit(url).hostname == 'www.golmansketreninky.cz'


def fetch(url):
    """Four bounded downloads at most; retain bodies and minimal provenance."""
    global LAST_REQUEST
    key = hashlib.sha256(url.encode()).hexdigest()[:24]
    meta = ROOT / 'raw/http' / (key + '.json')
    body = ROOT / 'raw/http' / (key + '.body')
    if meta.exists() and body.exists():
        info = json.loads(meta.read_text())
        if info['ok']:
            return info, body
    temp = body.with_suffix('.part')
    with REQUEST_LOCK:
        time.sleep(max(0, .6 - (time.monotonic() - LAST_REQUEST)))
        LAST_REQUEST = time.monotonic()
    run = subprocess.run(['curl', '--silent', '--show-error', '--fail-with-body', '--location',
        '--retry', '2', '--retry-delay', '1', '--connect-timeout', '12', '--max-time', '50',
        '--user-agent', 'GoalieContentArchive/1.0 (public content migration)',
        '--output', str(temp), '--write-out', '%{http_code}\n%{url_effective}\n%{content_type}', url],
        capture_output=True, text=True)
    lines = run.stdout.splitlines()
    info = {'url': url, 'final_url': lines[1] if len(lines) > 1 else url,
        'status': int(lines[0]) if lines and lines[0].isdigit() else 0,
        'content_type': lines[2] if len(lines) > 2 else '', 'fetched_at': datetime.now(timezone.utc).isoformat(),
        'ok': run.returncode == 0, 'error': run.stderr.strip() if run.returncode else None,
        'raw_file': str(body.relative_to(ROOT))}
    if temp.exists():
        temp.replace(body)
    meta.write_text(json.dumps(info, ensure_ascii=False, indent=2))
    time.sleep(.1)
    return info, body


def get_text(url):
    info, path = fetch(url)
    return info, path.read_text(encoding='utf-8-sig', errors='replace') if info['ok'] else ''


def collection(kind):
    items, page = [], 1
    while True:
        url = BASE + f'wp-json/wp/v2/{kind}?per_page=100&page={page}'
        info, text = get_text(url)
        if not info['ok']:
            body = ROOT / info['raw_file']
            error = json.loads(body.read_text(encoding='utf-8-sig')) if body.exists() and info['status'] == 400 else {}
            if error.get('code') == 'rest_post_invalid_page_number':
                break
            raise RuntimeError(f'Incomplete REST collection {kind}, page {page}: {info}')
        batch = json.loads(text)
        if not isinstance(batch, list):
            raise RuntimeError(f'Unexpected REST response: {kind}')
        items.extend(batch)
        # A plugin can remove records after pagination: a short page is not the end.
        if not batch:
            break
        page += 1
    dump(f'raw/{kind}.json', items)
    print(f'REST {kind}: {len(items)}', flush=True)
    return items


def soup(text):
    return BeautifulSoup(text, 'html.parser')


def markdown(node):
    """Keep links, images, line breaks, lists and tables; raw HTML remains archived."""
    if isinstance(node, NavigableString):
        return str(node).replace('\xa0', ' ').replace('\ufeff', '')
    name = node.name
    if name in ('script', 'style', 'form', 'noscript'):
        return ''
    inner = ''.join(markdown(c) for c in node.children)
    if name == 'br':
        return '  \n'
    if name == 'img':
        return f"![{node.get('alt', '')}]({norm(node.get('src', ''))})"
    if name == 'a':
        return f"[{inner.strip()}]({node.get('href', '')})" if node.get('href') else inner
    if name in ('iframe', 'embed', 'object'):
        return f"\n[Video / vložený obsah]({node.get('src', node.get('data', ''))})\n"
    if re.fullmatch('h[1-6]', name or ''):
        return '\n\n' + '#' * int(name[1]) + ' ' + inner.strip() + '\n\n'
    if name in ('strong', 'b'):
        return '**' + inner.strip() + '**' if inner.strip() else ''
    if name in ('em', 'i'):
        return '*' + inner.strip() + '*'
    if name == 'li':
        return '\n- ' + inner.strip() + '\n'
    if name == 'table':
        rows = []
        for tr in node.select('tr'):
            rows.append('| ' + ' | '.join(clean(td.get_text(' ', strip=True)).replace('|', '\\|') for td in tr.find_all(['td', 'th'], recursive=False)) + ' |')
        if rows:
            cols = len(node.select_one('tr').find_all(['td', 'th'], recursive=False))
            rows.insert(1, '| ' + ' | '.join(['---'] * cols) + ' |')
        return '\n\n' + '\n'.join(rows) + '\n\n'
    if name in ('p', 'div', 'section', 'ul', 'ol', 'blockquote'):
        return '\n\n' + inner.strip() + '\n\n'
    return inner


def mdtext(markup):
    return re.sub(r'\n[ \t]*\n(?:[ \t]*\n)+', '\n\n', markdown(soup(markup))).strip()


def main():
    print('Archive:', ROOT, flush=True)
    api = {}
    with cf.ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(collection, k): k for k in ['posts', 'pages', 'media', 'categories', 'tags', 'comments']}
        for future in cf.as_completed(futures):
            api[futures[future]] = future.result()

    # Enumerate all public sitemap records, including legacy events and locations.
    sitemaps, sitemap_urls, queue = {}, set(), [BASE + 'wp-sitemap.xml']
    while queue:
        url = queue.pop(0)
        info, text = get_text(url)
        if not info['ok']:
            raise RuntimeError('Cannot read sitemap ' + url)
        tree = ET.fromstring(text)
        locs = [n.text for n in tree.iter() if n.tag.endswith('}loc')]
        sitemaps[url] = locs
        if tree.tag.endswith('sitemapindex'):
            queue.extend(locs)
        else:
            sitemap_urls.update(map(norm, locs))
    dump('data/sitemaps.json', sitemaps)
    get_text(BASE + 'robots.txt')

    records = {}
    for kind in ('posts', 'pages'):
        for obj in api[kind]:
            url = norm(obj['link'])
            records[url] = {'id': obj['id'], 'type': obj['type'], 'title': clean(soup(obj['title']['rendered']).get_text()),
                'slug': obj['slug'], 'source_url': url, 'date': obj['date'], 'modified': obj['modified'],
                'parent': obj.get('parent', 0), 'categories': obj.get('categories', []), 'tags': obj.get('tags', []),
                'featured_media': obj.get('featured_media', 0), 'content_html': obj['content']['rendered']}
    pending = set(records) | {BASE}
    pending.update(u for sitemap, urls in sitemaps.items() if '-posts-event-' in sitemap or '-posts-location-' in sitemap for u in map(norm, urls))
    rendered, failures = {}, []
    while pending:
        batch = sorted(pending - rendered.keys())
        if not batch:
            break
        pending.clear()
        with cf.ThreadPoolExecutor(max_workers=WORKERS) as pool:
            futures = {pool.submit(get_text, u): u for u in batch}
            for i, future in enumerate(cf.as_completed(futures), 1):
                url = futures[future]
                info, text = future.result()
                rendered[url] = text
                if not info['ok']:
                    failures.append(info)
                    continue
                doc = soup(text)
                entry = doc.select_one('.entry-content')
                if url in records:
                    records[url]['rendered_content_html'] = str(entry or '')
                    records[url]['raw_html'] = info['raw_file']
                elif '/events/' in url or '/locations/' in url:
                    title = doc.select_one('.entry-title') or doc.select_one('h1')
                    kind = 'event' if '/events/' in url else 'location'
                    records[url] = {'type': kind, 'title': clean(title.get_text(' ', strip=True) if title else url),
                        'slug': urlsplit(url).path.strip('/').split('/')[-1], 'source_url': url,
                        'content_html': str(entry or ''), 'raw_html': info['raw_file']}
                # NextGEN pagination is not represented by WordPress REST or sitemaps.
                for a in doc.select('.entry-content a[href]'):
                    link = norm(a['href'], url)
                    if internal(link) and re.search(r'/nggallery/page/\d+/?$', urlsplit(link).path) and link not in rendered:
                        # Sidebar calendar adds ?mo=&yr= to gallery URLs indefinitely.
                        link = urlunsplit(urlsplit(link)._replace(query=''))
                        if link not in rendered:
                            pending.add(link)
                if i % 50 == 0 or i == len(batch):
                    print(f'HTML: {len(rendered)} pages; gallery pagination queued: {len(pending)}', flush=True)

    # Map WordPress resized renditions to the full source image, retaining all metadata.
    assets, aliases = {}, {}

    def add_asset(url, source, role='content', **extra):
        url = norm(url, source, asset=True)
        if not url or not internal(url):
            return None
        if not re.search(r'\.(?:jpe?g|png|gif|webp|svg|avif|heic|pdf|docx?|xlsx?|zip|mp4|mov|mp3|webm|flv)(?:$)', unquote(urlsplit(url).path), re.I):
            return None
        url = aliases.get(url, url)
        item = assets.setdefault(url, {'source_url': url, 'referenced_by': [], 'roles': []})
        if source not in item['referenced_by']:
            item['referenced_by'].append(source)
        if role not in item['roles']:
            item['roles'].append(role)
        item.update(extra)
        return url

    for obj in api['media']:
        full = norm(obj['source_url'], asset=True)
        details = obj.get('media_details', {})
        original = details.get('original_image')
        if original:
            full = norm(urljoin(full, original), asset=True)
        aliases[norm(obj['source_url'], asset=True)] = full
        for size in details.get('sizes', {}).values():
            if size.get('source_url'):
                aliases[norm(size['source_url'], asset=True)] = full
        add_asset(full, norm(obj['link']), 'wordpress-media', wordpress_id=obj['id'],
            title=clean(soup(obj['title']['rendered']).get_text()), alt=obj.get('alt_text', ''),
            caption=clean(soup(obj['caption']['rendered']).get_text()), date=obj['date'],
            mime_type=obj['mime_type'], parent_post_id=obj.get('post'), media_details=details)

    galleries, partners, videos, external_links = {}, [], [], {}
    def gallery_order(url):
        match = re.search(r'/nggallery/page/(\d+)', url)
        return (url.split('/nggallery/')[0], int(match[1]) if match else 0)

    for url in sorted(rendered, key=gallery_order):
        text = rendered[url]
        if not text:
            continue
        doc = soup(text)
        entry = doc.select_one('.entry-content')
        scope = entry if url != BASE and entry else doc
        for gallery in doc.select('[data-nextgen-gallery-id]'):
            gid = gallery['data-nextgen-gallery-id']
            item = galleries.setdefault(gid, {'id': gid, 'name': gallery.get('data-gallery-name', gid), 'source_pages': [], 'content_source_pages': [], 'widget_source_pages': [], 'images': []})
            if url not in item['source_pages']:
                item['source_pages'].append(url)
            placement = 'content_source_pages' if gallery.find_parent(class_='entry-content') else 'widget_source_pages'
            if url not in item[placement]:
                item[placement].append(url)
            for a in gallery.select('a[data-src]'):
                full = norm(a['data-src'], url, asset=True)
                thumb = a.get('data-thumbnail')
                if thumb:
                    aliases[norm(thumb, url, asset=True)] = full
                asset = add_asset(full, url, 'gallery')
                if asset and not any(im['source_url'] == asset for im in item['images']):
                    item['images'].append({'id': a.get('data-image-id'), 'source_url': asset,
                        'title': a.get('data-title', ''), 'description': a.get('data-description', ''),
                        'alt': a.img.get('alt', '') if a.img else '', 'position': len(item['images']) + 1})
        for img in scope.select('img[src]'):
            src = img['src']
            parent = img.find_parent('a')
            if parent and re.search(r'\.(jpe?g|png|gif|webp)(?:\?|$)', parent.get('href', ''), re.I):
                original = norm(parent['href'], url, asset=True)
                aliases[norm(src, url, asset=True)] = aliases.get(original, original)
                src = original
            add_asset(src, url, 'content', **({'alt': img['alt']} if img.get('alt') and norm(src, asset=True) not in assets else {}))
        for a in scope.select('a[href]'):
            link = norm(a['href'], url)
            add_asset(link, url)
            if link and not internal(link):
                external_links.setdefault(link, {'url': link, 'label': clean(a.get_text(' ', strip=True)), 'source_pages': []})['source_pages'].append(url)
        for el in scope.select('iframe[src], embed[src], object[data]'):
            src = el.get('src', el.get('data'))
            if src:
                videos.append({'url': norm(src, url), 'source_page': url, 'title': el.get('title', '')})
        if url == BASE:
            for widget in doc.select('#secondary .widget_simpleimage'):
                a, img = widget.select_one('a[href]'), widget.select_one('img[src]')
                if a and img:
                    logo = add_asset(img['src'], BASE, 'partner-logo')
                    partners.append({'website': a['href'], 'logo_source_url': logo, 'source_page': BASE,
                        'name_from_source': img.get('alt') or Path(urlsplit(img['src']).path).stem,
                        'widget_id': widget.get('id')})
            # Header/brand assets are outside entry content.
            for img in doc.select('header img[src], #branding img[src]'):
                add_asset(img['src'], BASE, 'branding')

    # REST HTML can expose media or video URLs absent from rendered shortcodes.
    for url, record in records.items():
        doc = soup(record['content_html'])
        for el in doc.select('img[src], a[href]'):
            add_asset(el.get('src', el.get('href')), url)
        for el in doc.select('iframe[src], embed[src], object[data]'):
            src = norm(el.get('src', el.get('data')), url)
            if not any(v['url'] == src and v['source_page'] == url for v in videos):
                videos.append({'url': src, 'source_page': url, 'title': el.get('title', '')})
        # Legacy Flowplayer hides actual MP4/FLV URLs in inline scripts. Parse
        # literal URLs only; never execute archived JavaScript.
        for script in doc.select('script'):
            for raw_url in re.findall(r'https?://[^\s\x22\x27<>]+\.(?:mp4|flv|mov|webm)(?:\?[^\s\x22\x27<>]*)?', script.get_text(), re.I):
                src = norm(raw_url, url, asset=True)
                if not any(v['url'] == src and v['source_page'] == url for v in videos):
                    heading = script.find_previous(['h3', 'h2'])
                    videos.append({'url': src, 'source_page': url, 'title': clean(heading.get_text()) if heading else '', 'kind': 'self_hosted_video'})
                add_asset(src, url, 'video')

    # Fold any late-discovered thumbnail aliases into originals before downloading.
    for url in list(assets):
        full = aliases.get(url, url)
        if full != url and full in assets:
            for field in ('referenced_by', 'roles'):
                assets[full][field] = sorted(set(assets[full][field] + assets[url][field]))
            del assets[url]
    dump('data/asset-aliases.json', aliases)
    dump('data/galleries.json', list(galleries.values()))
    dump('data/partners.json', partners)
    dump('data/videos.json', videos)
    dump('data/external-links.json', list(external_links.values()))
    dump('data/records.json', list(records.values()))
    print(f'Discovered {len(galleries)} galleries, {sum(len(g["images"]) for g in galleries.values())} gallery photos, {len(assets)} unique asset URLs', flush=True)

    def download(item):
        url = item['source_url']
        parts = [p for p in unquote(urlsplit(url).path).split('/') if p not in ('', '.', '..')]
        if 'wp-content' in parts:
            parts = parts[parts.index('wp-content') + 1:]
        dest = ROOT / 'media' / Path(*parts)
        info, raw = fetch(url)
        item['download_status'] = 'ok' if info['ok'] else 'failed'
        if info['ok'] and ('text/html' in info['content_type']):
            item['download_status'] = 'failed'
            info['error'] = 'Expected media, received HTML'
        if item['download_status'] == 'ok':
            dest.parent.mkdir(parents=True, exist_ok=True)
            data = raw.read_bytes()
            dest.write_bytes(data)
            item.update(local_path=str(dest.relative_to(ROOT)), bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), fetched_at=info['fetched_at'])
            # Keep one physical copy: the raw response body is the original media file.
            if raw.exists() and not raw.is_symlink():
                raw.unlink()
                raw.symlink_to(Path('../../') / item['local_path'])
        else:
            item['error'] = info['error']
        return item

    downloaded = []
    with cf.ThreadPoolExecutor(max_workers=WORKERS) as pool:
        for i, item in enumerate(pool.map(download, assets.values()), 1):
            downloaded.append(item)
            if i % 50 == 0 or i == len(assets):
                dump('data/media.json', downloaded)
                print(f'Media: {i}/{len(assets)}; {sum(m.get("bytes", 0) for m in downloaded) // 1048576} MB', flush=True)
    assets = {m['source_url']: m for m in downloaded}
    for video in videos:
        video['local_path'] = assets.get(video['url'], {}).get('local_path')
    dump('data/videos.json', videos)
    for record in records.values():
        markup = record.get('rendered_content_html') or record['content_html']
        record['text'] = clean(soup(markup).get_text(' ', strip=True))
        record['media'] = [m['local_path'] for m in downloaded if record['source_url'] in m['referenced_by'] and m.get('local_path')]
        folder = {'post': 'aktuality', 'page': 'stranky', 'event': 'udalosti', 'location': 'mista'}[record['type']]
        basename = (str(record.get('id', '')) + '-' + slug(unquote(record['slug']))).strip('-')
        record['markdown_path'] = f'{folder}/{basename}.md'
        content = mdtext(markup)
        local_videos = [v for v in videos if v['source_page'] == record['source_url'] and v.get('local_path')]
        if local_videos:
            content += '\n\n## Původní videosoubory\n\n' + '\n'.join(f'- [{v["title"] or Path(v["local_path"]).name}](../{v["local_path"]})' for v in local_videos)
        for source, item in assets.items():
            if item.get('local_path'):
                content = content.replace(source, '../' + item['local_path'])
                content = content.replace(source.replace('https:', 'http:'), '../' + item['local_path'])
        for alias, full in aliases.items():
            if assets.get(full, {}).get('local_path'):
                content = content.replace(alias, '../' + assets[full]['local_path'])
                content = content.replace(alias.replace('https:', 'http:'), '../' + assets[full]['local_path'])
        meta = '\n'.join(f'{key}: {json.dumps(record[key], ensure_ascii=False)}' for key in ['title', 'source_url', 'date', 'modified', 'type'] if key in record)
        (ROOT / record['markdown_path']).write_text(f'---\n{meta}\narchived_at: {STAMP}\neditorial_status: "původní text – k revizi"\n---\n\n# {record["title"]}\n\n{content}\n')
    dump('data/records.json', list(records.values()))
    for g in galleries.values():
        for im in g['images']:
            im['local_path'] = assets.get(im['source_url'], {}).get('local_path')
        g['photo_count'] = len(g['images'])
        dump(f'galerie/{g["id"]}-{slug(g["name"])}.json', g)
    dump('data/galleries.json', list(galleries.values()))
    for p in partners:
        p['logo_local_path'] = assets.get(p['logo_source_url'], {}).get('local_path')
    dump('data/partners.json', partners)
    # Save the public navigation and partner widgets without crawling third-party sites.
    home = soup(rendered[BASE])
    dump('data/navigation.json', [{'label': clean(a.get_text()), 'url': a['href']} for a in home.select('#menu-menu a[href]')])
    dump('data/coverage.json', {'archived_at': STAMP, 'api_counts': {k: len(v) for k, v in api.items()},
        'sitemap_count': len(sitemap_urls), 'rendered_page_count': len(rendered),
        'record_counts': {kind: sum(r['type'] == kind for r in records.values()) for kind in ['post', 'page', 'event', 'location']},
        'gallery_count': len(galleries), 'gallery_photos': sum(len(g['images']) for g in galleries.values()),
        'media_count': len(downloaded), 'media_downloaded': sum(m['download_status'] == 'ok' for m in downloaded),
        'media_bytes': sum(m.get('bytes', 0) for m in downloaded), 'partners': len(partners), 'video_embeds': sum(not v.get('kind') for v in videos), 'self_hosted_videos': sum(v.get('kind') == 'self_hosted_video' for v in videos),
        'page_failures': failures, 'media_failures': [m for m in downloaded if m['download_status'] != 'ok'],
        'scope': 'Public WordPress posts/pages/media/comments/taxonomies; sitemap events/locations; all linked NextGEN pagination; visible partner widgets. No private content, accounts, registrations or third-party video downloads.'})
    print('DONE: data/coverage.json', flush=True)


if __name__ == '__main__':
    main()
