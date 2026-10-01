"use client";

import { useMemo, useState } from "react";
import {
  getComponentRows,
  getFinancialObservations,
  getMetricDefinition,
  formatThousands,
  transparency2023,
} from "@/lib/lgpi-data";

export function CompareTool() {
  const [leftSlug, setLeftSlug] = useState("calgary");
  const [rightSlug, setRightSlug] = useState("edmonton");
  const left = transparency2023.find((record) => record.slug === leftSlug)!;
  const right = transparency2023.find((record) => record.slug === rightSlug)!;

  const componentRows = useMemo(() => {
    const a = getComponentRows(left);
    const b = getComponentRows(right);
    return a.map((row, index) => ({
      label: row.label,
      max: row.max,
      left: row.value,
      right: b[index]?.value ?? null,
    }));
  }, [left, right]);

  const financialRows = useMemo(() => {
    const a = getFinancialObservations(leftSlug);
    const b = getFinancialObservations(rightSlug);
    const keys = [...new Set([...a.map((x) => x.metric), ...b.map((x) => x.metric)])];
    return keys.map((key) => ({
      key,
      label: getMetricDefinition(key)?.label ?? key,
      left: a.find((x) => x.metric === key),
      right: b.find((x) => x.metric === key),
    }));
  }, [leftSlug, rightSlug]);

  const options = [...transparency2023].sort((a, b) => a.name.localeCompare(b.name));

  return (
    <>
      <div className="two-col">
        <label>
          <span className="eyebrow">Municipality A</span>
          <select value={leftSlug} onChange={(event) => setLeftSlug(event.target.value)}>
            {options.map((record) => <option key={record.slug} value={record.slug}>{record.name}, {record.province}</option>)}
          </select>
        </label>
        <label>
          <span className="eyebrow">Municipality B</span>
          <select value={rightSlug} onChange={(event) => setRightSlug(event.target.value)}>
            {options.map((record) => <option key={record.slug} value={record.slug}>{record.name}, {record.province}</option>)}
          </select>
        </label>
      </div>

      <div className="stat-grid" style={{ marginTop: 24 }}>
        <div className="stat"><strong>{left.score}/33</strong><span>{left.name} transparency score</span></div>
        <div className="stat"><strong>{right.score}/33</strong><span>{right.name} transparency score</span></div>
        <div className="stat"><strong>{left.components ? "10/10" : "Total"}</strong><span>{left.name} component evidence</span></div>
        <div className="stat"><strong>{right.components ? "10/10" : "Total"}</strong><span>{right.name} component evidence</span></div>
      </div>

      <h2 style={{ marginTop: 38 }}>Transparency components</h2>
      {componentRows.length && right.components ? (
        <div className="table-wrap">
          <table>
            <thead><tr><th>Criterion</th><th>{left.name}</th><th>{right.name}</th><th>Maximum</th></tr></thead>
            <tbody>
              {componentRows.map((row) => (
                <tr key={row.label}>
                  <td>{row.label}</td>
                  <td><strong>{row.left}</strong></td>
                  <td><strong>{row.right}</strong></td>
                  <td>{row.max}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : <div className="empty-state">Component-level evidence is not yet loaded for both selected municipalities.</div>}

      <h2 style={{ marginTop: 38 }}>Verified financial observations</h2>
      <div className="notice" style={{ marginBottom: 16 }}>
        Financial comparisons are shown only where the reconstruction has source-mapped 2023 observations. Service responsibilities can differ substantially between municipalities.
      </div>
      {financialRows.length ? (
        <div className="table-wrap">
          <table>
            <thead><tr><th>Metric</th><th>{left.name}</th><th>{right.name}</th></tr></thead>
            <tbody>
              {financialRows.map((row) => (
                <tr key={row.key}>
                  <td>{row.label}</td>
                  <td>{row.left?.valueThousands != null ? formatThousands(row.left.valueThousands) : "—"}</td>
                  <td>{row.right?.valueThousands != null ? formatThousands(row.right.valueThousands) : "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : <div className="empty-state">No mapped financial observations overlap with this comparison yet.</div>}
    </>
  );
}
