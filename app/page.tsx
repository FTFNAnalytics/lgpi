import Link from "next/link";
import { MunicipalitySearch } from "@/components/municipality-search";
import {
  financial2023,
  TARGET_MUNICIPALITIES,
  VERIFIED_COMPONENT_BREAKDOWNS,
  VERIFIED_TRANSPARENCY_TOTALS,
  transparency2023,
} from "@/lib/lgpi-data";

export default function Home() {
  const leaders = transparency2023.filter((record) => record.score === Math.max(...transparency2023.map((x) => x.score)));

  return (
    <main>
      <section className="hero">
        <div className="shell">
          <p className="eyebrow">2023 public reconstruction · working prototype</p>
          <h1>Canadian municipal finance, made inspectable.</h1>
          <p className="hero-deck">
            A modern reconstruction of the Local Government Performance Index using the published 33-point transparency methodology and source-cited municipal financial records.
          </p>
          <div style={{ marginTop: 30 }}>
            <MunicipalitySearch />
          </div>
          <div className="hero-actions">
            <Link className="button primary" href="/transparency">Explore the 2023 index</Link>
            <Link className="button secondary" href="/methodology">See methodology & provenance</Link>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="shell">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Reconstruction status</p>
              <h2>Evidence first. Missing never means zero.</h2>
            </div>
            <p>The prototype publishes only observations recoverable from the LGPI report or official municipal financial records. Pending research stays visibly pending.</p>
          </div>
          <div className="stat-grid">
            <div className="stat"><strong>{VERIFIED_TRANSPARENCY_TOTALS}/{TARGET_MUNICIPALITIES}</strong><span>published 2023 scores loaded</span></div>
            <div className="stat"><strong>{VERIFIED_COMPONENT_BREAKDOWNS}</strong><span>municipalities with all 10 component scores loaded</span></div>
            <div className="stat"><strong>33</strong><span>maximum published transparency score</span></div>
            <div className="stat"><strong>{financial2023.length}</strong><span>official financial observations seeded so far</span></div>
          </div>
        </div>
      </section>

      <section className="section white">
        <div className="shell">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Highest published scores loaded</p>
              <h2>2023 transparency</h2>
            </div>
            <p>Transparency measures the quality and accessibility of financial reporting. It is not a rating of whether a municipality spends well.</p>
          </div>
          <div className="card-grid">
            {leaders.map((record) => (
              <article className="card" key={record.slug}>
                <span className="chip good">{record.provinceName}</span>
                <h2 style={{ marginTop: 15 }}>{record.name}</h2>
                <span className="metric-value">{record.score} / 33</span>
                <Link className="card-link" href={"/cities/" + record.slug}>Open profile →</Link>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="section">
        <div className="shell">
          <div className="card-grid">
            <article className="card">
              <p className="eyebrow">01</p>
              <h2>Transparency Index</h2>
              <p>Filter verified 2023 scores and inspect the ten published scoring components municipality by municipality.</p>
              <Link className="card-link" href="/transparency">Open index →</Link>
            </article>
            <article className="card">
              <p className="eyebrow">02</p>
              <h2>Compare municipalities</h2>
              <p>Place two municipalities side-by-side without pretending differing service responsibilities are directly equivalent.</p>
              <Link className="card-link" href="/compare">Compare →</Link>
            </article>
            <article className="card">
              <p className="eyebrow">03</p>
              <h2>Financial explorer</h2>
              <p>Browse the reconstructed legacy LGPI field catalogue and see which 2023 observations have verified source mappings.</p>
              <Link className="card-link" href="/metrics">Explore metrics →</Link>
            </article>
          </div>
        </div>
      </section>
    </main>
  );
}
