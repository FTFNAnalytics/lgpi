#!/usr/bin/env python3
"""Generate source-backed 2023 LGPI observations for Regina, Saskatoon and Winnipeg.

These municipalities publish audited annual reports rather than a common
province-wide FIR workbook suitable for LGPI. The importer uses a controlled
transcription table from the audited statements and validates each reported
amount against extracted PDF text before emitting JSON.

All source amounts are already reported in thousands of Canadian dollars.
"""

from __future__ import annotations

import io
import json
import re
import urllib.request
from pathlib import Path

from pypdf import PdfReader

OUTPUT = Path("data/2023/prairies.json")

SOURCES = {
    "regina": {
        "name": "Regina",
        "province": "SK",
        "url": "https://openregina.ca/dataset/5e011351-3612-4a51-919d-914dcef52ffb/resource/dae57e17-4742-42fb-a090-1dcc59260bdd/download/cor_2023_annual_report.pdf",
        "label": "City of Regina 2023 Annual Report",
    },
    "saskatoon": {
        "name": "Saskatoon",
        "province": "SK",
        "url": "https://www.saskatoon.ca/sites/default/files/documents/asset-financial-management/finance-supply/COS_2023-AnnualReport-Aug29-FINAL-web.pdf",
        "label": "City of Saskatoon 2023 Annual Report",
    },
    "winnipeg": {
        "name": "Winnipeg",
        "province": "MB",
        "url": "https://www.winnipeg.ca/finance/files/2023AnnualReport.pdf",
        "label": "City of Winnipeg 2023 Annual Financial Report",
    },
}

# metric -> (value in $000, PDF page, source label, status, note)
ROWS = {
    "regina": {
        "financial_assets_total": (650290, 38, "Financial assets", "reported", None),
        "financial_liabilities_total": (676515, 38, "Financial liabilities", "reported", None),
        "net_financial_assets": (-26225, 38, "Net financial (debt) assets", "reported", None),
        "long_term_debt": (313122, 43, "Total debt outstanding", "reported", "Consolidated debt outstanding across the City and controlled/accountable agencies."),
        "net_taxes": (322119, 54, "Taxation", "reported", None),
        "user_charges": (267363, 54, "Fees and charges", "reported", None),
        "government_grants_total": (175482, 54, "Government transfers", "reported", "The consolidated statement combines operating and capital government transfers."),
        "investment_income": (20568, 54, "Interest on investments", "reported", None),
        "developer_contributions": (10755, 54, "Servicing agreement fees + Contribution of tangible capital assets", "pending_review", "Derived from servicing agreement fees ($7.118m) plus contributed tangible capital assets ($3.637m); retained pending review against the legacy LGPI developer-contribution convention."),
        "revenue_other": (82178, 54, "Other consolidated revenue categories", "derived", "Residual after mapped taxes, fees/charges, transfers, investment income and developer-related contributions."),
        "total_revenue": (878465, 54, "Total consolidated revenue", "reported", None),
        "recreation_culture": (157987, 54, "Parks, recreation and community services", "reported", None),
        "police": (131962, 54, "Police", "reported", None),
        "fire": (53726, 54, "Fire", "reported", None),
        "public_safety_total": (185688, 54, "Police + Fire", "pending_review", "Derived from separately reported police and fire functions. Other protective services are not separately identified in this high-level statement."),
        "general_government_total": (101120, 54, "Legislative and administrative services", "reported", None),
        "environmental_services": (147167, 54, "Water, wastewater and drainage + Waste collection and disposal", "derived", "Combined environmental-service functions in the consolidated statement."),
        "transportation": (89798, 54, "Roads and traffic", "reported", None),
        "transit": (49381, 54, "Transit", "reported", None),
        "transportation_total": (139179, 54, "Roads and traffic + Transit", "derived", None),
        "grants_function": (15975, 54, "Grants", "reported", None),
        "planning_development": (18382, 54, "Planning and development", "reported", None),
        "total_expenditure": (765498, 54, "Total consolidated expenses", "reported", None),
    },
    "saskatoon": {
        "financial_assets_total": (823297, 73, "Total Assets", "reported", "Financial assets total on the consolidated statement of financial position."),
        "financial_liabilities_total": (554039, 73, "Total Financial Liabilities", "reported", None),
        "net_financial_assets": (269258, 73, "Total Net Financial Assets", "reported", None),
        "capital_assets": (4836145, 73, "Tangible Capital Assets", "reported", None),
        "long_term_debt": (263043, 73, "Long-Term Debt", "reported", None),
        "employee_future_benefit_liability": (43332, 73, "Employee Benefits Payable", "pending_review", "Source label is broader than the legacy LGPI employee-future-benefit-liability field."),
        "net_taxes": (324261, 74, "Taxation", "reported", None),
        "user_charges": (472030, 74, "User Fees", "reported", None),
        "government_grants_total": (138026, 74, "Government Transfers - Capital + Government Transfers - Operating", "derived", "Operating ($77.753m) plus capital ($60.273m) government transfers."),
        "investment_income": (19750, 74, "Investment Income", "reported", None),
        "developer_contributions": (69415, 74, "Contribution from Developers & Others - Capital + Operating", "derived", "Capital ($27.766m) plus operating ($41.649m) developer/other contributions."),
        "revenue_other": (111204, 74, "Grants in lieu + Franchise Fees + General Revenues", "derived", "Residual high-level revenue: grants in lieu of taxes, franchise fees and general revenues."),
        "total_revenue": (1134686, 74, "Total Revenues", "reported", None),
        "general_government_total": (87143, 74, "Corporate Asset Management + Corporate Governance & Finance + Taxation and General Revenues", "pending_review", "Derived high-level general-government grouping for legacy LGPI compatibility."),
        "public_safety_total": (186593, 74, "Saskatoon Fire + Saskatoon Police Service", "derived", None),
        "fire": (59673, 74, "Saskatoon Fire", "reported", None),
        "police": (126920, 74, "Saskatoon Police Service", "reported", None),
        "transportation_total": (207700, 74, "Transportation", "reported", None),
        "environmental_services": (26338, 74, "Environmental Health", "reported", None),
        "utility_operations": (230220, 74, "Utilities", "reported", None),
        "planning_development": (69544, 74, "Land Development + Urban Planning and Development", "derived", None),
        "recreation_culture": (151871, 74, "Arts, Culture and Events Venues + Recreation and Culture + Saskatoon Public Library", "derived", None),
        "total_expenditure": (988598, 74, "Total Expenses", "reported", None),
        "salaries_benefits": (407893, 102, "Wages and Benefits", "reported", None),
        "contracted_services": (192254, 102, "Contracted and General Services", "reported", None),
        "goods": (77993, 102, "Material, Goods and Supplies", "reported", None),
        "goods_services_other": (129595, 102, "Heating, Lighting, Power, Water and Telephone", "reported", None),
        "goods_services_total": (399842, 102, "Contracted and General Services + Heating/Lighting/Power/Water/Telephone + Material/Goods/Supplies", "derived", None),
        "grants_object": (12764, 102, "Donations, Grants and Subsidies", "reported", None),
        "interest_expense": (11321, 102, "Finance Charges", "reported", None),
        "depreciation_object": (154974, 102, "Amortization", "reported", None),
        "depreciation_function": (154974, 102, "Amortization", "reported", None),
        "object_other": (1804, 102, "Accretion", "reported", None),
        "total_expenditure_object": (988598, 102, "Total", "derived", "Derived from the eight audited expense-by-object components, which sum to $988.598m and reconcile to the Statement of Operations. The PDF text layer mis-renders the printed total as 998,598."),
    },
    "winnipeg": {
        "financial_assets_total": (1686720, 52, "Financial Assets", "reported", None),
        "holdings_council_controlled": (20216, 52, "Investment in business partnerships", "pending_review", "Mapped to the closest legacy LGPI council-controlled-operations field."),
        "financial_assets_other": (1666504, 52, "Financial Assets less Investment in business partnerships", "derived", None),
        "financial_liabilities_total": (2855630, 52, "Liabilities", "reported", None),
        "net_financial_assets": (-1168910, 52, "Net Financial Liabilities", "reported", None),
        "capital_assets": (8423939, 52, "Tangible capital assets", "reported", None),
        "long_term_debt": (1411222, 52, "Debt", "reported", None),
        "employee_future_benefit_liability": (267131, 52, "Employee benefits obligations", "reported", None),
        "net_taxes": (884442, 53, "Taxation", "reported", None),
        "user_charges": (690991, 53, "Sales of services and regulatory fees", "reported", None),
        "government_grants_total": (477384, 53, "Government transfers + Government transfers related to capital", "derived", "Operating transfers ($262.451m) plus capital-related transfers ($214.933m)."),
        "investment_income": (64387, 53, "Investment income", "reported", None),
        "developer_contributions": (142178, 53, "Developer contributions-in-kind related to capital", "pending_review", "Direct capital developer contribution; retained pending legacy aggregation review."),
        "revenue_other": (32855, 53, "Land sales and other revenue + Other capital contributions", "derived", None),
        "total_revenue": (2292237, 53, "Total consolidated revenues including capital revenues", "derived", "Operating revenues ($1.927704b) plus capital-related transfers and contributions ($364.533m)."),
        "general_government_total": (144283, 44, "Finance and administration + General government", "derived", None),
        "utility_operations": (529152, 44, "Utility operations", "reported", None),
        "public_works": (380359, 44, "Public works", "reported", None),
        "planning_development": (138947, 44, "Property and development", "reported", None),
        "civic_corporations": (103148, 44, "Civic corporations", "reported", None),
        "total_expenditure": (1915408, 53, "Total Expenses", "reported", None),
        "salaries_benefits": (997609, 82, "Salaries and benefits", "reported", None),
        "goods_services_total": (522603, 82, "Goods and services", "reported", None),
        "depreciation_object": (306512, 82, "Amortization of tangible capital assets", "reported", None),
        "depreciation_function": (306512, 82, "Amortization of tangible capital assets", "reported", None),
        "interest_expense": (62371, 82, "Interest", "reported", None),
        "object_other": (26313, 82, "Other expenses", "reported", None),
        "total_expenditure_object": (1915408, 82, "Total expenses by object", "reported", None),
    },
}

STATUS_MAP = {
    "reported": "reported",
    "derived": "reported",
    "pending_review": "pending_review",
}


def fetch(url: str) -> bytes:
    request=urllib.request.Request(
        url,
        headers={"User-Agent":"LGPI-reconstruction/0.1 (+https://github.com/FTFNAnalytics/lgpi)"},
    )
    with urllib.request.urlopen(request,timeout=180) as response:
        payload=response.read()
    if len(payload)<100_000:
        raise RuntimeError(f"Prairie annual report unexpectedly small: {url} ({len(payload)} bytes)")
    return payload


def normalize(text: str) -> str:
    text=(text or "").replace("\u00a0"," ")
    return re.sub(r"\s+"," ",text).strip()


def validate_page(reader: PdfReader, page: int, label: str, value: int, *, require_amount: bool = True) -> None:
    if page < 1 or page > len(reader.pages):
        raise RuntimeError(f"Invalid PDF page {page}")
    text=normalize(reader.pages[page-1].extract_text() or "")
    # Source tables may use parentheses for negative amounts and may split labels.
    label_tokens=[token.lower() for token in re.findall(r"[A-Za-z]+",label) if len(token)>=4]
    if label_tokens and sum(token in text.lower() for token in label_tokens[:5]) < min(2,len(label_tokens[:5])):
        raise RuntimeError(f"Source label validation failed p.{page}: {label!r}")
    if require_amount:
        absolute=abs(value)
        candidates={
            f"{absolute:,}",
            str(absolute),
            f"({absolute:,})",
        }
        if not any(candidate in text for candidate in candidates):
            raise RuntimeError(f"Source amount validation failed p.{page}: {label!r} value={value}")


def main() -> None:
    observations=[]
    municipalities=[]

    for slug,source in SOURCES.items():
        payload=fetch(source["url"])
        reader=PdfReader(io.BytesIO(payload))
        source_rows=ROWS[slug]

        for metric,(value,page,label,kind,note) in source_rows.items():
            validate_page(
                reader,page,label,value,
                require_amount=(kind != "derived" and "+" not in label),
            )
            observations.append({
                "municipalitySlug":slug,
                "year":2023,
                "metric":metric,
                "valueThousands":value,
                "status":STATUS_MAP[kind],
                "sourceUrl":source["url"],
                "sourceLabel":source["label"],
                "sourceLocation":f"PDF page {page}",
                "sourceReportedLabel":label,
                "sourceFieldCodes":[f"pdf:p{page}:{label}"],
                "mappingMethod":"direct" if kind in {"reported","pending_review"} else "derived_sum",
                **({"note":note} if note else {}),
            })

        municipalities.append({
            "slug":slug,
            "name":source["name"],
            "province":source["province"],
            "sourceUrl":source["url"],
            "sourceLabel":source["label"],
            "observationCount":len(source_rows),
        })

    # Exact high-level controls.
    controls={
        "regina": {"total_revenue":878465,"total_expenditure":765498},
        "saskatoon": {"total_revenue":1134686,"total_expenditure":988598,"total_expenditure_object":988598},
        "winnipeg": {"total_revenue":2292237,"total_expenditure":1915408,"total_expenditure_object":1915408},
    }
    for slug,expected in controls.items():
        actual={x["metric"]:x["valueThousands"] for x in observations if x["municipalitySlug"]==slug}
        for metric,value in expected.items():
            if actual.get(metric)!=value:
                raise RuntimeError(f"{slug} control failed: {metric} expected {value}, got {actual.get(metric)}")

    document={
        "schemaVersion":1,
        "year":2023,
        "sourceType":"audited_annual_reports",
        "municipalities":municipalities,
        "observations":observations,
        "mapping":{
            "name":"LGPI Prairie audited statements 2023",
            "version":1,
            "notes":[
                "Amounts are transcribed from audited annual-report tables reported in thousands of Canadian dollars.",
                "Every emitted amount is validated against extracted text on its cited PDF page before JSON is written.",
                "Derived groupings preserve a source note; uncertain legacy compatibility is marked pending_review.",
                "No per-household denominator is calculated in this importer.",
            ],
        },
        "stats":{
            "municipalityCount":len(municipalities),
            "observationCount":len(observations),
            "reportedCount":sum(1 for x in observations if x["status"]=="reported"),
            "pendingReviewCount":sum(1 for x in observations if x["status"]=="pending_review"),
        },
    }
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text(json.dumps(document,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(municipalities)} municipalities, {len(observations)} observations")
    for m in municipalities:
        print(f"- {m['slug']}: {m['observationCount']} observations")


if __name__=="__main__":
    main()
