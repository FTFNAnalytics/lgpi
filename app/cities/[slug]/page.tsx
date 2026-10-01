import { notFound } from "next/navigation";
import {
  formatThousands,
  getComponentRows,
  getFinancialObservations,
  getMetricDefinition,
  getMunicipality,
  sourceDiscrepancies,
  transparency2023,
} from "@/lib/lgpi-data";

export function generateStaticParams() {
  return transparency2023.map((record) => ({ slug: record.slug }));
}

export default async function CityPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const record = getMunicipality(slug);
  if (!record) notFound();

  const components = getComponentRows(record);
  const financial = getFinancialObservations(slug);
  const discrepancy = sourceDiscrepancies.find((item) => item.municipality === record.name);

  return (
    <main>
      <section className="page-hero">
        <div className="shell city-head">
          <div>
            <p className="eyebrow">{record.provinceName} · fiscal year 2023</p>
            <h1 className="city-title">{record.name}</h1>
            <p>Source-cited reconstruction status: <strong>{record.components ? "component table verified" : "published total verified"}</strong>.</p>
          </div>
          <div className="big-score">
            {record.score}<small>Transparency score / 33</small>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="shell">
          {discrepancy && <div className="notice" style={{ marginBottom: 26 }}><strong>Source discrepancy under review:</strong> {discrepancy.issue}</div>}

          <div className="section-heading">
            <div>
              <p className="eyebrow">Published scoring evidence</p>
              <h2>Transparency components</h2>
            </div>
            <p>Component values are transcribed from the detailed regional tables where those tables have been recovered.</p>
          </div>

          {components.length ? (
            <div className="component-grid">
              {components.map((row) => (
                <div className="component" key={row.key}>
                  <span>{row.label}</span>
                  <strong>{row.value} / {row.max}</strong>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-state">
              The 2023 total is verified, but its ten component values are not yet loaded. No component scores have been inferred.
            </div>
          )}

          <p style={{ marginTop: 16 }}>
            <a className="source-link" href={record.sourceUrl} target="_blank" rel="noreferrer">Open transparency source ↗</a>
          </p>
        </div>
      </section>

      <section className="section white">
        <div className="shell">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Official-source ingestion</p>
              <h2>2023 financial observations</h2>
            </div>
            <p>Amounts below are source-mapped observations only. Per-household and provincial-average calculations stay off until their denominators and legacy mappings are independently verified.</p>
          </div>
          {financial.length ? (
            <div className="metric-grid">
              {financial.map((observation) => {
                const metric = getMetricDefinition(observation.metric);
                return (
                  <article className="metric-card" key={observation.metric}>
                    <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                      <span className={"chip " + (observation.status === "reported" ? "good" : "pending")}>
                        {observation.status.replaceAll("_", " ")}
                      </span>
                      {observation.mappingMethod && (
                        <span className="chip pending">{observation.mappingMethod.replaceAll("_", " ")}</span>
                      )}
                    </div>
                    <h3>{metric?.label ?? observation.metric}</h3>
                    <span className="metric-value">{formatThousands(observation.valueThousands)}</span>
                    {observation.sourceReportedLabel && (
                      <p className="metric-meta"><strong>Source field:</strong> {observation.sourceReportedLabel}</p>
                    )}
                    <p className="metric-meta">{observation.sourceLocation}</p>
                    {observation.note && <p className="metric-meta">{observation.note}</p>}
                    <a className="source-link" href={observation.sourceUrl} target="_blank" rel="noreferrer">Open official source ↗</a>
                  </article>
                );
              })}
            </div>
          ) : (
            <div className="empty-state">
              Transparency evidence is loaded; 2023 financial field mapping for this municipality is still queued. This is not a zero-value record.
            </div>
          )}
        </div>
      </section>
    </main>
  );
}
