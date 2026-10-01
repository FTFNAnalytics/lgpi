import { TransparencyTable } from "@/components/transparency-table";
import {
  REPORT_URL,
  TARGET_MUNICIPALITIES,
  VERIFIED_COMPONENT_BREAKDOWNS,
  VERIFIED_TRANSPARENCY_TOTALS,
} from "@/lib/lgpi-data";

export default function TransparencyPage() {
  return (
    <main>
      <section className="page-hero">
        <div className="shell">
          <p className="eyebrow">LGPI · fiscal year 2023</p>
          <h1>Transparency Index</h1>
          <p>
            Reconstructed from the published 2025 LGPI report, which assesses municipal financial reporting for 2023 using a 33-point framework.
          </p>
        </div>
      </section>
      <section className="section">
        <div className="shell">
          <div className="stat-grid">
            <div className="stat"><strong>{VERIFIED_TRANSPARENCY_TOTALS}</strong><span>municipality totals recovered</span></div>
            <div className="stat"><strong>{VERIFIED_COMPONENT_BREAKDOWNS}</strong><span>full component breakdowns recovered</span></div>
            <div className="stat"><strong>{TARGET_MUNICIPALITIES - VERIFIED_TRANSPARENCY_TOTALS}</strong><span>Quebec records awaiting table extraction</span></div>
            <div className="stat"><strong>33</strong><span>maximum possible score</span></div>
          </div>
          <div className="notice" style={{ marginTop: 24 }}>
            <strong>Interpretation:</strong> this is a financial-reporting transparency measure, not a fiscal-health or government-performance verdict. A municipality can report clearly and still face fiscal challenges.
          </div>
          <TransparencyTable />
          <p style={{ color: "#65717c", marginTop: 22 }}>
            Primary reconstruction source: <a href={REPORT_URL} target="_blank" rel="noreferrer"><strong>Frontier Centre LGPI 2025 report ↗</strong></a>
          </p>
        </div>
      </section>
    </main>
  );
}
