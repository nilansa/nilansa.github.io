#!/usr/bin/env python3
"""Build compact static venue/year shards from ai-conferences Parquet datasets."""
from __future__ import annotations
import argparse, hashlib, json, re, sys, tempfile, urllib.error, urllib.request
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
VENUES = ["CVPR", "ICCV", "ECCV", "NeurIPS", "ICML", "ICLR", "AAAI", "ACL", "EMNLP", "NAACL", "ICRA", "ICASSP"]
YEARS = range(2022, 2027)
HOSTS = {
 "CVPR":{"openaccess.thecvf.com"}, "ICCV":{"openaccess.thecvf.com"}, "ECCV":{"openaccess.thecvf.com","www.ecva.net","ecva.net","eccv.ecva.net","eccv2024.ecva.net","eccv2022.ecva.net"},
 "NeurIPS":{"openreview.net","proceedings.neurips.cc"}, "ICML":{"openreview.net","proceedings.mlr.press"}, "ICLR":{"openreview.net"},
 "AAAI":{"ojs.aaai.org"}, "ACL":{"aclanthology.org"}, "EMNLP":{"aclanthology.org"}, "NAACL":{"aclanthology.org"},
 "ICRA":{"ieeexplore.ieee.org","doi.org"}, "ICASSP":{"ieeexplore.ieee.org","doi.org","cmsworkshops.com"}}
TAXONOMY = {"Computer Vision & 3D":["CVPR","ICCV","ECCV"], "Machine Learning & AI":["NeurIPS","ICML","ICLR","AAAI"], "Language/NLP":["ACL","EMNLP","NAACL"], "Robotics & Speech":["ICRA","ICASSP"]}

def digest(data: bytes) -> str: return hashlib.sha256(data).hexdigest()
def safe_url(value, venue, extension=""):
    if not isinstance(value, str): return ""
    try: u=urlsplit(value.strip())
    except ValueError: return ""
    if u.scheme!="https" or u.hostname not in HOSTS[venue] or u.username or u.password or u.fragment: return ""
    forum = (venue in ("NeurIPS","ICML","ICLR") and u.hostname=="openreview.net" and
             u.path in ("/forum","/pdf") and bool(re.fullmatch(r"id=[A-Za-z0-9_-]{6,80}",u.query)))
    icassp = (venue=="ICASSP" and u.hostname=="cmsworkshops.com" and
              bool(re.fullmatch(r"/ICASSP20\d{2}/view_paper\.php",u.path)) and
              bool(re.fullmatch(r"PaperNum=\d{1,10}",u.query)))
    if u.query and not (forum or icassp): return ""
    aaai_pdf=(venue=="AAAI" and extension==".pdf" and
              bool(re.fullmatch(r"/index\.php/AAAI/article/download/\d+/\d+",u.path)))
    if extension and not (u.path.lower().endswith(extension) or aaai_pdf): return ""
    return value.strip()

def cluster(area, venue):
    if area: return str(area).strip()[:100]
    return {"CVPR":"Computer Vision & 3D","ICCV":"Computer Vision & 3D","ECCV":"Computer Vision & 3D","NeurIPS":"Machine Learning & AI","ICML":"Machine Learning & AI","ICLR":"Machine Learning & AI","AAAI":"Machine Learning & AI","ACL":"Language/NLP","EMNLP":"Language/NLP","NAACL":"Language/NLP","ICRA":"Robotics & Speech","ICASSP":"Robotics & Speech"}[venue]
def atomic_write(path: Path, data: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() == data: return
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as f: f.write(data); tmp=Path(f.name)
    tmp.chmod(0o644); tmp.replace(path)
def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":"CS-Conference-Research-Hub/1.0"})
    with urllib.request.urlopen(req,timeout=90) as response: return response.read()
def records_from_parquet(data, venue, year, source_url):
    import pyarrow.parquet as pq
    import pyarrow as pa
    table=pq.read_table(pa.BufferReader(data))
    rows=table.to_pylist(); output=[]; seen=set()
    for row in rows:
        title=str(row.get("title") or "").strip()
        if not title: continue
        key=str(row.get("paper_id") or row.get("anthology_id") or title).strip()
        identity=f"{venue.lower()}-{year}-{hashlib.sha256(key.encode()).hexdigest()[:16]}"
        if identity in seen: continue
        seen.add(identity)
        authors=row.get("authors") or []
        if isinstance(authors,str): authors=[authors]
        authors=", ".join(str(a).strip() for a in authors if a)
        paper_url=safe_url(row.get("paper_url") or row.get("ecva_url") or row.get("cvf_url") or row.get("openaccess_url"),venue)
        pdf_url=safe_url(row.get("pdf_url"),venue,".pdf")
        abstract=str(row.get("abstract") or "").strip()
        area=row.get("primary_area") or row.get("session_topics") or row.get("keywords")
        if isinstance(area,list): area=", ".join(str(a) for a in area[:3])
        track=str(row.get("track") or row.get("type") or "").strip()
        output.append({"id":identity,"venue":venue,"year":year,"title":title,"authors":authors,"abstract":abstract,"paper_url":paper_url,"pdf_url":pdf_url,"source":"Curated venue record · ai-conferences","track_status":f"Source track label: {track}" if track else "Curated venue record; track not independently verified","cluster":cluster(area,venue),"primary_area":str(area or cluster(None,venue))})
    output.sort(key=lambda p:(p["title"].casefold(),p["id"]))
    bundle={"venue":venue,"year":year,"source":source_url,"papers":output}
    return (json.dumps(bundle,ensure_ascii=False,separators=(",",":"))+"\n").encode(),len(output),sum(bool(p["abstract"]) for p in output)
def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--venue",action="append",choices=VENUES); parser.add_argument("--year",type=int,action="append"); args=parser.parse_args()
    venues=args.venue or VENUES; years=args.year or list(YEARS)
    import concurrent.futures
    catalog_path=ROOT/"catalog.json"
    try: catalog=json.loads(catalog_path.read_text())
    except (OSError,json.JSONDecodeError): catalog={"schema":"cs-conf-catalog-v1","taxonomy":TAXONOMY,"venues":{}}
    catalog.update(schema="cs-conf-catalog-v1",taxonomy=TAXONOMY,source_dataset="https://huggingface.co/datasets/ai-conferences")
    failures=[]
    for venue in venues:
        old=catalog.setdefault("venues",{}).setdefault(venue,{"available_years":[],"years":{},"missing_years":[]})
        available=set(old.get("available_years",[])); manifest=old.setdefault("years",{})
        for year in years:
            if venue=="CVPR":
                # The original CVPR corpus is authoritative for this hub and remains untouched.
                f=ROOT/"data"/f"{year}.json"
                if f.exists():
                    b=f.read_bytes(); oldrec=json.loads(b); entry={"count":len(oldrec["papers"]),"file":f"data/{year}.json","bytes":len(b),"sha256":digest(b),"source_url":oldrec.get("source","existing CVPR corpus"),"revision":"existing-cvpr-corpus","abstract_coverage":sum(bool(p.get("abstract")) for p in oldrec["papers"])/max(len(oldrec["papers"]),1),"license":"MIT dataset license; see provenance.json"}; manifest[str(year)]=entry; available.add(year); continue
            dataset=f"{venue}{year}"
            try:
                api=json.loads(fetch(f"https://huggingface.co/api/datasets/ai-conferences/{dataset}"))
                revision=api.get("sha") or "unknown"
                source=f"https://huggingface.co/datasets/ai-conferences/{dataset}/resolve/{revision}/data/train-00000-of-00001.parquet"
                parquet=fetch(source); out,count,with_abstract=records_from_parquet(parquet,venue,year,source)
                rel=f"data/venues/{venue}/{year}.json"; target=ROOT/rel; atomic_write(target,out)
                cards=api.get("cardData",{}).get("dataset_info",[]); license_name=api.get("cardData",{}).get("license")
                entry={"count":count,"file":rel,"bytes":len(out),"sha256":digest(out),"source_url":source,"dataset_url":f"https://huggingface.co/datasets/ai-conferences/{dataset}","source_bytes":len(parquet),"source_sha256":digest(parquet),"revision":revision,"abstract_count":with_abstract,"abstract_coverage":round(with_abstract/max(count,1),4),"license":license_name or "Dataset card does not declare a license"}
                manifest[str(year)]=entry; available.add(year)
                print(f"{venue} {year}: {count} records, {len(out)} bytes")
            except urllib.error.HTTPError as exc:
                if exc.code in (401,404):
                    print(f"UNAVAILABLE {venue} {year}: source dataset is not public or does not exist")
                    continue
                failures.append(f"{venue} {year}: HTTP {exc.code}: {exc.reason}")
                print(f"FAILED {venue} {year}: HTTP {exc.code}: {exc.reason}",file=sys.stderr)
            except Exception as exc:
                failures.append(f"{venue} {year}: {type(exc).__name__}: {exc}")
                print(f"FAILED {venue} {year}: {type(exc).__name__}: {exc}",file=sys.stderr)
        old["available_years"]=sorted(available); old["missing_years"]=[y for y in YEARS if y not in available]
        old["total_records"]=sum(manifest.get(str(y),{}).get("count",0) for y in available)
    data=(json.dumps(catalog,ensure_ascii=False,indent=2)+"\n").encode(); atomic_write(catalog_path,data)
    print(f"Catalog: {catalog_path}; failures: {len(failures)}")
    return 1 if failures else 0
if __name__=="__main__": raise SystemExit(main())
