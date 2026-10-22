"""Regenerate GitHub Pages HTML from tools/content.json. Python 3 standard library only."""
from pathlib import Path
import json,html,re,urllib.parse,datetime
ROOT=Path(__file__).resolve().parents[1];D=json.loads((ROOT/'tools/content.json').read_text());pages={}
E=lambda s:html.escape(str(s),quote=True)
BASE='https://casey-co.github.io/Aacropolis/'
NAV=[('Home',''),('Show Homes','show-homes'),('Our Homes','our-homes'),('Photo Gallery','gallery'),('Our Story','about'),('Our Process','process'),('Blog','blog')]
EXTRA=[('Meet the Team','about-1'),('Edmonton Communities','general-7'),('Quick Possession','quick-possession'),('Video Tours','copy-of-show-homes'),('Promotions','copy-of-about'),('STEF Tester Homepage','copy-of-home-1'),('Welcome Home','copy-of-home'),('Book a Visit','book-online')]
def link(path,text,cls='button'):return f'<a class="{cls}" href="@@/{path.strip("/")}/">{E(text)}</a>' if path else f'<a class="{cls}" href="@@/">{E(text)}</a>'
def image(src,alt='',cls='',eager=False):return f'<img class="{cls}" src="@@/{E(src)}" alt="{E(alt)}" loading="{"eager" if eager else "lazy"}" decoding="async">'
def pic(src,alt='',cls=''):return image(src,alt,cls)
def block(n,i):return D[n]['blocks'][i]
def paragraphs(b):
 return ''.join(f'<{x["tag"] if x["tag"] in ["p","li"] else "p"}>{E(x["text"])}</{x["tag"] if x["tag"] in ["p","li"] else "p"}>' for x in b['paragraphs']) or f'<p>{E(b["text"])}</p>'
def local(u):
 if u in D['pdfs']:return '@@/'+D['pdfs'][u]
 if u.startswith('https://www.aacropolishomes.com'):
  p=u.split('.com',1)[1]
  if p=='':return '@@/'
  if any(p.startswith('/'+v) for v in ['booking-calendar','booking-form','intake-form','service-page']):return u
  return '@@/'+p.strip('/')+'/'
 if u.startswith('tel:'):return 'tel:+18255102298'
 return u

def head(title,sub=''):
 return f'<section class="page-intro wrap"><p class="eyebrow">AACROPOLIS HOMES · EDMONTON & AREA</p><h1>{E(title)}</h1>'+ (f'<p class="lede">{E(sub)}</p>' if sub else '')+'</section>'
def section(body,cls=''):return f'<section class="section {cls}"><div class="wrap">{body}</div></section>'
def gallery(items):
 return '<div class="gallery">'+''.join(f'<a class="photo" data-lightbox href="@@/{E(x["src"])}" aria-label="Enlarge photo: {E(x["alt"])}">{pic(x["src"],x["alt"])}<span class="photo-zoom" aria-hidden="true">↗</span></a>' for x in items)+'</div>'
def add(route,title,body,kind='standard',noindex=False):pages[route]=dict(title=title,body=body,kind=kind,noindex=noindex)
def backend(title,original,desc=''):
 return head(title,desc)+section('<div class="service-panel"><p>Choose your time and complete your details in our secure booking system.</p>'+f'<a class="button" href="{E(original)}">Continue to booking</a><p class="small">You’ll continue on the Aacropolis Homes website.</p></div>')
add('','Custom Home Builder in Edmonton',f'''<section class="home-hero" style="background-image:linear-gradient(90deg,#28231fe0,#28231f44),url('@@/{D['hero']}')"><div class="home-content"><p class="eyebrow">EDMONTON HOME BUILDER</p><h1>Better living<br><em>starts with us.</em></h1>{link('show-homes','Visit our Show Homes')}</div></section>''','home')
add('about','About Aacropolis Homes',head('About Aacropolis Homes')+section(f'<div class="split"><div class="prose">{paragraphs(block("about",1))}{link("about-1","Meet the Team","text-link")}</div>{pic(D["about"]["images"][0]["src"],"An Aacropolis custom home")}</div>'))
n='copy-of-home';add(n,'Welcome Home',section(f'<div class="split welcome"><div><p class="eyebrow">AACROPOLIS HOMES</p><h1>Welcome Home</h1><p class="serif lede">Allow us to take you for a tour</p>{paragraphs(block(n,2))}{link("show-homes","Visit our Showhome")}</div>{image(D[n]["images"][0]["src"],"Custom entryway and staircase",eager=True)}</div>'))
n='about-1'; bio=paragraphs(block(n,6)).replace('Casey Skarkey','Casey Sharkey')
add(n,'Meet the Team',head('Our Story','Better living starts with us.')+section('<div class="prose centered">'+paragraphs(block(n,2))+'</div>')+section(pic(D[n]['images'][0]['src'],'Aacropolis interior','wide-banner'))+section(f'<div class="team"><p class="eyebrow">MEET THE TEAM</p><h2>Casey Sharkey</h2><p class="serif">Area Sales Manager</p><div class="prose">{bio}</div><a class="text-link" href="mailto:casey@aacropolishomes.com">casey@aacropolishomes.com</a></div>'))
# All original process descriptions, with steps presented as consistent cards.
steps=[]
step_titles=['Lot Selection','Initial Project Assessment','Design Process','Specification Review','Enter into ANHWP Contract','Submission of Architectural Control','Apply for Building Permit & Start Construction','Notice of Possession, Pre-Occupancy Walkthrough, and Walkthrough','First Year, 6 Month & 12 Month Post Possessions Warranty Walkthrough']
step_counts=[1,3,2,2,1,2,4,4,4]
source_paragraphs=[p for b in D['process']['blocks'][1:] for p in b['paragraphs']]
offset=0
for title,count in zip(step_titles,step_counts):
 ps=source_paragraphs[offset:offset+count];offset+=count
 steps.append('<li><h2>'+E(title)+'</h2>'+''.join('<p>'+E(p['text'])+'</p>' for p in ps)+'</li>')
add('process','Our Process',head('Our Process','From your first lot selection to the years after you move in.')+section('<ol class="steps">'+''.join(steps)+'</ol>'))
# Listing pages preserve source availability labels and contact information.
for n,title in [('show-homes','Show Homes'),('quick-possession','Quick Possession Homes')]:
 t=[]
 # Source sections are manually grouped below; all descriptions remain in content.json.
 if n=='show-homes':
  cards=[('KESWICK · ELEANOR','Show Home Open & For Sale','Duplex Bungalow','4621 Knight Point SW, Edmonton, AB',D[n]['images'][0]['src'],'Monday–Thursday: 3–8 PM<br>Saturday–Sunday: Noon–5 PM<br>Closed Friday',0),('KESWICK · LOANNA','Sold','Rear Attached Garage · 2,371 Sq. Ft.','4541 Knight Wynd SW, Edmonton, AB',D[n]['images'][1]['src'],'',1),('RIVERSTEAD','Lots Now Available','Contact Casey to discuss Stage 52, 55 and 56 river lots!','',D[n]['images'][2]['src'],'',2)]
 else:
  cards=[('ELEANOR III','Show Home For Sale','1,598 Sq. Ft.','4621 Knight Point SW, Edmonton, AB',D[n]['images'][0]['src'],'',0),('LOANNA','Show Home For Sale','2,371 Sq. Ft.','4541 Knight Wynd SW, Edmonton, AB',D[n]['images'][1]['src'],'',1),('ELEANOR','Sold','1,581 Sq. Ft.','4616 Knight Point SW, Edmonton, AB',D[n]['images'][2]['src'],'',None)]
 pdf_links=[x for x in D[n]['links'] if '/_files/' in x['href']]
 for name,status,spec,address,src,hours,pidx in cards:
  brochure=''
  if pidx is not None and pidx<len(pdf_links):brochure=f'<a class="text-link" href="{E(local(pdf_links[pidx]["href"]))}" target="_blank" rel="noopener">Download information brochure ↗</a>'
  t.append(f'<article class="listing"><a data-lightbox href="@@/{src}">{pic(src,name)}</a><div class="listing-copy"><p class="status">{E(status)}</p><h2>{E(name)}</h2><p class="serif">{E(spec)}</p><p>{E(address)}</p>'+ (f'<p>{hours}</p>' if hours else '')+'<p><a href="tel:+18255102298">825.510.2298</a><br><a href="mailto:casey@aacropolishomes.com">casey@aacropolishomes.com</a></p>'+brochure+(f'<a class="text-link" href="https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(address)}" target="_blank" rel="noopener">View location ↗</a>' if address else '')+'</div></article>')
 add(n,title,head(title)+('' if n!='show-homes' else '<p class=\"center wrap\">Almost sold out! One luxury duplex bungalow available for quick possession.</p>')+section(''.join(t)))
# Full native gallery inventories, including images not initially shown by Wix.
g=next(iter(D['gallery']['galleries'].values()));add('gallery','Photo Gallery',head('Photo Gallery','Explore the details that make an Aacropolis home.')+section(gallery(g)))
parts=[]
n='our-homes';b=D[n]['blocks'];gs=D[n]['galleries'];groups=[('comp-kq11rumz_galleryData',0,1),('comp-kq11t6te_galleryData',2,3),('comp-m4bhm7hl_galleryData',4,5),('comp-m4bi19ll_galleryData',6,7)]
for key,ti,pi in groups:
 title=b[ti]['text'].title();extra=''
 if ti==2:extra=link('quick-possession','View Available Bungalows','text-link')+link('show-homes','Visit the Show Home','text-link')
 parts.append(section(f'<div class="section-heading"><h2>{E(title)}</h2><div class="prose">{paragraphs(b[pi])}{extra}</div></div>'+gallery(gs[key]),'soft' if ti in [2,6] else ''))
parts.append(section(f'<div class="section-heading"><h2>Rear Lane Homes</h2><div>{paragraphs(b[9])}'+''.join(f'<a class="text-link" href="{E(local(a["href"]))}">{E(a["text"])}</a>' for a in D[n]['links'] if a['text'] in ['VIEW AVAILABLE REAR LANE HOME','Read more about rear lane homes'])+'</div></div>'))
add(n,'Our Homes',head('Our Homes','Custom homes, thoughtfully built around you.')+''.join(parts))
# Blog: complete nine-article local archive, with original dates and wording.
posts=[]
for n,d in D.items():
 if not n.startswith('post__') or 'body' not in d:continue
 route=n.replace('__','/',1)
 # Join sentence fragments separated by image wrapping in the Wix article HTML.
 merged=[]
 for paragraph in d['body']:
  if merged and paragraph['tag']=='p' and paragraph['text'][:1].islower() and not re.search(r'[.!?:]$',merged[-1]['text']):
   merged[-1]['text']+=' '+paragraph['text']
  else:merged.append(dict(paragraph))
 d['body']=merged
 posts.append((route,d))
 body=''.join(f'<{p["tag"]}>{E(p["text"])}</{p["tag"]}>' for p in d['body'])
 imgs=gallery(d['images']) if d['images'] else ''
 add(route,d['title'],head(d['title'])+section(f'<article class="article prose"><p class="eyebrow">{E(d["date"])} · AACROPOLIS HOMES</p>'+body+'</article>'+imgs+link('blog','All Articles','text-link')))
posts.sort(key=lambda x:datetime.datetime.strptime(x[1]['date'],'%b %d, %Y'),reverse=True)
add('blog','Our Blog',head('Our Blog','Ideas, insights, and a closer look at the homebuilding journey.')+section('<div class="blog-grid">'+''.join(f'<article class="blog-card">'+(f'<a href="@@/{route}/">{pic(d["cover"],d["title"])}</a>' if d.get('cover') else '')+f'<div><p class="eyebrow">{E(d["date"])}</p><h2><a href="@@/{route}/">{E(d["title"])}</a></h2><p>{E(next((p["text"] for p in d["body"] if len(p["text"])>100),"")[:180])}…</p>{link(route,"Read Article","text-link")}</div></article>' for route,d in posts)+'</div>'))
# Communities: actual published locations; no made-up case studies or stock testimonials.
locs=D['locations'];options='<button class="place active" data-lat="53.54" data-lon="-113.50" data-title="Edmonton & Surrounding Area" aria-pressed="true">Edmonton & Surrounding Area</button>'
options+=''.join(f'<button class="place" data-lat="{x["latitude"]}" data-lon="{x["longitude"]}" data-title="{E(x["title"].strip())}" aria-pressed="false">{E(x["title"].strip())}</button>' for x in locs)
community=f'<div class="communities"><div><p class="eyebrow">PLACES WE’VE BUILT</p><h2 id="map-title">Edmonton & Surrounding Area</h2><iframe id="community-map" title="Map of Edmonton and surrounding area" loading="lazy" src="https://maps.google.com/maps?q=53.54,-113.50&z=10&output=embed" referrerpolicy="no-referrer-when-downgrade"></iframe><p><a id="map-link" class="text-link" href="https://www.google.com/maps/search/?api=1&query=53.54,-113.50" target="_blank" rel="noopener">Open in Google Maps ↗</a></p></div><div class="places">{options}</div></div>'
build_map = '<div class="aac-build-map" id="aacropolis-build-map"><div class="section-heading"><div><p class="eyebrow">OUR BUILDING HISTORY</p><h2>Our homes.<br><em>Your communities.</em></h2></div><p>From Edmonton’s favourite neighbourhoods to wide-open Alberta acreages, we’ve been building in the places you call home.</p></div><div class="toolbar"><span class="section-label">WHERE WE’VE BUILT</span><div class="filters" role="group" aria-label="Explore our building history"><button type="button" data-filter="alberta" aria-pressed="true">Across Alberta</button><button type="button" data-filter="new" aria-pressed="false">New neighbourhoods</button><button type="button" data-filter="infill" aria-pressed="false">Infills</button><button type="button" data-filter="acreage" aria-pressed="false">Acreages</button></div></div><div class="map-wrap"><div id="map" aria-label="Interactive map showing communities where Aacropolis Homes has built"></div><div class="map-caption"><span class="eyebrow">A LOCAL LEGACY</span><h3>Built here.<br>Rooted here.</h3><p id="view-copy">Our roots in Edmonton.<br>Our reach across Alberta.</p><div class="caption-rule"></div><span class="map-hint">Select an emblem to explore.</span></div><button type="button" class="reset" aria-label="Reset current map view">↗ &nbsp; Reset view</button><div class="map-warning" role="status" hidden>The map background couldn’t load. Please check your connection.</div></div><noscript><p>Enable JavaScript to explore the interactive map.</p></noscript></div>'

copy=paragraphs(block('general-7',4));add('general-7','Edmonton Communities',head("Where We’ve Built",'Homes in Edmonton, surrounding communities, and beyond.')+section(community)+section('<div class="split"><div><p class="eyebrow">NEW NEIGHBOURHOODS</p><h2>A blank page, a fresh community, and a home that’s truly yours.</h2></div><div class="prose">'+copy+'</div></div>','soft')+section(build_map,'build-map-section'))
# Referral terms and registration use the working original service.
n='copy-of-about';p=''.join(paragraphs(x) for x in D[n]['blocks'] if x['id'] == D[n]['blocks'][1]['id'])
add(n,'Promotions & Referrals',head('Promotions & Referrals')+section('<div class="split"><div class="prose">'+p+'</div><div class="service-panel"><h2>Register Your Interest</h2><p>Register for the $2,000 new home discount and share the kind of home you’re looking for.</p><a class="button" href="https://www.aacropolishomes.com/copy-of-about">Open Registration Form</a><p class="small">Complete your registration on the Aacropolis Homes website.</p></div></div>'))
add('copy-of-show-homes','Video Tours',head('Video Tours','Take a virtual tour of the community of Keswick.')+section(f'<div class="video-wrap"><video controls playsinline preload="none" poster="@@/{D["videoPoster"]}"><source src="{E("@@/"+D["video"])}" type="video/mp4"><p><a href="{E("@@/"+D["video"])}">Watch the community tour</a></p></video></div>'))
for n in ['digitalwelcome','copy-of-home-1']:
 add(n,'STEF Tester Homepage' if n=='copy-of-home-1' else 'Welcome',f'<section class="welcome-hero" style="background-image:linear-gradient(90deg,#28231fe0,#28231f44),url(\'@@/{D["hero"]}\')"><div><p class="eyebrow">WELCOME</p><h1>Interested in the lot you see?<br><em>Let’s talk.</em></h1><div class="actions"><a class="button" href="tel:+18255102298">Call Us</a><a class="button outline" href="https://maps.app.goo.gl/Y2CTzXy8F17ZEzSH6">Visit Us</a></div></div></section>')
for n,title in [('book-online','Book a Visit'),('booking-calendar','Custom Home Consultation'),('booking-calendar/custom-home-consultation','Custom Home Consultation'),('service-page','Custom Home Consultation'),('booking-form','Complete Your Booking'),('intake-form','Book a Show Home Tour')]:
 original='https://www.aacropolishomes.com/'+('booking-calendar/custom-home-consultation' if n in ['book-online','booking-calendar','service-page','booking-form'] else n)
 add(n,title,backend(title,original,'Meet with us to discuss your home.'),noindex=n!='book-online')
add('inquiry-services-page','Our Services',head('Our Services')+section('<div class="service-panel"><h2>Let’s Talk About Your Home</h2><p>Contact our team to discuss your plans.</p><a class="button" href="mailto:casey@aacropolishomes.com">Email Casey</a></div>'))
# Preserve system URLs without suggesting that private account data has been copied.
for n,title in [('my-bookings','My Bookings'),('my-subscriptions','My Subscriptions'),('account-settings','Account Settings'),('cart-page','Cart'),('checkout','Checkout'),('thank-you-page','Thank You')]:
 add(n,title,head(title)+section(f'<div class="service-panel"><p>Continue on the Aacropolis Homes website to access this service.</p><a class="button" href="https://www.aacropolishomes.com/{n}">Continue to {E(title)}</a></div>'),noindex=True)
for n in ['items','items/this-is-a-title-01','items/this-is-a-title-02','items/this-is-a-title-03','fullscreen-page']:
 add(n,'Homes We’ve Built',head('Homes We’ve Built')+section('<p class="center">Explore our custom homes and photo gallery.</p><div class="actions">'+link('our-homes','Our Homes')+link('gallery','Photo Gallery','button outline')+'</div>'),noindex=True)
add('404','Page Not Found',head('Page Not Found','Let’s help you find your way home.')+section('<div class="actions">'+link('','Home')+link('site-map','All Pages','button outline')+'</div>'),noindex=True)
for n in ['popup-u505g','popup-auiju']:pages[n]=pages['404'].copy()
# Human-readable page index makes every hidden content page accessible.
add('site-map','All Pages',head('Explore Aacropolis Homes')+section('<div class="page-list">'+''.join(link(p,t,'page-link') for t,p in NAV+EXTRA)+link('digitalwelcome','Digital Welcome','page-link')+'</div>'))
# Friendly route aliases and original URL compatibility.
for a,b in {'home':'','meet-the-team':'about-1','communities':'general-7','edmonton-communities':'general-7','promotions':'copy-of-about','video-tours':'copy-of-show-homes','stef-tester-homepage':'copy-of-home-1'}.items():pages[a]=pages[b].copy()
for route,d in posts:pages['blog/'+route.split('/',1)[1]]=pages[route].copy()

def render(route,p):
 prefix='./' if not route else '../'*(len(route.split('/')))
 map_assets = '<link rel="stylesheet" href="@@/assets/build-map/leaflet.css"><link rel="stylesheet" href="@@/assets/build-map/map.css"><script src="@@/assets/build-map/leaflet.js" defer></script><script src="@@/assets/build-map/map.js" defer></script>' if route in ['general-7','communities','edmonton-communities'] else ''
 nav=''.join(f'<a href="@@/{path+"/" if path else ""}"'+(' aria-current="page"' if route==path else '')+f'>{E(t)}</a>' for t,path in NAV)
 more=''.join(f'<a href="@@/{path}/"'+(' aria-current="page"' if route==path else '')+f'>{E(t)}</a>' for t,path in EXTRA)
 description='Aacropolis Homes: custom homes, infills and acreage homes in Edmonton and surrounding communities. Better living starts with us.'
 body=f'''<!doctype html>
<html lang="en-CA"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(p['title'])} | Aacropolis Homes</title><meta name="description" content="{E(description)}"><meta name="theme-color" content="#59534f">{ '<meta name="robots" content="noindex,follow">' if p['noindex'] else ''}<link rel="stylesheet" href="@@/assets/site.css"><script src="@@/assets/site.js" defer></script>{map_assets}</head>
<body class="{p['kind']}"><a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="header-main wrap"><a class="brand" href="@@/" aria-label="Aacropolis Homes – Home">{image(D['logo'],'Aacropolis Homes',eager=True)}</a><button class="menu-toggle" aria-expanded="false" aria-controls="site-navigation">Menu <span aria-hidden="true">☰</span></button><nav id="site-navigation" aria-label="Main navigation">{nav}<details class="more-nav"><summary>More</summary><div>{more}<a href="@@/site-map/">All Pages</a></div></details></nav></div><nav class="explore-nav" aria-label="More Aacropolis pages"><a href="@@/about-1/">Meet the Team</a><a href="@@/general-7/">Edmonton Communities</a><a href="@@/copy-of-home-1/">STEF Tester Homepage</a></nav></header>
<main id="main">{p['body']}</main>
<footer class="site-footer"><div class="wrap"><div class="footer-top"><a class="brand" href="@@/">{image(D['logo'],'Aacropolis Homes')}</a><div><p class="serif">Better living starts with us.</p><a href="mailto:sales@aacropolishomes.com">sales@aacropolishomes.com</a><a href="tel:+18255102298">(825) 510-2298</a></div><div class="footer-links"><a href="@@/site-map/">All Pages</a><a href="@@/book-online/">Book a Visit</a><a href="https://www.instagram.com/aacropolishomes/" target="_blank" rel="noopener">Instagram ↗</a><a href="https://www.facebook.com/AacropolisHomes/" target="_blank" rel="noopener">Facebook ↗</a></div></div><p class="copyright">© {datetime.date.today().year} Aacropolis Homes Ltd. · Edmonton, Alberta</p></div></footer>
<dialog id="lightbox" aria-label="Photo viewer"><button id="lightbox-close" aria-label="Close photo viewer">Close ×</button><img id="lightbox-image" alt=""><p id="lightbox-caption"></p></dialog></body></html>'''
 return body.replace('@@/',prefix)
for route,p in pages.items():
 dest=ROOT/(route+'/index.html' if route else 'index.html');dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(render(route,p))
 if route and '/' not in route:
  # Previously shared .html links remain usable on GitHub Pages.
  alias=ROOT/(route+'.html');alias.write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url=./{route}/"><title>{E(p["title"])}</title></head><body><a href="./{route}/">Open {E(p["title"])}</a></body></html>')
(ROOT/'404.html').write_text(render('',pages['404']).replace('<head>','<head><base href=\"/Aacropolis/\">',1))
(ROOT/'.nojekyll').write_text('')
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+BASE+route+('/' if route else '')+'</loc></url>' for route,p in pages.items() if not p['noindex'])+'</urlset>')
(ROOT/'tools/page-inventory.json').write_text(json.dumps({r:{'title':p['title'],'noindex':p['noindex']} for r,p in pages.items()},indent=2))
print(f'Generated {len(pages)} routes, {len(posts)} original articles and {len(g)} gallery photos.')
