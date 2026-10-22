"""Validate generated local links, image references, document structure and source coverage."""
from pathlib import Path
from html.parser import HTMLParser
import re,json
ROOT=Path(__file__).resolve().parents[1]
class Document(HTMLParser):
 def __init__(self):super().__init__();self.refs=[];self.h1=0;self.viewport=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='h1':self.h1+=1
  if tag=='meta' and a.get('name')=='viewport':self.viewport=True
  for k in ['href','src','poster']:
   if a.get(k):self.refs.append(a[k])
errors=[];count=0
for route in json.loads((ROOT/'tools/page-inventory.json').read_text()):
 p=ROOT/(route+'/index.html' if route else 'index.html');s=p.read_text();t=Document();t.feed(s);count+=1
 if t.h1!=1:errors.append(f'{p}: expected one h1, got {t.h1}')
 if not t.viewport:errors.append(f'{p}: missing viewport')
 for ref in t.refs+re.findall(r"url\(['\"]?([^)'\"]+)",s):
  if ref.startswith(('https:','http:','mailto:','tel:','#','data:')):continue
  q=(p.parent/ref.split('#')[0].split('?')[0]).resolve()
  if q.is_dir():q=q/'index.html'
  if not q.exists():errors.append(f'{p.relative_to(ROOT)}: missing {ref}')
 for prohibited in ['@@/','This is a Paragraph','Thanks for submitting!','Casey Skarkey','Managaer']:
  if prohibited in s:errors.append(f'{p}: unexpected {prohibited}')
process=(ROOT/'process/index.html').read_text()
if process.count('<li>')!=9:errors.append('Expected nine process steps')
print(f'Checked {count} routes; {len(errors)} errors.')
for e in errors:print(e)
raise SystemExit(bool(errors))
