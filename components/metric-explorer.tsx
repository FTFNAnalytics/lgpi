"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import {
  financial2023,
  formatThousands,
  getMetricDefinition,
  metricCatalog,
  transparency2023,
} from "@/lib/lgpi-data";

export function MetricExplorer() {
  const seededMetric = financial2023[0]?.metric ?? metricCatalog[0].key;
  const [metric, setMetric] = useState(seededMetric);

  const rows = useMemo(() => (
    financial2023
      .filter((observation) => observation.metric === metric)
      .map((observation) => ({
        observation,
        municipality: transparency2023.find((record) => record.slug === observation.municipalitySlug),
      }))
      .sort((a, b) => (b.observation.valueThousands ?? -Infinity) - (a.observation.valueThousands ?? -Infinity))
  ), [metric]);

  const definition = getMetricDefinition(metric);

  return (
    <>
      <label>
        <span className="eyebrow">Legacy LGPI metric</span>
        <select value={metric} onChange={(event) => setMetric(event.target.value)}>
          {metricCatalog.map((item) => (
            <option key={item.key} value={item.key}>{item.section} — {item.label}</option>
          ))}
        </select>
      </label>
      <div style={{ margin: "20px 0" }}>
        <h2 style={{ marginBottom: 4 }}>{definition?.label}</h2>
        <span className="chip good">{definition?.section}</span>
      </div>
      {rows.length ? (
        <div className="table-wrap">
          <table>
            <thead><tr><th>Municipality</th><th>2023 reported value</th><th>Status</th><th>Source</th></tr></thead>
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
          This metric is part of the reconstructed LGPI field catalogue, but no 2023 observation has passed source mapping yet.
        </div>
      )}
    </>
  );
}
