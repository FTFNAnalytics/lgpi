"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { provinceNames, transparency2023 } from "@/lib/lgpi-data";

export function TransparencyTable() {
  const [query, setQuery] = useState("");
  const [province, setProvince] = useState("ALL");

  const rows = useMemo(() => {
    const q = query.trim().toLowerCase();
    return [...transparency2023]
      .filter((record) => province === "ALL" || record.province === province)
      .filter((record) => !q || record.name.toLowerCase().includes(q))
      .sort((a, b) => b.score - a.score || a.name.localeCompare(b.name));
  }, [query, province]);

  const provinceOptions = [...new Set(transparency2023.map((record) => record.province))].sort();

  return (
    <>
      <div className="filters">
        <input
          aria-label="Filter municipalities"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Filter municipalities"
        />
        <select
          aria-label="Filter by province"
          value={province}
          onChange={(event) => setProvince(event.target.value)}
        >
          <option value="ALL">All loaded provinces</option>
          {provinceOptions.map((code) => (
            <option value={code} key={code}>{provinceNames[code]}</option>
          ))}
        </select>
      </div>
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Municipality</th>
              <th>Province</th>
              <th>2023 score</th>
              <th>Evidence loaded</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((record) => (
              <tr key={record.slug}>
                <td><Link href={"/cities/" + record.slug}><strong>{record.name}</strong></Link></td>
                <td>{record.provinceName}</td>
                <td><span className="score">{record.score}</span> / 33</td>
                <td>
                  <span className={"chip " + (record.components ? "good" : "pending")}>
                    {record.components ? "components + total" : "total verified"}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p style={{ color: "#65717c", fontSize: ".8rem" }}>{rows.length} verified records shown.</p>
    </>
  );
}
