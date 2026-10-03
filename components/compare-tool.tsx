"use client";

import { useMemo, useState } from "react";
import { FinancialValue } from "@/components/financial-value";
import { coreMetricKeys } from "@/lib/financial-comparison";
import {
  availableFinancialYears,
  FinancialYear,
  getComponentRows,
  getFinancialObservations,
  getFinancialSourceUnavailable,
  getMetricDefinition,
  metricCatalog,
  municipalities2023,
} from "@/lib/lgpi-data";

export function CompareTool() {
  const [leftSlug, setLeftSlug] = useState("calgary");
  const [rightSlug, setRightSlug] = useState("edmonton");
  const [leftYear, setLeftYear] = useState<FinancialYear>(2024);
  const [rightYear, setRightYear] = useState<FinancialYear>(2024);
  const left = municipalities2023.find((record) => record.slug === leftSlug)!;
  const right = municipalities2023.find((record) => record.slug === rightSlug)!;

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
    const a = getFinancialObservations(leftSlug, leftYear);
    const b = getFinancialObservations(rightSlug, rightYear);
    const keys = [...new Set([...a.map((x) => x.metric), ...b.map((x) => x.metric)])];
    const catalogOrder = new Map(metricCatalog.map((metric, index) => [metric.key, index]));
    return keys
      .map((key) => ({
        key,
        label: getMetricDefinition(key)?.label ?? key,
        left: a.find((x) => x.metric === key),
        right: b.find((x) => x.metric === key),
      }))
      .sort((a, b) => (catalogOrder.get(a.key) ?? 999) - (catalogOrder.get(b.key) ?? 999));
  }, [leftSlug, rightSlug, leftYear, rightYear]);

  const leftUnavailable = getFinancialSourceUnavailable(leftSlug, leftYear);
  const rightUnavailable = getFinancialSourceUnavailable(rightSlug, rightYear);
  const coreRows = coreMetricKeys
    .map((key) => financialRows.find((row) => row.key === key))
    .filter((row): row is NonNullable<typeof row> => Boolean(row));

  const options = [...municipalities2023].sort((a, b) => a.name.localeCompare(b.name));

  return (
    <>
      <div className="compare-selector-grid">
        <div className="compare-selector-card">
          <label>
            <span className="eyebrow">Municipality A</span>
            <select value={leftSlug} onChange={(event) => setLeftSlug(event.target.value)}>
              {options.map((record) => <option key={record.slug} value={record.slug}>{record.name}, {record.province}</option>)}
            </select>
          </label>
          <label>
            <span className="eyebrow">Financial year A</span>
            <select value={leftYear} onChange={(event) => setLeftYear(Number(event.target.value) as FinancialYear)}>
              {availableFinancialYears.map((year) => <option key={year} value={year}>{year}</option>)}
            </select>
          </label>
        </div>
        <div className="compare-selector-card">
          <label>
            <span className="eyebrow">Municipality B</span>
            <select value={rightSlug} onChange={(event) => setRightSlug(event.target.value)}>
              {options.map((record) => <option key={record.slug} value={record.slug}>{record.name}, {record.province}</option>)}
            </select>
          </label>
          <label>
            <span className="eyebrow">Financial year B</span>
            <select value={rightYear} onChange={(event) => setRightYear(Number(event.target.value) as FinancialYear)}>
              {availableFinancialYears.map((year) => <option key={year} value={year}>{year}</option>)}
            </select>
          </label>
        </div>
      </div>

      <div className="stat-grid" style={{ marginTop: 24 }}>
        <div className="stat"><strong>{leftYear}</strong><span>{left.name} financial year</span></div>
        <div className="stat"><strong>{rightYear}</strong><span>{right.name} financial year</span></div>
        <div className="stat"><strong>{!left.transparencyPublished ? "—" : left.components ? "10/10" : "Total"}</strong><span>{left.name} component evidence</span></div>
        <div className="stat"><strong>{!right.transparencyPublished ? "—" : right.components ? "10/10" : "Total"}</strong><span>{right.name} component evidence</span></div>
      </div>

      <h2 style={{ marginTop: 38 }}>2023 transparency components</h2>
      <p className="metric-meta">Published 2023 evidence stays fixed when financial years change.</p>
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
      ) : <div className="empty-state">Published component scoring is unavailable for one or both selected municipalities. Quebec was not scored in the published 2023 LGPI edition.</div>}

      <h2 style={{ marginTop: 38 }}>Financial comparison</h2>
      <div className="notice" style={{ marginBottom: 16 }}>
        Amounts are in Canadian dollars, without inflation adjustment. Financial comparisons use the independently selected year for each municipality. Service responsibilities can differ substantially between municipalities. Review labels and source details accompany each value.
      </div>
      {[
        { city: left, year: leftYear, unavailable: leftUnavailable },
        { city: right, year: rightYear, unavailable: rightUnavailable },
      ].map(({ city, year, unavailable }, index) => unavailable && (
        <div className="notice" style={{ marginBottom: 16 }} key={index}>
          <strong>{city.name} · {year} source unavailable.</strong> {unavailable.reason} No missing financial value is treated as zero.
        </div>
      ))}

      {coreRows.length > 0 && (
        <div className="comparison-core-grid">
          {coreRows.map((row) => (
            <article className="comparison-core-card" key={"core-" + row.key}>
              <span className="eyebrow">{row.label}</span>
              <div className="comparison-values">
                <div>
                  <small>{left.name} · {leftYear}</small>
                  <FinancialValue observation={row.left} year={leftYear} sourceUnavailable={Boolean(leftUnavailable)} />
                </div>
                <div>
                  <small>{right.name} · {rightYear}</small>
                  <FinancialValue observation={row.right} year={rightYear} sourceUnavailable={Boolean(rightUnavailable)} />
                </div>
              </div>
            </article>
          ))}
        </div>
      )}

      <h2 style={{ marginTop: 38 }}>Full mapped field set</h2>
      {financialRows.length ? (
        <div className="table-wrap">
          <table>
            <thead><tr><th>Metric</th><th>{left.name} · {leftYear}</th><th>{right.name} · {rightYear}</th></tr></thead>
            <tbody>
              {financialRows.map((row) => (
                <tr key={row.key}>
                  <td>{row.label}</td>
                  <td><FinancialValue observation={row.left} year={leftYear} sourceUnavailable={Boolean(leftUnavailable)} /></td>
                  <td><FinancialValue observation={row.right} year={rightYear} sourceUnavailable={Boolean(rightUnavailable)} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : <div className="empty-state">No mapped financial observations are available for the selected municipalities and years.</div>}
    </>
  );
}
