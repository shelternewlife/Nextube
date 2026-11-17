#!/usr/bin/env python3
import json,pathlib,sys,xml.etree.ElementTree as ET
ROOT=pathlib.Path(__file__).resolve().parents[1]; D=ROOT/"dist"; APP=json.loads((ROOT/"content/app.json").read_text()); LO=json.loads((ROOT/"content/locales.json").read_text()); S=json.loads((ROOT/"content/market-strategy.json").read_text())
errors=[]
def check(ok,msg):
 if not ok: errors.append(msg)
check((D/"index.html").is_file(),"Missing root redirect")
check("Nextube" in (D/"index.html").read_text(),"Root redirect is not branded Nextube")
check(APP["package_id"] in APP["google_play_url"],"Google Play package ID mismatch")
check(set(LO)==set(S["published_locales"]),"Locale bundles do not match published locale registry")
expected=set()
for code in S["published_locales"]:
 for tail in ("","about","features","download","faq","tips","blog","guide","comparison"):
  expected.add(f'{APP["website_url"].rstrip("/")}/{code.lower()}/'+(tail+"/" if tail else ""))
 for f in json.loads((ROOT/"content/features.json").read_text()):
  expected.add(f'{APP["website_url"].rstrip("/")}/{code.lower()}/features/{f["id"]}/')
 for tail in ("","about","features","download","faq","tips","blog","guide","comparison"):
  p=D/code.lower()/(tail or "")/"index.html"
  check(p.is_file(),f"Missing route {p.relative_to(D)}")
  if p.is_file():
   source=p.read_text()
   check("Job Connect" not in source,f"Legacy brand remains in {p.relative_to(D)}")
   check('rel="canonical"' in source,f"Missing canonical in {p.relative_to(D)}")
   check('application/ld+json' in source,f"Missing structured data in {p.relative_to(D)}")
for p in D.rglob("*.html"):
 source=p.read_text()
 check("Job Connect" not in source,f"Legacy brand remains in {p.relative_to(D)}")
 check("job search" not in source.lower(),f"Legacy job-search content remains in {p.relative_to(D)}")
try:
 ns="{http://www.sitemaps.org/schemas/sitemap/0.9}"
 urls={x.findtext(ns+"loc") for x in ET.parse(D/"sitemap.xml").getroot().findall(ns+"url")}
 check(urls==expected,"XML sitemap does not exactly match generated locale routes")
 txt=set((D/"sitemap.txt").read_text().splitlines())
 check(txt==expected,"Text sitemap does not exactly match generated locale routes")
except Exception as ex: errors.append("Invalid sitemap: "+str(ex))
if errors: print("\n".join(errors)); sys.exit(1)
print(f"Validated {len(expected)} Nextube routes across {len(LO)} locales.")
