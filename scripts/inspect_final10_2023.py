#!/usr/bin/env python3
"""Inspect official 2023 financial statements for the final 10 LGPI municipalities.

The purpose of this research helper is to locate the exact audited statement
pages needed by the production importer. It does not write application data.
"""

from __future__ import annotations

import io
import re
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup
from pypdf import PdfReader

SOURCES = {
    "halifax": {
        "name": "Halifax",
        "province": "NS",
        "url": "https://cdn.halifax.ca/sites/default/files/documents/city-hall/budget-finances/march-31-2023-financial-statements_cao-approved.pdf",
        "label": "Halifax Regional Municipality Consolidated Financial Statements — March 31, 2023",
    },
    "cape-breton": {
        "name": "Cape Breton",
        "province": "NS",
        "url": "https://cbrm.ns.ca/wp-content/uploads/2026/01/2022-2023-CBRM_Audited_Financial_Statements_22-23.pdf",
        "label": "Cape Breton Regional Municipality Audited Financial Statements — 2022-2023",
    },
    "moncton": {
        "name": "Moncton",
        "province": "NB",
        "url": "https://www5.moncton.ca/docs/budget/2024_Consolidated_Financial_Statements.pdf",
        "label": "City of Moncton 2024 Consolidated Financial Statements (2023 comparative, including restatements where applicable)",
        "comparative_2023": True,
    },
    "fredericton": {
        "name": "Fredericton",
        "province": "NB",
        "url": "https://www.fredericton.ca/sites/default/files/2025-04/City%20of%20Fredericton%20-%202023%20Consolidated%20Financial%20Statements%20-%20English%20(2).pdf",
        "label": "City of Fredericton 2023 Consolidated Financial Statements",
    },
    "saint-john": {
        "name": "Saint John",
        "province": "NB",
        "url": "https://saintjohn.ca/sites/default/files/documents/City%20of%20Saint%20John%20December%2031%202023%20Financial%20Statements%20Eng%20(002)%20-%20with%20Signature.pdf",
        "label": "City of Saint John 2023 Consolidated Financial Statements",
    },
    "st-johns": {
        "name": "St. John's",
        "province": "NL",
        "url": "https://www.stjohns.ca/media/miopyywx/20231231_city-of-st-johns-consolidated-financial-statements_final-signed.pdf",
        "label": "City of St. John's 2023 Consolidated Financial Statements",
    },
    "charlottetown": {
        "name": "Charlottetown",
        "province": "PE",
        "url": "https://cdnsm5-hosted.civiclive.com/UserFiles/Servers/Server_10500298/File/City%20of%20Charlottetown%20Consolidated%20Financial%20Statements%20-%20March%2031,%202023.pdf",
        "label": "City of Charlottetown Consolidated Financial Statements — March 31, 2023",
        "discovery": "https://www.charlottetown.ca/mayor___council/finance/audited_financial_statements",
    },
    "whitehorse": {
        "name": "Whitehorse",
        "province": "YT",
        "url": "https://www.whitehorse.ca/wp-content/uploads/2024/10/2023-City-of-Whitehorse_AR-WEB.pdf",
        "label": "City of Whitehorse 2023 Annual Report",
    },
    "yellowknife": {
        "name": "Yellowknife",
        "province": "NT",
        "url": "https://www.yellowknife.ca/en/city-government/resources/Reports/Annual_Report/2023-FINANCIAL-REPORT.pdf",
        "label": "City of Yellowknife 2023 Financial Report",
    },
    "iqaluit": {
        "name": "Iqaluit",
        "province": "NU",
        "url": "https://iqaluit.ca/sites/default/files/city_of_iqaluit_2023_fs_-_english_-_cao_signed.pdf",
        "label": "City of Iqaluit 2023 Financial Statements",
    },
}

TERMS = [
    "statement of financial position",
    "statement of operations",
    "consolidated statement of financial position",
    "consolidated statement of operations",
    "financial assets",
    "financial liabilities",
    "net financial",
    "tangible capital assets",
    "long-term debt",
    "long term debt",
    "taxation",
    "taxes",
    "user charges",
    "sales of services",
    "government transfers",
    "government grants",
    "investment income",
    "developer",
    "contributions",
    "expenses by object",
    "expenditures by object",
    "salaries",
    "wages",
    "benefits",
    "amortization",
    "interest",
    "segment",
    "segmented",
]


def safe_url(url: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit(
        (
            parsed.scheme,
            parsed.netloc,
            urllib.parse.quote(urllib.parse.unquote(parsed.path), safe="/,()"),
            parsed.query,
            parsed.fragment,
        )
    )


def fetch(url: str) -> bytes:
    req = urllib.request.Request(
        safe_url(url),
        headers={
            "User-Agent": "Mozilla/5.0 LGPI-reconstruction/0.1 (+https://github.com/FTFNAnalytics/lgpi)"
        },
    )
    with urllib.request.urlopen(req, timeout=120) as response:
        return response.read()


def discover_pdf(page_url: str, year_phrase: str = "2023") -> str | None:
    html = fetch(page_url)
    soup = BeautifulSoup(html, "html.parser")
    candidates = []
    for a in soup.find_all("a", href=True):
        text = " ".join(a.stripped_strings)
        href = urllib.parse.urljoin(page_url, a["href"])
        if year_phrase in text and ".pdf" in href.lower():
            candidates.append((text, href))
    if not candidates:
        return None
    # Prefer statement/audit language.
    candidates.sort(
        key=lambda item: (
            "financial" in item[0].lower() or "audit" in item[0].lower(),
            len(item[0]),
        ),
        reverse=True,
    )
    print(f"DISCOVERY {page_url}: {candidates[:5]}")
    return candidates[0][1]


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def inspect(slug: str, config: dict) -> None:
    url = config["url"]
    try:
        payload = fetch(url)
    except Exception as first_error:
        discovery = config.get("discovery")
        if not discovery:
            raise
        found = discover_pdf(discovery)
        if not found:
            raise RuntimeError(f"{slug}: direct URL failed ({first_error}); discovery found no PDF")
        url = found
        payload = fetch(url)

    print(f"\n=== {slug.upper()} bytes={len(payload)} url={url} ===")
    reader = PdfReader(io.BytesIO(payload))
    print(f"pages={len(reader.pages)} label={config['label']!r}")

    hits = []
    for idx, page in enumerate(reader.pages):
        text = normalize(page.extract_text() or "")
        low = text.lower()
        score = sum(1 for term in TERMS if term in low)
        if score:
            hits.append((score, idx + 1, text))

    for score, page_num, text in sorted(hits, reverse=True)[:24]:
        print(f"\n--- PAGE {page_num} score={score} ---")
        print(text[:8000])


def main() -> None:
    for slug, config in SOURCES.items():
        try:
            inspect(slug, config)
        except Exception as exc:
            print(f"\n!!! SOURCE FAILURE {slug}: {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()
