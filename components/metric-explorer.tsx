"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import {
  availableFinancialYears,
  FinancialYear,
  financialByYear,
  formatThousands,
  getMetricDefinition,
  metricCatalog,
  municipalities2023,
} from "@/lib/lgpi-data";

export function MetricExplorer() {
  const [year, setYear] = useState<FinancialYear>(2024);
  const seededMetric = financialByYear[2024][0]?.metric ?? metricCatalog[0].key;
  const [metric, setMetric] = useState(seededMetric);

  const rows = useMemo(() => (
    financialByYear[year]
      .filter((observation) => observation.metric === metric)
      .map((observation) => ({
        observation,
        municipality: municipalities2023.find((record) => record.slug === observation.municipalitySlug),
      }))
      .sort((a, b) => (b.observation.valueThousands ?? -Infinity) - (a.observation.valueThousands ?? -Infinity))
  ), [metric, year]);

  const definition = getMetricDefinition(metric);

  return (
    <>
      <div className="two-col">
        <label>
          <span className="eyebrow">Legacy LGPI metric</span>
          <select value={metric} onChange={(event) => setMetric(event.target.value)}>
            {metricCatalog.map((item) => (
              <option key={item.key} value={item.key}>{item.section} — {item.label}</option>
            ))}
          </select>
        </label>
        <label>
          <span className="eyebrow">Financial year</span>
          <select value={year} onChange={(event) => setYear(Number(event.target.value) as FinancialYear)}>
            {availableFinancialYears.map((item) => <option key={item} value={item}>{item}</option>)}
          </select>
        </label>
      </div>
      <div style={{ margin: "20px 0" }}>
        <h2 style={{ marginBottom: 4 }}>{definition?.label}</h2>
        <span className="chip good">{definition?.section}</span>
      </div>
      {rows.length ? (
        <div className="table-wrap">
          <table>
            <thead><tr><th>Municipality</th><th>{year} reported value</th><th>Status</th><th>Source</th></tr></thead>
            <tbody>
              {rows.map(({ observation, municipality }) => (
                <tr key={observation.municipalitySlug}>
                  <td>
                    {municipality ? <Link href={"/cities/" + municipality.slug}><strong>{municipality.name}</strong></Link> : observation.municipalitySlug}
                  </td>
                  <td>{formatThousands(observation.valueThousands)}</td>
                  <td><span className={"chip " + (observation.status === "reported" ? "good" : "pending")}>{observation.status.replaceAll("_", " ")}</span></td>
                  <td><a className="source-link" href={observation.sourceUrl} target="_blank" rel="noreferrer">Official report ↗</a></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="empty-state">
          This metric is part of the reconstructed LGPI field catalogue, but no {year} observation has passed source mapping yet.
        </div>
      )}
    </>
  );
}
