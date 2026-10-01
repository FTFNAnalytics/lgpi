import Link from "next/link";
import { provinceNames, transparency2023 } from "@/lib/lgpi-data";

export default function CitiesPage() {
  const provinces = [...new Set(transparency2023.map((record) => record.province))].sort();

  return (
    <main>
      <section className="page-hero">
        <div className="shell">
          <p className="eyebrow">2023 municipal profiles</p>
          <h1>Explore cities</h1>
          <p>Open any verified municipality to inspect its transparency score, component evidence, source notes, and financial observations loaded so far.</p>
        </div>
      </section>
      <section className="section">
        <div className="shell">
          {provinces.map((province) => {
            const rows = transparency2023
              .filter((record) => record.province === province)
              .sort((a, b) => a.name.localeCompare(b.name));
            return (
              <section key={province} style={{ marginBottom: 42 }}>
                <div className="section-heading">
                  <h2>{provinceNames[province]}</h2>
                  <p>{rows.length} verified 2023 records</p>
                </div>
                <div className="city-list">
                  {rows.map((record) => (
                    <Link className="city-link" href={"/cities/" + record.slug} key={record.slug}>
                      <strong>{record.name}</strong>
                      <span>{record.score}/33</span>
                    </Link>
                  ))}
                </div>
              </section>
            );
          })}
          <div className="notice">
            <strong>Quebec:</strong> 19 municipalities remain in the source-extraction queue. They are intentionally not represented as zero or missing-score records.
          </div>
        </div>
      </section>
    </main>
  );
}
