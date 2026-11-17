#!/usr/bin/env python3
import html, json, pathlib, re, shutil, xml.etree.ElementTree as ET
ROOT=pathlib.Path(__file__).resolve().parents[1]; DIST=ROOT/"dist"
def load(name): return json.loads((ROOT/"content"/name).read_text(encoding="utf-8"))
APP=load("app.json"); LOCALES=load("locales.json"); FEATURES=load("features.json"); FAQ=load("faq.json"); SHOTS=load("screenshots.json"); STRATEGY=load("market-strategy.json")
BASE=APP["website_url"].rstrip("/"); CODES=STRATEGY["published_locales"]
def e(v): return html.escape(str(v),quote=True)
def url(code,tail=""): return f"{BASE}/{code.lower()}/"+(f"{tail}/" if tail else "")
CSS=r"""*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#080d1d;color:#f4f6ff;font:16px/1.72 system-ui,-apple-system,Segoe UI,sans-serif;background-image:radial-gradient(ellipse at 75% 0%,#22235a55,transparent 42%)}a{color:#76e7ff}a:focus-visible,summary:focus-visible{outline:3px solid #76e7ff;outline-offset:4px}header,main,footer{width:min(1160px,calc(100% - 36px));margin:auto}.home-header{display:flex;flex-direction:column;align-items:stretch;padding:18px 0 22px;border-bottom:1px solid #ffffff20}.standard-header{display:flex;align-items:center;gap:16px;padding:20px 0;border-bottom:1px solid #ffffff20}.locale-switch{display:flex;align-items:center;gap:8px;flex-wrap:wrap;width:100%;margin-bottom:12px}.locale-flag{display:inline-flex;width:42px;height:34px;align-items:center;justify-content:center;border:1px solid #465178;border-radius:8px;background:#111a35}.locale-flag img{width:28px;height:21px;object-fit:cover;border-radius:2px}.locale-flag[aria-current=page]{border-color:#55e7ff;box-shadow:0 0 0 1px #55e7ff}.header-main{display:flex;align-items:center;gap:18px;flex-wrap:wrap;width:100%}.standard-header .locale-switch{width:auto;flex:0 0 auto;margin:0}.brand{font-weight:950;font-size:1.25rem;letter-spacing:.08em;text-decoration:none;color:#fff}.brand b,.tag,.num{color:#65eaff}.header-main nav{display:flex;gap:10px;align-items:center;margin-inline-start:auto;flex-wrap:wrap}.nav-menu{position:relative}.nav-menu>summary{list-style:none;cursor:pointer;border:1px solid #465178;border-radius:10px;background:#111a35;padding:8px 13px;min-height:42px;font-weight:700}.nav-menu>summary::-webkit-details-marker{display:none}.nav-menu>summary:after{content:"⌄";color:#65eaff;margin-inline-start:8px}.nav-dropdown{position:absolute;z-index:20;top:calc(100% + 8px);inset-inline-start:0;display:grid;gap:3px;width:min(260px,calc(100vw - 36px));padding:8px;background:#101a34;border:1px solid #465178;border-radius:12px;box-shadow:0 18px 40px #000b}.nav-dropdown a{padding:8px 12px;text-decoration:none;border-radius:8px;color:#e8f4ff}.nav-dropdown a:hover{background:#25345a}.social-links{display:flex;gap:8px;margin-inline-start:auto}.social-link{width:34px;height:34px;display:grid;place-items:center;border:1px solid #465178;border-radius:9px;color:#eaf7ff}.social-link svg{width:18px;height:18px;fill:currentColor}.hero{display:grid;grid-template-columns:1.05fr .8fr;gap:40px;align-items:center;padding:64px 0 58px}.tag{font-size:.78rem;letter-spacing:.15em;font-weight:800}.hero h1,.page h1{font-size:clamp(2.5rem,6vw,4.7rem);line-height:1.08;margin:14px 0 18px;letter-spacing:-.035em}.lead{font-size:1.16rem;color:#bdc9e6;max-width:760px}.preview,.item,.faq,.step,.fact,.shot{background:linear-gradient(145deg,#141e3d,#10172e);border:1px solid #38466d;border-radius:18px;box-shadow:0 14px 36px #0003}.preview{padding:16px;text-align:center}.preview img{width:100%;height:auto;max-height:480px;object-fit:contain;border-radius:12px}.btn{display:inline-flex;align-items:center;justify-content:center;min-height:48px;margin-top:18px;padding:12px 22px;border-radius:999px;background:linear-gradient(100deg,#ffcf65,#ff8d46);color:#14172a;text-decoration:none;font-weight:900;box-shadow:0 6px 24px #ff9d4b44}.section{padding:42px 0;border-top:1px solid #ffffff1c}.section h2{font-size:clamp(1.7rem,3vw,2.3rem);margin-top:0}.muted{color:#aebbd8}.gallery{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px}.shot{padding:10px;margin:0}.shot img{width:100%;height:auto;display:block;border-radius:10px}.shot figcaption{font-size:.9rem;color:#c6d3ef;padding:9px 2px 2px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.item,.faq{padding:22px}.item h2,.faq h2{font-size:1.25rem;line-height:1.35}.item p,.faq p{color:#bdc9e6}.feature-shot{width:100%;max-height:250px;object-fit:contain;display:block;margin-bottom:12px}.steps,.facts{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.step,.fact{padding:18px}.step b{display:block;color:#65eaff;font-size:1.3rem}.fact small{display:block;color:#aebbd8}.faqgrid{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}.end{text-align:center;padding:32px;background:linear-gradient(130deg,#172a4b,#22204a);border:1px solid #4b6c9a;border-radius:20px;margin:32px 0}.page{padding:42px 0 64px}.page h1{font-size:clamp(2.2rem,5vw,3.7rem)}.detail-shot{width:min(100%,650px);height:auto;display:block;margin:24px 0;border-radius:14px;border:1px solid #38466d}.resource-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:26px}.resource-cards article{padding:18px;border:1px solid #38466d;border-radius:16px;background:#111a35}.download-hero{display:grid;grid-template-columns:1fr .65fr;gap:36px;align-items:center;padding:42px 0}.download-hero h1{font-size:clamp(2.2rem,5vw,3.8rem);line-height:1.12}.footer{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;padding:28px 0;border-top:1px solid #ffffff20;color:#aebbd8}.skip-link{position:absolute;left:10px;top:-100px;background:#fff;color:#111;padding:10px}.skip-link:focus{top:10px}.social-link:hover,.locale-flag:hover{border-color:#65eaff}html[dir=rtl] body{text-align:right}html[dir=rtl] .header-main nav{margin-inline-start:0;margin-inline-end:auto}@media(max-width:760px){.hero,.download-hero{grid-template-columns:1fr;padding:36px 0}.grid,.faqgrid,.steps,.facts,.resource-cards{grid-template-columns:1fr}.standard-header{flex-wrap:wrap}.standard-header .header-main{flex-wrap:wrap}.header-main nav{margin-inline-start:0;width:100%}.locale-switch{gap:6px}.social-links{margin-inline-start:auto}}"""
def analytics():
 return f"""<script async src="https://www.googletagmanager.com/gtag/js?id={e(APP['ga4_measurement_id'])}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{e(APP['ga4_measurement_id'])}');document.addEventListener('click',function(ev){{const a=ev.target.closest('a[data-play-click]');if(a)gtag('event','google_play_click',{{page_path:location.pathname,cta_location:a.dataset.playClick,link_url:a.href}});}});</script>"""
def socials():
 paths=[("Facebook","https://www.facebook.com/",'<path d="M13.5 21v-8h2.7l.4-3h-3.1V8.1c0-.9.3-1.5 1.6-1.5h1.7V3.9c-.3 0-1.3-.1-2.5-.1-2.5 0-4.2 1.5-4.2 4.2V10H7.3v3h2.8v8z"/>'),("X","https://x.com/",'<path d="M18.9 2H22l-6.8 7.8L23.2 22h-6.3L12 14.6 5.5 22H2.4l7.3-8.4L1.9 2h6.5l4.4 6.8zm-1.1 18h1.7L7.4 3.9H5.6z"/>'),("TikTok","https://www.tiktok.com/",'<path d="M19.6 7.2a6.9 6.9 0 0 1-4.2-1.4v8.1a6.1 6.1 0 1 1-6.1-6.1c.4 0 .8 0 1.2.1v3.4a2.8 2.8 0 1 0 1.6 2.6V2h3.4a3.9 3.9 0 0 0 4.1 3.7z"/>'),("Instagram","https://www.instagram.com/",'<rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="2"/>')]
 return '<div class="social-links" aria-label="Social media">'+''.join(f'<a class="social-link" href="{u}" target="_blank" rel="noopener noreferrer" aria-label="{n}"><svg viewBox="0 0 24 24" aria-hidden="true">{p}</svg></a>' for n,u,p in paths)+'</div>'
def flags(code,tail):
 out=[]
 for c in CODES:
  d=LOCALES[c]; current=' aria-current="page"' if c==code else ''
  out.append(f'<a class="locale-flag" lang="{c}" href="{url(c,tail)}" title="{e(d["language"])}" aria-label="{e(d["language"])}"{current}><img src="https://flagcdn.com/w80/{d["flag"]}.png" alt="{e(d["country"])} flag" width="40" height="30" loading="eager"></a>')
 return ''.join(out)
def header(code,tail):
 d=LOCALES[code]; t=d["text"]; home=(tail=="")
 nav=[("primary",t["navExplore"],[("about",t["navAbout"]),("features",t["navFeatures"]),("download",t["navDownload"]),("faq",t["navFaq"])]),("resources",t["navResources"],[("tips",t["navTips"]),("blog",t["navBlog"]),("guide",t["navGuide"]),("comparison",t["navCompare"])])]
 menus=[]
 for group,label,items in nav:
  menus.append(f'<details class="nav-menu" data-nav-group="{group}"><summary>{e(label)}</summary><div class="nav-dropdown">'+''.join(f'<a data-nav-item="{k}" href="{url(code,k)}">{e(v)}</a>' for k,v in items)+'</div></details>')
 switch='<div class="locale-switch" aria-label="Country and language">'+flags(code,tail)+socials()+'</div>'
 main=f'<div class="header-main"><a class="brand" href="{url(code)}">NEXT<b>UBE</b></a><nav aria-label="Primary navigation">{"".join(menus)}</nav></div>'
 return f'<header class="{"home-header" if home else "standard-header"}">{switch}{main}</header>'
def cta(t,loc):
 return f'<a class="btn" href="{e(APP["google_play_url"])}" target="_blank" rel="noopener noreferrer" data-play-click="{loc}">{e(t["cta"])}</a>'
def gallery(code):
 t=LOCALES[code]["text"]
 cards=''.join(f'<figure class="shot"><img src="{e(s["src"])}" width="526" height="296" alt="{e(t["galleryAlt"])} {i+1}" loading="lazy" decoding="async"><figcaption>{e(s["caption"])}</figcaption></figure>' for i,s in enumerate(SHOTS))
 return f'<section class="section"><h2>{e(t["galleryH2"])}</h2><p class="muted">{e(t["galleryIntro"])}</p><div class="gallery">{cards}</div></section>'
def feature_cards(code):
 d=LOCALES[code]; t=d["text"]; cards=[]
 for i,(title,desc) in enumerate(d["features"]):
  slug=FEATURES[i]["id"]; shot=SHOTS[min(i+1,len(SHOTS)-1)]["src"]
  cards.append(f'<article class="item"><img class="feature-shot" src="{e(shot)}" alt="{e(t["galleryAlt"])}" loading="lazy"><h2><a href="{url(code,"features/"+slug)}">{e(title)}</a></h2><p>{e(desc)}</p><a href="{url(code,"features/"+slug)}">{e(t["learn"])}</a></article>')
 return '<div class="grid">'+''.join(cards)+'</div>'
def faq_cards(code):
 d=LOCALES[code]
 return '<div class="faqgrid">'+''.join(f'<article class="faq"><h2>{e(q)}</h2><p>{e(a)}</p></article>' for q,a in d["faq"])+'</div>'
def schema(code,tail,title,desc):
 canonical=url(code,tail); d=LOCALES[code]
 graph=[{"@type":"Organization","@id":BASE+"/#organization","name":APP["developer"],"url":BASE+"/","email":APP["support_email"]},{"@type":"VideoGame","@id":BASE+"/#game","name":APP["name"],"gamePlatform":"Android","applicationCategory":"GameApplication","description":d["text"]["aboutIntro"],"image":APP["icon_url"],"url":APP["google_play_url"],"publisher":{"@id":BASE+"/#organization"}},{"@type":"WebPage","name":title,"description":desc,"url":canonical,"inLanguage":code}]
 if tail=="faq": graph.append({"@type":"FAQPage","@id":canonical+"#faq","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in d["faq"]]})
 return {"@context":"https://schema.org","@graph":graph}
def meta(code,tail,title,desc):
 canonical=url(code,tail); alternates=''.join(f'<link rel="alternate" hreflang="{c}" href="{url(c,tail)}">' for c in CODES)+f'<link rel="alternate" hreflang="x-default" href="{url("en-US",tail)}">'
 return f'<title>{e(title)}</title><meta name="description" content="{e(desc)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{canonical}">{alternates}<meta property="og:type" content="website"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{e(APP["icon_url"])}"><meta name="twitter:card" content="summary"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}">'
def page(code,tail,title,desc,body):
 d=LOCALES[code]; direction="ltr"
 canonical=url(code,tail); ld=json.dumps(schema(code,tail,title,desc),ensure_ascii=False)
 return f'''<!doctype html><html lang="{code}" dir="{direction}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">{meta(code,tail,title,desc)}<meta name="theme-color" content="#080d1d"><link rel="icon" href="{e(APP["icon_url"])}"><link rel="preconnect" href="https://play-lh.googleusercontent.com" crossorigin><link rel="stylesheet" href="{BASE}/assets/style.css"><script type="application/ld+json">{ld}</script>{analytics()}</head><body data-page-section="{tail or "home"}"><a class="skip-link" href="#main-content">{e(d["text"]["skip"])}</a>{header(code,tail)}<main id="main-content">{body}</main><footer class="footer"><span>© DevImpact · Nextube</span><span><a href="{e(APP["privacy_policy_url"])}">{e(d["text"]["privacy"])}</a> · <a href="mailto:{e(APP["support_email"])}">{e(d["text"]["support"])}</a></span></footer></body></html>'''
def page_content(code,section):
 d=LOCALES[code]; t=d["text"]
 if section=="home":
  body=f'<section class="hero"><div><div class="tag">{e(t["tag"])}</div><h1>{e(t["homeH1"])}</h1><p class="lead">{e(t["homeIntro"])}</p>{cta(t,"home_hero")}</div><div class="preview"><img src="{e(SHOTS[0]["src"])}" width="526" height="296" alt="{e(t["galleryAlt"])} 1" fetchpriority="high"></div></section>{gallery(code)}<section class="section"><h2>{e(t["featuresH1"])}</h2>{feature_cards(code)}</section><section class="end"><h2>{e(t["downloadH1"])}</h2>{cta(t,"home_end")}</section>'
 elif section=="about":
  body=f'<section class="page"><div class="tag">NEXTUBE · {e(t["tag"])}</div><h1>{e(t["aboutH1"])}</h1><p class="lead">{e(t["aboutIntro"])}</p><img class="detail-shot" src="{e(APP["icon_url"])}" alt="Nextube app icon" width="240" height="240">{cta(t,"about")}</section>{gallery(code)}'
 elif section=="features":
  body=f'<section class="page"><div class="tag">NEXTUBE · ANDROID PUZZLE</div><h1>{e(t["featuresH1"])}</h1><p class="lead">{e(t["featuresIntro"])}</p>{feature_cards(code)}</section><section class="end"><h2>{e(t["downloadH1"])}</h2>{cta(t,"features_end")}</section>'
 elif section=="download":
  body=f'<section class="download-hero"><div><div class="tag">NEXTUBE · ANDROID</div><h1>{e(t["downloadH1"])}</h1><p class="lead">{e(t["downloadIntro"])}</p>{cta(t,"download_hero")}<p class="muted">{e(t["note"])}</p></div><div class="preview"><img src="{e(SHOTS[0]["src"])}" alt="{e(t["galleryAlt"])}" width="526" height="296"></div></section><section class="section"><h2>{e(t["stepsH2"])}</h2><div class="steps">'+''.join(f'<article class="step"><b>0{i+1}</b>{e(t[k])}</article>' for i,k in enumerate(("step1","step2","step3")))+'</div></section><section class="section"><div class="facts"><div class="fact"><small>{e(t["platform"])}</small>Android</div><div class="fact"><small>{e(t["developer"])}</small>DevImpact</div><div class="fact"><small>{e(t["package"])}</small>{e(APP["package_id"])}</div></div></section>'
 elif section=="faq":
  body=f'<section class="page"><div class="tag">NEXTUBE · FAQ</div><h1>{e(t["faqH1"])}</h1><p class="lead">{e(t["faqIntro"])}</p>{faq_cards(code)}</section><section class="end"><h2>{e(t["downloadH1"])}</h2>{cta(t,"faq_end")}</section>'
 else: raise ValueError(section)
 titles={
 "home":t["homeH1"]+" | Nextube","about":t["aboutH1"]+" | Nextube","features":t["featuresH1"]+" | Nextube","download":t["downloadH1"]+" | Nextube","faq":t["faqH1"]+" | Nextube"}
 desc={"home":t["homeIntro"],"about":t["aboutIntro"],"features":t["featuresIntro"],"download":t["downloadIntro"],"faq":t["faqIntro"]}[section]
 return page(code,"" if section=="home" else section,titles[section],desc,body)
def resource_page(code,section):
 d=LOCALES[code]; t=d["text"]; r=d["resources"][section]
 topics=d["features"][:3]
 cards=''.join(f'<article><h2>{e(x)}</h2><p>{e(y)}</p><a href="{url(code,"features/"+FEATURES[i]["id"])}">{e(t["learn"])}</a></article>' for i,(x,y) in enumerate(topics))
 body=f'<section class="page"><div class="tag">NEXTUBE · {e(t["navResources"])}</div><h1>{e(r["title"])}</h1><p class="lead">{e(r["description"])}</p><div class="resource-cards">{cards}</div><section class="section"><h2>{e(t["featuresH1"])}</h2><p>{e(t["featuresIntro"])}</p><a class="btn" href="{url(code,"features")}">{e(t["navFeatures"])}</a></section></section>'
 return page(code,section,r["title"],r["description"],body)
def feature_page(code,index):
 d=LOCALES[code]; t=d["text"]; title,desc=d["features"][index]; slug=FEATURES[index]["id"]; shot=SHOTS[min(index+1,len(SHOTS)-1)]
 body=f'<article class="page"><div class="tag">NEXTUBE · PUZZLE FEATURE</div><h1>{e(title)}</h1><p class="lead">{e(desc)}</p><img class="detail-shot" src="{e(shot["src"])}" width="526" height="296" alt="{e(t["galleryAlt"])}"><p>{e(desc)}</p><a href="{url(code,"features")}">{e(t["navFeatures"])}</a><br>{cta(t,"feature_detail")}</article>'
 return page(code,"features/"+slug,title+" | Nextube",desc,body)
def main():
 if DIST.exists(): shutil.rmtree(DIST)
 (DIST/"assets").mkdir(parents=True)
 (DIST/"assets/style.css").write_text(CSS,encoding="utf-8")
 target=url("en-US","about")
 root=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="google-site-verification" content="8mOiNMu4Tn477yFaR-IWrNQGhdqH1TpF6NKKoN94Oms"><meta name="robots" content="noindex,follow"><title>Nextube</title><link rel="canonical" href="{target}"><meta http-equiv="refresh" content="0; url={target}"><script>window.location.replace("{target}");</script></head><body><p><a href="{target}">Continue to Nextube</a></p></body></html>'''
 (DIST/"index.html").write_text(root,encoding="utf-8")
 routes=[]
 for code in CODES:
  for section in ("home","about","features","download","faq"):
   tail="" if section=="home" else section
   p=DIST/code.lower()/(tail or "")/"index.html"; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(page_content(code,section),encoding="utf-8"); routes.append((url(code,tail),code,tail))
  for i,f in enumerate(FEATURES):
   tail="features/"+f["id"]; p=DIST/code.lower()/tail/"index.html"; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(feature_page(code,i),encoding="utf-8"); routes.append((url(code,tail),code,tail))
  for section in ("tips","blog","guide","comparison"):
   p=DIST/code.lower()/section/"index.html"; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(resource_page(code,section),encoding="utf-8"); routes.append((url(code,section),code,section))
 (DIST/"robots.txt").write_text("User-agent: *\nAllow: /\n\nSitemap: "+BASE+"/sitemap.xml\nSitemap: "+BASE+"/sitemap.txt\n",encoding="utf-8")
 ns="http://www.sitemaps.org/schemas/sitemap/0.9"; xns="http://www.w3.org/1999/xhtml"; ET.register_namespace("",ns); ET.register_namespace("xhtml",xns)
 rootel=ET.Element("{"+ns+"}urlset")
 for loc,code,tail in routes:
  node=ET.SubElement(rootel,"{"+ns+"}url"); ET.SubElement(node,"{"+ns+"}loc").text=loc
  for c in CODES: ET.SubElement(node,"{"+xns+"}link",{"rel":"alternate","hreflang":c,"href":url(c,tail)})
  ET.SubElement(node,"{"+xns+"}link",{"rel":"alternate","hreflang":"x-default","href":url("en-US",tail)})
 ET.ElementTree(rootel).write(DIST/"sitemap.xml",encoding="utf-8",xml_declaration=True)
 (DIST/"sitemap.txt").write_text("\n".join(x[0] for x in routes)+"\n",encoding="utf-8")
 ll="# Nextube\n\n"+APP["description"]+"\n\n- Google Play: "+APP["google_play_url"]+"\n- Official website: "+BASE+"/\n"
 for c in CODES: ll+=f"- {c}: {url(c)}\n"
 (DIST/"llms.txt").write_text(ll,encoding="utf-8")
if __name__=="__main__": main()
