#!/usr/bin/env python3
"""Generate source-backed 2024 Atlantic/territorial LGPI financial observations.

These jurisdictions do not share one standardized provincial FIR. Values are
mapped from official audited municipal statements (or explicit comparative
columns / official actuals where noted), preserving the same legacy LGPI
concepts used in the 2023 reconstruction.

Amounts are entered in each source's reporting unit and normalized to $000.
Missing or non-comparable fields are omitted rather than converted to zero.
"""

from __future__ import annotations

import json
from pathlib import Path

OUTPUT = Path("data/2024/atlantic_territories.json")

SOURCES = {
    "halifax": {
        "name":"Halifax","province":"NS","units":"thousands",
        "url":"https://cdn.halifax.ca/sites/default/files/documents/city-hall/budget-finances/march-31-2024-audited-financial-statements-cao-approved.pdf",
        "label":"Halifax Regional Municipality Consolidated Financial Statements — March 31, 2024",
    },
    "cape-breton": {
        "name":"Cape Breton","province":"NS","units":"dollars",
        "url":"https://cbrm.ns.ca/wp-content/uploads/2026/01/2023-2024-CBRM_2023-24.pdf",
        "label":"Cape Breton Regional Municipality Consolidated Financial Statements — March 31, 2024",
    },
    "moncton": {
        "name":"Moncton","province":"NB","units":"dollars",
        "url":"https://www5.moncton.ca/docs/budget/2024_Consolidated_Financial_Statements.pdf",
        "label":"City of Moncton 2024 Consolidated Financial Statements",
    },
    "fredericton": {
        "name":"Fredericton","province":"NB","units":"dollars",
        "url":"https://www.fredericton.ca/sites/default/files/2025-06/CoF-2024AnnualReport-EN-.pdf",
        "label":"City of Fredericton 2024 Consolidated Financial Statements",
    },
    "saint-john": {
        "name":"Saint John","province":"NB","units":"dollars",
        "url":"https://saintjohn.ca/sites/default/files/documents/City%20of%20Saint%20John%20-%202024%20Consolidated%20FS%20-%20Final%20-%20Eng%20Statements.pdf",
        "label":"City of Saint John 2024 Consolidated Financial Statements",
    },
    "st-johns": {
        "name":"St. John's","province":"NL","units":"dollars",
        "url":"https://www.stjohns.ca/2024_Consolidated-Financial-Statements_City-of-St.-John%27s.pdf",
        "label":"City of St. John's 2024 Consolidated Financial Statements",
    },
    "charlottetown": {
        "name":"Charlottetown","province":"PE","units":"dollars",
        "url":"https://www.charlottetown.ca/UserFiles/Servers/Server_10500298/File/Mayor%20and%20Council/Finance/Audited%20Financial%20Statements/Draft%202024%20CoC%20Consolidated%20Financial%20Statements%20(1).pdf",
        "label":"City of Charlottetown Consolidated Financial Statements — March 31, 2024",
    },
    "whitehorse": {
        "name":"Whitehorse","province":"YT","units":"dollars",
        "url":"https://www.whitehorse.ca/wp-content/uploads/2025/10/COW-2024-AR-Web.pdf",
        "label":"City of Whitehorse 2024 Annual Report",
    },
    "yellowknife": {
        "name":"Yellowknife","province":"NT","units":"thousands",
        "url":"https://www.yellowknife.ca/en/city-government/resources/Reports/Annual_Report/2024-FINANCIAL-STATEMENTS.pdf",
        "label":"City of Yellowknife 2024 Financial Statements",
    },
    "iqaluit": {
        "name":"Iqaluit","province":"NU","units":"dollars",
        "url":"https://iqaluit.ca/sites/default/files/2024_consolidated_financial_statements_eng_-_signed.pdf",
        "label":"City of Iqaluit 2024 Consolidated Financial Statements",
    },
}

# metric -> (amount, reported label, mapping method, status, note)
ROWS = {
    "halifax": {
        "financial_assets_total": (1216776, "Financial assets", "direct", "reported", None),
        "financial_liabilities_total": (637215, "Financial liabilities", "direct", "reported", None),
        "long_term_debt": (245837, "Long-term debt", "direct", "reported", None),
        "net_financial_assets": (579561, "Net financial assets", "direct", "reported", None),
        "capital_assets": (2080155, "Tangible capital assets", "direct", "reported", None),
        "net_taxes": (999392, "Taxation + taxation from other governments", "derived_sum", "reported", None),
        "user_charges": (159056, "User fees and charges", "direct", "reported", None),
        "government_grants_total": (86359, "Government grants", "direct", "reported", None),
        "developer_contributions": (1617, "Development levies", "direct", "pending_review", "Development levies retained as the closest explicit developer-related revenue line."),
        "investment_income": (37830, "Investment income", "direct", "reported", None),
        "revenue_other": (56392, "Other consolidated revenue", "derived_residual", "reported", "Residual to total revenue after mapped headline revenue categories."),
        "total_revenue": (1340446, "Total revenue", "direct", "reported", None),
        "general_government_total": (151983, "General government services", "direct", "reported", None),
        "public_safety_total": (291549, "Protective services", "direct", "reported", None),
        "transportation_total": (372811, "Transportation services", "direct", "reported", None),
        "environmental_services": (48389, "Environmental services", "direct", "reported", None),
        "recreation_culture": (179313, "Recreation and cultural services", "direct", "reported", None),
        "planning_development": (42583, "Planning and development services", "direct", "reported", None),
        "total_expenditure": (1274758, "Total expenses", "direct", "reported", None),
        "salaries_benefits": (498200, "Salaries, wages and benefits", "direct", "reported", None),
        "interest_expense": (6264, "Interest on long-term debt", "direct", "reported", None),
        "goods": (85734, "Materials, goods, supplies and utilities", "direct", "reported", None),
        "contracted_services": (168053, "Contracted services", "direct", "reported", None),
        "grants_object": (242049, "External transfers and grants", "direct", "reported", None),
        "depreciation_object": (172504, "Amortization of tangible capital assets", "direct", "reported", None),
        "depreciation_function": (172504, "Amortization of tangible capital assets", "direct", "reported", None),
        "object_other": (101954, "Other operating expenses", "direct", "reported", None),
        "total_expenditure_object": (1274758, "Total expenses", "direct", "reported", None),
    },
    "cape-breton": {
        "financial_assets_total": (83435429, "Total financial assets", "direct", "reported", None),
        "financial_liabilities_total": (157064925, "Total financial liabilities", "direct", "reported", "Total reconciles to the individual liability lines; the OCR text rendered the leading digit inconsistently."),
        "employee_future_benefit_liability": (7343717, "Accrued employee benefits", "direct", "reported", None),
        "long_term_debt": (67352632, "Long-term debt", "direct", "reported", None),
        "net_financial_assets": (-73629496, "Net debt", "direct", "reported", None),
        "capital_assets": (475386549, "Tangible capital assets", "direct", "reported", "Work in progress is reported separately and is not silently added to this legacy field."),
        "net_taxes": (141136123, "Taxes + grants in lieu of taxes", "derived_sum", "reported", None),
        "user_charges": (27215284, "Services to other governments + sales of services + water utility revenue", "derived_sum", "pending_review", "Closest high-level legacy user-charge grouping."),
        "government_grants_total": (42098397, "Unconditional + conditional transfers + capital grants", "derived_sum", "reported", None),
        "investment_income": (1313531, "Investment income", "direct", "reported", None),
        "developer_contributions": (6928900, "Contributed assets", "direct", "pending_review", "Contributed assets retained as the closest developer/contribution concept."),
        "revenue_other": (14278673, "Other own-source / PSDC / disaster recovery / property gain", "derived_residual", "reported", None),
        "total_revenue": (232970908, "Total revenues", "direct", "reported", None),
        "general_government_total": (18809258, "General government services", "direct", "reported", None),
        "public_safety_total": (51406914, "Protective services", "direct", "reported", None),
        "transportation_total": (52989151, "Transportation services", "direct", "reported", None),
        "environmental_services": (26423318, "Environmental health services", "direct", "reported", None),
        "health_services": (3465650, "Public health and welfare services", "direct", "reported", None),
        "planning_development": (1182880, "Environmental development services", "direct", "pending_review", "Closest high-level planning/development concept."),
        "recreation_culture": (14891487, "Recreation and cultural services", "direct", "reported", None),
        "utility_operations": (17495843, "Water utility expenses", "direct", "reported", None),
        "civic_corporations": (2380052, "Port of Sydney Development Corporation", "direct", "pending_review", None),
        "depreciation_function": (22776736, "Amortization of tangible capital assets", "direct", "reported", None),
        "total_expenditure": (206382310, "Total expenses", "direct", "reported", None),
    },
    "moncton": {
        "financial_assets_total": (221066287, "Financial assets", "direct", "reported", None),
        "financial_liabilities_total": (218253506, "Liabilities", "direct", "reported", None),
        "employee_future_benefit_liability": (14507000, "Post-employment benefits", "direct", "reported", None),
        "long_term_debt": (147507000, "Long-term debt", "direct", "reported", None),
        "net_financial_assets": (2812781, "Net financial assets", "direct", "reported", None),
        "capital_assets": (982991992, "Tangible capital assets", "direct", "reported", None),
        "net_taxes": (185299993, "Property tax warrant", "direct", "pending_review", "Legacy grants-in-lieu treatment remains under review."),
        "user_charges": (41038679, "Water and wastewater user fees", "direct", "reported", None),
        "government_grants_total": (24659744, "Community/equalization + operating/capital government transfers", "derived_sum", "reported", None),
        "investment_income": (11320694, "Interest and return on investments", "direct", "reported", None),
        "developer_contributions": (9018264, "Contributed capital assets", "direct", "pending_review", None),
        "revenue_other": (32484623, "Other own-source revenue residual", "derived_residual", "reported", None),
        "total_revenue": (303821997, "Operating revenue plus capital transfers/contributions", "derived_sum", "reported", "Matches the 2023 LGPI reconstruction convention for Moncton."),
        "total_expenditure": (234960731, "Total expenses", "direct", "reported", None),
        "depreciation_function": (42849196, "Amortization of tangible capital assets", "direct", "reported", None),
        "depreciation_object": (42849196, "Amortization of tangible capital assets", "direct", "reported", None),
    },
    "fredericton": {
        "financial_assets_total": (126831275, "Financial assets", "direct", "reported", None),
        "financial_liabilities_total": (76052982, "Liabilities", "direct", "reported", None),
        "long_term_debt": (23357474, "External long-term debt and capital lease obligations", "direct", "reported", None),
        "net_financial_assets": (50778293, "Net surplus", "direct", "reported", None),
        "capital_assets": (701926079, "Tangible capital assets", "direct", "reported", None),
        "net_taxes": (149424529, "Property tax + community/equalization + federal grant-in-lieu adjustment", "derived_sum", "reported", None),
        "user_charges": (43179746, "Services to other governments + sales/fines/other fees", "derived_sum", "pending_review", "Broader than pure user charges; retained pending legacy mapping review."),
        "government_grants_total": (26994639, "Government transfers", "direct", "reported", None),
        "investment_income": (4830726, "Interest and return on investments", "direct", "reported", None),
        "developer_contributions": (33408146, "Third-party contributions", "direct", "pending_review", "Broader than developer contributions."),
        "revenue_other": (6413507, "Other revenue", "direct", "reported", None),
        "total_revenue": (230843147, "Total revenue", "direct", "reported", None),
        "general_government_total": (8849918, "Governance & Civic Engagement + General Government Services - Corporate", "derived_sum", "reported", None),
        "public_safety_total": (57713541, "Public Safety", "direct", "reported", None),
        "transportation_total": (37374977, "Mobility including Transit", "direct", "reported", None),
        "environmental_services": (7171104, "Environmental Stewardship", "direct", "reported", None),
        "planning_development": (41478352, "Economic Vitality + Livable Community", "derived_sum", "pending_review", "Broader than the legacy planning/development field."),
        "utility_operations": (19451953, "Water and Wastewater", "direct", "reported", None),
        "total_expenditure": (175310216, "Total expenses", "direct", "reported", None),
        "salaries_benefits": (89589329, "Salaries and benefits", "direct", "reported", None),
        "goods_services_total": (59586719, "Goods and services", "direct", "reported", None),
        "depreciation_object": (25448079, "Amortization", "direct", "reported", None),
        "depreciation_function": (25448079, "Amortization", "direct", "reported", None),
        "interest_expense": (701454, "Interest", "direct", "reported", None),
        "object_other": (-15365, "Other (gain) loss on assets", "direct", "reported", None),
        "total_expenditure_object": (175310216, "Total expenses", "direct", "reported", None),
    },
    "saint-john": {
        "financial_assets_total": (294266216, "Total financial assets", "direct", "reported", None),
        "financial_liabilities_total": (300343424, "Total financial liabilities", "direct", "reported", None),
        "long_term_debt": (157173000, "Long-term debt", "direct", "reported", None),
        "net_financial_assets": (-6077208, "Net debt", "direct", "reported", None),
        "capital_assets": (1012608566, "Tangible capital assets", "direct", "reported", None),
        "total_revenue": (266782013, "Consolidated revenues", "direct", "reported", None),
        "total_expenditure": (227571985, "Consolidated expenses", "direct", "reported", None),
        "depreciation_function": (44532711, "Amortization of tangible capital assets", "direct", "reported", None),
        "depreciation_object": (44532711, "Amortization of tangible capital assets", "direct", "reported", None),
    },
    "st-johns": {
        "financial_assets_total": (237400994, "Financial assets", "direct", "reported", None),
        "financial_liabilities_total": (654811512, "Financial liabilities", "direct", "reported", None),
        "employee_future_benefit_liability": (230519561, "Employee benefits", "direct", "reported", None),
        "long_term_debt": (318754531, "Debenture debt + long-term debt", "derived_sum", "reported", None),
        "net_financial_assets": (-417410518, "Net debt", "direct", "reported", None),
        "capital_assets": (1319111542, "Tangible capital assets", "direct", "reported", None),
        "net_taxes": (251375556, "Taxation + grants in lieu of taxes", "derived_sum", "reported", None),
        "government_grants_total": (46974627, "Grants and transfers", "direct", "reported", None),
        "user_charges": (60421617, "Sales of goods and services", "direct", "reported", None),
        "revenue_other": (27318453, "Other revenue from own sources", "direct", "reported", None),
        "total_revenue": (386090253, "Total revenue", "direct", "reported", None),
        "general_government_total": (59562795, "General government services + fiscal services", "derived_sum", "reported", None),
        "transportation_total": (84485619, "Transportation services", "direct", "reported", None),
        "public_safety_total": (41579640, "Protective services", "direct", "reported", None),
        "environmental_services": (56947838, "Environmental health services", "direct", "reported", None),
        "recreation_culture": (40799424, "Recreation and cultural services", "direct", "reported", None),
        "planning_development": (8261146, "Environmental development services", "direct", "pending_review", "Closest high-level planning/development function."),
        "depreciation_function": (51059663, "Amortization and allowances", "direct", "pending_review", "Source combines amortization with allowances."),
        "total_expenditure": (342696125, "Total expenses", "direct", "reported", None),
    },
    "charlottetown": {
        "financial_assets_total": (44628544, "Total Financial Assets", "direct", "reported", "Official image-heavy statement extracted through targeted OCR."),
        "holdings_council_controlled": (2060350, "Investment in Government Business Enterprise", "direct", "pending_review", "Closest legacy council-controlled-operations concept."),
        "financial_assets_other": (42568194, "Financial assets less Government Business Enterprise investment", "derived_residual", "reported", None),
        "financial_liabilities_total": (177288424, "Total Liabilities", "direct", "reported", None),
        "employee_future_benefit_liability": (7006135, "Sick leave and post-employment benefits", "direct", "reported", None),
        "long_term_debt": (127032013, "Long term debt", "direct", "reported", None),
        "net_financial_assets": (-132659880, "Net Debt", "direct", "reported", None),
        "capital_assets": (372415485, "Tangible capital assets", "direct", "reported", None),
        "net_taxes": (43892492, "Property taxes", "direct", "reported", None),
        "user_charges": (24311889, "Water/sewer + recreation + police services + parking + rentals", "derived_sum", "pending_review", "Selected service/user-charge lines; broader own-source revenues remain in other revenue."),
        "government_grants_total": (55001310, "Operating transfers + capital transfers + municipal capital expenditure grant", "derived_sum", "reported", None),
        "investment_income": (178984, "Interest and other", "direct", "pending_review", "Source combines interest with other minor revenue."),
        "revenue_other": (5426467, "Other revenue / statement adjustments residual", "derived_residual", "pending_review", None),
        "total_revenue": (128811142, "Operating revenue + other revenues/expenditures", "derived_sum", "pending_review", "Full-statement basis retained pending exact legacy aggregation convention."),
        "general_government_total": (9168133, "General government", "direct", "reported", None),
        "public_safety_total": (17913412, "Protective services", "direct", "reported", None),
        "transportation_total": (16136572, "Street maintenance and environment", "direct", "pending_review", "Closest high-level transportation/public-works function."),
        "planning_development": (15779181, "Development, heritage, and other", "direct", "pending_review", "Broader than the legacy planning/development field."),
        "recreation_culture": (10049193, "Parks and recreation", "direct", "reported", None),
        "utility_operations": (8989316, "Water and sewer", "direct", "reported", None),
        "depreciation_function": (12432037, "Amortization of tangible capital assets", "direct", "reported", None),
        "interest_expense": (3467439, "Interest on long term debt", "direct", "reported", None),
        "total_expenditure": (98067919, "Total expenditures", "direct", "reported", None),
    },
    "whitehorse": {
        "financial_assets_total": (125831761, "Total financial assets", "direct", "reported", None),
        "financial_liabilities_total": (56006879, "Total liabilities", "direct", "reported", None),
        "long_term_debt": (12365538, "Debt", "direct", "reported", None),
        "net_financial_assets": (69824882, "Net financial assets", "direct", "reported", None),
        "capital_assets": (471340119, "Tangible capital assets", "direct", "reported", None),
        "net_taxes": (53025323, "Taxes and payments in lieu of taxes", "direct", "reported", None),
        "government_grants_total": (34449828, "Government transfers", "direct", "reported", None),
        "user_charges": (23770171, "Sales of goods and services", "direct", "reported", None),
        "developer_contributions": (716176, "Developers' contributions", "direct", "reported", None),
        "investment_income": (4844110, "Investment income", "direct", "reported", None),
        "revenue_other": (3832711, "Licenses/permits/penalties/fines + other revenues", "derived_sum", "reported", None),
        "total_revenue": (124509092, "Total revenues", "direct", "reported", None),
        "general_government_total": (29882431, "General government services", "direct", "reported", None),
        "public_safety_total": (13812518, "Protective services", "direct", "reported", None),
        "transportation_total": (31585697, "Transportation services", "direct", "reported", None),
        "environmental_services": (21821794, "Environmental services", "direct", "reported", None),
        "health_services": (205529, "Public health services", "direct", "reported", None),
        "planning_development": (4040485, "Community development services", "direct", "pending_review", "Closest high-level planning/development field."),
        "recreation_culture": (19634359, "Recreation and cultural services", "direct", "reported", None),
        "total_expenditure": (120982813, "Total expenses", "direct", "reported", None),
        "salaries_benefits": (60359597, "Salaries and benefits", "direct", "reported", None),
        "goods": (20359942, "Materials and supplies", "direct", "reported", None),
        "contracted_services": (12203521, "Professional services", "direct", "reported", None),
        "grants_object": (2534857, "Community grants", "direct", "reported", None),
        "interest_expense": (412688, "Interest", "direct", "reported", None),
        "depreciation_object": (22058921, "Amortization", "direct", "reported", None),
        "depreciation_function": (22058921, "Amortization", "direct", "reported", None),
        "object_other": (3053287, "Public relations + other", "derived_sum", "reported", None),
        "total_expenditure_object": (120982813, "Total expense by object", "direct", "reported", None),
    },
    "yellowknife": {
        "financial_assets_total": (143024, "Total Financial Assets", "direct", "reported", None),
        "financial_liabilities_total": (84192, "Total Liabilities", "direct", "reported", None),
        "employee_future_benefit_liability": (4473, "Accrued employee benefits", "direct", "reported", None),
        "long_term_debt": (25118, "Debt", "direct", "reported", None),
        "net_financial_assets": (58832, "Net Financial Assets", "direct", "reported", None),
        "capital_assets": (342858, "Tangible capital assets", "direct", "reported", None),
        "net_taxes": (37931, "Municipal taxation", "direct", "reported", None),
        "user_charges": (26092, "User fees and sale of goods", "direct", "reported", None),
        "government_grants_total": (2951, "Grants and transfers", "direct", "reported", None),
        "investment_income": (5230, "Investment income", "direct", "reported", None),
        "revenue_other": (5143, "Land sales + fines/penalties + development levies + franchise fees", "derived_sum", "reported", None),
        "total_revenue": (77347, "Total Revenues", "direct", "reported", None),
        "salaries_benefits": (34910, "Salaries, wages and employee benefits", "direct", "reported", None),
        "contracted_services": (22674, "Contracted and general services", "direct", "reported", None),
        "goods": (1255, "Materials and supplies", "direct", "reported", None),
        "interest_expense": (1163, "Bank/short-term interest + long-term debt interest", "derived_sum", "reported", None),
        "depreciation_object": (15876, "Amortization of tangible assets", "direct", "reported", None),
        "depreciation_function": (15876, "Amortization of tangible assets", "direct", "reported", None),
        "object_other": (13557, "Other audited expense objects", "derived_sum", "reported", None),
        "total_expenditure": (83435, "Total Expenses", "direct", "reported", None),
        "total_expenditure_object": (83435, "Total Expenses", "direct", "reported", None),
    },
    "iqaluit": {
        "financial_assets_total": (97255381, "Total Financial Assets", "direct", "reported", "2024 comparative column in the subsequent audited financial statements."),
        "financial_liabilities_total": (78549490, "Total Liabilities", "direct", "reported", "2024 comparative column in the subsequent audited financial statements."),
        "employee_future_benefit_liability": (1900931, "Post-employment benefits payable", "direct", "reported", None),
        "long_term_debt": (20382297, "Long term debt", "direct", "reported", None),
        "net_financial_assets": (18705891, "Net Financial Assets", "direct", "reported", None),
        "capital_assets": (294591958, "Tangible capital assets", "direct", "reported", None),
        "net_taxes": (25085560, "Taxes and grants in lieu", "direct", "reported", None),
        "user_charges": (26321516, "Water and sewer + sanitation", "derived_sum", "reported", None),
        "government_grants_total": (9048029, "Operating government-transfer schedules", "derived_sum", "reported", None),
        "revenue_other": (10765056, "Other own-source/service revenues", "derived_residual", "reported", None),
        "total_revenue": (71220161, "Total Revenue", "direct", "reported", "2024 actual reported in the City's official subsequent operating statement."),
        "general_government_total": (5628779, "General government", "direct", "reported", None),
        "public_safety_total": (6337612, "Emergency services + by-law enforcement", "derived_sum", "reported", None),
        "transportation_total": (4707306, "Public works and transportation", "direct", "reported", None),
        "environmental_services": (23200365, "Water/sewer + sanitation", "derived_sum", "reported", None),
        "planning_development": (3091880, "Land development + engineering + economic development", "derived_sum", "pending_review", "Closest high-level legacy planning/development grouping."),
        "recreation_culture": (7037251, "Recreational and cultural", "direct", "reported", None),
        "grants_function": (4324500, "Community funding", "direct", "pending_review", "Source function may include transfers broader than the legacy grants field."),
        "depreciation_function": (10808811, "Depreciation", "direct", "reported", None),
        "depreciation_object": (10808811, "Depreciation", "direct", "reported", None),
        "total_expenditure": (65136504, "Total Expenses", "direct", "reported", "2024 actual reported in the City's official subsequent operating statement."),
    },
}

def normalize_amount(slug: str, amount: int | float) -> float:
    return float(amount) if SOURCES[slug]["units"] == "thousands" else float(amount) / 1000.0

def main() -> None:
    municipalities=[]
    observations=[]
    for slug,source in SOURCES.items():
        rows=ROWS[slug]
        municipalities.append({
            "slug":slug,
            "name":source["name"],
            "province":source["province"],
            "sourceUrl":source["url"],
            "sourceLabel":source["label"],
            "sourceUnits":source["units"],
            "observationCount":len(rows),
        })
        for metric,(amount,label,method,status,note) in rows.items():
            observations.append({
                "municipalitySlug":slug,
                "year":2024,
                "metric":metric,
                "valueThousands":normalize_amount(slug,amount),
                "status":status,
                "sourceUrl":source["url"],
                "sourceLabel":source["label"],
                "sourceLocation":label,
                "sourceReportedLabel":label,
                "sourceFieldCodes":[f"statement:{label}"],
                "mappingMethod":method,
                **({"note":note} if note else {}),
            })

    required={
        "financial_assets_total","financial_liabilities_total","long_term_debt",
        "net_financial_assets","capital_assets","total_revenue","total_expenditure",
    }
    by_slug={}
    for row in observations:
        by_slug.setdefault(row["municipalitySlug"],{})[row["metric"]]=row

    failures=[]
    for slug in SOURCES:
        missing=sorted(required-set(by_slug.get(slug,{})))
        if missing:
            failures.append(f"{slug}: missing core metrics {missing}")
            continue
        vals=by_slug[slug]
        assets=vals["financial_assets_total"]["valueThousands"]
        liabilities=vals["financial_liabilities_total"]["valueThousands"]
        net=vals["net_financial_assets"]["valueThousands"]
        if abs((assets-liabilities)-net) > 0.01:
            failures.append(
                f"{slug}: financial position does not reconcile: "
                f"{assets} - {liabilities} != {net}"
            )

    seen=set()
    duplicates=[]
    for row in observations:
        key=(row["municipalitySlug"],row["metric"])
        if key in seen:
            duplicates.append(key)
        seen.add(key)
    if duplicates:
        failures.append(f"duplicate municipality/metric keys: {duplicates}")

    if failures:
        raise RuntimeError("2024 final-ten QA failed:\n" + "\n".join(failures))

    doc={
        "schemaVersion":1,
        "year":2024,
        "sourceType":"official_audited_statements",
        "municipalities":municipalities,
        "observations":observations,
        "mapping":{
            "name":"LGPI Atlantic and territorial audited statements 2024",
            "version":1,
            "notes":[
                "Core financial-position, revenue and expenditure fields are required for every municipality.",
                "Values reported in dollars are normalized to thousands of Canadian dollars; Halifax and Yellowknife already report in thousands.",
                "Image-heavy statements were extracted with targeted OCR; subsequent audited comparative columns are used where a municipal PDF cannot be reliably machine-fetched.",
                "Derived mappings preserve source labels and uncertain legacy compatibility is marked pending_review.",
                "No missing source value is converted to numeric zero.",
            ],
        },
        "stats":{
            "municipalityCount":len(municipalities),
            "municipalitiesWithObservations":len({x["municipalitySlug"] for x in observations}),
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
