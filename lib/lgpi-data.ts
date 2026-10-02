import alberta2023 from "@/data/2023/alberta.json";
import bc2023 from "@/data/2023/bc.json";
import ontario2023 from "@/data/2023/ontario.json";
import quebec2023 from "@/data/2023/quebec.json";
import prairies2023 from "@/data/2023/prairies.json";
import atlanticTerritories2023 from "@/data/2023/atlantic_territories.json";

export const REPORT_URL =
  "https://frontiercentre.org/wp-content/uploads/PR148_LGPI2025_JN0525_F1.pdf";

export const TARGET_MUNICIPALITIES = 99;
export const VERIFIED_TRANSPARENCY_TOTALS = 80;
export const VERIFIED_COMPONENT_BREAKDOWNS = 73;
export const QUEBEC_UNSCORED = 19;

export const provinceNames = {
  AB: "Alberta",
  BC: "British Columbia",
  MB: "Manitoba",
  NB: "New Brunswick",
  NL: "Newfoundland and Labrador",
  NS: "Nova Scotia",
  NT: "Northwest Territories",
  NU: "Nunavut",
  ON: "Ontario",
  PE: "Prince Edward Island",
  QC: "Quebec",
  SK: "Saskatchewan",
  YT: "Yukon",
} as const;

export type ProvinceCode = keyof typeof provinceNames;

export const transparencyCriteria = [
  { key: "timeliness", label: "Timeliness of audit opinion", max: 4 },
  { key: "accountingAward", label: "Receipt of accounting award", max: 2 },
  { key: "commentary", label: "Additional commentary and statistics", max: 8 },
  { key: "capitalReported", label: "Capital assets reported", max: 8 },
  { key: "capitalDepFunded", label: "Capital assets depreciated / funded", max: 4 },
  { key: "expenditureByObject", label: "Expenditures by object reported", max: 1 },
  { key: "goodsSeparate", label: "Goods / contracted services separately identified", max: 1 },
  { key: "depreciationRecorded", label: "Depreciation recorded", max: 1 },
  { key: "lineItemsDefined", label: "Expenditure line items defined", max: 2 },
  { key: "historicalTrends", label: "Historical trend statistics provided", max: 2 },
] as const;

type RawTransparency = [
  slug: string,
  name: string,
  province: ProvinceCode,
  components: number[] | null,
  score: number,
];

const transparencyRaw: RawTransparency[] = [
  ["abbotsford","Abbotsford","BC",[3,0,8,8,4,1,0,1,2,1],28],
  ["burnaby","Burnaby","BC",[3,2,8,8,4,1,1,1,2,2],32],
  ["chilliwack","Chilliwack","BC",[3,0,5,8,4,0,0,1,2,0],23],
  ["coquitlam","Coquitlam","BC",[3,2,8,8,4,1,1,1,2,2],32],
  ["delta","Delta","BC",[2,0,8,8,4,1,1,1,2,2],29],
  ["kamloops","Kamloops","BC",[2,0,8,8,4,1,1,1,2,2],29],
  ["kelowna","Kelowna","BC",[3,2,8,8,4,1,1,1,2,2],32],
  ["langley-township","Langley Township","BC",[2,0,7,8,4,1,1,0,1,2],26],
  ["maple-ridge","Maple Ridge","BC",[3,2,7,8,4,1,1,1,2,2],31],
  ["nanaimo","Nanaimo","BC",[3,0,8,8,4,1,1,1,1,1],28],
  ["new-westminster","New Westminster","BC",[2,0,7,8,4,1,1,1,2,2],28],
  ["port-coquitlam","Port Coquitlam","BC",[2,2,8,8,4,1,1,1,2,2],31],
  ["prince-george","Prince George","BC",[2,0,7,8,4,1,1,1,2,0],26],
  ["richmond","Richmond","BC",[2,2,8,8,4,1,1,1,2,2],31],
  ["saanich","Saanich","BC",[2,2,8,8,4,1,0,1,2,2],30],
  ["vancouver","Vancouver","BC",[3,0,8,8,4,1,1,1,2,2],30],
  ["victoria","Victoria","BC",[3,2,8,8,4,1,0,1,2,2],31],

  ["calgary","Calgary","AB",[3,0,8,8,4,1,1,1,2,2],30],
  ["edmonton","Edmonton","AB",[3,2,8,8,4,1,1,1,2,2],32],
  ["grande-prairie","Grande Prairie","AB",[2,2,7,4,4,1,1,1,2,0],24],
  ["lethbridge","Lethbridge","AB",[3,2,7,4,4,1,1,1,2,2],27],
  ["medicine-hat","Medicine Hat","AB",[3,0,6,4,4,1,0,0,1,1],20],
  ["red-deer","Red Deer","AB",[3,0,8,4,4,1,1,1,2,1],25],
  ["st-albert","St. Albert","AB",[3,2,8,4,4,1,1,1,2,2],28],
  ["strathcona-county","Strathcona County","AB",[3,0,6,4,4,1,1,1,0,0],20],
  ["wood-buffalo","Wood Buffalo","AB",[3,2,8,4,4,1,1,1,2,2],28],
  ["regina","Regina","SK",[2,2,4,8,2,1,1,1,2,2],25],
  ["saskatoon","Saskatoon","SK",[2,2,7,8,4,1,1,1,2,2],30],
  ["winnipeg","Winnipeg","MB",[2,2,8,8,4,1,0,1,2,2],30],

  ["ajax","Ajax","ON",[2,0,6,8,4,1,1,1,2,0],25],
  ["aurora","Aurora","ON",[1,0,7,8,4,1,1,1,2,0],25],
  ["barrie","Barrie","ON",[2,0,7,8,4,1,1,1,2,0],26],
  ["brampton","Brampton","ON",[2,2,8,8,4,1,1,1,2,2],31],
  ["brantford","Brantford","ON",[2,0,8,8,4,1,1,1,2,2],29],
  ["burlington","Burlington","ON",[1,0,7,8,4,1,1,1,2,1],26],
  ["caledon","Caledon","ON",[0,0,8,8,4,1,1,1,2,2],27],
  ["cambridge","Cambridge","ON",[2,2,8,8,4,1,0,1,1,2],29],
  ["chatham-kent","Chatham-Kent","ON",[1,0,7,8,4,0,0,0,2,0],22],
  ["clarington","Clarington","ON",[0,0,0,0,0,0,0,0,0,0],0],
  ["greater-sudbury","Greater Sudbury","ON",[1,0,8,8,4,1,1,1,2,1],27],
  ["guelph","Guelph","ON",[1,0,7,8,4,1,1,1,2,1],26],
  ["halton-hills","Halton Hills","ON",[1,0,7,8,4,1,1,1,2,1],26],
  ["hamilton","Hamilton","ON",[0,0,0,0,0,0,0,0,0,0],0],
  ["kawartha-lakes","Kawartha Lakes","ON",[2,0,8,8,4,1,1,1,1,0],26],
  ["kingston","Kingston","ON",[1,0,8,8,4,1,1,1,1,0],25],
  ["kitchener","Kitchener","ON",[1,2,8,8,4,1,1,1,2,2],30],
  ["london","London","ON",[1,0,7,8,4,1,1,1,2,1],26],
  ["markham","Markham","ON",[3,2,8,8,4,1,1,1,2,2],32],
  ["milton","Milton","ON",[2,2,8,8,4,1,1,1,2,2],31],
  ["mississauga","Mississauga","ON",[2,2,8,8,4,1,1,1,2,2],31],
  ["newmarket","Newmarket","ON",[2,0,7,8,4,1,1,1,2,0],26],
  ["niagara-falls","Niagara Falls","ON",[2,2,7,8,4,1,1,1,2,0],28],
  ["norfolk-county","Norfolk County","ON",[1,0,8,8,4,1,1,1,2,0],26],
  ["north-bay","North Bay","ON",[0,0,7,8,4,1,1,1,2,2],26],
  ["oakville","Oakville","ON",[2,0,8,8,4,1,1,1,2,2],29],
  ["oshawa","Oshawa","ON",[2,0,7,8,4,1,1,1,2,0],26],
  ["ottawa","Ottawa","ON",[2,0,8,8,4,1,1,1,2,2],29],
  ["peterborough","Peterborough","ON",[0,0,7,8,4,1,1,1,2,2],26],
  ["pickering","Pickering","ON",[0,0,6,8,4,1,1,1,2,1],24],
  ["richmond-hill","Richmond Hill","ON",[1,0,6,8,4,1,1,1,2,0],24],
  ["st-catharines","St. Catharines","ON",[0,0,6,8,4,1,1,1,2,0],23],
  ["sarnia","Sarnia","ON",[2,0,6,8,4,1,1,1,2,0],25],
  ["sault-ste-marie","Sault Ste. Marie","ON",[1,0,6,8,4,1,1,1,2,0],24],
  ["thunder-bay","Thunder Bay","ON",[1,0,6,8,4,1,1,1,2,0],24],
  ["toronto","Toronto","ON",[1,2,8,8,4,1,1,1,2,2],30],
  ["vaughan","Vaughan","ON",[2,0,6,8,4,1,0,1,1,0],23],
  ["waterloo","Waterloo","ON",[2,0,6,8,4,1,0,1,1,0],23],
  ["welland","Welland","ON",[1,0,6,8,4,1,0,1,2,0],23],
  ["whitby","Whitby","ON",[2,0,5,8,4,1,1,1,1,0],23],
  ["windsor","Windsor","ON",[1,0,6,8,4,0,0,1,2,0],22],

  ["moncton","Moncton","NB",null,27],
  ["fredericton","Fredericton","NB",null,24],
  ["saint-john","Saint John","NB",null,24],
  ["halifax","Halifax","NS",null,26],
  ["st-johns","St. John's","NL",null,25],
  ["charlottetown","Charlottetown","PE",null,20],
  ["cape-breton","Cape Breton","NS",null,23],

  ["whitehorse","Whitehorse","YT",[2,2,8,8,4,1,1,1,2,2],31],
  ["yellowknife","Yellowknife","NT",[3,0,7,8,4,1,1,1,2,2],29],
  ["iqaluit","Iqaluit","NU",[1,0,6,6,4,1,1,1,1,0],21],
];

export type TransparencyRecord = {
  slug: string;
  name: string;
  province: ProvinceCode;
  provinceName: string;
  year: 2023;
  score: number;
  components: number[] | null;
  verification: "report-table-total" | "report-table-components";
  sourceUrl: string;
  sourceLabel: string;
};

export const transparency2023: TransparencyRecord[] = transparencyRaw.map(
  ([slug, name, province, components, score]) => ({
    slug,
    name,
    province,
    provinceName: provinceNames[province],
    year: 2023,
    score,
    components,
    verification: components ? "report-table-components" : "report-table-total",
    sourceUrl: REPORT_URL,
    sourceLabel: "Frontier Centre — Local Government Performance Index 2025 (2023 statements)",
  }),
);

export type MunicipalityProfileRecord = {
  slug: string;
  name: string;
  province: ProvinceCode;
  provinceName: string;
  year: 2023;
  score: number | null;
  components: number[] | null;
  transparencyPublished: boolean;
  sourceUrl: string | null;
  sourceLabel: string | null;
};

export const municipalities2023: MunicipalityProfileRecord[] = [
  ...transparency2023.map((record) => ({
    slug: record.slug,
    name: record.name,
    province: record.province,
    provinceName: record.provinceName,
    year: 2023 as const,
    score: record.score,
    components: record.components,
    transparencyPublished: true,
    sourceUrl: record.sourceUrl,
    sourceLabel: record.sourceLabel,
  })),
  ...quebec2023.municipalities.map((record) => ({
    slug: record.slug,
    name: record.name,
    province: "QC" as const,
    provinceName: provinceNames.QC,
    year: 2023 as const,
    score: null,
    components: null,
    transparencyPublished: false,
    sourceUrl: null,
    sourceLabel: null,
  })),
].sort((a, b) => a.name.localeCompare(b.name));

export function getMunicipality(slug: string) {
  return municipalities2023.find((record) => record.slug === slug);
}

export function getComponentRows(record: { components: number[] | null }) {
  if (!record.components) return [];
  return transparencyCriteria.map((criterion, index) => ({
    ...criterion,
    value: record.components?.[index] ?? null,
  }));
}

export const sourceDiscrepancies = [
  {
    municipality: "Kawartha Lakes",
    issue:
      "Frontier's web release describes Kawartha Lakes as receiving a zero, while the detailed Ontario report table lists 26/33. This reconstruction uses the detailed table value pending editorial confirmation.",
  },
  {
    municipality: "Chatham-Kent",
    issue:
      "An Ontario media-release summary reports 23/33, while the detailed Ontario report table sums to and lists 22/33. This reconstruction uses the detailed table value pending editorial confirmation.",
  },
];

export type FinancialSection =
  | "Financial position"
  | "Revenue"
  | "Expenditure"
  | "Expenditures by object";

export type MetricDefinition = {
  key: string;
  label: string;
  section: FinancialSection;
};

export const metricCatalog: MetricDefinition[] = [
  { key: "capital_assets", label: "Capital assets", section: "Financial position" },
  { key: "financial_assets_total", label: "Financial assets total", section: "Financial position" },
  { key: "holdings_council_controlled", label: "Holdings in council controlled operations", section: "Financial position" },
  { key: "financial_assets_other", label: "Financial assets other", section: "Financial position" },
  { key: "long_term_debt", label: "Long-term debt", section: "Financial position" },
  { key: "employee_future_benefit_liability", label: "Employee future benefit liability", section: "Financial position" },
  { key: "financial_liabilities_total", label: "Financial liabilities total", section: "Financial position" },
  { key: "net_financial_assets", label: "Financial assets less financial liabilities", section: "Financial position" },

  { key: "developer_contributions", label: "Developer contributions", section: "Revenue" },
  { key: "investment_income", label: "Investment income", section: "Revenue" },
  { key: "revenue_other", label: "Other", section: "Revenue" },
  { key: "net_taxes", label: "Net taxes", section: "Revenue" },
  { key: "government_grants_total", label: "Total grants from other governments", section: "Revenue" },
  { key: "federal_grants", label: "Federal grants", section: "Revenue" },
  { key: "provincial_grants", label: "Provincial grants", section: "Revenue" },
  { key: "remitted_second_tier", label: "Remitted to second-tier local government", section: "Revenue" },
  { key: "user_charges", label: "User charges", section: "Revenue" },
  { key: "total_revenue", label: "Total revenue", section: "Revenue" },

  { key: "civic_corporations", label: "Civic corporations", section: "Expenditure" },
  { key: "grants_function", label: "Grants", section: "Expenditure" },
  { key: "expenditure_other", label: "Other", section: "Expenditure" },
  { key: "recreation_culture", label: "Recreation and culture", section: "Expenditure" },
  { key: "social_services_total", label: "Total social services", section: "Expenditure" },
  { key: "health_services", label: "Health services", section: "Expenditure" },
  { key: "social_family_services", label: "Social and family services", section: "Expenditure" },
  { key: "social_housing", label: "Social housing", section: "Expenditure" },
  { key: "social_other", label: "Miscellaneous social-program expenditure", section: "Expenditure" },
  { key: "general_government_total", label: "General government total", section: "Expenditure" },
  { key: "democracy_costs", label: "Democracy costs", section: "Expenditure" },
  { key: "general_government", label: "General government", section: "Expenditure" },
  { key: "non_core_total", label: "Total non-core expenditure", section: "Expenditure" },
  { key: "environmental_services", label: "Environmental services", section: "Expenditure" },
  { key: "planning_development", label: "Planning and development", section: "Expenditure" },
  { key: "public_works", label: "Public works", section: "Expenditure" },
  { key: "utility_operations", label: "Utility operations", section: "Expenditure" },
  { key: "solid_waste", label: "Solid-waste disposal", section: "Expenditure" },
  { key: "public_safety_total", label: "Public safety total", section: "Expenditure" },
  { key: "fire", label: "Fire", section: "Expenditure" },
  { key: "police", label: "Police", section: "Expenditure" },
  { key: "public_safety_other", label: "Miscellaneous public-safety items", section: "Expenditure" },
  { key: "transit", label: "Transit", section: "Expenditure" },
  { key: "transportation", label: "Transportation", section: "Expenditure" },
  { key: "transportation_total", label: "Total transportation-related items", section: "Expenditure" },
  { key: "depreciation_function", label: "Depreciation", section: "Expenditure" },
  { key: "core_expenditure_total", label: "Total core expenditure", section: "Expenditure" },
  { key: "total_expenditure", label: "Total expenditure", section: "Expenditure" },

  { key: "grants_object", label: "Grants", section: "Expenditures by object" },
  { key: "interest_expense", label: "Interest expense", section: "Expenditures by object" },
  { key: "object_other", label: "Other", section: "Expenditures by object" },
  { key: "salaries_benefits", label: "Salaries and benefits", section: "Expenditures by object" },
  { key: "goods_services_total", label: "Goods and services total", section: "Expenditures by object" },
  { key: "contracted_services", label: "Contracted services", section: "Expenditures by object" },
  { key: "goods", label: "Goods", section: "Expenditures by object" },
  { key: "goods_services_other", label: "Miscellaneous goods and services", section: "Expenditures by object" },
  { key: "depreciation_object", label: "Depreciation", section: "Expenditures by object" },
  { key: "total_expenditure_object", label: "Total expenditure by object", section: "Expenditures by object" },
];

export type ObservationStatus =
  | "reported"
  | "pending_review"
  | "not_reported"
  | "not_applicable"
  | "source_unavailable";

export type FinancialObservation = {
  municipalitySlug: string;
  year: 2023;
  metric: string;
  valueThousands: number | null;
  status: ObservationStatus;
  sourceUrl: string;
  sourceLabel: string;
  sourceLocation: string;
  sourceReportedLabel?: string;
  sourceFieldCodes?: string[];
  mappingMethod?: "direct" | "derived_sum" | "derived_residual";
  note?: string;
};

const albertaFinancial2023 =
  alberta2023.observations as unknown as FinancialObservation[];
const bcFinancial2023 =
  bc2023.observations as unknown as FinancialObservation[];
const ontarioFinancial2023 =
  ontario2023.observations as unknown as FinancialObservation[];
const quebecFinancial2023 =
  quebec2023.observations as unknown as FinancialObservation[];
const prairiesFinancial2023 =
  prairies2023.observations as unknown as FinancialObservation[];
const atlanticTerritoriesFinancial2023 =
  atlanticTerritories2023.observations as unknown as FinancialObservation[];

export const financial2023: FinancialObservation[] = [
  ...albertaFinancial2023,
  ...bcFinancial2023,
  ...ontarioFinancial2023,
  ...quebecFinancial2023,
  ...prairiesFinancial2023,
  ...atlanticTerritoriesFinancial2023,
];

export const alberta2023MunicipalityContext = alberta2023.municipalities;
export const bc2023MunicipalityContext = bc2023.municipalities;
export const ontario2023MunicipalityContext = ontario2023.municipalities;
export const quebec2023MunicipalityContext = quebec2023.municipalities;
export const ontario2023SourceUnavailable = ontario2023.sourceUnavailableMunicipalities;

export function getAlbertaMunicipalityContext(slug: string) {
  return alberta2023MunicipalityContext.find((record) => record.slug === slug);
}

export function getBcMunicipalityContext(slug: string) {
  return bc2023MunicipalityContext.find((record) => record.slug === slug);
}

export function getOntarioMunicipalityContext(slug: string) {
  return ontario2023MunicipalityContext.find((record) => record.slug === slug);
}

export function getFinancialSourceUnavailable(slug: string) {
  return ontario2023SourceUnavailable.find((record) => record.slug === slug);
}

export function getFinancialObservations(slug: string) {
  return financial2023.filter((observation) => observation.municipalitySlug === slug);
}

export function getMetricDefinition(key: string) {
  return metricCatalog.find((metric) => metric.key === key);
}

export function formatThousands(value: number | null) {
  if (value === null) return "—";
  return new Intl.NumberFormat("en-CA", {
    style: "currency",
    currency: "CAD",
    maximumFractionDigits: 0,
  }).format(value * 1000);
}

export const coverageByProvince = Object.entries(provinceNames).map(([province, name]) => {
  const verified = transparency2023.filter((record) => record.province === province).length;
  const expected = province === "QC" ? QUEBEC_UNSCORED : verified;
  return { province: province as ProvinceCode, name, verified, expected };
});
