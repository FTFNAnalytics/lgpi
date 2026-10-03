#!/usr/bin/env python3
"""Inspect official 2024 audited reports for Regina, Saskatoon and Winnipeg."""

from __future__ import annotations

import io
import json
import re
import urllib.request

from pypdf import PdfReader

REGINA_PACKAGE = "https://openregina.ca/api/3/action/package_show?id=5e011351-3612-4a51-919d-914dcef52ffb"
SASKATOON = "https://www.saskatoon.ca/sites/default/files/documents/asset-financial-management/COS_2024-AnnualReport-Aug28-F.pdf"
WINNIPEG = "https://legacy.winnipeg.ca/finance/files/2024AnnualReport.pdf"

TERMS = [
    "statement of financial position",
    "consolidated statement of financial position",
    "statement of operations",
    "consolidated statement of operations",
    "financial assets",
    "financial liabilities",
    "long-term debt",
    "long term debt",
    "tangible capital assets",
    "taxation",
    "fees and charges",
    "user fees",
    "government transfers",
    "investment income",
    "expenses by object",
    "wages and benefits",
    "salaries and benefits",
    "amortization",
    "interest",
]

UA={"User-Agent":"Mozilla/5.0 LGPI-reconstruction/0.2 (+https://github.com/FTFNAnalytics/lgpi)"}

def fetch(url: str) -> bytes:
    req=urllib.request.Request(url,headers=UA)
    with urllib.request.urlopen(req,timeout=180) as r:
        return r.read()

def clean(text: str) -> str:
    return re.sub(r"\s+"," ",text or "").strip()

def regina_2024_url() -> str:
    obj=json.loads(fetch(REGINA_PACKAGE))
    resources=obj["result"]["resources"]
    candidates=[]
    for r in resources:
        text=" ".join(str(r.get(k,"")) for k in ("name","description","url","format")).lower()
        if "2024" in text and ("annual" in text or "report" in text or "financial" in text) and "pdf" in text:
            candidates.append(r)
    if not candidates:
        raise RuntimeError("No Regina 2024 annual-report resource found")
    candidates.sort(key=lambda r: ("annual report" in (r.get("name") or "").lower(), "financial" in (r.get("name") or "").lower()), reverse=True)
    print("REGINA RESOURCE",json.dumps({k:candidates[0].get(k) for k in ("id","name","url","format")}))
    return candidates[0]["url"]

def inspect(slug: str, url: str) -> None:
    payload=fetch(url)
    if not payload.startswith(b"%PDF"):
        raise RuntimeError(f"{slug}: resource is not PDF; prefix={payload[:80]!r}")
    reader=PdfReader(io.BytesIO(payload))
    print(f"\n=== {slug.upper()} url={url} bytes={len(payload)} pages={len(reader.pages)} ===")
    hits=[]
    for i,page in enumerate(reader.pages):
        text=clean(page.extract_text() or "")
        low=text.lower()
        score=sum(term in low for term in TERMS)
        if score>=2:
            hits.append((score,i+1,text))
    for score,page,text in sorted(hits,reverse=True)[:26]:
        print(f"\n--- PAGE {page} score={score} ---")
        print(text[:9500])

def main() -> None:
    sources={
        "regina":regina_2024_url(),
        "saskatoon":SASKATOON,
        "winnipeg":WINNIPEG,
    }
    for slug,url in sources.items():
        inspect(slug,url)

if __name__=="__main__":
    main()
