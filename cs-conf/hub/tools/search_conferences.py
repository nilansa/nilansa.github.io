#!/usr/bin/env python3
"""Search the checked-in multi-conference metadata shards without network access."""
from __future__ import annotations
import argparse,json,sys,textwrap
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
VENUES=("CVPR","ICCV","ECCV","NeurIPS","ICML","ICLR","AAAI","ACL","EMNLP","NAACL","ICRA","ICASSP")
YEARS=range(2022,2027)
sys.path.insert(0,str(ROOT/"tools"))
from search_cvpr import rank_papers

def load(venue,year):
 path=ROOT/"data"/f"{year}.json" if venue=="CVPR" else ROOT/"data"/"venues"/venue/f"{year}.json"
 with path.open(encoding="utf-8") as f: bundle=json.load(f)
 if bundle.get("year")!=year or not isinstance(bundle.get("papers"),list):raise ValueError(f"Invalid corpus file: {path}")
 for paper in bundle["papers"]:
  paper.setdefault("venue",venue);paper.setdefault("source","Hugging Face dataset" if venue=="CVPR" else "Curated venue record · ai-conferences")
  paper.setdefault("paper_url",paper.get("cvf_url",""))
 return bundle["papers"]
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("query",help="Words or a quoted phrase in titles, authors, and abstracts");p.add_argument("--venue",action="append",choices=VENUES,help="Venue to search; repeat for more than one (default: CVPR)");p.add_argument("--year",type=int,action="append",help="Year to search; repeat to select several");p.add_argument("--limit",type=int,default=10);p.add_argument("--json",action="store_true",help="Write structured JSON to stdout");a=p.parse_args()
 if not 1<=a.limit<=500:p.error("--limit must be between 1 and 500")
 venues=a.venue or ["CVPR"];years=sorted(set(a.year or YEARS))
 if any(y not in YEARS for y in years):p.error("years must be between 2022 and 2026")
 try:
  hits=[]
  for venue in venues:
   for year in years:
    try: papers=load(venue,year)
    except FileNotFoundError: continue
    for item in rank_papers(papers,a.query):item["venue"]=venue;item["paper_url"]=item.get("paper_url") or item.get("cvf_url","");hits.append(item)
  hits.sort(key=lambda x:(-x["score"],-x["year"],x["venue"],x["title"].casefold()));hits=hits[:a.limit]
 except (OSError,ValueError,json.JSONDecodeError) as exc:print(f"search_conferences: {exc}",file=sys.stderr);return 1
 if a.json:json.dump({"query":a.query,"venues":venues,"years":years,"results":hits},sys.stdout,ensure_ascii=False,indent=2);sys.stdout.write("\n");return 0
 if not hits:print("No matches.");return 0
 print(f"{'SCORE':>7}  {'VENUE':8}  {'YEAR':4}  TITLE — AUTHORS");print("─"*115)
 for x in hits:
  print(f"{x['score']:7.3f}  {x['venue']:8}  {x['year']:4}  {textwrap.shorten(x['title'],width=68,placeholder='…')} — {textwrap.shorten(x['authors'],width=28,placeholder='…')}")
  print(f"         Paper: {x['paper_url'] or 'No trusted paper URL in source metadata'}")
 return 0
if __name__=="__main__":raise SystemExit(main())
