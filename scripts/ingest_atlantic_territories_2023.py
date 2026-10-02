#!/usr/bin/env python3
"""Generate the final 2023 Atlantic/territorial LGPI financial tranche.

The final jurisdictions do not share one common machine-readable return.
This controlled adapter maps values from official audited statements into the
legacy LGPI catalogue. Values that combine source lines are documented as
derived; mappings that may not exactly match the old LGPI convention are
pending_review. No unavailable field is converted to zero.
"""

from __future__ import annotations

import json
from pathlib import Path

OUTPUT = Path("data/2023/atlantic_territories.json")

SOURCES = {
    "halifax": ("Halifax", "NS", "https://cdn.halifax.ca/sites/default/files/documents/city-hall/budget-finances/march-31-2023-financial-statements_cao-approved.pdf", "Halifax Regional Municipality Consolidated Financial Statements — March 31, 2023", "thousands"),
    "cape-breton": ("Cape Breton", "NS", "https://cbrm.ns.ca/wp-content/uploads/2026/01/2022-2023-CBRM_Audited_Financial_Statements_22-23.pdf", "Cape Breton Regional Municipality Audited Financial Statements — March 31, 2023", "dollars"),
    "moncton": ("Moncton", "NB", "https://www5.moncton.ca/docs/budget/2024_Consolidated_Financial_Statements.pdf", "City of Moncton 2024 Consolidated Financial Statements — 2023 comparative column", "dollars"),
    "fredericton": ("Fredericton", "NB", "https://www.fredericton.ca/sites/default/files/2025-04/City%20of%20Fredericton%20-%202023%20Consolidated%20Financial%20Statements%20-%20English%20%282%29.pdf", "City of Fredericton 2023 Consolidated Financial Statements", "dollars"),
    "saint-john": ("Saint John", "NB", "https://saintjohn.ca/sites/default/files/documents/City%20of%20Saint%20John%20December%2031%202023%20Financial%20Statements%20Eng%20%28002%29%20-%20with%20Signature.pdf", "City of Saint John 2023 Consolidated Financial Statements", "dollars"),
    "st-johns": ("St. John's", "NL", "https://www.stjohns.ca/media/miopyywx/20231231_city-of-st-johns-consolidated-financial-statements_final-signed.pdf", "City of St. John's 2023 Consolidated Financial Statements", "dollars"),
    "charlottetown": ("Charlottetown", "PE", "https://www.charlottetown.ca/UserFiles/Servers/Server_10500298/File/City%20of%20Charlottetown%20Consolidated%20Financial%20Statements%20-%20March%2031,%202023.pdf", "City of Charlottetown Consolidated Financial Statements — March 31, 2023", "dollars"),
    "whitehorse": ("Whitehorse", "YT", "https://www.whitehorse.ca/wp-content/uploads/2024/10/2023-City-of-Whitehorse_AR-WEB.pdf", "City of Whitehorse 2023 Annual Report", "dollars"),
    "yellowknife": ("Yellowknife", "NT", "https://www.yellowknife.ca/en/city-government/resources/Reports/Annual_Report/2023-FINANCIAL-REPORT.pdf", "City of Yellowknife 2023 Financial Report", "thousands"),
    "iqaluit": ("Iqaluit", "NU", "https://iqaluit.ca/sites/default/files/city_of_iqaluit_2023_fs_-_english_-_cao_signed.pdf", "City of Iqaluit 2023 Financial Statements", "dollars"),
}

# metric: (source amount, source label, mapping kind, note)
# kind: direct | derived | pending
ROWS = {
    "halifax": {
        "financial_assets_total": (1161128, "Financial assets", "direct", None),
        "holdings_council_controlled": (296323, "Investment in Halifax Regional Water Commission", "pending", "Government business enterprise equity; closest legacy LGPI council-controlled-operations concept."),
        "financial_assets_other": (864805, "Financial assets less HRWC investment", "derived", None),
        "financial_liabilities_total": (607493, "Financial liabilities", "direct", None),
        "employee_future_benefit_liability": (70274, "Employee future benefits", "direct", None),
        "long_term_debt": (198262, "Long-term debt", "direct", None),
        "net_financial_assets": (553635, "Net financial assets", "direct", None),
        "capital_assets": (2033615, "Tangible capital assets", "direct", None),
        "net_taxes": (953085, "Taxation + taxation from other governments", "derived", None),
        "user_charges": (138962, "User fees and charges", "direct", None),
        "government_grants_total": (109686, "Government grants", "direct", None),
        "developer_contributions": (1737, "Development levies", "pending", "Development levies used as the closest explicit developer-related revenue line."),
        "investment_income": (19661, "Investment income", "direct", None),
        "revenue_other": (166744, "Remaining consolidated revenue", "derived", "Residual includes penalties/fines, land sales/contributions, HRWC income and grant in lieu."),
        "total_revenue": (1389875, "Total revenue", "direct", None),
        "general_government_total": (146986, "General government services", "direct", None),
        "public_safety_total": (270084, "Protective services", "direct", None),
        "transportation_total": (333893, "Transportation services", "direct", None),
        "environmental_services": (51411, "Environmental services", "direct", None),
        "recreation_culture": (165912, "Recreation and cultural services", "direct", None),
        "planning_development": (37769, "Planning and development services", "direct", None),
        "total_expenditure": (1181179, "Total expenses", "direct", None),
        "salaries_benefits": (472923, "Salaries, wages and benefits", "direct", None),
        "interest_expense": (5109, "Interest on long-term debt", "direct", None),
        "goods": (82642, "Materials, goods, supplies and utilities", "direct", None),
        "contracted_services": (163531, "Contracted services", "direct", None),
        "grants_object": (228194, "External transfers and grants", "direct", None),
        "depreciation_object": (146991, "Amortization of tangible capital assets", "direct", None),
        "depreciation_function": (146991, "Amortization of tangible capital assets", "direct", None),
        "object_other": (81789, "Other operating expenses", "direct", None),
        "total_expenditure_object": (1181179, "Total expenses", "direct", None),
    },
    "cape-breton": {
        "financial_assets_total": (102629185, "Total financial assets", "direct", "Audited statement is image-based; values visually verified from the official signed statement."),
        "financial_liabilities_total": (171687131, "Total financial liabilities", "direct", None),
        "employee_future_benefit_liability": (6186993, "Employee benefits", "direct", None),
        "long_term_debt": (85000433, "Long-term debt", "direct", None),
        "net_financial_assets": (-69057946, "Net debt", "direct", None),
        "capital_assets": (466939369, "Tangible capital assets", "direct", "Work in progress is reported separately and is not silently added to this legacy field."),
        "net_taxes": (128483308, "Taxes + grants in lieu", "derived", None),
        "user_charges": (24494970, "Sales of services + water utility revenue", "pending", "Closest high-level user-charge grouping from the audited statement."),
        "government_grants_total": (49547148, "Unconditional + conditional + capital grants", "derived", None),
        "investment_income": (794255, "Investment income", "direct", None),
        "revenue_other": (16872273, "Other own-source/consolidated revenue", "derived", None),
        "total_revenue": (220191954, "Total revenue", "direct", None),
        "general_government_total": (17022224, "General government", "direct", None),
        "public_safety_total": (49198662, "Protective services", "direct", None),
        "transportation_total": (56957968, "Transportation", "direct", None),
        "environmental_services": (0, "Environmental functions", "pending", "Placeholder avoided; component presentation is not safely comparable."),
        "health_services": (2721969, "Public health and welfare", "direct", None),
        "planning_development": (1988815, "Environmental development + planning/development", "derived", None),
        "recreation_culture": (13278176, "Recreation and cultural services", "direct", None),
        "utility_operations": (16753009, "Water utility expenses", "direct", None),
        "total_expenditure": (174439945, "Total expenses", "direct", None),
    },
    "moncton": {
        "financial_assets_total": (188356414, "Financial assets — 2023 comparative", "direct", "Transcribed from the official 2024 consolidated statements' 2023 comparative column."),
        "financial_liabilities_total": (218402681, "Liabilities — 2023 comparative", "direct", None),
        "employee_future_benefit_liability": (13908200, "Post-employment benefits — 2023 comparative", "direct", None),
        "long_term_debt": (144999000, "Long-term debt — 2023 comparative", "direct", None),
        "net_financial_assets": (-30046267, "Net debt — 2023 comparative", "direct", None),
        "capital_assets": (948117107, "Tangible capital assets — 2023 comparative", "direct", None),
        "net_taxes": (168249168, "Property tax warrant", "pending", "Legacy grants-in-lieu treatment remains under review."),
        "user_charges": (38587922, "Water and wastewater user fees", "direct", None),
        "government_grants_total": (17185068, "Community/equalization + operating/capital government transfers", "derived", None),
        "investment_income": (12816099, "Interest and return on investments", "direct", None),
        "revenue_other": (0, "Other own-source and capital contributions", "pending", "High-level source grouping not fully decomposed into legacy categories."),
        "total_revenue": (273424014, "Operating revenue plus capital transfers/contributions", "derived", None),
        "salaries_benefits": (66281297, "Salaries and benefits", "direct", None),
        "total_expenditure": (230277911, "Total expenses", "direct", None),
    },
    "fredericton": {
        "financial_assets_total": (119438860, "Financial assets", "direct", None),
        "financial_liabilities_total": (79586782, "Liabilities", "direct", None),
        "long_term_debt": (26147000, "Long-term debt", "direct", None),
        "net_financial_assets": (39852078, "Net surplus", "direct", None),
        "capital_assets": (657111435, "Tangible capital assets", "direct", None),
        "net_taxes": (137293532, "Property tax/community funding and equalization grant", "pending", "Segment source combines property taxation and community funding/equalization."),
        "user_charges": (33615229, "Sales, fines and other fees", "pending", "Broader than pure user charges; retained pending legacy mapping review."),
        "government_grants_total": (18494887, "Government transfers", "direct", None),
        "investment_income": (4660868, "Interest and return on investments", "direct", None),
        "developer_contributions": (23181234, "Third-party contributions", "pending", "Broader than developer contributions."),
        "total_revenue": (203847849, "Total revenue", "direct", None),
        "general_government_total": (8728882, "Governance & Civic Engagement + General Government Services - Corporate", "derived", None),
        "public_safety_total": (55265211, "Public Safety", "direct", None),
        "transportation_total": (35872329, "Mobility including Transit", "direct", None),
        "environmental_services": (0, "Environmental Stewardship + Water and Wastewater", "pending", "Combined environmental grouping pending legacy review."),
        "planning_development": (0, "Economic Vitality + Livable Community", "pending", "Not emitted as a numeric value because source functions are broader than the legacy field."),
        "total_expenditure": (165836419, "Total expenses", "direct", None),
        "salaries_benefits": (85457889, "Salaries and benefits", "direct", None),
        "goods_services_total": (52303370, "Goods and services", "direct", None),
        "depreciation_object": (24473410, "Amortization", "direct", None),
        "depreciation_function": (24473410, "Amortization", "direct", None),
        "interest_expense": (838282, "Interest", "direct", None),
        "object_other": (2763468, "Other loss on assets", "direct", None),
        "total_expenditure_object": (165836419, "Total expenses", "direct", None),
    },
    "saint-john": {
        "financial_assets_total": (263160883, "Financial assets", "direct", "Official 2023 signed statement; values visually verified where the PDF text layer is incomplete."),
        "holdings_council_controlled": (88117000, "Investment in energy services", "pending", "Closest legacy council-controlled-operations concept."),
        "financial_assets_other": (175043883, "Financial assets less energy-services investment", "derived", None),
        "financial_liabilities_total": (321964045, "Liabilities", "direct", None),
        "employee_future_benefit_liability": (61683400, "Employee future benefits", "direct", None),
        "long_term_debt": (170491740, "Long-term debt", "direct", None),
        "net_financial_assets": (-58803162, "Net debt", "direct", None),
        "capital_assets": (1000845631, "Tangible capital assets", "direct", None),
        "net_taxes": (142169733, "Property taxes", "direct", None),
        "user_charges": (47634536, "Water and sewer revenue", "pending", "Direct utility user-charge line; other municipal own-source revenue remains in other revenue."),
        "government_grants_total": (42792365, "Unconditional + regional-service + capital government grants", "derived", None),
        "revenue_other": (0, "Other own-source/contributions/energy-services income", "pending", "Grouped source categories retained as other revenue."),
        "total_revenue": (270420541, "Operating revenue plus capital government transfers", "derived", None),
        "general_government_total": (29313989, "General government", "direct", None),
        "public_safety_total": (55542543, "Protective services", "direct", None),
        "transportation_total": (44923863, "Transportation", "direct", None),
        "environmental_services": (52555010, "Water/sewer services + environmental health", "derived", None),
        "planning_development": (20484761, "Environmental development", "pending", "Closest high-level planning/development function."),
        "recreation_culture": (11038059, "Recreation and cultural services", "direct", None),
        "total_expenditure": (213858225, "Total expenses", "direct", None),
    },
    "st-johns": {
        "financial_assets_total": (233815890, "Financial assets", "direct", None),
        "financial_liabilities_total": (659734608, "Liabilities", "direct", None),
        "employee_future_benefit_liability": (228827854, "Employee benefit obligations", "direct", None),
        "long_term_debt": (339177136, "Debenture debt + other long-term debt", "derived", None),
        "net_financial_assets": (-425918718, "Net debt", "direct", None),
        "capital_assets": (1283935929, "Tangible capital assets", "direct", None),
        "net_taxes": (232633228, "Taxation + grants in lieu of taxes", "derived", None),
        "user_charges": (59105203, "Sales of goods and services", "direct", None),
        "government_grants_total": (38886727, "Government grants and transfers", "direct", None),
        "revenue_other": (27484825, "Other own-source revenue", "direct", None),
        "total_revenue": (358109983, "Total revenue", "direct", None),
        "general_government_total": (58930532, "General government + fiscal services", "derived", None),
        "transportation_total": (70323260, "Transportation", "direct", None),
        "public_safety_total": (38812790, "Protective services", "direct", None),
        "environmental_services": (52778399, "Environmental health", "direct", None),
        "planning_development": (7221837, "Environmental development", "pending", "Closest high-level planning/development function."),
        "recreation_culture": (36555179, "Recreation and cultural services", "direct", None),
        "depreciation_function": (46222819, "Amortization and allowances", "pending", "Source combines amortization with allowances."),
        "total_expenditure": (310844816, "Total expenses", "direct", None),
    },
    "whitehorse": {
        "financial_assets_total": (120630937, "Total financial assets", "direct", None),
        "financial_liabilities_total": (48473987, "Total liabilities", "direct", None),
        "employee_future_benefit_liability": (3797000, "Employee future benefits", "direct", None),
        "long_term_debt": (13650345, "Debt", "direct", None),
        "net_financial_assets": (72156950, "Net financial assets", "direct", None),
        "capital_assets": (465488380, "Tangible capital assets", "direct", None),
        "net_taxes": (49483510, "Taxes and payments in lieu of taxes", "direct", None),
        "government_grants_total": (30073719, "Government transfers", "direct", None),
        "user_charges": (22203509, "Sales of goods and services", "direct", None),
        "developer_contributions": (531824, "Developers' contributions", "direct", None),
        "investment_income": (5415598, "Investment income", "direct", None),
        "revenue_other": (7413187, "Licenses/permits/penalties/fines + other revenues", "derived", None),
        "total_revenue": (115121347, "Total revenues", "direct", None),
        "general_government_total": (23392478, "General government services", "direct", None),
        "public_safety_total": (11274749, "Protective services", "direct", None),
        "transportation_total": (28441800, "Transportation services", "direct", None),
        "environmental_services": (19898674, "Environmental services", "direct", None),
        "health_services": (187569, "Public health services", "direct", None),
        "planning_development": (3324934, "Community development services", "pending", "Closest high-level planning/development field."),
        "recreation_culture": (17599782, "Recreation and cultural services", "direct", None),
        "total_expenditure": (104119986, "Total expenses", "direct", None),
        "salaries_benefits": (51784688, "Salaries and benefits", "direct", None),
        "goods": (16995496, "Materials and supplies", "direct", None),
        "contracted_services": (8504222, "Professional services", "direct", None),
        "grants_object": (1919001, "Community grants", "direct", None),
        "interest_expense": (446842, "Interest", "direct", None),
        "depreciation_object": (21400462, "Amortization", "direct", None),
        "depreciation_function": (21400462, "Amortization", "direct", None),
        "object_other": (3069275, "Public relations + other", "derived", None),
        "total_expenditure_object": (104119986, "Total expense by object", "direct", None),
    },
    "yellowknife": {
        "financial_assets_total": (171820, "Financial assets", "direct", None),
        "financial_liabilities_total": (107554, "Liabilities", "direct", None),
        "employee_future_benefit_liability": (4277, "Employee benefits", "direct", None),
        "long_term_debt": (27800, "Long-term debt", "direct", None),
        "net_financial_assets": (64266, "Net financial assets", "direct", None),
        "capital_assets": (321409, "Tangible capital assets", "direct", None),
        "net_taxes": (35842, "Property taxation", "direct", None),
        "user_charges": (23703, "User charges / sales of services", "direct", None),
        "government_grants_total": (40836, "Operating + capital government transfers", "derived", None),
        "investment_income": (5748, "Investment income", "direct", None),
        "revenue_other": (5964, "Other operating revenue", "derived", None),
        "total_revenue": (112093, "Operating revenue plus capital transfers", "derived", None),
        "general_government_total": (16847, "General government", "direct", None),
        "public_safety_total": (20079, "Protective services", "direct", None),
        "public_works": (13596, "Public works", "direct", None),
        "solid_waste": (4149, "Solid waste", "direct", None),
        "utility_operations": (16257, "Water and sewer", "direct", None),
        "planning_development": (2384, "Planning and development", "direct", None),
        "total_expenditure": (85465, "Total expenses", "direct", None),
        "salaries_benefits": (30827, "Salaries, wages and benefits", "direct", None),
        "contracted_services": (29491, "Contracted and general services", "direct", None),
        "goods": (1012, "Materials and supplies", "direct", None),
        "interest_expense": (1239, "Long-term debt interest + bank/short-term interest", "derived", None),
        "depreciation_object": (16001, "Amortization", "direct", None),
        "depreciation_function": (16001, "Amortization", "direct", None),
        "object_other": (16895, "Other audited expense objects", "derived", None),
        "total_expenditure_object": (85465, "Total expense by object", "direct", None),
    },
    "iqaluit": {
        "financial_assets_total": (81181558, "Financial assets", "direct", None),
        "financial_liabilities_total": (70385042, "Liabilities", "direct", None),
        "employee_future_benefit_liability": (1478638, "Post-employment benefits", "direct", None),
        "long_term_debt": (22597626, "Long-term debt", "direct", None),
        "net_financial_assets": (10796516, "Net financial assets", "direct", None),
        "capital_assets": (263975760, "Tangible capital assets", "direct", None),
        "net_taxes": (24941525, "Taxes and grants in lieu", "direct", None),
        "user_charges": (19270223, "Water/sewer + sanitation user revenue", "derived", None),
        "government_grants_total": (46591656, "Operating government transfers + capital government transfers", "derived", None),
        "revenue_other": (0, "Other own-source revenue", "pending", "Not emitted numerically until the high-level revenue residual is reconciled."),
        "total_revenue": (102449421, "Operating revenue plus capital government transfers", "derived", None),
        "general_government_total": (4933560, "General government", "direct", None),
        "public_safety_total": (5992614, "Emergency services + bylaw enforcement", "derived", None),
        "transportation_total": (5526980, "Public works / transportation", "direct", None),
        "environmental_services": (10355688, "Water/sewer + sanitation", "derived", None),
        "planning_development": (2499399, "Land development/administration + engineering + economic development", "derived", None),
        "recreation_culture": (7000821, "Recreation", "direct", None),
        "grants_function": (14143538, "Community funding", "pending", "Source function may include transfers not directly comparable to legacy grants."),
        "depreciation_function": (10663856, "Amortization", "direct", None),
        "total_expenditure": (61116456, "Total expenses", "direct", None),
    },
    "charlottetown": {},
}

# Remove intentional non-numeric placeholders encoded as zero in ambiguous rows.
AMBIGUOUS_SKIP = {
    ("cape-breton", "environmental_services"),
    ("moncton", "revenue_other"),
    ("fredericton", "environmental_services"),
    ("fredericton", "planning_development"),
    ("saint-john", "revenue_other"),
    ("iqaluit", "revenue_other"),
}

def to_thousands(slug: str, amount: int | float) -> float:
    unit=SOURCES[slug][4]
    return float(amount) if unit=="thousands" else float(amount)/1000.0

def main() -> None:
    municipalities=[]
    observations=[]

    for slug,(name,province,url,label,unit) in SOURCES.items():
        municipalities.append({
            "slug":slug,
            "name":name,
            "province":province,
            "sourceUrl":url,
            "sourceLabel":label,
            "sourceUnits":unit,
            "observationCount":sum(1 for metric in ROWS[slug] if (slug,metric) not in AMBIGUOUS_SKIP),
        })
        for metric,(amount,source_label,kind,note) in ROWS[slug].items():
            if (slug,metric) in AMBIGUOUS_SKIP:
                continue
            status="pending_review" if kind=="pending" else "reported"
            method="direct" if kind in {"direct","pending"} else "derived_sum"
            observations.append({
                "municipalitySlug":slug,
                "year":2023,
                "metric":metric,
                "valueThousands":to_thousands(slug,amount),
                "status":status,
                "sourceUrl":url,
                "sourceLabel":label,
                "sourceLocation":source_label,
                "sourceReportedLabel":source_label,
                "sourceFieldCodes":[f"statement:{source_label}"],
                "mappingMethod":method,
                **({"note":note} if note else {}),
            })

    doc={
        "schemaVersion":1,
        "year":2023,
        "sourceType":"official_audited_statements",
        "municipalities":municipalities,
        "observations":observations,
        "mapping":{
            "name":"LGPI Atlantic and territorial audited statements 2023",
            "version":1,
            "notes":[
                "Values are mapped from official audited municipal statements or official subsequent-year comparative columns where explicitly noted.",
                "Source values reported in dollars are converted to thousands of Canadian dollars for LGPI display consistency.",
                "Image-only audited statements were visually transcribed and retained with their official source labels; no missing value was converted to zero.",
                "Derived groupings list their source meaning in notes; uncertain compatibility is marked pending_review.",
                "The City of Moncton's 2023 values are taken from the official 2024 statement's comparative 2023 column because the direct 2023 resource is not reliably retrievable.",
            ],
        },
        "stats":{
            "municipalityCount":len(municipalities),
            "municipalitiesWithObservations":sum(1 for m in municipalities if m["observationCount"]>0),
            "observationCount":len(observations),
            "reportedCount":sum(1 for x in observations if x["status"]=="reported"),
            "pendingReviewCount":sum(1 for x in observations if x["status"]=="pending_review"),
        },
    }
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text(json.dumps(doc,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(municipalities)} municipalities, {len(observations)} observations")
    for m in municipalities:
        print(f"- {m['slug']}: {m['observationCount']} observations")

if __name__=="__main__":
    main()
