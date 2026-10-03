# LGPI continuation checkpoint

## Recovery

The linked chat stopped its visible completion notes at presentation commit `259eff630df5e247de9d91799c99cfb07c8215f2`. The repository had subsequently advanced to `b98cdb5a4a3cd0c15f954ea87d13b3b2f24bf0a9`, merging [PR #10](https://github.com/FTFNAnalytics/lgpi/pull/10), **Add 2024 financial data and year-over-year views**. The main-branch CI run for that commit succeeded.

The continuation starts from that newer, clean main commit. No financial JSON, original importer, or previous commit is replaced. The project mirror and saved `D:\LGPI` folder contained no checkout; the repository was recovered into this project's `lgpi` directory.

## Preserved data

| Financial year | Observation records | Reported | Pending review | Not reported | Municipalities with records |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2023 | 2,981 | 2,672 | 196 | 113 | 98 |
| 2024 | 2,987 | 2,674 | 197 | 116 | 98 |

Hamilton has an explicit unavailable-source record in both years. There are 99 municipality profiles and 56 financial metric definitions. The 80 published transparency scores remain the separate 2023 layer; Quebec's 19 municipalities remain unscored.

## Follow-up changes

- Year-over-year calculations now require accepted, finite values for the same municipality and metric in consecutive years. Ontario debt and Charlottetown revenue remain visible, with changes withheld while their mappings are under review.
- Missing values never become zero. A zero or negative baseline yields a dollar change but no percentage; the reason is shown.
- Both years' review status and expandable source evidence accompany the trend values. Compare uses the same evidence display in core cards and the complete table, and explicitly identifies unavailable sources.
- Transparency headings and the profile score explicitly identify 2023, even while financial year 2024 is selected.
- Metric Explorer city links preserve the chosen year. Year navigation announces the current selection to assistive technology.
- Trend cards use two columns on larger screens and stack on narrow screens. Mobile section headings stack above their explanation.
- Regression checks protect the recovered annual record counts, keys, provenance, missing states, transparency boundaries and calculation edge cases. Route checks verify rendered content instead of checking HTTP success alone. Dependencies are locked and CI uses `npm ci`.

## Validation

Run `npm test`, `npm run typecheck` and `npm run build`. Start the production server and run `npm run test:smoke` (12 routes); `LGPI_TEST_URL` selects a non-default preview/deployment URL. Browser QA covers year switching, review evidence, independent comparison years, the metric-to-profile link, and narrow-screen financial cards.

Local results: all 7 regression tests and all 12 route checks passed; TypeScript and the production build passed on Node 24.15.0 / Windows. The production dependency audit found zero vulnerabilities. Browser checks passed at the normal desktop viewport and at 375px phone width, with no horizontal page overflow or browser console errors in the exercised flows. CI repeats the automated checks on Node 22 / Ubuntu.

The legacy website could not be reopened during this continuation (fetch/browser failures). The prior research preserved in `PITCH_STATUS_2024.md` and the publicly indexed [Metric page](https://www.lgpi.ca/metric) both describe selected-year views; the continuation preserves the already merged interaction rather than claiming a new live-site audit.

## Next unfinished work

See [next data tranche](NEXT_DATA_TRANCHE.md). Household normalization, provincial-average rules, outstanding mapping review, historical restatement reconciliation and a stable deployment remain separate unfinished work. This continuation does not infer those results from the existence of 2024 records.
