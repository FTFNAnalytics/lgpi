#!/usr/bin/env python3
"""Verify official structured 2024 municipal-finance sources used by LGPI."""

from __future__ import annotations
import json, urllib.request, urllib.parse, zipfile, io

UA={"User-Agent":"LGPI-reconstruction/0.2 (+https://github.com/FTFNAnalytics/lgpi)"}

def fetch(url):
    req=urllib.request.Request(url,headers=UA)
    with urllib.request.urlopen(req,timeout=120) as r:
        return r.read(),r.geturl(),r.headers.get("content-type","")

def check(url,label,min_bytes=1000):
    try:
        data,final,ctype=fetch(url)
        print(f"OK {label}: bytes={len(data)} type={ctype} final={final}")
        if len(data)<min_bytes: print(f"  WARNING small resource")
        return data
    except Exception as e:
        print(f"FAIL {label}: {type(e).__name__}: {e}")
        return None

print("=== ALBERTA CKAN ===")
for api in [
    "https://open.alberta.ca/api/3/action/package_show?id=cde4c4fd-a0b2-4816-af43-13de7a3fd3e3",
    "https://open.alberta.ca/data/api/3/action/package_show?id=cde4c4fd-a0b2-4816-af43-13de7a3fd3e3",
]:
    try:
        data,_,_=fetch(api)
        obj=json.loads(data)
        print(f"CKAN OK {api}")
        for r in obj.get("result",{}).get("resources",[]):
            text=" ".join(str(r.get(k,"")) for k in ("name","description","url","format"))
            if "2024" in text:
                print("RESOURCE",json.dumps({k:r.get(k) for k in ("id","name","format","url")},ensure_ascii=False))
        break
    except Exception as e:
        print(f"CKAN FAIL {api}: {type(e).__name__}: {e}")

print("\n=== BC ===")
base="https://www2.gov.bc.ca/assets/gov/british-columbians-our-governments/local-governments/finance/local-government-statistics"
for name in ["201","301","302","304","401","402","502"]:
    check(f"{base}/schedule{name}_2024.xlsx",f"BC {name}",9000)
check(f"{base}/schedule601_1_2024.xlsx","BC 601.1",9000)

print("\n=== ONTARIO ===")
base_on="https://efis.fma.csc.gov.on.ca/fir/wp-content/uploads/fir-files/open-data/by-schedule-and-year/2019-on"
for sched in ["02","10","40","42","51","70","74"]:
    data=check(f"{base_on}/VIEWFIR2024-{sched}.zip",f"ON {sched}",9000)
    if data:
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                print("  members",z.namelist()[:3])
        except Exception as e: print("  zip error",e)

print("\n=== QUEBEC ===")
url="https://mamh.gouv.qc.ca/fichiersdonneesouvertes/Donn%C3%A9es-r%C3%A9elles-2024.xlsx"
check(url,"QC Données réelles 2024",1000000)
