#!/usr/bin/env python3
"""Import Ontario 2023 FIR schedule data for the 41 LGPI municipalities.

The Ontario Ministry of Municipal Affairs and Housing publishes each FIR
schedule as a ZIP containing an XLSX workbook. This importer uses only
source line codes whose meaning can be mapped to the legacy LGPI catalogue
without guessing. Ambiguous legacy mappings remain pending_review.
"""

from __future__ import annotations

import io
import json
import re
import urllib.request
import zipfile
from pathlib import Path

from openpyxl import load_workbook

BASE = "https://efis.fma.csc.gov.on.ca/fir/wp-content/uploads/fir-files/open-data/by-schedule-and-year/2019-on"
INDEX_URL = "https://efis.fma.csc.gov.on.ca/fir/index.php/en/open-data/fir-by-schedule-and-year/"
OUTPUT = Path("data/2023/ontario.json")
SCHEDULES = ["02","10","40","42","51","70","74"]

ALLOW_MISSING = {
    "hamilton": "Ontario's 2023 FIR by-year page lists Hamilton C as Not Available.",
}

TARGETS = {
    "ajax": "Ajax T",
    "aurora": "Aurora T",
    "barrie": "Barrie C",
    "brampton": "Brampton C",
    "brantford": "Brantford C",
    "burlington": "Burlington C",
    "caledon": "Caledon T",
    "cambridge": "Cambridge C",
    "chatham-kent": "Chatham-Kent M",
    "clarington": "Clarington M",
    "greater-sudbury": "Greater Sudbury C",
    "guelph": "Guelph C",
    "halton-hills": "Halton Hills T",
    "hamilton": "Hamilton C",
    "kawartha-lakes": "Kawartha Lakes C",
    "kingston": "Kingston C",
    "kitchener": "Kitchener C",
    "london": "London C",
    "markham": "Markham C",
    "milton": "Milton T",
    "mississauga": "Mississauga C",
    "newmarket": "Newmarket T",
    "niagara-falls": "Niagara Falls C",
    "norfolk-county": "Norfolk County",
    "north-bay": "North Bay C",
    "oakville": "Oakville T",
    "oshawa": "Oshawa C",
    "ottawa": "Ottawa C",
    "peterborough": "Peterborough C",
    "pickering": "Pickering C",
    "richmond-hill": "Richmond Hill C",
    "st-catharines": "St. Catharines C",
    "sarnia": "Sarnia C",
    "sault-ste-marie": "Sault Ste Marie C",
    "thunder-bay": "Thunder Bay C",
    "toronto": "Toronto C",
    "vaughan": "Vaughan C",
    "waterloo": "Waterloo C",
    "welland": "Welland C",
    "whitby": "Whitby T",
    "windsor": "Windsor C",
}


def normalize(value: object) -> str:
    return re.sub(r"[^A-Z0-9]+", "", str(value or "").upper())


def fetch_zip(schedule: str) -> tuple[str, bytes]:
    url=f"{BASE}/VIEWFIR2023-{schedule}.zip"
    request=urllib.request.Request(
        url,
        headers={"User-Agent":"LGPI-reconstruction/0.1 (+https://github.com/FTFNAnalytics/lgpi)"},
    )
    with urllib.request.urlopen(request,timeout=120) as response:
        payload=response.read()
    if len(payload)<10_000:
        raise RuntimeError(f"Ontario FIR download unexpectedly small: schedule={schedule} bytes={len(payload)}")
    return url,payload


def number(value: object) -> int | None:
    if value is None or value == "":
        return None
    if isinstance(value,str) and value.strip().upper() in {"N/A","NA","-","—"}:
        return None
    return int(round(float(value)))


def load_schedule(schedule: str) -> dict:
    url,payload=fetch_zip(schedule)
    with zipfile.ZipFile(io.BytesIO(payload)) as zf:
        members=[name for name in zf.namelist() if name.lower().endswith(".xlsx")]
        if len(members)!=1:
            raise RuntimeError(f"Expected one XLSX in Ontario schedule {schedule}: {members}")
        xlsx=zf.read(members[0])
    workbook=load_workbook(io.BytesIO(xlsx),read_only=True,data_only=True)

    rows=[]
    for sheet_name in workbook.sheetnames:
        if not sheet_name.startswith("SCHEDULE"):
            continue
        if schedule == "74" and sheet_name != "SCHEDULE 74":
            continue
        ws=workbook[sheet_name]
        header_values=list(next(ws.iter_rows(min_row=5,max_row=5,values_only=True)))
        headers=[str(v).strip() if v is not None else "" for v in header_values]
        if "Municipality" not in headers or "Line" not in headers:
            continue
        for row_number,values in enumerate(ws.iter_rows(min_row=6,values_only=True),start=6):
            row={header:values[i] if i<len(values) else None for i,header in enumerate(headers) if header}
            municipality=row.get("Municipality")
            line=row.get("Line")
            if municipality is None or line is None:
                continue
            row["_sheet"]=sheet_name
            row["_source_row"]=row_number
            rows.append(row)

    descriptions={}
    for row in rows:
        key=(normalize(row.get("Municipality")),int(float(row["Line"])))
        descriptions.setdefault(
            key,
            str(row.get("Line Description") or f"Line {int(float(row['Line']))}"),
        )
    return {
        "schedule":schedule,
        "url":url,
        "rows":rows,
        "descriptions":descriptions,
    }


def target_source_names(rows: list[dict]) -> tuple[dict[str,str],dict[str,str]]:
    available={}
    for row in rows:
        name=str(row.get("Municipality") or "").strip()
        available.setdefault(normalize(name),name)

    found={}
    missing={}
    for slug,expected in TARGETS.items():
        key=normalize(expected)
        if key not in available:
            if slug in ALLOW_MISSING:
                missing[slug]=ALLOW_MISSING[slug]
                continue
            fuzzy=sorted({
                str(row.get("Municipality") or "").strip()
                for row in rows
                if normalize(expected.split()[0]) in normalize(row.get("Municipality"))
            })
            raise RuntimeError(f"Ontario municipality match failed for {slug}: expected={expected!r}, fuzzy={fuzzy[:20]}")
        found[slug]=available[key]
    return found,missing


def index_rows(schedule_data: dict, source_names: dict[str,str]) -> dict[tuple[str,int],dict]:
    wanted={normalize(name):slug for slug,name in source_names.items()}
    indexed={}
    for row in schedule_data["rows"]:
        name_norm=normalize(row.get("Municipality"))
        slug=wanted.get(name_norm)
        if slug is None:
            continue
        line=int(float(row["Line"]))
        key=(slug,line)
        # Schedule 51 spans A/B. Duplicate line codes are not expected for
        # the exact lines used below; fail if one appears.
        if key in indexed:
            existing=indexed[key]
            if existing["_sheet"] != row["_sheet"]:
                raise RuntimeError(f"Duplicate Ontario schedule line for {key}: {existing['_sheet']} and {row['_sheet']}")
        indexed[key]=row
    return indexed


def field(schedule: dict, indexes: dict[str,dict], slug: str, line: int, column: str) -> tuple[int|None,dict]:
    row=indexes[schedule["schedule"]].get((slug,line))
    if row is None:
        raise RuntimeError(f"Missing Ontario row schedule={schedule['schedule']} slug={slug} line={line}")
    if column not in row:
        raise RuntimeError(f"Missing Ontario column schedule={schedule['schedule']} column={column!r}")
    return number(row.get(column)),row


def obs(slug,metric,amount,schedule,row,column,method="direct",status=None,note=None,extra_lines=None):
    resolved=status or ("reported" if amount is not None else "not_reported")
    lines=[int(float(row["Line"]))] if extra_lines is None else extra_lines
    municipality_key=normalize(row.get("Municipality"))
    descriptions=[
        schedule["descriptions"].get((municipality_key,line),f"Line {line}")
        for line in lines
    ]
    return {
        "municipalitySlug":slug,
        "year":2023,
        "metric":metric,
        "valueThousands":None if amount is None else amount/1000,
        "status":resolved,
        "sourceUrl":schedule["url"],
        "sourceLabel":f"Ontario Ministry of Municipal Affairs and Housing — FIR 2023 Schedule {schedule['schedule']}",
        "sourceLocation":f"{row['_sheet']}: line(s) {', '.join(map(str,lines))}; column {column}",
        "sourceReportedLabel":" + ".join(descriptions),
        "sourceFieldCodes":[f"{schedule['schedule']}:{line}:{column}" for line in lines],
        "mappingMethod":method,
        **({"note":note} if note else {}),
    }


def line_value(schedule,indexes,slug,line,column):
    return field(schedule,indexes,slug,line,column)


def build(slug,schedules,indexes):
    s={x["schedule"]:x for x in schedules}

    def direct(metric,sched,line,column,status=None,note=None):
        amount,row=line_value(s[sched],indexes,slug,line,column)
        return obs(slug,metric,amount,s[sched],row,column,status=status,note=note)

    def direct_optional(metric,sched,line,column,note):
        row=indexes[sched].get((slug,line))
        if row is None:
            return {
                "municipalitySlug":slug,
                "year":2023,
                "metric":metric,
                "valueThousands":None,
                "status":"not_reported",
                "sourceUrl":s[sched]["url"],
                "sourceLabel":f"Ontario Ministry of Municipal Affairs and Housing — FIR 2023 Schedule {sched}",
                "sourceLocation":f"Schedule {sched}: line {line} absent for municipality; column {column}",
                "sourceReportedLabel":f"Expected FIR line {line}",
                "sourceFieldCodes":[f"{sched}:{line}:{column}"],
                "mappingMethod":"direct",
                "note":note + " The source row is absent for this municipality, so the observation is recorded as not_reported rather than zero.",
            }
        amount=number(row.get(column))
        return obs(
            slug,metric,amount,s[sched],row,column,
            status="pending_review",note=note,
        )

    def summed(metric,sched,lines,column,note,status=None):
        values=[]
        source_rows=[]
        for line in lines:
            amount,row=line_value(s[sched],indexes,slug,line,column)
            values.append(amount)
            source_rows.append(row)
        amount=None if any(v is None for v in values) else sum(v for v in values if v is not None)
        return obs(slug,metric,amount,s[sched],source_rows[0],column,method="derived_sum",status=status,note=note,extra_lines=lines)

    out=[
        direct("financial_assets_total","70",9930,"70 xxxx 01"),
        direct("financial_liabilities_total","70",9940,"70 xxxx 01"),
        direct("net_financial_assets","70",9945,"70 xxxx 01"),
        direct("capital_assets","70",6210,"70 xxxx 01"),
        direct_optional(
            "employee_future_benefit_liability","70",6601,"70 xxxx 01",
            note="Ontario FIR label is 'Unfunded employee benefits'; legacy LGPI field compatibility is retained for review.",
        ),
        direct(
            "long_term_debt","74",9910,"74 xxxx 01",
            status="pending_review",
            note="Ontario FIR label is 'TOTAL Net Long Term Liabilities of the Municipality'; mapped provisionally to the narrower legacy long-term-debt field.",
        ),
        direct(
            "net_taxes","10",9940,"10 xxxx 01",
            status="pending_review",
            note="Ontario FIR 'Property Taxation Subtotal' combines own-purpose taxation and payments-in-lieu; legacy net-tax treatment is retained for review.",
        ),
        summed(
            "government_grants_total","10",[699,899],"10 xxxx 01",
            "OMPF/unconditional subtotal plus conditional-grants subtotal.",
        ),
        direct("user_charges","10",1299,"10 xxxx 01"),
        direct("investment_income","10",1805,"10 xxxx 01"),
        direct("total_revenue","10",9910,"10 xxxx 01"),

        direct("democracy_costs","40",240,"40 xxxx 11"),
        direct("general_government_total","40",299,"40 xxxx 11"),
        direct("fire","40",410,"40 xxxx 11"),
        direct("police","40",420,"40 xxxx 11"),
        direct("public_safety_total","40",499,"40 xxxx 11"),
        direct("transportation_total","40",699,"40 xxxx 11"),
        direct("environmental_services","40",899,"40 xxxx 11"),
        direct("health_services","40",1099,"40 xxxx 11"),
        direct("social_family_services","40",1299,"40 xxxx 11"),
        direct("social_housing","40",1499,"40 xxxx 11"),
        summed(
            "social_services_total","40",[1099,1299,1499],"40 xxxx 11",
            "Health, social/family services and social housing.",
        ),
        direct("recreation_culture","40",1699,"40 xxxx 11"),
        direct("planning_development","40",1899,"40 xxxx 11"),
        direct("total_expenditure","40",9910,"40 xxxx 11"),
        direct("salaries_benefits","42",5099,"42 xxxx 01"),
    ]

    # General government excluding governance/democracy costs.
    total,row=line_value(s["40"],indexes,slug,299,"40 xxxx 11")
    governance,_=line_value(s["40"],indexes,slug,240,"40 xxxx 11")
    amount=None if total is None or governance is None else total-governance
    out.append(obs(
        slug,"general_government",amount,s["40"],row,"40 xxxx 11",
        method="derived_residual",
        note="General government total less governance/democracy costs.",
        extra_lines=[299,240],
    ))

    # Remaining protection services outside police and fire.
    protective,row=line_value(s["40"],indexes,slug,499,"40 xxxx 11")
    fire,_=line_value(s["40"],indexes,slug,410,"40 xxxx 11")
    police,_=line_value(s["40"],indexes,slug,420,"40 xxxx 11")
    amount=None if any(v is None for v in (protective,fire,police)) else protective-fire-police
    out.append(obs(
        slug,"public_safety_other",amount,s["40"],row,"40 xxxx 11",
        method="derived_residual",
        note="Protection-services total less fire and police.",
        extra_lines=[499,410,420],
    ))

    # Broad 'other revenue' residual while developer-contribution mapping is still open.
    total,row=line_value(s["10"],indexes,slug,9910,"10 xxxx 01")
    taxes,_=line_value(s["10"],indexes,slug,9940,"10 xxxx 01")
    grants_a,_=line_value(s["10"],indexes,slug,699,"10 xxxx 01")
    grants_b,_=line_value(s["10"],indexes,slug,899,"10 xxxx 01")
    user,_=line_value(s["10"],indexes,slug,1299,"10 xxxx 01")
    investment,_=line_value(s["10"],indexes,slug,1805,"10 xxxx 01")
    vals=(total,taxes,grants_a,grants_b,user,investment)
    amount=None if any(v is None for v in vals) else total-taxes-grants_a-grants_b-user-investment
    out.append(obs(
        slug,"revenue_other",amount,s["10"],row,"10 xxxx 01",
        method="derived_residual",
        note="Total revenues less property-taxation subtotal, grant subtotals, user fees/service charges and investment income. Developer/donation subcomponents remain inside this residual pending legacy mapping review.",
        extra_lines=[9910,9940,699,899,1299,1805],
    ))
    return out


def main():
    schedules=[load_schedule(code) for code in SCHEDULES]
    source_names,missing_sources=target_source_names(schedules[0]["rows"])
    indexes={item["schedule"]:index_rows(item,source_names) for item in schedules}
    s={item["schedule"]:item for item in schedules}

    municipalities=[]
    observations=[]
    for slug,source_name in source_names.items():
        household,row=field(s["02"],indexes,slug,40,"02 xxxx 01")
        population,_=field(s["02"],indexes,slug,41,"02 xxxx 01")
        municipality={
            "slug":slug,
            "sourceMunicipality":source_name,
            "assessmentCode":str(row.get("Asmt Code") or ""),
            "mahCode":str(row.get("MAH Code") or ""),
            "municipalId":str(row.get("MunID") or ""),
            "tier":row.get("Tier"),
            "mso":row.get("MSO"),
            "householdsCandidate":household,
            "householdsCandidateSource":row.get("02 xxxx 02"),
            "populationCandidate":population,
            "normalizationNote":"FIR Schedule 02 household/population values are retained as source context. Per-household LGPI calculations stay disabled until the historical denominator convention is reconciled across provinces.",
        }
        municipalities.append(municipality)
        observations.extend(build(slug,schedules,indexes))

    # Cross-check Schedule 70 tangible capital assets against Schedule 51 line 9921 col 11.
    failures=[]
    for slug in source_names:
        tca70,_=field(s["70"],indexes,slug,6210,"70 xxxx 01")
        tca51,_=field(s["51"],indexes,slug,9921,"51 xxxx 11")
        if tca70 != tca51:
            failures.append(f"{slug}: schedule70={tca70} schedule51={tca51}")
    if failures:
        raise RuntimeError("Ontario tangible-capital-asset reconciliation failed:\n" + "\n".join(failures))

    document={
        "schemaVersion":1,
        "province":"ON",
        "year":2023,
        "source":{
            "publisher":"Ontario Ministry of Municipal Affairs and Housing",
            "title":"Financial Information Return — FIR Data by Schedule, 2023",
            "indexUrl":INDEX_URL,
            "scheduleArchives":{code:f"{BASE}/VIEWFIR2023-{code}.zip" for code in SCHEDULES},
        },
        "mapping":{
            "name":"LGPI Ontario FIR 2023",
            "version":1,
            "notes":[
                "Ontario open-data FIR amounts are published as dollars; output values are divided by 1,000 for legacy LGPI display units.",
                "Only line codes with explicit LGPI-compatible meanings are emitted.",
                "Ambiguous net-tax, employee-benefit-liability and long-term-debt mappings are marked pending_review.",
                "Tangible capital assets must reconcile between Schedule 70 line 6210 and Schedule 51 line 9921 column 11.",
                "Schedule 02 households are retained as denominator candidates but are not yet used for per-household calculations.",
            ],
        },
        "municipalities":municipalities,
        "sourceUnavailableMunicipalities":[
            {
                "slug":slug,
                "expectedSourceMunicipality":TARGETS[slug],
                "status":"source_unavailable",
                "reason":reason,
            }
            for slug,reason in missing_sources.items()
        ],
        "observations":observations,
        "stats":{
            "targetMunicipalityCount":len(TARGETS),
            "municipalityCount":len(municipalities),
            "sourceUnavailableMunicipalityCount":len(missing_sources),
            "observationCount":len(observations),
            "reportedCount":sum(1 for row in observations if row["status"]=="reported"),
            "pendingReviewCount":sum(1 for row in observations if row["status"]=="pending_review"),
        },
    }
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text(json.dumps(document,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(
        f"Wrote {OUTPUT}: {len(municipalities)} source-available municipalities, "
        f"{len(missing_sources)} source-unavailable municipalities, {len(observations)} observations"
    )
    for slug,reason in missing_sources.items():
        print(f"- {slug}: SOURCE UNAVAILABLE — {reason}")
    for m in municipalities:
        print(f"- {m['slug']}: source={m['sourceMunicipality']!r} tier={m['tier']} households={m['householdsCandidate']} population={m['populationCandidate']}")


if __name__=="__main__":
    main()
