# Data provenance and QA contract

LGPI is being rebuilt as a source-backed data product. Every observation should be traceable through this chain:

```
municipality
  -> fiscal year
  -> source document
  -> original reported concept
  -> normalized LGPI metric
  -> value
  -> QA status
  -> publication
```

## Required provenance fields

Financial observations store:

- municipality slug
- fiscal year
- normalized metric key
- value in reported LGPI units
- observation status
- source URL
- source label
- source location/page/table
- mapping or review note when needed

## Observation states

`reported`
: Source and mapping are verified strongly enough to publish.

`pending_review`
: A source value exists, but aggregation or semantic mapping needs human confirmation.

`not_reported`
: The applicable source does not report the field.

`not_applicable`
: The field does not apply to that municipal structure.

`source_unavailable`
: The expected source cannot currently be retrieved.

No state is automatically converted to numeric zero.

## Transparency sources

The 2023 transparency index is reconstructed from the detailed regional tables in Frontier Centre's 2025 LGPI publication. When a detailed table and a summary/media release conflict, the detailed table is used provisionally and the conflict is registered in `docs/RECONSTRUCTION_STATUS.md`.

## Legacy metric compatibility

The public LGPI financial pages expose a stable four-section field structure:

1. Financial position
2. Revenue
3. Expenditure
4. Expenditures by object

The app preserves those field identities in `metricCatalog`. Source terms are not automatically collapsed into legacy fields when definitions may differ. For example, a city's "sales of goods and services" line is not silently renamed "user charges" without confirming the legacy LGPI mapping rule.

## Household normalization

Historic LGPI pages provide total values, dollars per household, and percentage of provincial average. This reconstruction does not calculate the latter two until the exact dwelling denominator and provincial aggregation logic are verified for each financial year.

That preserves comparability and prevents a convenient but methodologically different population denominator from replacing the published household convention.

## Year-over-year publication rules

- Only two `reported`, finite observations for the same municipality and metric in consecutive years produce a change.
- Pending-review values remain visible with their labels and evidence, but never produce a calculated delta.
- Dollar change is current minus prior; percentage change is that difference divided by a strictly positive prior value.
- A zero or negative baseline retains its dollar change with an explanation for the absent percentage.
- Figures are nominal CAD, not inflation adjusted. The original annual observations remain intact; no restatement reconciliation is implied.
- City comparison cards and tables retain each value's year, review status, source concept, mapping note and source link.
