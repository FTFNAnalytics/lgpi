# Next data tranche

## Recovered baseline

The 2023 and 2024 financial-source passes are already merged in `main` at `b98cdb5a4a3cd0c15f954ea87d13b3b2f24bf0a9` (PR #10). Do not restart these imports. Each year has observations for 98 municipalities and an explicit unavailable source for Hamilton; 99 municipalities remain represented.

The follow-up presentation pass preserves all imported files, exposes review labels in comparisons, withholds unreviewed year-over-year changes, preserves selected years in Metric Explorer links, and adds data and rendered-content checks. See [continuation handoff](CONTINUATION_HANDOFF.md).

## Remaining work, in order

1. Reproduce the historical Statistics Canada dwelling denominator for each year and the provincial-average aggregation convention. Record exact geography, dwelling concept, reference year and any interpolation rules. Do not substitute population or source-workbook household fields without reconciliation.
2. Resolve provisional financial mappings against the legacy definitions, especially Ontario net long-term liabilities and Charlottetown total revenue. In 2024, 197 mappings remain pending review; 116 observation records explicitly report no value. A resolved source pass does not mean every field is available or accepted.
3. Reconcile missing historical comparison fields, including Regina's unloaded 2023 capital-assets metric, against the original cited statement before adding values. Existing 2024 values do not supply a missing 2023 baseline.
4. Resolve the Kawartha Lakes and Chatham-Kent published transparency discrepancies with editorial evidence. Keep the provisional table values and discrepancy notices until then.
5. Validate a stable presentation deployment and run the same route checks against its URL.
6. Consider 2025 only as a separate annual tranche after confirming source completeness.

## Definition of complete for calculated views

A municipality's derived financial views are ready only when each displayed field has an explicit observation state, every numeric value is sourced, source-to-LGPI mappings are accepted, totals reconcile within documented tolerance, household denominators are sourced, calculated fields can be reproduced, and remaining exceptions are visible.
