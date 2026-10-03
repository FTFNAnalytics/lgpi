import Link from "next/link";
import {
  FinancialYear,
  getFinancialCoverageByProvince,
  getFinancialSummary,
  TARGET_MUNICIPALITIES,
  VERIFIED_COMPONENT_BREAKDOWNS,
  VERIFIED_TRANSPARENCY_TOTALS,
} from "@/lib/lgpi-data";

export default async function CoveragePage({
  searchParams,
}: {
  searchParams: Promise<{ year?: string }>;
}) {
  const query = await searchParams;
  const year: FinancialYear = Number(query.year) === 2023 ? 2023 : 2024;
  const summary = getFinancialSummary(year);
  const coverage = getFinancialCoverageByProvince(year);

  return (
    <main>
      <section className="page-hero">
        <div className="shell">
          <p className="eyebrow">2023–2024 reconstruction · national status</p>
          <h1>Coverage</h1>
          <p>
            Both financial-source passes resolve the complete 99-municipality LGPI universe.
            Switch years to inspect source availability and observation coverage without changing
            the published 2023 transparency-score layer.
          </p>
        </div>
      </section>

      <section className="year-nav-section">
        <div className="shell">
          <div className="year-nav" aria-label="Coverage year">
            <span className="year-nav-label">Financial year</span>
            {[2023, 2024].map((item) => (
              <Link
                key={item}
                href={"/coverage?year=" + item}
                className={"year-tab " + (year === item ? "active" : "")}
              >
                {item}
              </Link>
            ))}
          </div>
          <p className="year-context-note">
            Transparency remains the published 2023 LGPI index; this selector changes the financial-source coverage shown below.
          </p>
        </div>
      </section>

      <section className="section">
        <div className="shell">
          <div className="stat-grid">
            <div className="stat">
              <strong>{TARGET_MUNICIPALITIES}/99</strong>
              <span>municipalities represented in the product</span>
            </div>
            <div className="stat">
              <strong>{summary.municipalitiesWithObservations}</strong>
              <span>municipalities with {year} financial observations</span>
            </div>
            <div className="stat">
              <strong>{summary.observationCount.toLocaleString("en-CA")}</strong>
              <span>source-backed {year} financial observations</span>
            </div>
            <div className="stat">
              <strong>{VERIFIED_TRANSPARENCY_TOTALS}/80</strong>
              <span>published 2023 non-Quebec transparency scores</span>
            </div>
          </div>

          <div className="coverage-band">
            <div>
              <span className="chip good">Resolved source pass</span>
              <h2>Every municipality has a resolved {year} financial-data status.</h2>
              <p>
                {summary.municipalitiesWithObservations} municipalities have financial observations.
                {summary.sourceUnavailableCount > 0
                  ? " Hamilton remains source unavailable in Ontario's FIR and is not treated as zero."
                  : " No municipality is represented with fabricated zeroes."}
              </p>
            </div>
            <div className="coverage-band-stats">
              <div><strong>{summary.reportedCount.toLocaleString("en-CA")}</strong><span>reported / accepted mappings</span></div>
              <div><strong>{summary.pendingReviewCount.toLocaleString("en-CA")}</strong><span>explicit pending-review mappings</span></div>
              <div><strong>{summary.notReportedCount.toLocaleString("en-CA")}</strong><span>explicit not-reported observations</span></div>
              <div><strong>{VERIFIED_COMPONENT_BREAKDOWNS}</strong><span>full 2023 transparency component breakdowns</span></div>
            </div>
          </div>
        </div>
      </section>

      <section className="section white">
        <div className="shell">
          <div className="section-heading">
            <div>
              <p className="eyebrow">{year} province and territory coverage</p>
              <h2>National source coverage</h2>
            </div>
            <p>
              Structured provincial returns are used where available; official audited municipal
              statements are used for the remaining jurisdictions.
            </p>
          </div>

          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Jurisdiction</th>
                  <th>LGPI municipalities</th>
                  <th>With observations</th>
                  <th>Source unavailable</th>
                  <th>Observations</th>
                </tr>
              </thead>
              <tbody>
                {coverage.map((row) => (
                  <tr key={row.province}>
                    <td><strong>{row.name}</strong></td>
                    <td>{row.municipalities}</td>
                    <td>{row.withObservations}</td>
                    <td>{row.sourceUnavailable || "—"}</td>
                    <td>{row.observations.toLocaleString("en-CA")}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="shell">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Deliberate boundaries</p>
              <h2>What remains intentionally withheld</h2>
            </div>
          </div>
          <div className="card-grid">
            <article className="card">
              <span className="chip pending">Withheld</span>
              <h2 style={{ marginTop: 14 }}>Per-household values</h2>
              <p>
                The historic LGPI used a dwelling denominator. Those calculated views stay off until
                the exact Statistics Canada denominator convention is reproduced for each year.
              </p>
            </article>
            <article className="card">
              <span className="chip pending">Withheld</span>
              <h2 style={{ marginTop: 14 }}>Provincial-average percentages</h2>
              <p>
                Provincial-average comparisons remain disabled until the historic denominator and
                aggregation rules are confirmed end-to-end.
              </p>
            </article>
            <article className="card">
              <span className="chip good">Preserved</span>
              <h2 style={{ marginTop: 14 }}>Transparency year</h2>
              <p>
                The latest public transparency edition identified is based on 2023 statements.
                Financial data can advance to 2024 without inventing a 2024 transparency score.
              </p>
            </article>
          </div>

          <div className="hero-actions" style={{ marginTop: 28 }}>
            <Link className="button ink" href="/cities">Browse all 99 profiles</Link>
            <Link className="button ink" href="/methodology">Review methodology</Link>
          </div>
        </div>
      </section>
    </main>
  );
}
