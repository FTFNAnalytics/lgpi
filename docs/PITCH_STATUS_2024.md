# LGPI 2024 — Financial Update Status

## Presentable now

The rebuild now contains a two-year financial history across the complete **99-municipality LGPI universe**.

- Published transparency layer: 80 non-Quebec scores from the Frontier edition based on 2023 statements.
- 2023 financial layer: 2,981 observations across 98 municipalities; Hamilton source-unavailable.
- 2024 financial layer: 2,987 observations across 98 municipalities; Hamilton source-unavailable.
- 19 Quebec municipalities have both 2023 and 2024 MAMH financial profiles and remain transparency-unscored exactly as published.
- The 56-field legacy financial catalogue is stable across years.
- City profiles have a 2023 / 2024 year strip plus compact year-over-year core metrics.
- Compare supports independent year selection for each municipality.
- Metric Explorer supports year selection.
- Every financial observation preserves source, source concept/code, mapping method and review state.
- Trend and Compare values expose review states and expandable evidence. Only accepted mappings produce year-over-year changes; missing or pending-review values do not.
- The 2,987 records include 2,674 accepted mappings, 197 pending-review mappings and 116 explicit not-reported observations; the record count is not a count of accepted numeric values.

## 2024 source coverage

| Source block | LGPI municipalities | 2024 observations | Status |
| --- | ---: | ---: | --- |
| Alberta FIR/SIR | 9 / 9 | 414 | Complete |
| British Columbia schedules | 17 / 17 | 510 | Complete |
| Ontario FIR | 40 / 41 | 1,160 | Complete where source available; Hamilton unavailable |
| Quebec MAMH | 19 / 19 | 589 | Complete mapped layer |
| Prairie audited reports | 3 / 3 | 98 | Complete |
| Atlantic / territorial statements | 10 / 10 | 216 | Complete |
| **Total** | **98 observed + 1 unavailable** | **2,987** | **Resolved national source status** |

## Year-over-year behavior

The original LGPI presents history primarily as a **selected-year view**: choose a year and the same financial categories reload for that year. Metric and comparison tools also include year controls.

The rebuild preserves that pattern and adds:

- a compact 2023 → 2024 core financial summary on each city profile;
- independent year selection on each side of Compare;
- year selection in Metric Explorer;
- year-aware national Coverage.

## Methodology boundary

- Transparency remains the published 2023 index; no 2024 transparency score is inferred.
- Missing data is never converted to zero.
- Pending-review mappings remain explicit.
- Per-household and provincial-average calculations remain gated until the historical Statistics Canada dwelling-denominator convention is reproduced by year.
- Cross-city comparisons do not imply identical service responsibilities.

## Next work

1. reproduce the historical household denominator and provincial-average calculations;
2. add 2025 when official sources are sufficiently complete;
3. decide whether any future performance methodology should be introduced as a separate versioned layer.
