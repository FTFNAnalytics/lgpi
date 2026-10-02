# LGPI 2023 presentation run-of-show

## Five-minute walkthrough

### 1. Open the homepage — 30 seconds

Lead with the core claim:

> The original LGPI can be reproduced from public evidence and turned into a maintainable annual data product.

Point to:

- 99 / 99 municipalities represented
- 98 municipalities with source-backed financial observations
- Hamilton explicitly source-unavailable
- 2,981 official/source-backed 2023 observations
- 80 / 80 published non-Quebec transparency scores loaded

Then open **Coverage**.

### 2. Coverage — 45 seconds

Use the coverage page to show that the product distinguishes:

- complete municipality coverage
- source-backed financial observations
- published transparency-score coverage
- explicit source-unavailable states
- deliberately withheld calculated views

Emphasize **missing does not mean zero**.

The main methodological boundary to explain is that dollars-per-household and percentage-of-provincial-average views have not been re-enabled until the historical Statistics Canada dwelling denominator is reproduced exactly.

### 3. Calgary profile — 75 seconds

Open the Calgary city profile.

Show:

1. Published transparency score and component breakdown.
2. Financial-source status strip.
3. Core financial snapshot:
   - total revenue
   - total expenditure
   - long-term debt
   - capital assets
4. Detailed observations with:
   - normalized LGPI field
   - original source field
   - mapping status
   - official source link

Message:

> This is no longer a black-box spreadsheet. A user can trace a displayed number back to the field it came from.

### 4. Compare Calgary and Edmonton — 60 seconds

Open the comparison page.

Use Calgary and Edmonton because both are generated from the same standardized Alberta FIR/SIR source.

Show:

- transparency components side-by-side
- core financial values first
- full mapped field set below

Then explain the caution:

> The tool exposes comparisons without pretending that every municipality provides the same bundle of services.

### 5. Quebec example — 45 seconds

Open Montréal or Québec.

Point out that:

- the financial profile is populated from MAMH's official 2023 open-data workbook
- transparency is shown as **not published**
- no zero or substitute score is invented

Message:

> The new architecture can represent a real absence honestly instead of making the interface look complete by filling it with a number.

### 6. Methodology — 45 seconds

Close on the methodology page.

Highlight:

- published 33-point transparency framework preserved
- source provenance retained
- explicit observation states
- known publication conflicts surfaced
- denominator-dependent calculated views intentionally gated

## Suggested pitch close

The reconstruction demonstrates that LGPI can become an annual product rather than a periodic manual exercise:

1. province/source-specific ingestion adapters collect the strongest available official data;
2. mappings normalize those sources into the stable LGPI field catalogue;
3. QA catches source and entity anomalies before publication;
4. provenance remains visible in the public interface;
5. the same pipeline can be rerun for 2024 and subsequent years.

## Questions to be ready for

**Why are Quebec transparency scores blank?**  
Because the published 2023 LGPI edition omitted Quebec transparency scoring. The reconstruction preserves the published result rather than inventing replacement scores.

**Why is Hamilton missing financial data?**  
Ontario lists Hamilton's 2023 FIR as unavailable. The product exposes that source state explicitly instead of treating missing fields as zero.

**Why are per-household values not shown yet?**  
The historical LGPI used a dwelling denominator. That calculated view is intentionally gated until the exact Statistics Canada denominator and provincial aggregation convention are reproduced.

**Is this a new fiscal-performance score?**  
No. The pitch build first reconstructs the existing product faithfully. A future performance methodology can be designed as a separate, clearly versioned layer.
