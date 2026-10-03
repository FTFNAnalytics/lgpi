import { MetricExplorer } from "@/components/metric-explorer";
import { metricCatalog } from "@/lib/lgpi-data";

export default function MetricsPage() {
  return (
    <main>
      <section className="page-hero">
        <div className="shell">
          <p className="eyebrow">Financial data · 2023–2024</p>
          <h1>Metric Explorer</h1>
          <p>The old LGPI financial field structure has been reconstructed as a {metricCatalog.length}-metric catalogue. Choose a financial year and metric; values appear only after an official-source mapping is verified.</p>
        </div>
      </section>
      <section className="section">
        <div className="shell">
          <div className="notice" style={{ marginBottom: 24 }}>
            <strong>Comparison caution:</strong> Canadian municipalities do not all deliver the same bundle of services. This matters especially in two-tier systems. Raw expenditure differences should not be read as direct efficiency rankings.
          </div>
          <MetricExplorer />
        </div>
      </section>
    </main>
  );
}
