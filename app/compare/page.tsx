import { CompareTool } from "@/components/compare-tool";

export default function ComparePage() {
  return (
    <main>
      <section className="page-hero">
        <div className="shell">
          <p className="eyebrow">Side-by-side · 2023</p>
          <h1>Compare municipalities</h1>
          <p>Compare published transparency components and source-mapped financial observations without collapsing different municipal service responsibilities into a single fiscal verdict.</p>
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
