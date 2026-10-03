import Link from "next/link";
import { notFound } from "next/navigation";
import {
  availableFinancialYears,
  FinancialYear,
  formatThousands,
  getFinancialObservation,
  getComponentRows,
  getFinancialObservations,
  getFinancialSourceUnavailable,
  getMetricDefinition,
  getMunicipality,
  municipalities2023,
  sourceDiscrepancies,
} from "@/lib/lgpi-data";

export function generateStaticParams() {
  return municipalities2023.map((record) => ({ slug: record.slug }));
}

export default async function CityPage({
  params,
  searchParams,
}: {
  params: Promise<{ slug: string }>;
  searchParams: Promise<{ year?: string }>;
}) {
  const { slug } = await params;
  const query = await searchParams;
  const requestedYear = Number(query.year);
  const year: FinancialYear = requestedYear === 2023 ? 2023 : 2024;
  const record = getMunicipality(slug);
  if (!record) notFound();

  const components = getComponentRows(record);
  const financial = getFinancialObservations(slug, year);
  const financialSourceUnavailable = getFinancialSourceUnavailable(slug, year);
  const discrepancy = sourceDiscrepancies.find((item) => item.municipality === record.name);
  const reportedCount = financial.filter((observation) => observation.status === "reported").length;
  const pendingCount = financial.filter((observation) => observation.status === "pending_review").length;
  const coreMetricKeys = ["total_revenue", "total_expenditure", "long_term_debt", "capital_assets"];
  const coreFinancial = coreMetricKeys
    .map((key) => financial.find((observation) => observation.metric === key))
    .filter((observation): observation is NonNullable<typeof observation> => Boolean(observation));
  const trendRows = coreMetricKeys.map((metric) => ({
    metric,
    definition: getMetricDefinition(metric),
    prior: getFinancialObservation(slug, 2023, metric),
    current: getFinancialObservation(slug, 2024, metric),
  }));

  return (
    <main>
      <section className="page-hero">
        <div className="shell city-head">
          <div>
            <p className="eyebrow">{record.provinceName} · financial year {year}</p>
            <h1 className="city-title">{record.name}</h1>
            <p>
              Source-cited reconstruction status:{" "}
              <strong>
                {!record.transparencyPublished
                  ? "financial profile verified; transparency not published"
                  : record.components
                    ? "component table verified"
                    : "published total verified"}
              </strong>.
            </p>
          </div>
          <div className="big-score">
            {record.score === null ? "—" : record.score}
            <small>{record.score === null ? "Transparency score not published" : "Transparency score / 33"}</small>
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

          {!record.transparencyPublished ? (
            <div className="notice">
              <strong>Transparency score not published:</strong> the published 2023 LGPI edition explicitly omitted Quebec transparency scoring. This profile preserves that omission rather than calculating or assigning a score.
            </div>
          ) : components.length ? (
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

          {record.sourceUrl && (
            <p style={{ marginTop: 16 }}>
              <a className="source-link" href={record.sourceUrl} target="_blank" rel="noreferrer">Open transparency source ↗</a>
            </p>
          )}
        </div>
      </section>

      <section className="year-nav-section">
        <div className="shell">
          <div className="year-nav" aria-label="Financial year">
            <span className="year-nav-label">Financial year</span>
            {availableFinancialYears.map((item) => (
              <Link
                key={item}
                href={"/cities/" + slug + "?year=" + item}
                className={"year-tab " + (year === item ? "active" : "")}
              >
                {item}
              </Link>
            ))}
          </div>
          {year === 2024 && (
            <p className="year-context-note">
              Financial data shown for 2024. Transparency remains the published 2023 LGPI score because no later public transparency edition has been identified.
            </p>
          )}
        </div>
      </section>

      <section className="section tight">
        <div className="shell">
          <div className="section-heading compact-heading">
            <div>
              <p className="eyebrow">Year over year</p>
              <h2>2023 → 2024 core financial change</h2>
            </div>
            <p>The legacy site switches the full table by year; this summary adds a compact two-year comparison without replacing that interaction.</p>
          </div>
          <div className="yoy-grid">
            {trendRows.map((row) => {
              const prior = row.prior?.valueThousands ?? null;
              const current = row.current?.valueThousands ?? null;
              const change = prior !== null && current !== null ? current - prior : null;
              const percent = prior !== null && current !== null && prior !== 0
                ? (change! / Math.abs(prior)) * 100
                : null;
              return (
                <article className="yoy-card" key={row.metric}>
                  <span className="eyebrow">{row.definition?.label ?? row.metric}</span>
                  <div className="yoy-values">
                    <div><small>2023</small><strong>{formatThousands(prior)}</strong></div>
                    <div><small>2024</small><strong>{formatThousands(current)}</strong></div>
                  </div>
                  <p className="yoy-change">
                    {change === null
                      ? "Comparable value unavailable"
                      : `${change >= 0 ? "+" : "−"}${formatThousands(Math.abs(change))}${percent === null ? "" : ` · ${percent >= 0 ? "+" : ""}${percent.toFixed(1)}%`}`}
                  </p>
                </article>
              );
            })}
          </div>
        </div>
      </section>

      <section className="section white">
        <div className="shell">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Official-source ingestion</p>
              <h2>{year} financial observations</h2>
            </div>
            <p>Amounts below are source-mapped observations only. Per-household and provincial-average calculations stay off until their denominators and legacy mappings are independently verified.</p>
          </div>
          <div className="stat-grid" style={{ marginBottom: 24 }}>
            <div className="stat">
              <strong>{financial.length || "—"}</strong>
              <span>source-mapped financial observations</span>
            </div>
            <div className="stat">
              <strong>{reportedCount || "—"}</strong>
              <span>reported / accepted mappings</span>
            </div>
            <div className="stat">
              <strong>{pendingCount || "0"}</strong>
              <span>explicit pending-review mappings</span>
            </div>
            <div className="stat">
              <strong>{financialSourceUnavailable ? "Unavailable" : financial.length ? "Resolved" : "Pending"}</strong>
              <span>{year} financial-source status</span>
            </div>
          </div>

          {financialSourceUnavailable && (
            <div className="notice" style={{ marginBottom: 20 }}>
              <strong>{year} financial source unavailable:</strong> {financialSourceUnavailable.reason}
              The municipality remains in the LGPI universe; no missing financial value is treated as zero.
            </div>
          )}

          {coreFinancial.length > 0 && (
            <>
              <div className="section-heading compact-heading">
                <div>
                  <p className="eyebrow">Core financial snapshot</p>
                  <h2>At a glance</h2>
                </div>
                <p>Core fields shown first for presentation; the complete provenance-backed field set follows below.</p>
              </div>
              <div className="metric-grid core-metric-grid">
                {coreFinancial.map((observation) => {
                  const metric = getMetricDefinition(observation.metric);
                  return (
                    <article className="metric-card core-metric-card" key={"core-" + observation.metric}>
                      <span className={"chip " + (observation.status === "reported" ? "good" : "pending")}>
                        {observation.status.replaceAll("_", " ")}
                      </span>
                      <h3>{metric?.label ?? observation.metric}</h3>
                      <span className="metric-value">{formatThousands(observation.valueThousands)}</span>
                      <p className="metric-meta">{observation.sourceReportedLabel ?? observation.sourceLocation}</p>
                    </article>
                  );
                })}
              </div>
            </>
          )}

          {financial.length ? (
            <>
              <div className="section-heading compact-heading detailed-heading">
                <div>
                  <p className="eyebrow">Field-level evidence</p>
                  <h2>Detailed observations</h2>
                </div>
                <p>Every displayed value retains its original source concept, mapping status and official source link.</p>
              </div>
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
            </>
          ) : (
            <div className="empty-state">
              {financialSourceUnavailable
                ? "The official 2023 structured financial source is unavailable for this municipality. No zero values have been inferred."
                : "Transparency evidence is loaded; 2023 financial field mapping for this municipality is still queued. This is not a zero-value record."}
            </div>
          )}
        </div>
      </section>
    </main>
  );
}
