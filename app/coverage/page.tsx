import Link from "next/link";
import {
  financialCoverageByProvince,
  financialObservationCount,
  financialSourceUnavailableCount,
  municipalitiesWithFinancialObservations,
  pendingFinancialObservationCount,
  reportedFinancialObservationCount,
  TARGET_MUNICIPALITIES,
  VERIFIED_COMPONENT_BREAKDOWNS,
  VERIFIED_TRANSPARENCY_TOTALS,
} from "@/lib/lgpi-data";

export default function CoveragePage() {
  return (
    <main>
      <section className="page-hero">
        <div className="shell">
          <p className="eyebrow">2023 reconstruction · national status</p>
          <h1>Coverage</h1>
          <p>
            The 2023 financial-source pass now resolves the complete 99-municipality LGPI universe.
            This page separates what is complete from what is intentionally withheld pending exact
            historical-method reproduction.
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
              <strong>{municipalitiesWithFinancialObservations}</strong>
              <span>municipalities with source-backed financial observations</span>
            </div>
            <div className="stat">
              <strong>{financialObservationCount.toLocaleString("en-CA")}</strong>
              <span>official/source-backed 2023 financial observations</span>
            </div>
            <div className="stat">
              <strong>{VERIFIED_TRANSPARENCY_TOTALS}/80</strong>
              <span>published non-Quebec transparency scores loaded</span>
            </div>
          </div>

          <div className="coverage-band">
            <div>
              <span className="chip good">Complete source pass</span>
              <h2>Every municipality has a resolved 2023 financial-data status.</h2>
              <p>
                Ninety-eight municipalities have financial observations. Hamilton is preserved as
                source unavailable because Ontario does not publish its 2023 FIR.
              </p>
            </div>
            <div className="coverage-band-stats">
              <div><strong>{reportedFinancialObservationCount.toLocaleString("en-CA")}</strong><span>reported / accepted mappings</span></div>
              <div><strong>{pendingFinancialObservationCount.toLocaleString("en-CA")}</strong><span>explicit pending-review mappings</span></div>
              <div><strong>{financialSourceUnavailableCount}</strong><span>source-unavailable municipality</span></div>
              <div><strong>{VERIFIED_COMPONENT_BREAKDOWNS}</strong><span>full transparency component breakdowns</span></div>
            </div>
          </div>
        </div>
      </section>

      <section className="section white">
        <div className="shell">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Province and territory coverage</p>
              <h2>National source coverage</h2>
            </div>
            <p>
              Financial observations are drawn from provincial structured returns where available,
              and official audited municipal statements elsewhere.
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
                {financialCoverageByProvince.map((row) => (
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
              <h2>What is not being faked for the demo</h2>
            </div>
          </div>
          <div className="card-grid">
            <article className="card">
              <span className="chip pending">Withheld</span>
              <h2 style={{ marginTop: 14 }}>Per-household values</h2>
              <p>
                The historic LGPI used a dwelling denominator. Those calculated views stay off until
                the exact Statistics Canada denominator convention is reproduced.
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
              <h2 style={{ marginTop: 14 }}>Quebec transparency status</h2>
              <p>
                The published LGPI edition omitted Quebec transparency scores. Quebec is therefore
                shown as unscored, not zero and not independently rescored.
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
