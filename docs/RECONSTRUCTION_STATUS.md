# LGPI 2023–2024 reconstruction status

Last reconstruction pass: 2026-10-01.

## What is loaded

- Target universe: 99 municipalities.
- Published 2023 transparency scores loaded: 80 of 80 scores reported outside Quebec.
- Verified component-level transparency records: 73.
- Published total-only Atlantic records: 7.
- Quebec municipalities without published transparency scores in this edition: 19 (the report explicitly omits Quebec scores).
- Legacy financial field catalogue: reconstructed from the public LGPI site.
- Alberta 2023 bulk financial import: 9 LGPI municipalities, 414 source-backed observations, generated from the official FIR/SIR workbook.
- British Columbia 2023 bulk financial import: 17 LGPI municipalities, 510 source-backed observations, generated from standardized provincial schedules.
- Ontario 2023 bulk financial import: 40 source-available LGPI municipalities, 1,160 source-backed observations; Hamilton is explicitly source-unavailable in the provincial FIR.
- Quebec 2023 bulk financial import: all 19 LGPI municipalities, 589 source-backed observations from the MAMH audited financial-report open-data workbook. Quebec remains transparency-unscored because the published LGPI edition omitted Quebec scoring.
- Prairie audited-report import: Regina, Saskatoon and Winnipeg, 85 source-backed observations validated against cited PDF pages.
- Atlantic and territorial audited-statement import: Halifax, Cape Breton, Moncton, Fredericton, Saint John, St. John's, Charlottetown, Whitehorse, Yellowknife and Iqaluit; 223 source-backed observations.

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

Quebec is intentionally absent from the score dataset because the 2025 LGPI report explicitly says its current report omits transparency scores for Quebec. These municipalities are unscored in the publication, not zero-score records. Any future Quebec scoring produced by this repository must be identified as an independent reconstruction rather than a transcribed published result.

## Source discrepancy register

### Kawartha Lakes

The Frontier web release describes Kawartha Lakes as receiving a zero, while the detailed Ontario table in the LGPI report lists 26/33 with components that sum to 26. The reconstruction uses the detailed table value provisionally and flags it for editorial confirmation.

### Chatham-Kent

An Ontario media-release summary reports 23/33, while the detailed Ontario table lists components summing to 22 and a total of 22. The reconstruction uses 22 provisionally and flags it for editorial confirmation.

## Financial-data status

The financial ingestion layer is deliberately stricter than a visual mock-up. Values are only attached to a legacy LGPI metric where the source concept can be mapped without silently changing the definition.

Current financial coverage:

- Alberta: all 9 LGPI municipalities are bulk-imported from the Government of Alberta 2023 Financial and Statistical Data workbook. The importer emits 414 observations with exact source field codes and mapping methods.
- Calgary is the Alberta control municipality: headline FIR-derived mappings reconcile against its audited 2023 Annual Financial Report before the importer is allowed to emit data.
- British Columbia: all 17 LGPI municipalities are bulk-imported from provincial Schedules 201, 301, 302, 304, 401, 402, 502 and 601.1. The importer emits 510 observations and requires financial assets, liabilities, net financial assets, non-financial assets and total debt to reconcile across schedules before publication. Langley Township is selected by municipal type so it cannot be confused with the City of Langley.
- Ontario: 40 of 41 LGPI municipalities are imported from official 2023 FIR Schedules 02, 10, 40, 42, 51, 70 and 74. The importer emits 1,160 observations, cross-checks tangible capital assets between Schedules 70 and 51, and marks ambiguous legacy mappings as pending review. Hamilton is preserved as source_unavailable because Ontario lists its 2023 FIR as not available.
- Quebec: all 19 municipalities are imported from MAMH's 2023 `SimpleOccurrence` accounting data using current-year actual integral (`CRIIX`) fields. The importer reconciles function/object total charges and net financial assets before publication.
- Alberta population/SIR dwelling fields, B.C. population fields, Ontario Schedule 02 household/population fields and Quebec MAMH population are retained as source context only. They are not yet used for LGPI per-household normalization.

Financial observations are now loaded for 98 municipalities. Hamilton is explicitly source-unavailable, giving all 99 LGPI municipalities a resolved 2023 financial-data status. Statistics Canada dwelling denominators and provincial-average calculations remain gated until the exact LGPI denominator convention is reproduced.


## 2024 financial-data status

- Alberta: 9 municipalities, 414 observations.
- British Columbia: 17 municipalities, 510 observations.
- Ontario: 40 source-available municipalities, 1,160 observations; Hamilton remains explicitly source-unavailable.
- Quebec: 19 municipalities, 589 observations from MAMH 2024 data.
- Prairie audited reports: Regina, Saskatoon and Winnipeg, 98 observations.
- Atlantic and territorial audited statements: 10 municipalities, 216 observations.
- Total: 2,987 source-backed 2024 financial observations across 98 municipalities, with all 99 municipalities assigned a resolved data/source status.
- Published transparency scoring remains the 2023 Frontier edition; no 2024 transparency score is inferred.
