#!/usr/bin/env python3
"""Inspect Quebec MAMH 2023 open financial data and recover LGPI Quebec universe."""

from __future__ import annotations

import io
import json
import re
import urllib.parse
import urllib.request
import unicodedata
from pathlib import Path

from bs4 import BeautifulSoup
from openpyxl import load_workbook

CKAN_ENDPOINTS = [
    "https://www.donneesquebec.ca/recherche/api/3/action/package_show?id=rapport-financier-des-organismes-municipaux-et-autres-documents",
    "https://donneesquebec.ca/recherche/api/3/action/package_show?id=rapport-financier-des-organismes-municipaux-et-autres-documents",
    "https://donnees.iriu.ca/api/3/action/package_show?id=rapport-financier-des-organismes-municipaux-et-autres-documents",
]
LGPI_URL = "https://lgpi.ca/"
RECOVERED_QUEBEC_CITIES = [
    "Blainville",
    "Brossard",
    "Drummondville",
    "Gatineau",
    "Granby",
    "Laval",
    "Levis",
    "Longueuil",
    "Montreal",
    "Quebec",
    "Repentigny",
    "Saguenay",
    "Saint-Hyacinthe",
    "Saint-Jean-sur-Richelieu",
    "Saint-Jerome",
    "Shawinigan",
    "Sherbrooke",
    "Terrebonne",
    "Trois-Rivieres",
]


def fetch(url: str) -> bytes:
    parsed=urllib.parse.urlsplit(url)
    safe_url=urllib.parse.urlunsplit((
        parsed.scheme,
        parsed.netloc,
        urllib.parse.quote(urllib.parse.unquote(parsed.path), safe="/"),
        parsed.query,
        parsed.fragment,
    ))
    request = urllib.request.Request(
        safe_url,
        headers={"User-Agent":"LGPI-reconstruction/0.1 (+https://github.com/FTFNAnalytics/lgpi)"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def get_package() -> dict:
    failures=[]
    for url in CKAN_ENDPOINTS:
        try:
            data=json.loads(fetch(url))
            if data.get("success") and data.get("result"):
                print(f"CKAN endpoint={url}")
                return data["result"]
            failures.append(f"{url}: success={data.get('success')}")
        except Exception as exc:
            failures.append(f"{url}: {type(exc).__name__}: {exc}")
    raise RuntimeError("No CKAN endpoint succeeded:\n" + "\n".join(failures))


def recover_lgpi_city_options() -> list[str]:
    html=fetch(LGPI_URL)
    soup=BeautifulSoup(html,"html.parser")
    print(f"LGPI homepage bytes={len(html)} selects={len(soup.find_all('select'))}")
    for idx,select in enumerate(soup.find_all("select"),start=1):
        opts=[" ".join(o.stripped_strings) for o in select.find_all("option")]
        print(f"SELECT {idx}: attrs={dict(select.attrs)} option_count={len(opts)} sample={opts[:12]}")

    # Prefer the select with the largest set of non-numeric labels; it is the city selector.
    candidates=[]
    for select in soup.find_all("select"):
        opts=[" ".join(o.stripped_strings).strip() for o in select.find_all("option")]
        labels=[x for x in opts if x and not re.fullmatch(r"\d{4}",x)]
        candidates.append((len(labels),labels))
    if not candidates:
        raise RuntimeError("No select options found on LGPI homepage")
    labels=max(candidates,key=lambda x:x[0])[1]
    # remove prompt labels
    labels=[
        x for x in labels
        if x.lower() not in {"select","browse cities","city","choose a city","- choose a city -"}
    ]
    return labels


def loaded_non_quebec_names() -> set[str]:
    text=Path("lib/lgpi-data.ts").read_text(encoding="utf-8")
    # transparencyRaw tuples: ["slug","Name","PC",...
    return set(re.findall(r'\["[^"]+","([^"]+)","[A-Z]{2}",',text))



def norm(value: object) -> str:
    text=unicodedata.normalize("NFKD",str(value or ""))
    text="".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"[^A-Z0-9]+","",text.upper())


def probe_mamh_workbook(payload: bytes) -> None:
    wb=load_workbook(io.BytesIO(payload),read_only=True,data_only=True)
    simple=wb["SimpleOccurrence"]
    headers=[str(v) if v is not None else "" for v in next(simple.iter_rows(min_row=1,max_row=1,values_only=True))]
    name_idx=headers.index("nom_organisme")
    code_idx=headers.index("cod_geo")
    pop_idx=headers.index("population")
    target_norms={norm(name):name for name in RECOVERED_QUEBEC_CITIES}
    found={}
    for row in simple.iter_rows(min_row=2,values_only=True):
        n=norm(row[name_idx])
        if n in target_norms:
            found[target_norms[n]]=(row[code_idx],row[name_idx],row[pop_idx])
    print(f"TARGET MUNICIPALITIES FOUND={len(found)}")
    for expected in RECOVERED_QUEBEC_CITIES:
        print(f"  TARGET {expected!r}: {found.get(expected)}")

    desc=wb["DescriptionPoste"]
    terms=[
        "actifs financiers",
        "passifs",
        "actifs financiers nets",
        "total des revenus",
        "revenus",
        "total des charges",
        "charges",
        "dette a long terme",
        "dette à long terme",
        "immobilisations corporelles",
        "revenus totaux",
        "total des revenus",
        "taxes",
        "services rendus",
        "transferts",
        "revenus de placements",
        "contributions des promoteurs",
        "administration generale",
        "sécurité publique",
        "securite publique",
        "transport",
        "hygiène du milieu",
        "hygiene du milieu",
        "santé et bien-être",
        "sante et bien-etre",
        "aménagement, urbanisme",
        "amenagement, urbanisme",
        "loisirs et culture",
        "charges totales",
        "total des charges",
        "salaires",
        "rémunération",
        "remuneration",
        "amortissement",
        "frais de financement",
    ]
    print("ACCOUNTING CODE CANDIDATES:")
    seen=set()
    for row in desc.iter_rows(min_row=2,values_only=True):
        code=str(row[0] or "")
        subsection=str(row[1] or "")
        subject=str(row[2] or "")
        facets=str(row[3] or "")
        low=norm(subject)
        for term in terms:
            if norm(term) in low:
                key=(code,subject,facets)
                if key not in seen:
                    seen.add(key)
                    print(f"  CODE {code} | {subsection} | {subject} | {facets}")
                break

def inspect_resource(resource: dict) -> None:
    name=resource.get("name") or resource.get("title") or ""
    url=resource.get("url") or ""
    fmt=(resource.get("format") or "").upper()
    print(f"RESOURCE name={name!r} format={fmt!r} id={resource.get('id')} url={url}")
    if not url:
        return

    low=name.lower()
    if "2023" not in low:
        return
    if fmt == "XLSX" and ("données réelles" in low or "donnees reelles" in low or "financial" in low):
        payload=fetch(url)
        print(f"  XLSX bytes={len(payload)}")
        wb=load_workbook(io.BytesIO(payload),read_only=True,data_only=True)
        print(f"  sheets={wb.sheetnames}")
        if "SimpleOccurrence" in wb.sheetnames:
            probe_mamh_workbook(payload)
        for sheet_name in wb.sheetnames[:12]:
            ws=wb[sheet_name]
            print(f"  SHEET {sheet_name!r} rows={ws.max_row} cols={ws.max_column}")
            shown=0
            for row_num,row in enumerate(ws.iter_rows(values_only=True),start=1):
                vals=[str(v)[:160] if v is not None else None for v in row[:16]]
                if any(v not in (None,"") for v in vals):
                    print(f"    ROW {row_num}: {vals}")
                    shown+=1
                if shown>=6:
                    break
    elif fmt == "CSV" and ("description" in low or "simple occurrence" in low or "simple occurrence" in low):
        payload=fetch(url)
        print(f"  CSV bytes={len(payload)} prefix={payload[:500]!r}")


def main() -> None:
    missing=RECOVERED_QUEBEC_CITIES
    print(f"Recovered Quebec LGPI city universe={len(missing)}")
    print("QUEBEC CITY LABELS:")
    for city in missing:
        print(f"  - {city}")

    package=get_package()
    resources=package.get("resources") or []
    matches=[]
    for resource in resources:
        name=(resource.get("name") or resource.get("title") or "")
        if "2023" in name and (
            "Données réelles" in name
            or "Donnees reelles" in name
            or "Description poste" in name
            or "Description des postes" in name
            or "financial" in name.lower()
        ):
            matches.append(resource)
    print(f"2023 relevant resources={len(matches)}")
    for resource in matches:
        inspect_resource(resource)


if __name__=="__main__":
    main()
