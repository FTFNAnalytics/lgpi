#!/usr/bin/env python3
"""Inspect 2023 audited/annual financial reports for Regina, Saskatoon, Winnipeg."""

from __future__ import annotations

import io
import re
import urllib.request

from pypdf import PdfReader

SOURCES = {
    "regina": "https://openregina.ca/dataset/5e011351-3612-4a51-919d-914dcef52ffb/resource/dae57e17-4742-42fb-a090-1dcc59260bdd/download/cor_2023_annual_report.pdf",
    "saskatoon": "https://www.saskatoon.ca/sites/default/files/documents/asset-financial-management/finance-supply/COS_2023-AnnualReport-Aug29-FINAL-web.pdf",
    "winnipeg": "https://www.winnipeg.ca/finance/files/2023AnnualReport.pdf",
}

TERMS = [
    "consolidated statement of financial position",
    "statement of financial position",
    "consolidated statement of operations",
    "statement of operations",
    "tangible capital assets",
    "long-term debt",
    "long term debt",
    "financial assets",
    "financial liabilities",
    "taxation",
    "taxes",
    "user fees",
    "user charges",
    "government transfers",
    "government grants",
    "investment income",
    "developer",
    "salaries",
    "wages",
    "benefits",
    "amortization",
    "interest",
    "expenses",
    "expenditures",
]


def fetch(url: str) -> bytes:
    req=urllib.request.Request(url,headers={"User-Agent":"LGPI-reconstruction/0.1 (+https://github.com/FTFNAnalytics/lgpi)"})
    with urllib.request.urlopen(req,timeout=120) as response:
        return response.read()


def normalize(text: str) -> str:
    return re.sub(r"\s+"," ",text or "").strip()


def main() -> None:
    for slug,url in SOURCES.items():
        payload=fetch(url)
        print(f"\n=== {slug.upper()} bytes={len(payload)} url={url} ===")
        reader=PdfReader(io.BytesIO(payload))
        print(f"pages={len(reader.pages)}")
        hits=[]
        for idx,page in enumerate(reader.pages):
            text=normalize(page.extract_text() or "")
            low=text.lower()
            score=sum(1 for term in TERMS if term in low)
            if score:
                hits.append((score,idx+1,text))
        for score,page_num,text in sorted(hits,reverse=True)[:18]:
            print(f"\n--- PAGE {page_num} score={score} ---")
            print(text[:6500])

        exact_pages = {
            "regina": [53, 54, 94],
            "saskatoon": [71, 72, 100, 112, 117, 128],
            "winnipeg": [52, 53, 82, 88],
        }.get(slug, [])
        print("\n=== EXACT PAGE PROBE ===")
        for page_num in exact_pages:
            if 1 <= page_num <= len(reader.pages):
                text=normalize(reader.pages[page_num-1].extract_text() or "")
                print(f"\n--- EXACT PAGE {page_num} ---")
                print(text[:9000])


if __name__=="__main__":
    main()
