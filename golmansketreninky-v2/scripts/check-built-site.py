"""Check local links, image targets, anchors and noindex in an Astro build."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else 'dist').resolve()
base='/' + (sys.argv[2].strip('/')+'/' if len(sys.argv)>2 and sys.argv[2].strip('/') else '')
class Page(HTMLParser):
 def __init__(self,path):
  super().__init__(convert_charrefs=True);self.path=path;self.ids=set();self.refs=[];self.noindex=False;self.errors=[];self.feed(path.read_text())
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:
   if a['id'] in self.ids:self.errors.append(f'Duplicate id {a["id"]}')
   self.ids.add(a['id'])
  if tag=='meta' and a.get('name')=='robots':self.noindex='noindex' in a.get('content','')
  if tag=='img' and 'alt' not in a:self.errors.append('Missing image alt')
  for key in ['href','src','poster','data-src']:
   if a.get(key):self.refs.append((key,a[key]))
pages={p:Page(p) for p in root.rglob('*.html')};errors=[];count=0
for path,page in pages.items():
 if not page.noindex:errors.append(f'{path}: noindex absent')
 errors += [f'{path}: {e}' for e in page.errors]
 for kind,value in page.refs:
  u=urlsplit(value)
  if u.scheme or u.netloc:continue
  if u.path.startswith('/'):
   if not u.path.startswith(base):errors.append(f'{path}: outside base {value}');continue
   target=root/unquote(u.path[len(base):])
  else:target=path.parent/unquote(u.path) if u.path else path
  if target.is_dir():target/='index.html'
  target=target.resolve();count+=1
  if not target.exists():errors.append(f'{path}: missing {value}')
  elif kind=='href' and u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:errors.append(f'{path}: missing anchor {value}')
assert not list(root.rglob('*.flv')), 'Legacy videos leaked into build'
assert not (root/'content').exists(), 'Source archive leaked into build'
if errors:print('\n'.join(errors[:50]));sys.exit(1)
print(f'OK: {len(pages)} stránek, {count} místních odkazů a médií, kotvy, alt a noindex. Base: {base}')
