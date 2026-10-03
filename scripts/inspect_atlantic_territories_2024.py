#!/usr/bin/env python3
"""Resolve and inspect 2024 official audited statements for the final 10 LGPI municipalities."""

from __future__ import annotations

import re
import ssl
import subprocess
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup

CONFIG = {
    "halifax": {
        "direct": "https://cdn.halifax.ca/sites/default/files/documents/city-hall/budget-finances/march-31-2024-audited-financial-statements-cao-approved.pdf",
    },
    "cape-breton": {
        "page": "https://cbrm.ns.ca/city-hall/budget-documents/",
        "must": ["2023-2024", "consolidated financial statements"],
    },
    "moncton": {
        "direct": "https://www5.moncton.ca/docs/budget/2024_Consolidated_Financial_Statements.pdf",
        "insecure_tls": True,
    },
    "fredericton": {
        "direct": "https://www.fredericton.ca/media/file/cof-2024annualreport-en-pdf",
    },
    "saint-john": {
        "page": "https://saintjohn.ca/en/city-hall/city-corporation/rates-and-finances/audited-financial-statements",
        "must": ["2024", "audited consolidated financial statements"],
    },
    "st-johns": {
        "direct": "https://www.stjohns.ca/2024_Consolidated-Financial-Statements_City-of-St.-John%27s.pdf",
    },
    "charlottetown": {
        "page": "https://www.charlottetown.ca/mayor___council/finance/audited_financial_statements",
        "must": ["city of charlottetown consolidated financial statements", "march 31, 2024"],
    },
    "whitehorse": {
        "direct": "https://www.whitehorse.ca/wp-content/uploads/2025/10/COW-2024-AR-Web.pdf",
    },
    "yellowknife": {
        "page": "https://www.yellowknife.ca/budget-and-initiatives/past-and-present-budgets",
        "must": ["financial report", "2024"],
    },
    "iqaluit": {
        "direct": "https://iqaluit.ca/sites/default/files/2024_consolidated_financial_statements_eng_-_signed.pdf",
    },
}

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
    "property taxes",
    "user fees",
    "sales of services",
    "government transfers",
    "government grants",
    "investment income",
    "developer contributions",
    "expenses by object",
    "expenditures by object",
    "salaries and benefits",
    "wages and benefits",
    "amortization",
]

UA={"User-Agent":"Mozilla/5.0 LGPI-reconstruction/0.2 (+https://github.com/FTFNAnalytics/lgpi)"}

def fetch(url: str, insecure: bool=False) -> bytes:
    p=urllib.parse.urlsplit(url)
    safe=urllib.parse.urlunsplit((p.scheme,p.netloc,urllib.parse.quote(urllib.parse.unquote(p.path),safe="/,()"),p.query,p.fragment))
    req=urllib.request.Request(safe,headers=UA)
    ctx=ssl._create_unverified_context() if insecure else None
    with urllib.request.urlopen(req,timeout=180,context=ctx) as r:
        return r.read()

def discover(cfg: dict) -> str:
    html=fetch(cfg["page"])
    soup=BeautifulSoup(html,"html.parser")
    candidates=[]
    for a in soup.find_all("a",href=True):
        text=" ".join(a.stripped_strings)
        href=urllib.parse.urljoin(cfg["page"],a["href"])
        combined=(text+" "+href).lower()
        if all(term.lower() in combined for term in cfg["must"]):
            candidates.append((text,href))
    if not candidates:
        raise RuntimeError(f"No matching link on {cfg['page']}")
    candidates.sort(key=lambda item: len(item[0]))
    print("DISCOVERED",repr(candidates[0][0]),candidates[0][1])
    return candidates[0][1]

def extract(slug: str, cfg: dict) -> None:
    url=cfg.get("direct") or discover(cfg)
    payload=fetch(url,cfg.get("insecure_tls",False))
    if not payload.startswith(b"%PDF"):
        raise RuntimeError(f"{slug}: not PDF: {payload[:80]!r}")
    with tempfile.TemporaryDirectory() as td:
        pdf=Path(td)/"source.pdf"
        txt=Path(td)/"source.txt"
        pdf.write_bytes(payload)
        subprocess.run(["pdftotext","-layout",str(pdf),str(txt)],check=True)
        text=txt.read_text(errors="replace")
    pages=text.split("\f")
    scored=[]
    for i,page in enumerate(pages,1):
        low=page.lower()
        score=sum(term in low for term in TERMS)
        if score>=2:
            scored.append((score,i,page))
    print(f"\n=== {slug.upper()} url={url} bytes={len(payload)} pages={len(pages)} ===")
    for score,page_num,page in sorted(scored,reverse=True)[:22]:
        compact="\n".join(line.rstrip() for line in page.splitlines())
        print(f"\n--- PAGE {page_num} score={score} ---")
        print(compact[:11000])

def main() -> None:
    for slug,cfg in CONFIG.items():
        try:
            extract(slug,cfg)
        except Exception as exc:
            print(f"\n!!! {slug.upper()} FAILED: {type(exc).__name__}: {exc}")

if __name__=="__main__":
    main()
