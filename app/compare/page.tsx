import { CompareTool } from "@/components/compare-tool";

export default function ComparePage() {
  return (
    <main>
      <section className="page-hero">
        <div className="shell">
          <p className="eyebrow">Side-by-side · 2023–2024</p>
          <h1>Compare municipalities</h1>
          <p>Compare published 2023 transparency components and source-mapped 2023 or 2024 financial observations. Each municipality can use a different financial year without collapsing service differences into a single fiscal verdict.</p>
        </div>
      </section>
      <section className="section">
        <div className="shell">
          <CompareTool />
        </div>
      </section>
    </main>
  );
}
