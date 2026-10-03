# LGPI 2023–2024 presentation run-of-show

## Five-minute walkthrough

### 1. Homepage — 30 seconds

Lead with the core claim:

> The original LGPI can be reproduced from public evidence, updated annually, and presented as a traceable municipal-finance product.

Point to:

- 99 / 99 municipalities represented
- 98 municipalities with source-backed 2024 financial observations
- Hamilton explicitly source-unavailable
- 2,987 source-backed 2024 observations
- 80 / 80 published non-Quebec 2023 transparency scores loaded

Then open **Coverage**.

### 2. Coverage — 45 seconds

Switch the Financial year control between **2023** and **2024**.

Show that the product separates annual financial-source coverage from the published 2023 transparency-score layer, explicit source-unavailable states, pending-review mappings, and deliberately withheld calculated views.

> We can advance the financial database annually without pretending Frontier has published a new transparency score.

### 3. Calgary profile — 75 seconds

Open `/cities/calgary?year=2024`.

Show the published transparency components, the horizontal 2023 / 2024 financial-year strip, the compact 2023 → 2024 change cards, the selected-year core financial snapshot, and detailed source provenance.

Then click **2023** and back to **2024**.

Expand either year's **source details** in a trend card. Explain that the amounts are nominal Canadian dollars from separately sourced annual observations. For a review-state example, open Toronto: debt values retain their review labels and the change is withheld. The 2023 transparency score stays explicitly labeled when financial year 2024 is selected.

> This preserves the original LGPI interaction — choose a year and inspect the same field structure — while adding a compact year-over-year summary.

### 4. Compare — 60 seconds

Open `/compare`. Use Calgary and Edmonton first because both are generated from Alberta's standardized FIR/SIR source.

Show that each side can independently select municipality and financial year. Demonstrate Calgary 2023 vs Calgary 2024, or Calgary 2024 vs Edmonton 2024.

> The comparison layer now supports both cross-city and cross-year analysis without changing the underlying metric definitions.

### 5. Metric Explorer — 40 seconds

Open `/metrics`. Pick a legacy metric such as long-term debt or total revenue and switch between 2023 and 2024.

### 6. Quebec example — 35 seconds

Open Montréal with financial year 2024. Its financial profile comes from MAMH's official 2024 data while transparency remains **not published**.

### 7. Methodology — 35 seconds

Close on `/methodology`. Highlight the preserved 33-point transparency framework, stable 2023–2024 financial catalogue, source provenance, explicit observation states, and denominator-dependent views that remain gated.

## Pitch close

The reconstruction demonstrates that LGPI can operate as an annual product:

1. source-specific adapters collect official annual data;
2. stable mappings normalize each source into the LGPI field catalogue;
3. QA catches schema drift, entity ambiguity and accounting inconsistencies;
4. the UI switches years without changing metric definitions;
5. provenance remains visible;
6. the same process can now be repeated for 2025.

## Questions to be ready for

**Why does the transparency score still say 2023 when I select 2024?**  
Because the latest public Frontier transparency edition identified is based on 2023 municipal statements. The 2024 update is a financial-data update, not an invented transparency rescoring.

**Why is Hamilton missing financial data?**  
Ontario's FIR source is unavailable for Hamilton. The product exposes that source state instead of treating missing fields as zero.

**Why are per-household values not shown yet?**  
The historical LGPI used a Statistics Canada dwelling denominator. That calculated view remains gated until the exact year-specific denominator and provincial aggregation convention are reproduced.

**How does the new year-over-year experience relate to the old site?**  
The old site changes the city financial table when the user selects a year, and its Metric/Compare tools also include year controls. The rebuild preserves that behavior and adds a compact two-year summary on city profiles.

**Is this a new fiscal-performance score?**  
No. The rebuild first preserves and updates the existing product architecture. Any future performance methodology should be a separate, versioned layer.
