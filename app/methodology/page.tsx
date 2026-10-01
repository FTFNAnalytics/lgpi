import {
  REPORT_URL,
  sourceDiscrepancies,
  transparencyCriteria,
  VERIFIED_COMPONENT_BREAKDOWNS,
  VERIFIED_TRANSPARENCY_TOTALS,
  TARGET_MUNICIPALITIES,
} from "@/lib/lgpi-data";

export default function MethodologyPage() {
  return (
    <main>
      <section className="page-hero">
        <div className="shell">
          <p className="eyebrow">Methods · provenance · QA</p>
          <h1>How this reconstruction works</h1>
          <p>The goal is faithful replication before reinterpretation: preserve the published LGPI scoring model, recover 2023 values from evidence, and make every uncertainty explicit.</p>
        </div>
      </section>
      <section className="section">
        <div className="shell prose">
          <h2>The 33-point transparency framework</h2>
          <p>The published 2023 index uses ten financial-reporting criteria. This prototype stores the individual components rather than only the final total.</p>
          <div className="table-wrap">
            <table>
              <thead><tr><th>Criterion</th><th>Maximum</th></tr></thead>
              <tbody>
                {transparencyCriteria.map((criterion) => (
                  <tr key={criterion.key}><td>{criterion.label}</td><td><strong>{criterion.max}</strong></td></tr>
                ))}
                <tr><td><strong>Total</strong></td><td><strong>33</strong></td></tr>
              </tbody>
            </table>
          </div>

          <h2>Coverage as of this build</h2>
          <p>
            The published project universe is {TARGET_MUNICIPALITIES} municipalities. This reconstruction currently has {VERIFIED_TRANSPARENCY_TOTALS} verified 2023 totals, including {VERIFIED_COMPONENT_BREAKDOWNS} with all ten component values. The remaining 19 records are Quebec municipalities whose detailed source table is still being recovered.
          </p>
          <p>No pending municipality is assigned a zero. Missing evidence is represented as pending evidence.</p>

          <h2>Financial observations</h2>
          <p>
            The financial model mirrors the legacy LGPI categories, but the extraction layer keeps the original municipal source beside every normalized field. A value is published only when the source concept is sufficiently aligned with the legacy LGPI field.
          </p>
          <p>
            Values use explicit states: <span className="codeish">reported</span>, <span className="codeish">pending_review</span>, <span className="codeish">not_reported</span>, <span className="codeish">not_applicable</span>, and <span className="codeish">source_unavailable</span>. A blank is never silently converted to zero.
          </p>

          <h2>Household normalization</h2>
          <p>
            Legacy LGPI pages display totals, dollars per household, and percentage of provincial average. This prototype deliberately withholds the latter two until the exact 2023 dwelling denominators and aggregation rules are source-verified. The rebuild will preserve historical comparability rather than substituting population without disclosure.
          </p>

          <h2>Known source conflicts</h2>
          <p>Where two Frontier publications disagree, the detailed report table is used provisionally and the conflict remains visible for editorial review.</p>
          <ul>
            {sourceDiscrepancies.map((item) => <li key={item.municipality}><strong>{item.municipality}:</strong> {item.issue}</li>)}
          </ul>

          <h2>Primary source</h2>
          <p><a href={REPORT_URL} target="_blank" rel="noreferrer">Frontier Centre — Local Government Performance Index 2025 report ↗</a></p>
        </div>
      </section>
    </main>
  );
}
