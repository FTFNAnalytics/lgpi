import Link from "next/link";
import { MunicipalitySearch } from "@/components/municipality-search";
import {
  financialObservationCount,
  municipalitiesWithFinancialObservations,
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
          <p className="eyebrow">LGPI 2023 · national reconstruction</p>
          <h1>Canadian municipal finance, rebuilt for inspection.</h1>
          <p className="hero-deck">
            The complete 99-municipality LGPI product universe, reconstructed from the published transparency methodology and official 2023 municipal financial sources.
          </p>
          <div style={{ marginTop: 30 }}>
            <MunicipalitySearch />
          </div>
          <div className="hero-actions">
            <Link className="button primary" href="/cities">Explore all 99 municipalities</Link>
            <Link className="button secondary" href="/coverage">View national coverage</Link>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="shell">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Reconstruction status</p>
              <h2>The 2023 source pass is complete.</h2>
            </div>
            <p>All 99 LGPI municipalities now have a resolved financial-data status. Missing, unavailable and broader-than-legacy source concepts remain explicit rather than being converted to zero.</p>
          </div>
          <div className="stat-grid">
            <div className="stat"><strong>{TARGET_MUNICIPALITIES}/99</strong><span>municipalities represented</span></div>
            <div className="stat"><strong>{municipalitiesWithFinancialObservations}</strong><span>municipalities with financial observations</span></div>
            <div className="stat"><strong>{VERIFIED_TRANSPARENCY_TOTALS}/80</strong><span>published non-Quebec transparency scores loaded</span></div>
            <div className="stat"><strong>{financialObservationCount.toLocaleString("en-CA")}</strong><span>official/source-backed 2023 observations</span></div>
          </div>
        </div>
      </section>

      <section className="section white">
        <div className="shell">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Presentation route</p>
              <h2>Three ways to see the rebuild working.</h2>
            </div>
            <p>Start with a source-rich city, compare two jurisdictions, then inspect the national evidence layer.</p>
          </div>
          <div className="card-grid">
            <article className="card feature-card">
              <span className="chip good">City profile</span>
              <h2 style={{ marginTop: 14 }}>Calgary</h2>
              <p>Full transparency components plus structured Alberta financial-source mappings and provenance.</p>
              <Link className="card-link" href="/cities/calgary">Open Calgary →</Link>
            </article>
            <article className="card feature-card">
              <span className="chip good">Cross-jurisdiction</span>
              <h2 style={{ marginTop: 14 }}>Compare cities</h2>
              <p>Contrast transparency and source-backed financial fields without collapsing different service structures into a single score.</p>
              <Link className="card-link" href="/compare">Open comparison →</Link>
            </article>
            <article className="card feature-card">
              <span className="chip good">National evidence</span>
              <h2 style={{ marginTop: 14 }}>Coverage</h2>
              <p>See the full 99-city status, source availability, observations and deliberately withheld calculated views.</p>
              <Link className="card-link" href="/coverage">Open coverage →</Link>
            </article>
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
