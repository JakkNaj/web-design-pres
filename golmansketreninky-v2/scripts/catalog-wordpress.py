#!/usr/bin/env python3
"""Build editable editorial extracts and a standalone offline archive catalogue."""
import importlib.util
import json
import re
from html import escape
from pathlib import Path
from urllib.parse import unquote

spec = importlib.util.spec_from_file_location('archive', Path(__file__).with_name('archive-wordpress.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
R = a.ROOT
load = lambda name: json.loads((R / name).read_text())
records = load('data/records.json')
media = load('data/media.json')
galleries = load('data/galleries.json')
partners = load('data/partners.json')
coverage = load('data/coverage.json')
aliases = load('data/asset-aliases.json')
by_url = {m['source_url']: m for m in media}
by_id = {r.get('id'): r for r in records}

# Keep local filenames safe even when a legacy WordPress slug contains % escapes.
for r in records:
    path = Path(r['markdown_path'])
    safe = path.with_name((str(r.get('id', '')) + '-' + a.slug(unquote(r['slug']))).strip('-') + '.md')
    if path != safe:
        (R / path).replace(R / safe)
        r['markdown_path'] = str(safe)
a.dump('data/records.json', records)


def local(url):
    url = a.norm(url, asset=True)
    return by_url.get(aliases.get(url, url), {}).get('local_path')


def write(name, text):
    (R / name).parent.mkdir(parents=True, exist_ok=True)
    (R / name).write_text(text)


def link(path, text):
    return f'<a href="{escape(path, quote=True)}">{escape(text)}</a>'


coach_page = by_id[28]
names = ['Martin Altrichter', 'Mgr. Marek Zapletal', 'Daniel Zelenka', 'Luboš Horčička',
    'Vlastimil Lakosil', 'Hynek Kůdela', 'Patrik Polívka', 'Pavel Bílek', 'Lukáš Sochůrek', 'Tomáš Kalčík', 'Martin Sejpal']
profiles = []
for node in a.soup(coach_page['content_html']).find_all(recursive=False):
    text = a.clean(node.get_text(' ', strip=True))
    if text in names:
        profiles.append({'name': text, 'slug': a.slug(text), 'source_url': coach_page['source_url'],
            'source_modified': coach_page['modified'], 'editorial_status': 'původní text – k revizi', 'bio_html': ''})
    elif profiles:
        profiles[-1]['bio_html'] += str(node)
for p in profiles:
    doc = a.soup(p['bio_html'])
    img = doc.select_one('img[src]')
    p['portrait_local_path'] = local(img['src']) if img else None
    p['bio_text'] = a.clean(doc.get_text(' ', strip=True))
    p['profile_detail'] = 'full_bio' if p['bio_text'] else 'name_only'
    p['markdown_path'] = f'treneri/{p["slug"]}.md'
    for image in doc.select('img'):
        image.decompose()
    content = f'# {p["name"]}\n\nZdroj: {p["source_url"]}  \nPoslední úprava zdroje: {p["source_modified"]}. Původní text k revizi.\n\n'
    if p['portrait_local_path']:
        content += f'![{p["name"]}](../{p["portrait_local_path"]})\n\n'
    content += a.mdtext(str(doc)) or 'Starý web uvádí pouze jméno. Medailonek a fotografie nejsou na stránce trenérů uvedeny.'
    write(p['markdown_path'], content + '\n')
a.dump('data/coaches.json', profiles)

partner_names = {'comsys.cz': 'COM-SYS ICE ARENA', 'merkur-lifestyle.com': 'MERKUR', 'stridasport.cz': 'Střída Sport',
    'ribanadresy.cz': 'Ribana dresy', 'hokejovetreninky.cz': 'Hokejové tréninky'}
for p in partners:
    p['name'] = next((name for domain, name in partner_names.items() if domain in p['website']), p['name_from_source'])
    p['status'] = 'logo v postranním panelu původního webu; aktuální spolupráci potvrdit'
a.dump('data/partners.json', partners)
mentions = []
for r in records:
    if r['type'] not in ('post', 'page'):
        continue
    for p in a.soup(r['content_html']).select('p'):
        text = a.clean(p.get_text(' ', strip=True))
        if re.search(r'partner|spoluprac|spoluprác|H2\s*WORLD', text, re.I) and len(text) > 30:
            mentions.append({'source_url': r['source_url'], 'title': r['title'], 'date': r.get('date'), 'source_excerpt': text})
a.dump('data/partner-mentions.json', mentions)
partner_md = '# Partneři ze starého webu\n\nPřevzato z veřejného postranního panelu. Nejde o potvrzení aktuální spolupráce.\n\n'
for p in partners:
    partner_md += f'## {p["name"]}\n\nWeb: {p["website"]}\n\n'
    if p.get('logo_local_path'):
        partner_md += f'![{p["name"]}](../{p["logo_local_path"]})\n\n'
partner_md += '## Další spolupráce v článcích\n\nKemp 2026 zmiňuje Střída Sport / CCM a H2 WORLD health & beauty. Další historické zmínky včetně zdrojů jsou v [partner-mentions.json](../data/partner-mentions.json). Loga a historické bannery jsou také v katalogu všech médií.\n'
write('partneri/README.md', partner_md)

contact = {'source_url': by_id[951]['source_url'], 'source_modified': by_id[951]['modified'],
    'email': 'dotazy@golmansketreninky.cz', 'people': [
        {'name': 'Martin Altrichter', 'phone': '+420 737 268 000'}, {'name': 'Marek Zapletal', 'phone': '+420 603 118 008'}],
    'registration': 'Starý web žádá e-mailem celé jméno gólmana, rok narození a e-mail pro registraci.',
    'venue': {'name': 'COM-SYS ICE ARENA ŘÍČANY', 'address': 'Škroupova 2625/4, Říčany 251 01', 'source_url': by_id[10296]['source_url']},
    'editorial_status': 'převzato ze zdroje; před novým webem potvrdit'}
a.dump('data/contact.json', contact)
write('kontakt/README.md', f'''# Kontakt a registrace

Zdroj: {contact['source_url']}<br>
Poslední úprava zdroje: {contact['source_modified']}

- E-mail: **{contact['email']}**
- Martin Altrichter: **+420 737 268 000**
- Marek Zapletal: **+420 603 118 008**
- Místo tréninků: **COM-SYS ICE ARENA, Škroupova 2625/4, Říčany 251 01**. Adresa pochází z [článku o kempu 2026]({contact['venue']['source_url']}).

Starý postup registrace: e-mailem celé jméno gólmana, rok narození a e-mail pro registraci.

Mockup používá `info@golmansketreninky.cz`; stránka kontaktů uvádí `dotazy@golmansketreninky.cz`. Před použitím potvrdit správnou adresu a nový postup registrace.

Původní úplný text: [Kontakty](../{by_id[951]['markdown_path']}).
''')

for g in galleries:
    primary = g.get('content_source_pages') or g['source_pages']
    candidates = [r for r in records if r['source_url'] in primary and r['type'] == 'page' and r['title'] != 'Foto']
    g['title'] = candidates[0]['title'] if candidates else ('Ukázka tréninku / základní galerie' if g['id'] == '1' else g['name'])
    g['catalog_path'] = f'galerie/{g["id"]}-{a.slug(g["name"])}.html'
    g['json_path'] = f'galerie/{g["id"]}-{a.slug(g["name"])}.json'
    a.dump(g['json_path'], g)
a.dump('data/galleries.json', galleries)

style = '''*{box-sizing:border-box}body{margin:0;background:#f5f7fa;color:#17212b;font:15px/1.6 system-ui,sans-serif}header{background:#111c27;color:white;padding:46px max(24px,calc((100% - 1240px)/2));}main{max-width:1288px;margin:auto;padding:36px 24px 80px}h1{font-size:clamp(30px,4vw,50px);line-height:1.1;letter-spacing:-.035em;margin:10px 0 20px}h2{font-size:28px;letter-spacing:-.025em;margin:44px 0 16px}h3{font-size:16px;margin:10px 0 4px}p{max-width:850px}a{color:#076185;text-underline-offset:3px}header a{color:#9be3f6}.muted{color:#61707c}small{font-size:12px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(235px,1fr));gap:18px}.card{display:block;background:white;border:1px solid #dce3e9;border-radius:12px;overflow:hidden;color:inherit;text-decoration:none}.card img{width:100%;height:180px;object-fit:cover;background:#e8edf1}.card .body{padding:14px 18px 18px}.card p{margin:5px 0}.stats{display:flex;gap:12px;flex-wrap:wrap}.stat{background:#1f3445;padding:13px 20px;border-radius:8px}.stat b{display:block;font-size:26px}.nav{display:flex;gap:18px;flex-wrap:wrap;margin-top:24px}input,select{font:inherit;padding:12px;border:1px solid #aebdc9;border-radius:7px;max-width:100%}input{width:430px}.toolbar{display:flex;gap:10px;flex-wrap:wrap;margin:24px 0}table{border-collapse:collapse;width:100%;background:white}td,th{text-align:left;padding:12px;border-bottom:1px solid #dce3e9}th{font-size:12px;text-transform:uppercase;color:#61707c}td:first-child{white-space:nowrap}.table-wrap{overflow-x:auto}figure{margin:0}figcaption{padding:10px 14px;overflow-wrap:anywhere}button{padding:10px 18px;font:inherit;border:1px solid #bac8d3;border-radius:6px;background:white;cursor:pointer}.notice{background:#e5f2f6;border-left:3px solid #25809c;padding:14px 20px}.portrait{object-fit:contain!important}.logos img{object-fit:contain;padding:18px;background:white}.gallery img{height:230px;object-fit:contain;background:#e8edf1}code{font-size:13px}section{scroll-margin-top:20px}@media(max-width:600px){header{padding:30px 20px}.grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.card img{height:130px}.card .body{padding:10px}.gallery img{height:150px}main{padding:20px 16px}h3{font-size:14px}td,th{padding:8px}}'''


def page(title, body, header='', script=''):
    return f'<!doctype html><html lang="cs"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>{escape(title)}</title><style>{style}</style></head><body><header>{header or "<h1>" + escape(title) + "</h1>"}</header><main>{body}</main>{script}</body></html>'


gallery_cards = ''
for g in sorted(galleries, key=lambda g: int(g['id']), reverse=True):
    photos = [im for im in g['images'] if im.get('local_path')]
    if photos:
        gallery_cards += f'<a class="card" href="{g["catalog_path"]}"><img loading="lazy" src="{escape(photos[0]["local_path"], quote=True)}" alt=""><div class="body"><h3>{escape(g["title"])}</h3><p class="muted">{len(photos)} fotografií · galerie {g["id"]}</p></div></a>'
    tiles = ''.join(f'<figure class="card"><a href="../{escape(im["local_path"], quote=True)}"><img loading="lazy" src="../{escape(im["local_path"], quote=True)}" alt="{escape(im["alt"], quote=True)}"></a><figcaption><small>{im["position"]} · {escape(im["title"] or Path(im["local_path"]).name)}</small></figcaption></figure>' for im in photos)
    write(g['catalog_path'], page(g['title'], f'<p>{link("../index.html#galerie", "← Zpět do katalogu")} · {link("../" + g["json_path"], "Metadata galerie")}</p><p>{len(photos)} stažených fotografií. Kliknutím otevřete originál.</p><div class="grid gallery">{tiles}</div>'))
coach_cards = ''.join(f'<div class="card">' + (f'<img class="portrait" loading="lazy" src="{escape(p["portrait_local_path"], quote=True)}" alt="{escape(p["name"], quote=True)}">' if p['portrait_local_path'] else '') + f'<div class="body"><h3>{link(p["markdown_path"], p["name"])}</h3><p class="muted">{"Medailonek a fotografie" if p["profile_detail"] == "full_bio" else "Ve zdroji pouze jméno"}</p></div></div>' for p in profiles)
partner_cards = ''.join(f'<div class="card"><img loading="lazy" src="{escape(p["logo_local_path"], quote=True)}" alt="{escape(p["name"], quote=True)}"><div class="body"><h3>{escape(p["name"])}</h3>{link(p["logo_local_path"], "Soubor loga")}</div></div>' for p in partners if p.get('logo_local_path'))
news = sorted([r for r in records if r['type'] == 'post'], key=lambda r: r['date'], reverse=True)
rows = ''.join(f'<tr data-search="{escape((r["title"] + " " + r["date"]).lower(), quote=True)}"><td>{escape(r["date"][:10])}</td><td>{link(r["markdown_path"], r["title"])}</td><td>{"Výstroj" if 8 in r["categories"] else "Aktuality"}</td><td>{link(r["source_url"], "Zdroj ↗")}</td></tr>' for r in news)
stat_data = [(len(news), 'příspěvků'), (len(galleries), 'galerií'), (coverage['gallery_photos'], 'fotek v galeriích'), (coverage['media_downloaded'], 'stažených médií')]
stats = ''.join(f'<div class="stat"><b>{n}</b>{label}</div>' for n, label in stat_data)
header = f'<small>GÓLMANSKÉ TRÉNINKY · OBSAHOVÝ ARCHIV · 7. 9. 2026</small><h1>Podklady pro nový web.</h1><p>Původní texty, fotografie a zdroje. Připravené k výběru a úpravám.</p><div class="stats">{stats}</div><nav class="nav"><a href="#galerie">Galerie</a><a href="#treneri">Trenéři</a><a href="#partneri">Partneři</a><a href="#kontakt">Kontakt</a><a href="#aktuality">Aktuality</a><a href="media.html">Všechna média</a><a href="README.md">Přehled archivu</a></nav>'
body = f'''<p class="notice">Archiv starého webu. Historické ceny, termíny, kontakty a spolupráce čekají na revizi. <a href="K_REVIZI.md">Co ověřit před použitím →</a></p>
<section id="galerie"><h2>Fotografie a galerie</h2><div class="grid">{gallery_cards}</div><p>{link('media.html', 'Otevřít všechny fotografie, loga a dokumenty →')}</p></section>
<section id="treneri"><h2>Trenéři</h2><div class="grid">{coach_cards}</div></section>
<section id="partneri"><h2>Partneři a loga</h2><div class="grid logos">{partner_cards}</div><p>{link('partneri/README.md', 'Přehled a další spolupráce zmíněné v článcích →')}</p></section>
<section id="kontakt"><h2>Kontakt ze zdroje</h2><p><b>dotazy@golmansketreninky.cz</b><br>Martin Altrichter · +420 737 268 000<br>Marek Zapletal · +420 603 118 008<br>COM-SYS ICE ARENA · Škroupova 2625/4, Říčany</p><p>{link('kontakt/README.md', 'Kontakt, zdroje a původní registrace →')}</p></section>
<section id="aktuality"><h2>Příspěvky 2012–2026</h2><div class="toolbar"><input type="search" id="search" aria-label="Hledat v příspěvcích" placeholder="Hledat podle názvu nebo roku…"><span id="count" aria-live="polite">{len(news)} příspěvků</span></div><div class="table-wrap"><table><thead><tr><th>Datum</th><th>Název</th><th>Rubrika</th><th>Zdroj</th></tr></thead><tbody>{rows}</tbody></table></div></section>'''
script = '<script>document.querySelector("#search").addEventListener("input",e=>{let count=0;for(const row of document.querySelectorAll("tr[data-search]")){row.hidden=!row.dataset.search.includes(e.target.value.toLowerCase());if(!row.hidden)count++;}document.querySelector("#count").textContent=count+" příspěvků";});</script>'
write('index.html', page('Obsahový archiv · Gólmanské tréninky', body, header, script))

items = [{'path': m['local_path'], 'title': m.get('title') or Path(m['local_path']).name,
    'roles': m['roles'], 'bytes': m['bytes'], 'image': bool(re.search(r'\.(jpg|jpeg|png|gif|svg|webp|avif)$', m['local_path'], re.I))}
    for m in media if m.get('local_path')]
payload = json.dumps(items, ensure_ascii=False).replace('</', '<\\/')
media_script = '''<script>
const items=PAYLOAD;let page=0;const size=60;const grid=document.querySelector('#media');
function render(){const q=document.querySelector('#query').value.toLowerCase(),kind=document.querySelector('#kind').value;const filtered=items.filter(x=>(x.title+' '+x.path).toLowerCase().includes(q)&&(kind==='all'||(kind==='documents'?!x.image:x.roles.includes(kind))));grid.replaceChildren();for(const item of filtered.slice(page*size,(page+1)*size)){const card=document.createElement('a');card.className='card';card.href=item.path;if(item.image){const img=document.createElement('img');img.src=item.path;img.loading='lazy';img.alt='';img.className='portrait';card.append(img);}const body=document.createElement('div');body.className='body';const h=document.createElement('h3');h.textContent=item.title;const p=document.createElement('p');p.className='muted';p.textContent=(item.bytes/1024).toFixed(0)+' kB · '+item.path.split('/').pop();body.append(h,p);card.append(body);grid.append(card);}document.querySelector('#result').textContent=filtered.length+' souborů · strana '+(page+1)+' / '+Math.max(1,Math.ceil(filtered.length/size));document.querySelector('#prev').disabled=page===0;document.querySelector('#next').disabled=(page+1)*size>=filtered.length;}
for(const id of ['query','kind'])document.querySelector('#'+id).addEventListener('input',()=>{page=0;render();});document.querySelector('#prev').onclick=()=>{page--;render();};document.querySelector('#next').onclick=()=>{page++;render();};render();
</script>'''.replace('PAYLOAD', payload)
write('media.html', page('Všechna média', '<p><a href="index.html">← Zpět do katalogu</a></p><div class="toolbar"><input type="search" id="query" placeholder="Název nebo část cesty…" aria-label="Hledat média"><select id="kind" aria-label="Typ médií"><option value="all">Všechna média</option><option value="gallery">Fotografie z galerií</option><option value="partner-logo">Loga partnerů</option><option value="documents">Dokumenty a ostatní soubory</option></select></div><p id="result" aria-live="polite"></p><div class="toolbar"><button id="prev">Předchozí</button><button id="next">Další</button></div><div class="grid" id="media"></div>', script=media_script))

write('K_REVIZI.md', '''# K revizi před použitím na novém webu

Toto je obsahový archiv původního webu, nikoli schválené znění pro nový web. Zdrojové texty v Markdownu a raw exportech jsou zachovány.

| Oblast | Nález | Co rozhodnout |
| --- | --- | --- |
| E-mail | Kontakty uvádějí `dotazy@golmansketreninky.cz`; mockup používá `info@golmansketreninky.cz`. | Potvrdit adresu. |
| Telefony | Martin Altrichter +420 737 268 000; Marek Zapletal +420 603 118 008. | Určit hlavní kontakt. |
| Trenéři | 11 jmen, u 4 medailonek a fotografie; u dalších 7 pouze jméno. | Potvrdit současný tým a doplnit chybějící profily. |
| Trenérské životopisy | Obsahují historická angažmá, data narození a relativní délku působení („14 let“, „13 let“, „5 let“). | Aktualizovat a zkrátit pro nový web. |
| Skupinové tréninky | Článek březen 2026: neděle 14:50–15:50, 800 Kč, max. 6 gólmanů. Starší březen 2025: 750 Kč, max. 12. | Potvrdit současnou cenu, kapacitu a rozvrh; nepřebírat starší údaj. |
| Individuální trénink | Zdroj uvádí telefonickou domluvu v pracovní dny. | Potvrdit cenu a způsob rezervace. |
| Kemp 2026 | 12.–17. 7. 2026; 42 účastníků, 2 skupiny po 21; 11 jednotek na ledě + 11 na suchu; 14 990 Kč s ubytováním / 11 990 Kč bez. | Proběhlá akce; použít pro archiv nebo jako podklad, nikoli aktuální nabídku. |
| Platby a registrace | Historické články obsahují bankovní účet, platební pokyny a starý postup registrace. | Navrhnout aktuální postup. |
| Partneři | 5 log v panelu. Kemp 2026 navíc zmiňuje Střída Sport / CCM a H2 WORLD. | Potvrdit současné partnery a aktuální loga. |
| Fotografie | Zachovány názvy souborů, originály a popisky. Mnohé mají místo popisku jen IMG/DSC. | Vybrat fotografie a napsat smysluplné alt texty. |
| Aktuality | 327 příspěvků: 264 aktualit a 63 nabídek výstroje; archiv od roku 2012. | Vybrat reprezentativní aktuality a relevantní historii. |
| Události a místa | 181 historických událostí a 10 míst; nejsou to současné termíny a seznam aktivních stadionů. | Použít jen ověřené údaje. |
| Video a externí odkazy | Zachovány původní adresy; dostupnost a přehratelnost na externích platformách není garantována. | Vybrat videa pro nový web. |

## Přímé zdroje

- [Kontakty](https://www.golmansketreninky.cz/kontakty/)
- [Naši trenéři](https://www.golmansketreninky.cz/nasi-treneri/)
- [Tréninky – březen 2026](https://www.golmansketreninky.cz/2026/03/treninky-brezen-2026/)
- [Gólmanský speciální kemp 2026](https://www.golmansketreninky.cz/2026/04/golmansky-specialni-kemp-2026/)
''')

failed = coverage['media_failures']
file_types = {}
for m in media:
    ext = Path(m.get('local_path', m['source_url'])).suffix.lower()
    file_types[ext] = file_types.get(ext, 0) + 1
hashes = {}
for m in media:
    if m.get('sha256'):
        hashes.setdefault(m['sha256'], []).append(m['local_path'])
a.dump('data/duplicates.json', [{'sha256': k, 'paths': v} for k, v in hashes.items() if len(v) > 1])
write('README.md', f'''# Obsahový archiv původního WordPressu

Zdroj: https://www.golmansketreninky.cz/<br>
Staženo: {coverage['archived_at']}<br>
Určení: podklady k výběru, redakční úpravě a pozdější migraci. Archiv se automaticky nezobrazuje v Astro mockupu.

**Začněte souborem [index.html](index.html)** – lokální katalog galerií, trenérů, partnerů a článků. Funguje i bez internetu. [Všechna média](media.html) mají vyhledávání a filtry.

## Obsah

- **{coverage['record_counts']['post']} příspěvků** (264 aktualit, 63 nabídek výstroje), roky 2012–2026.
- **{coverage['record_counts']['page']} stránek**, **{coverage['record_counts']['event']} historických událostí**, **{coverage['record_counts']['location']} míst konání**.
- **{len(profiles)} trenérů**: 4 medailonky s fotografií, 7 dalších jmen.
- **{len(galleries)} galerií / {coverage['gallery_photos']} fotografií v galeriích** včetně všech nalezených stránek NextGEN.
- **{coverage['media_downloaded']} stažených médií**, {coverage['media_bytes'] / 1048576:.1f} MiB. Fotografie, loga, bannery a dokumenty.
- **{len(partners)} partnerů s logem** + historické zmínky o spolupráci v článcích.
- **{coverage.get('self_hosted_videos', 0)} odkazů na vlastní videosoubory** a **{coverage['video_embeds']} embedů**. Dostupná vlastní videa jsou v `media/videostream/`; videa z externích služeb zůstávají jako odkazy.

| Složka / soubor | Obsah |
| --- | --- |
| `stranky/` | Úplné texty stránek v Markdownu, včetně O nás, Foto, Video a Kontaktů. |
| `aktuality/` | Všechny příspěvky s názvem, daty a původním URL; rubrika je v `data/records.json`. |
| `treneri/` | Jednotlivé medailonky a odkazy na originální portréty. |
| `partneri/` | Přehled partnerů a jejich log. |
| `kontakt/` | Kontakty, registrace a zdroje. |
| `galerie/` | JSON seřazených fotografií a samostatný HTML náhled každé galerie. |
| `udalosti/`, `mista/` | Historické veřejné události a místa konání. |
| `media/uploads/` | WordPress média v původní struktuře rok/měsíc. |
| `media/gallery/` | Plné fotografie NextGEN podle původních galerií. |
| `media/videostream/` | Vlastní videa a náhledy ze starého Flash přehrávače. |
| `data/` | Strukturovaná data, vazby, zdroje, metadata, kontrolní součty a pokrytí. |
| `raw/` | Původní REST odpovědi a HTML/XML odpovědi pro dohledání přesného znění. |
| `K_REVIZI.md` | Rozdíly a otázky před použitím na novém webu. |

## Formát a dohledatelnost

Texty jsou zachovány; opravy a nové texty se mají dělat až redakčně. Markdown zachovává nadpisy, odkazy, tabulky a přílohy. V `data/records.json` je původní HTML i vykreslený obsah; `raw/http/*.json` mapuje požadavek na původní odpověď a datum stažení. Binární raw odpovědi odkazují relativním symlinkem na jedinou kopii média.

`data/media.json` obsahuje cestu, původní URL, využití na stránkách, velikost a SHA-256. `data/asset-aliases.json` mapuje náhledy na plné originály. Generované WordPress velikosti se nestahují opakovaně, jejich metadata zůstávají v raw exportu. Shodné soubory pod různými zdrojovými cestami jsou uvedeny v `data/duplicates.json`.

## Rozsah a kontrola

Veřejná REST API pro stránky, příspěvky, média, rubriky, štítky a komentáře; veřejné sitemapy pro události a místa; vykreslené stránky a stránkování NextGEN; viditelná navigace a panel partnerů. Soukromý obsah, účty a rezervace nejsou součástí exportu. Není to záloha databáze ani instalace WordPressu.

- Vykreslených HTML stránek: {coverage['rendered_page_count']}.
- Neúspěšná stažení stránek: {len(coverage['page_failures'])}.
- Neúspěšná stažení médií: {len(failed)}. Podrobnosti v [coverage.json](data/coverage.json).
- Externí obsah zůstává jako odkaz, externí weby se dále neprocházejí.

## Opakování

Z kořene projektu (`golmansketreninky-v2`), Python 3 + BeautifulSoup 4 + curl:

```sh
python3 scripts/archive-wordpress.py
python3 scripts/catalog-wordpress.py
```

Existující úspěšné odpovědi se používají z cache; skript tak pokračuje po přerušení. Pro nový časový snímek použijte novou složku / přejmenujte stávající archiv. Katalog a tematické výtahy jsou generované; redakční změny uchovávejte zvlášť, aby je opakované generování nepřepsalo.
''')
(R.parent / 'README.md').write_text('# Obsah pro nový web\n\n- [Katalog původního WordPressu](wordpress/index.html)\n- [Přehled archivu a struktury](wordpress/README.md)\n- [Všechny fotografie, loga a přílohy](wordpress/media.html)\n- [Co ověřit a upravit](wordpress/K_REVIZI.md)\n\nSložka `wordpress` uchovává zdrojové podklady. Vybrané a redakčně upravené texty lze následně připravit vedle ní.\n')
print(f'Catalogue ready: {len(profiles)} coaches, {len(partners)} partners, {len(galleries)} galleries, {len(items)} assets')

if (R / 'data/validation.json').exists():
    with (R / 'README.md').open('a') as f:
        f.write('\n## Výsledky kontroly\n\n[validation.json](data/validation.json) obsahuje výsledek kontroly pokrytí, souborů, kontrolních součtů a lokálních odkazů. Rozměry obrázků a metadata videí jsou v `data/image-dimensions.json` a `data/video-metadata.json`. Případná omezení původního zdroje popisuje [source-limitations.json](data/source-limitations.json).\n')
