import json,pathlib,subprocess,sys,unittest,xml.etree.ElementTree as ET
ROOT=pathlib.Path(__file__).resolve().parents[1]; D=ROOT/"dist"
class NextubeSiteTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  subprocess.run([sys.executable,str(ROOT/"scripts/build.py")],check=True)
  subprocess.run([sys.executable,str(ROOT/"scripts/validate.py")],check=True)
 def test_all_published_locales_have_all_routes(self):
  locales=json.loads((ROOT/"content/locales.json").read_text()); features=json.loads((ROOT/"content/features.json").read_text())
  for code in locales:
   for tail in ("","about","features","download","faq","tips","blog","guide","comparison"):
    self.assertTrue((D/code.lower()/(tail or "")/"index.html").is_file())
   for f in features:self.assertTrue((D/code.lower()/"features"/f["id"]/"index.html").is_file())
 def test_every_page_is_nextube_and_not_job_connect(self):
  for p in D.rglob("*.html"):
   s=p.read_text()
   self.assertNotIn("Job Connect",s)
   self.assertNotIn("job search",s.lower())
   self.assertIn("Nextube",s)
 def test_play_links_and_tracking_are_present(self):
  app=json.loads((ROOT/"content/app.json").read_text())
  for p in D.rglob("*.html"):
   if p == D/"index.html": continue
   s=p.read_text()
   self.assertIn(app["google_play_url"],s)
   self.assertIn("google_play_click",s)
 def test_eight_country_flag_images_are_rendered(self):
  for code in json.loads((ROOT/"content/locales.json").read_text()):
   s=(D/code.lower()/"index.html").read_text()
   self.assertEqual(s.count('class="locale-flag"'),8)
   self.assertIn("flagcdn.com/w80/",s)
 def test_sitemaps_have_all_routes(self):
  ns="{http://www.sitemaps.org/schemas/sitemap/0.9}"
  urls={x.findtext(ns+"loc") for x in ET.parse(D/"sitemap.xml").getroot().findall(ns+"url")}
  txt=set((D/"sitemap.txt").read_text().splitlines())
  self.assertEqual(urls,txt)
if __name__=="__main__":unittest.main()
