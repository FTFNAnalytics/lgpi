import Link from "next/link";
import {
  financialObservationCount,
  municipalities2023,
  municipalitiesWithFinancialObservations,
  provinceNames,
  TARGET_MUNICIPALITIES,
} from "@/lib/lgpi-data";

export default function CitiesPage() {
  const provinces = [...new Set(municipalities2023.map((record) => record.province))].sort();

  return (
    <main>
      <section className="page-hero">
        <div className="shell">
          <p className="eyebrow">2023 municipal profiles</p>
          <h1>Explore cities</h1>
          <p>Browse the complete 2023 LGPI municipality universe. Each profile separates published transparency evidence from reconstructed official-source financial data.</p>
        </div>
      </section>
      <section className="section">
        <div className="shell">
          <div className="stat-grid" style={{ marginBottom: 42 }}>
            <div className="stat"><strong>{TARGET_MUNICIPALITIES}/99</strong><span>municipalities represented</span></div>
            <div className="stat"><strong>{municipalitiesWithFinancialObservations}</strong><span>with financial observations</span></div>
            <div className="stat"><strong>{financialObservationCount.toLocaleString("en-CA")}</strong><span>source-backed observations</span></div>
            <div className="stat"><strong>2023</strong><span>fiscal-year reconstruction</span></div>
          </div>
          {provinces.map((province) => {
            const rows = municipalities2023
              .filter((record) => record.province === province)
              .sort((a, b) => a.name.localeCompare(b.name));
            return (
              <section key={province} style={{ marginBottom: 42 }}>
                <div className="section-heading">
                  <h2>{provinceNames[province]}</h2>
                  <p>{rows.length} LGPI municipalities</p>
                </div>
                <div className="city-list">
                  {rows.map((record) => (
                    <Link className="city-link" href={"/cities/" + record.slug} key={record.slug}>
                      <strong>{record.name}</strong>
                      <span>{record.score === null ? "Transparency unscored" : `${record.score}/33`}</span>
                    </Link>
                  ))}
                </div>
              </section>
            );
          })}
          <div className="notice">
            <strong>Quebec:</strong> all 19 LGPI municipalities now have 2023 financial profiles from MAMH. The published LGPI report omitted Quebec transparency scoring, so those profiles are shown as unscored rather than zero.
          </div>
        </div>
      </section>
    </main>
  );
}
