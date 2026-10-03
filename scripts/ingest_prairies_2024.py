#!/usr/bin/env python3
"""Generate 2024 Prairie LGPI observations from official audited annual reports."""

from __future__ import annotations
import json
from pathlib import Path

OUTPUT=Path("data/2024/prairies.json")

SOURCES={
 "regina":("Regina","SK","https://openregina.ca/dataset/5e011351-3612-4a51-919d-914dcef52ffb/resource/f84fc149-0569-4a6b-8fc2-62c2ed18a138/download/cor-2024-annual-report.pdf","City of Regina 2024 Annual Report"),
 "saskatoon":("Saskatoon","SK","https://www.saskatoon.ca/sites/default/files/documents/asset-financial-management/COS_2024-AnnualReport-Aug28-F.pdf","City of Saskatoon 2024 Annual Report"),
 "winnipeg":("Winnipeg","MB","https://legacy.winnipeg.ca/finance/files/2024AnnualReport.pdf","City of Winnipeg 2024 Annual Financial Report"),
}

# values are already $000
ROWS={
 "regina":{
  "financial_assets_total":(658155,"Financial assets total","derived","Derived from audited financial liabilities less net financial debt."),
  "financial_liabilities_total":(794928,"Financial liabilities","direct",None),
  "net_financial_assets":(-136773,"Net financial debt","direct",None),
  "capital_assets":(2947916,"Tangible capital assets - net book value","direct",None),
  "long_term_debt":(440006,"Long-term debt","direct",None),
  "employee_future_benefit_liability":(98615,"Employee benefit obligations","direct",None),
  "net_taxes":(332414,"Taxation","direct",None),
  "user_charges":(283936,"Fees and charges","direct",None),
  "government_grants_total":(145115,"Government transfers","direct",None),
  "investment_income":(15964,"Interest on investments","direct",None),
  "developer_contributions":(17703,"Servicing agreement fees + contribution of tangible capital assets","derived",None),
  "revenue_other":(101962,"Other consolidated revenue categories","derived","Residual of total revenue after LGPI headline categories."),
  "total_revenue":(897094,"Total consolidated revenue","direct",None),
  "recreation_culture":(152081,"Parks, recreation and community services","direct",None),
  "police":(125247,"Police","direct",None),
  "fire":(57913,"Fire","direct",None),
  "public_safety_total":(183160,"Police + Fire","pending","Other protective services are not separately identified in the high-level statement."),
  "general_government_total":(105647,"Legislative and administrative services","direct",None),
  "environmental_services":(152349,"Water, wastewater and drainage + waste collection and disposal","derived",None),
  "transportation":(95979,"Roads and traffic","direct",None),
  "transit":(51268,"Transit","direct",None),
  "transportation_total":(147247,"Roads and traffic + Transit","derived",None),
  "grants_function":(16310,"Grants","direct",None),
  "planning_development":(19750,"Planning and development","direct",None),
  "total_expenditure":(776544,"Total consolidated expenses","direct",None),
  "salaries_benefits":(361380,"Wages and benefits","direct",None),
  "goods":(76304,"Materials, supplies and other goods","direct",None),
  "contracted_services":(167337,"Contracted and general services","direct",None),
  "goods_services_other":(21585,"Utilities","direct",None),
  "goods_services_total":(265226,"Materials + contracted services + utilities","derived",None),
  "grants_object":(17279,"Transfer payments/grants","direct",None),
  "interest_expense":(15023,"Interest and bank charges","direct",None),
  "depreciation_object":(114339,"Amortization of tangible assets","direct",None),
  "depreciation_function":(114339,"Amortization of tangible assets","direct",None),
  "object_other":(3297,"Accretion","direct",None),
  "total_expenditure_object":(776544,"Total expenses by object","direct",None),
 },
 "saskatoon":{
  "financial_assets_total":(1053048,"Total Financial Assets","direct",None),
  "financial_liabilities_total":(606572,"Total Financial Liabilities","direct",None),
  "net_financial_assets":(446476,"Total Net Financial Assets","direct",None),
  "capital_assets":(4991002,"Tangible Capital Assets","direct",None),
  "long_term_debt":(296878,"Long-Term Debt","direct",None),
  "employee_future_benefit_liability":(44716,"Employee Benefits Payable","pending","Source label is broader than the legacy employee-future-benefit field."),
  "net_taxes":(347753,"Taxation","direct",None),
  "user_charges":(497486,"User Fees","direct",None),
  "government_grants_total":(146203,"Government Transfers - Capital + Operating","derived",None),
  "investment_income":(25548,"Investment Income","direct",None),
  "developer_contributions":(181624,"Contributions from Developers & Others - Capital + Operating","derived",None),
  "revenue_other":(110874,"Franchise Fees + General Revenues + Grants in lieu","derived",None),
  "total_revenue":(1309488,"Total Revenues","direct",None),
  "general_government_total":(77967,"Corporate Asset Management + Corporate Governance & Finance + Taxation and General Revenues","derived",None),
  "public_safety_total":(199661,"Saskatoon Fire + Saskatoon Police Service","derived",None),
  "fire":(62208,"Saskatoon Fire","direct",None),
  "police":(137453,"Saskatoon Police Service","direct",None),
  "transportation_total":(204072,"Transportation","direct",None),
  "environmental_services":(36983,"Environmental Health","direct",None),
  "utility_operations":(243414,"Utilities","direct",None),
  "planning_development":(68997,"Land Development + Urban Planning and Development","derived",None),
  "recreation_culture":(144189,"Arts, Culture and Events Venues + Recreation and Culture + Saskatoon Public Library","derived",None),
  "total_expenditure":(1011078,"Total Expenses","direct",None),
  "salaries_benefits":(422323,"Wages and Benefits","direct",None),
  "contracted_services":(196079,"Contracted and General Services","direct",None),
  "goods":(90639,"Material, Goods and Supplies","direct",None),
  "goods_services_other":(127412,"Heating, Lighting, Power, Water and Telephone","direct",None),
  "goods_services_total":(414130,"Contracted services + utilities + goods","derived",None),
  "grants_object":(12354,"Donations, Grants and Subsidies","direct",None),
  "interest_expense":(11839,"Finance Charges","direct",None),
  "depreciation_object":(162498,"Amortization","direct",None),
  "depreciation_function":(162498,"Amortization","direct",None),
  "object_other":(-12066,"Accretion (Recovery)","direct",None),
  "total_expenditure_object":(1011078,"Total","direct",None),
 },
 "winnipeg":{
  "financial_assets_total":(1906577,"Financial assets","direct",None),
  "holdings_council_controlled":(20865,"Investment in business partnerships","pending","Closest legacy council-controlled-operations concept."),
  "financial_assets_other":(1885712,"Financial assets less investment in business partnerships","derived",None),
  "financial_liabilities_total":(3174980,"Liabilities","direct",None),
  "net_financial_assets":(-1268403,"Net financial liabilities","direct",None),
  "capital_assets":(8793696,"Tangible capital assets","direct",None),
  "long_term_debt":(1629027,"Debt","direct",None),
  "employee_future_benefit_liability":(297666,"Employee benefits obligations","direct",None),
  "net_taxes":(915450,"Taxation","direct",None),
  "user_charges":(735846,"Sales of services and regulatory fees","direct",None),
  "government_grants_total":(471602,"Government transfers + capital-related transfers","derived",None),
  "investment_income":(75358,"Investment income","direct",None),
  "developer_contributions":(90966,"Developer contributions-in-kind related to capital","pending","Direct capital developer contribution."),
  "revenue_other":(60133,"Land sales/other + other capital contributions","derived",None),
  "total_revenue":(2349355,"Operating revenues + capital revenues","derived",None),
  "general_government_total":(211253,"Finance and administration + General government","derived",None),
  "utility_operations":(581996,"Utility operations","direct",None),
  "public_works":(384980,"Public works","direct",None),
  "planning_development":(137196,"Property and development","direct",None),
  "civic_corporations":(111082,"Civic corporations","direct",None),
  "total_expenditure":(2077723,"Total Expenses","direct",None),
  "salaries_benefits":(1081361,"Salaries and benefits","direct",None),
  "goods_services_total":(558363,"Goods and services","direct",None),
  "depreciation_object":(316063,"Amortization of tangible capital assets","direct",None),
  "depreciation_function":(316063,"Amortization of tangible capital assets","direct",None),
  "interest_expense":(78669,"Interest","direct",None),
  "object_other":(43267,"Other expenses","direct",None),
  "total_expenditure_object":(2077723,"Total expenses by object","direct",None),
 },
}

def main():
 observations=[]; municipalities=[]
 for slug,(name,province,url,label) in SOURCES.items():
  for metric,(value,source_label,kind,note) in ROWS[slug].items():
   observations.append({
    "municipalitySlug":slug,"year":2024,"metric":metric,"valueThousands":value,
    "status":"pending_review" if kind=="pending" else "reported",
    "sourceUrl":url,"sourceLabel":label,"sourceLocation":source_label,
    "sourceReportedLabel":source_label,"sourceFieldCodes":[f"statement:{source_label}"],
    "mappingMethod":"direct" if kind in {"direct","pending"} else "derived_sum",
    **({"note":note} if note else {})
   })
  municipalities.append({"slug":slug,"name":name,"province":province,"sourceUrl":url,"sourceLabel":label,"observationCount":len(ROWS[slug])})
 doc={"schemaVersion":1,"year":2024,"sourceType":"audited_annual_reports","municipalities":municipalities,"observations":observations,
      "stats":{"municipalityCount":len(municipalities),"observationCount":len(observations),"reportedCount":sum(x["status"]=="reported" for x in observations),"pendingReviewCount":sum(x["status"]=="pending_review" for x in observations)}}
 OUTPUT.parent.mkdir(parents=True,exist_ok=True);OUTPUT.write_text(json.dumps(doc,indent=2,ensure_ascii=False)+"\n")
 print(f"Wrote {OUTPUT}: {len(municipalities)} municipalities, {len(observations)} observations")
if __name__=="__main__": main()
