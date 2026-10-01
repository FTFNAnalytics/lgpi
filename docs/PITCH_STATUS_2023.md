# LGPI 2023 — Pitch Build Status

## Presentable now

The reconstruction now contains the complete **99-municipality LGPI product universe**.

- 80 published 2023 Transparency Index scores are reproduced from the Frontier Centre report.
- 19 Quebec municipalities are present as financial profiles and are explicitly marked **Transparency score not published**.
- 73 municipalities have the complete ten-component transparency breakdown.
- The 56-field legacy financial catalogue is preserved.
- 2,758 official 2023 financial observations are loaded for 88 municipalities.
- Hamilton is explicitly marked `source_unavailable` for Ontario's 2023 FIR rather than converted to zero.
- Every financial observation preserves an official source, original source field/code, mapping method and review state.
- City search, profiles, transparency explorer, comparisons, metric explorer and methodology/provenance views are functional.

## Bulk source coverage

| Source block | LGPI municipalities | Observations | Status |
| --- | ---: | ---: | --- |
| Alberta FIR/SIR | 9 / 9 | 414 | Complete |
| British Columbia schedules | 17 / 17 | 510 | Complete |
| Ontario FIR | 40 / 41 | 1,160 | Complete where source available; Hamilton unavailable |
| Quebec MAMH | 19 / 19 | 589 | Complete core mapping; transparency intentionally unscored |
| Prairie audited reports | 3 / 3 | 85 | Complete |
| Remaining Atlantic / territorial statements | 10 | — | In progress |

## Remaining presentation-week work

The remaining 10 municipalities are Halifax, Cape Breton, Moncton, Fredericton, Saint John, St. John's, Charlottetown, Whitehorse, Yellowknife and Iqaluit.

These are being treated as statement-based adapters: values are taken from official audited reports and normalized into the same LGPI model. Unavailable or non-comparable legacy fields stay explicit rather than being inferred.

## Methodology boundary

This build reconstructs the existing LGPI before proposing a new performance methodology.

- Transparency scores are transcribed only where Frontier published them.
- Quebec is not independently scored.
- A blank is never treated as zero.
- Per-household and provincial-average displays remain gated until the original denominator convention is fully reconciled.
- Financial comparisons do not imply that municipalities provide identical service bundles.

## Pitch framing

The prototype demonstrates three things:

1. The existing LGPI can be reproduced from public evidence.
2. The annual data pull can be converted from a largely manual exercise into reproducible province/source adapters.
3. The public product can expose provenance and uncertainty directly while remaining much easier to browse and compare.
