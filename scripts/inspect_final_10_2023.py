#!/usr/bin/env python3
"""Discover and inspect official 2023 financial statements for the final 10 LGPI municipalities."""

from __future__ import annotations

import io
import re
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup
from pypdf import PdfReader

CONFIG = {
    "halifax": {
        "name": "Halifax",
        "direct": "https://cdn.halifax.ca/sites/default/files/documents/city-hall/budget-finances/march-31-2023-financial-statements_cao-approved.pdf",
        "prefer": ["financial"],
    },
    "cape-breton": {
        "name": "Cape Breton",
        "pages": ["https://cbrm.ns.ca/city-hall/budget-documents/"],
        "must": ["2022-2023"],
        "prefer": ["consolidated", "financial", "audited"],
    },
    "moncton": {
        "name": "Moncton",
        "direct": "https://www5.moncton.ca/docs/budget/2024_Consolidated_Financial_Statements.pdf",
        "prefer": ["financial"],
    },
    "fredericton": {
        "name": "Fredericton",
        "pages": ["https://www.fredericton.ca/previous-budgets-annual-reports"],
        "must": ["2023"],
        "prefer": ["annual report", "audited financial"],
    },
    "saint-john": {
        "name": "Saint John",
        "pages": ["https://saintjohn.ca/en/city-hall/city-corporation/rates-and-finances/audited-financial-statements"],
        "must": ["2023"],
        "prefer": ["audited consolidated", "annual report"],
    },
    "st-johns": {
        "name": "St. John's",
        "direct": "https://www.stjohns.ca/media/miopyywx/20231231_city-of-st-johns-consolidated-financial-statements_final-signed.pdf",
        "prefer": ["financial"],
    },
    "charlottetown": {
        "name": "Charlottetown",
        "pages": ["https://www.charlottetown.ca/mayor___council/finance/audited_financial_statements"],
        "must": ["march 31, 2023"],
        "prefer": ["consolidated financial"],
    },
    "whitehorse": {
        "name": "Whitehorse",
        "direct": "https://www.whitehorse.ca/wp-content/uploads/2024/06/SC-Agenda-2024-June-17.pdf",
        "prefer": ["audited 2023 financial statements"],
    },
    "yellowknife": {
        "name": "Yellowknife",
        "direct": "https://www.yellowknife.ca/en/city-government/resources/Reports/Annual_Report/2023-FINANCIAL-REPORT.pdf",
        "prefer": ["financial"],
    },
    "iqaluit": {
        "name": "Iqaluit",
        "direct": "https://iqaluit.ca/sites/default/files/city_of_iqaluit_2023_fs_-_english_-_cao_signed.pdf",
        "prefer": ["2023 audited financial statements"],
    },
}

TERMS = [
    "statement of financial position",
    "consolidated statement of financial position",
    "statement of operations",
    "consolidated statement of operations",
    "financial assets",
    "liabilities",
    "net financial",
    "tangible capital assets",
    "long-term debt",
    "long term debt",
    "taxation",
    "property taxes",
    "user fees",
    "fees and charges",
    "government transfers",
    "government grants",
    "investment income",
    "developer contributions",
    "contributed tangible capital assets",
    "expenses by object",
    "salaries and benefits",
    "wages and benefits",
    "amortization",
    "interest",
]


def safe_url(url: str) -> str:
    parts=urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit((
        parts.scheme,
        parts.netloc,
        urllib.parse.quote(urllib.parse.unquote(parts.path), safe="/,()"),
        parts.query,
        parts.fragment,
    ))


def fetch(url: str) -> bytes:
    req=urllib.request.Request(
        safe_url(url),
        headers={
            "User-Agent":"Mozilla/5.0 LGPI-reconstruction/0.1 (+https://github.com/FTFNAnalytics/lgpi)",
            "Accept":"text/html,application/pdf,*/*",
        },
    )
    with urllib.request.urlopen(req,timeout=90) as response:
        return response.read()


def clean(value: str) -> str:
    return re.sub(r"\s+"," ",value or "").strip()


def discover(slug: str, cfg: dict) -> str:
    if cfg.get("direct"):
        return cfg["direct"]

    candidates=[]
    errors=[]
    for page in cfg["pages"]:
        try:
            html=fetch(page)
        except Exception as exc:
            errors.append(f"{page}: {type(exc).__name__}: {exc}")
            continue
        soup=BeautifulSoup(html,"html.parser")
        for a in soup.find_all("a",href=True):
            text=clean(" ".join(a.stripped_strings))
            href=urllib.parse.urljoin(page,a["href"])
            combined=(text+" "+href).lower()
            if not all(token.lower() in combined for token in cfg.get("must",[])):
                continue
            if ".pdf" not in href.lower() and "media/file" not in href.lower() and "document" not in href.lower():
                continue
            score=sum(1 for token in cfg.get("prefer",[]) if token.lower() in combined)
            candidates.append((score,text,href,page))

    if not candidates:
        raise RuntimeError(f"{slug}: no source candidate. errors={errors}")
    candidates.sort(reverse=True,key=lambda item:(item[0],len(item[1])))
    print(f"{slug}: discovered {len(candidates)} candidates")
    for item in candidates[:8]:
        print(f"  CANDIDATE score={item[0]} text={item[1]!r} url={item[2]}")
    return candidates[0][2]


def inspect_pdf(slug: str, url: str) -> None:
    payload=fetch(url)
    if not payload.startswith(b"%PDF"):
        print(f"{slug}: selected resource is not a PDF; prefix={payload[:100]!r}")
        return
    reader=PdfReader(io.BytesIO(payload))
    print(f"\n=== {slug.upper()} url={url} bytes={len(payload)} pages={len(reader.pages)} ===")
    hits=[]
    for i,page in enumerate(reader.pages):
        text=clean(page.extract_text() or "")
        low=text.lower()
        score=sum(1 for term in TERMS if term in low)
        if score>=2:
            hits.append((score,i+1,text))
    for score,page,text in sorted(hits,reverse=True)[:24]:
        print(f"\n--- PAGE {page} score={score} ---")
        print(text[:8500])


def main() -> None:
    for slug,cfg in CONFIG.items():
        try:
            url=discover(slug,cfg)
            inspect_pdf(slug,url)
        except Exception as exc:
            print(f"\n!!! {slug.upper()} FAILED: {type(exc).__name__}: {exc}")


if __name__=="__main__":
    main()
