"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { transparency2023 } from "@/lib/lgpi-data";

export function MunicipalitySearch() {
  const [query, setQuery] = useState("");
  const matches = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return transparency2023.slice(0, 8);
    return transparency2023
      .filter((record) =>
        [record.name, record.provinceName, record.province].some((value) =>
          value.toLowerCase().includes(q),
        ),
      )
      .slice(0, 8);
  }, [query]);

  return (
    <div>
      <label htmlFor="city-search" className="eyebrow" style={{ color: "#ead9b6" }}>
        Find a municipality
      </label>
      <input
        id="city-search"
        value={query}
        onChange={(event) => setQuery(event.target.value)}
        placeholder="Try Calgary, Toronto, Burnaby…"
        style={{ maxWidth: 620, marginTop: 8 }}
      />
      {query && (
        <div className="card" style={{ maxWidth: 620, padding: 0, marginTop: 8 }}>
          {matches.length ? matches.map((record) => (
            <Link
              key={record.slug}
              href={"/cities/" + record.slug}
              className="city-link"
              style={{ border: 0, borderBottom: "1px solid #e7e2d8" }}
            >
              <strong>{record.name}</strong>
              <span>{record.province} · {record.score}/33</span>
            </Link>
          )) : (
            <div className="empty-state">No verified 2023 record matches that search yet.</div>
          )}
        </div>
      )}
    </div>
  );
}
