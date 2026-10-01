# LGPI 2023 reconstruction status

Last reconstruction pass: 2026-10-01.

## What is loaded

- Target universe: 99 municipalities.
- Verified 2023 transparency totals: 80.
- Verified component-level transparency records: 73.
- Published total-only Atlantic records: 7.
- Quebec records pending detailed-table extraction: 19.
- Legacy financial field catalogue: reconstructed from the public LGPI site.
- Official 2023 financial seed observations: Calgary, Edmonton, Toronto.

## Transparency coverage

Component tables are loaded for:

- British Columbia: 17
- Alberta: 9
- Saskatchewan: 2
- Manitoba: 1
- Ontario: 41
- Yukon: 1
- Northwest Territories: 1
- Nunavut: 1

Published totals are loaded for:

- New Brunswick: 3
- Nova Scotia: 2
- Newfoundland and Labrador: 1
- Prince Edward Island: 1

Quebec is intentionally absent from the score dataset until the detailed table is independently recovered. Pending does not mean zero.

## Source discrepancy register

### Kawartha Lakes

The Frontier web release describes Kawartha Lakes as receiving a zero, while the detailed Ontario table in the LGPI report lists 26/33 with components that sum to 26. The reconstruction uses the detailed table value provisionally and flags it for editorial confirmation.

### Chatham-Kent

An Ontario media-release summary reports 23/33, while the detailed Ontario table lists components summing to 22 and a total of 22. The reconstruction uses 22 provisionally and flags it for editorial confirmation.

## Financial-data status

The financial ingestion layer is deliberately stricter than a visual mock-up. Values are only attached to a legacy LGPI metric where the source concept can be mapped without silently changing the definition.

Current seed:

- Calgary: capital assets, long-term debt, net taxes, investment income, developer contributions (pending aggregation review), total expenditure.
- Edmonton: total financial assets and total financial liabilities.
- Toronto: long-term debt.

Next financial-data tranche should prioritize the remaining official 2023 annual financial statements and provincial structured returns, then add household denominators and provincial-average calculations only after denominator rules are confirmed.
