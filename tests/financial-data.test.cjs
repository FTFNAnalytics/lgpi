const { test } = require('node:test');
const assert = require('node:assert/strict');
const {
  financialByYear, municipalities2023, metricCatalog, getFinancialSummary,
  getFinancialCoverageByProvince, getFinancialSourceUnavailable, getFinancialObservation,
  formatThousands,
} = require('../.test-build/lib/lgpi-data.js');
const { getFinancialChange } = require('../.test-build/lib/financial-comparison.js');

const fixture = (year, valueThousands, extra = {}) => ({
  municipalitySlug: 'example', metric: 'total_revenue', year, valueThousands,
  status: 'reported', sourceUrl: 'https://example.org/report', sourceLabel: 'Annual report',
  sourceLocation: 'Statement of operations', ...extra,
});

for (const [year, expected] of [[2023, 2981], [2024, 2987]]) {
  test(`${year}: complete recovered import, unique keys and usable provenance`, () => {
    const observations = financialByYear[year];
    const slugs = new Set(municipalities2023.map(row => row.slug));
    const metrics = new Set(metricCatalog.map(row => row.key));
    const keys = new Set();
    assert.equal(slugs.size, 99);
    assert.equal(metrics.size, 56);
    assert.equal(observations.length, expected);
    for (const row of observations) {
      const key = `${row.municipalitySlug}:${row.metric}`;
      assert.ok(!keys.has(key), `Duplicate ${year} ${key}`);
      keys.add(key);
      assert.ok(slugs.has(row.municipalitySlug), `Unknown municipality ${key}`);
      assert.ok(metrics.has(row.metric), `Unknown metric ${key}`);
      assert.equal(row.year, year);
      assert.ok(['reported', 'pending_review', 'not_reported', 'not_applicable', 'source_unavailable'].includes(row.status));
      assert.ok(/^https?:\/\//.test(row.sourceUrl), `Missing source ${key}`);
      assert.ok(row.sourceLabel && row.sourceLocation, `Missing provenance ${key}`);
      assert.ok(row.valueThousands === null || Number.isFinite(row.valueThousands), `Non-finite ${key}`);
      if (row.status === 'reported') assert.notEqual(row.valueThousands, null, `Reported null ${key}`);
      if (['not_reported', 'not_applicable', 'source_unavailable'].includes(row.status)) assert.equal(row.valueThousands, null, `Missing data converted to a value ${key}`);
    }
    const summary = getFinancialSummary(year);
    assert.equal(summary.municipalitiesWithObservations, 98);
    assert.equal(summary.sourceUnavailableCount, 1);
    assert.equal(summary.reportedCount + summary.pendingReviewCount + summary.notReportedCount, expected);
    assert.ok(getFinancialSourceUnavailable('hamilton', year));
    assert.equal(observations.filter(row => row.municipalitySlug === 'hamilton').length, 0);
    assert.equal(getFinancialCoverageByProvince(year).reduce((sum, row) => sum + row.observations, 0), expected);
    for (const city of municipalities2023) {
      const present = observations.some(row => row.municipalitySlug === city.slug);
      assert.notEqual(present, Boolean(getFinancialSourceUnavailable(city.slug, year)), `Unresolved/conflicting source status ${city.slug}`);
    }
  });
}

test('year-over-year math uses stored thousands consistently, with signed change', () => {
  assert.deepEqual(getFinancialChange(fixture(2023, 100), fixture(2024, 110)), {
    changeThousands: 10, percentChange: 10, explanation: null,
  });
  assert.equal(getFinancialChange(fixture(2023, 100), fixture(2024, 75)).percentChange, -25);
  assert.equal(getFinancialChange(fixture(2023, 100), fixture(2024, 100)).changeThousands, 0);
  assert.equal(formatThousands(10), '$10,000');
  assert.equal(formatThousands(null), '—');
  assert.equal(formatThousands(0), '$0');
});

test('zero and negative baselines preserve dollar change without misleading percentages', () => {
  for (const baseline of [0, -100]) {
    const result = getFinancialChange(fixture(2023, baseline), fixture(2024, 50));
    assert.equal(result.changeThousands, 50 - baseline);
    assert.equal(result.percentChange, null);
    assert.ok(result.explanation);
  }
});

test('unreviewed, missing and incompatible observations never produce a delta', () => {
  const accepted = fixture(2023, 100);
  for (const status of ['pending_review', 'not_reported', 'not_applicable', 'source_unavailable']) {
    assert.equal(getFinancialChange(accepted, fixture(2024, 110, { status })).changeThousands, null);
    assert.equal(getFinancialChange({ ...accepted, status }, fixture(2024, 110)).changeThousands, null);
  }
  for (const value of [null, NaN, Infinity]) {
    assert.equal(getFinancialChange(accepted, fixture(2024, value)).changeThousands, null);
  }
  assert.equal(getFinancialChange(undefined, fixture(2024, 110)).changeThousands, null);
  assert.equal(getFinancialChange(accepted, undefined).changeThousands, null);
  for (const extra of [{ municipalitySlug: 'different-city' }, { metric: 'capital_assets' }, { year: 2023 }]) {
    assert.equal(getFinancialChange(accepted, fixture(2024, 110, extra)).changeThousands, null);
  }
});

test('real imported review flags survive the 2024 integration', () => {
  for (const [slug, metric] of [['toronto', 'long_term_debt'], ['charlottetown', 'total_revenue']]) {
    const result = getFinancialChange(getFinancialObservation(slug, 2023, metric), getFinancialObservation(slug, 2024, metric));
    assert.equal(result.changeThousands, null);
    assert.match(result.explanation, /under review/);
  }
  for (const slug of ['calgary', 'edmonton', 'montreal']) {
    const prior = getFinancialObservation(slug, 2023, 'total_revenue');
    const current = getFinancialObservation(slug, 2024, 'total_revenue');
    assert.equal(getFinancialChange(prior, current).changeThousands, current.valueThousands - prior.valueThousands);
  }
});

test('financial update never creates 2024 transparency scores or Quebec scores', () => {
  assert.ok(municipalities2023.every(row => row.year === 2023));
  const quebec = municipalities2023.filter(row => row.province === 'QC');
  assert.equal(quebec.length, 19);
  assert.ok(quebec.every(row => row.score === null && !row.transparencyPublished));
});
