import hashlib, json, sys, unittest
from pathlib import Path
from urllib.parse import urlsplit
HUB=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HUB/"tools"))
import build_conferences
class MultiVenueTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls): cls.catalog=json.loads((HUB/"catalog.json").read_text())
 def test_catalog_has_cross_conference_coverage_and_unavailable_years(self):
  venues=self.catalog["venues"]
  self.assertGreaterEqual(sum(bool(x["available_years"]) for x in venues.values()),10)
  self.assertEqual(venues["ICCV"]["missing_years"],[2022,2024,2026])
  self.assertEqual(venues["NAACL"]["missing_years"],[2023,2026])
  for venue,meta in venues.items():
   self.assertEqual(set(meta["available_years"])|set(meta["missing_years"]),set(range(2022,2027)))
 def test_shards_match_catalog_hashes_counts_and_schema(self):
  for venue,meta in self.catalog["venues"].items():
   if venue=="CVPR": continue
   for year in meta["available_years"]:
    item=meta["years"][str(year)]; raw=(HUB/item["file"]).read_bytes()
    self.assertEqual(hashlib.sha256(raw).hexdigest(),item["sha256"]);self.assertEqual(len(raw),item["bytes"])
    bundle=json.loads(raw);self.assertEqual(bundle["year"],year);self.assertEqual(bundle["venue"],venue);self.assertEqual(len(bundle["papers"]),item["count"])
    for p in bundle["papers"]:
     for key in ("id","venue","year","title","authors","abstract","paper_url","pdf_url","source","track_status","cluster","primary_area"):self.assertIn(key,p)
     self.assertEqual(p["venue"],venue);self.assertEqual(p["year"],year)
     for key,ext in (("paper_url",""),("pdf_url",".pdf")):
      value=p[key]
      if value:
       self.assertEqual(build_conferences.safe_url(value, venue, ext), value)
 def test_url_allowlist_rejects_untrusted_hosts_and_decorated_urls(self):
  self.assertEqual(build_conferences.safe_url("https://aclanthology.org/2024.acl-long.1/","ACL"),"https://aclanthology.org/2024.acl-long.1/")
  for value in ("http://aclanthology.org/paper/","https://evil.example/paper/","https://user@aclanthology.org/paper/","https://aclanthology.org/paper/?next=x"):
   self.assertEqual(build_conferences.safe_url(value,"ACL"),"")
  valid={
   "NeurIPS":"https://openreview.net/forum?id=NaW6T93F34m",
   "ICLR":"https://openreview.net/forum?id=6T3wJQhvc3",
   "ICASSP":"https://cmsworkshops.com/ICASSP2026/view_paper.php?PaperNum=1003",
   "ICRA":"https://doi.org/10.1109/ICRA55743.2025.11128857",
   "ECCV":"https://eccv.ecva.net/virtual/2026/poster/4225",
  }
  for venue,url in valid.items():
   self.assertEqual(build_conferences.safe_url(url,venue),url)
  for venue,url in (("ICLR","https://openreview.net/forum?id=6T3wJQhvc3&redirect=https://evil.test"),("ICASSP","https://cmsworkshops.com/ICASSP2026/view_paper.php?PaperNum=1003&x=1"),("ECCV","https://eccv.ecva.net.evil.example/virtual/2026/poster/4225")):
   self.assertEqual(build_conferences.safe_url(url,venue),"")
 def test_cvpr_files_are_reused_and_cli_exists(self):
  self.assertTrue((HUB/"data/2026.json").is_file());self.assertTrue((HUB/"tools/search_conferences.py").is_file())
  self.assertIn("CVPR",self.catalog["venues"])
 def test_cross_venue_corpus_has_live_records(self):
  selected=[]
  for venue,year in (("ECCV",2024),("ACL",2024)):
   item=self.catalog["venues"][venue]["years"][str(year)]
   bundle=json.loads((HUB/item["file"]).read_text());selected.extend(bundle["papers"][:2])
  self.assertEqual({p["venue"] for p in selected},{"ECCV","ACL"});self.assertTrue(all(p["title"] and p["source"] for p in selected))
if __name__=="__main__":unittest.main()
