# LGPI 2023 Reconstruction

A pitch-ready, source-cited reconstruction of Canada's Local Government Performance Index (LGPI) for fiscal year 2023.

This project starts by faithfully reproducing the published LGPI transparency methodology and legacy financial field structure, then improves the product layer with modern navigation, explicit provenance, coverage reporting, QA states, and a maintainable ingestion model.

## What works now

- Modern Next.js frontend.
- 2023 Transparency Index explorer.
- All 80 transparency scores published for non-Quebec municipalities in the 2023 edition are loaded.
- 73 municipality records with all ten transparency components.
- Municipality profile pages.
- Side-by-side comparison.
- Reconstructed legacy financial metric catalogue.
- Reproducible 2023 bulk imports covering all 9 Alberta and all 17 British Columbia LGPI municipalities, plus the initial Toronto official-report seed.
- Source links and review states on financial observations.
- Explicit missing-data semantics: pending is never treated as zero.
- Known publication discrepancies documented rather than hidden.
- CI typecheck and production build.

## Current coverage

| Layer | Status |
| --- | ---: |
| Published municipality universe | 99 |
| Published 2023 transparency scores loaded | 80 / 80 non-Quebec scores |
| Full component breakdowns | 73 |
| Quebec municipalities unscored in the published report | 19 |
| Legacy financial fields reconstructed | 56 |
| Official financial observations loaded | 925 (414 Alberta + 510 B.C. bulk + 1 Toronto seed) |

The transparency data is reconstructed from Frontier Centre's 2025 LGPI publication, which assesses 2023 municipal financial statements. That report explicitly omits transparency scores for Quebec, so Quebec municipalities are treated as unscored rather than missing or zero. The financial layer is being rebuilt independently from official municipal reports and provincial data sources. Alberta is generated from the province's standardized 2023 FIR/SIR workbook with field-level source codes and a Calgary audited-report reconciliation. British Columbia is generated from eight standardized provincial 2023 financial schedules with cross-schedule balance-sheet and debt reconciliation.

## Product routes

- `/` — overview and municipality search
- `/transparency` — sortable/filterable 2023 index
- `/cities` — municipality directory
- `/cities/[slug]` — evidence-backed municipality profile
- `/compare` — two-municipality comparison
- `/metrics` — legacy LGPI financial metric explorer
- `/methodology` — reconstruction methodology and QA rules

## Data philosophy

The reconstruction uses five explicit financial observation states:

- `reported`
- `pending_review`
- `not_reported`
- `not_applicable`
- `source_unavailable`

No blank field is silently converted to zero.

Legacy LGPI per-household and provincial-average calculations are intentionally withheld until the exact 2023 dwelling denominators and aggregation rules are verified.

## Research notes

See:

- [Reconstruction status](docs/RECONSTRUCTION_STATUS.md)
- [Data provenance and QA contract](docs/DATA_PROVENANCE.md)
- [Next data tranche](docs/NEXT_DATA_TRANCHE.md)

## Run locally

```bash
npm install
npm run dev
```

For validation:

```bash
npm run typecheck
npm run build
```

## Status

This is an independent reconstruction/prototype, not an official Frontier Centre production release. The objective is to demonstrate that the existing LGPI can be reproduced, brought current, and turned into a transparent, maintainable municipal-data product without inventing missing observations.
