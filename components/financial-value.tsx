import { FinancialObservation, formatThousands } from "@/lib/lgpi-data";

/** Keep a value's evidence state visible wherever it is compared. */
export function FinancialValue({ observation, year, sourceUnavailable = false }: {
  observation?: FinancialObservation;
  year: number;
  sourceUnavailable?: boolean;
}) {
  const status = observation?.status.replaceAll("_", " ") ?? (sourceUnavailable ? "source unavailable" : "not loaded");
  return (
    <div className="financial-value">
      <strong>{formatThousands(observation?.valueThousands ?? null)}</strong>
      <span className={"chip " + (observation?.status === "reported" ? "good" : "pending")}>{status}</span>
      {observation && (
        <details className="value-evidence">
          <summary>{year} source details</summary>
          <p>{observation.sourceReportedLabel ?? observation.sourceLabel}</p>
          <p>{observation.sourceLocation}</p>
          {observation.note && <p>{observation.note}</p>}
          <a className="source-link" href={observation.sourceUrl} target="_blank" rel="noreferrer">Open {year} official source ↗</a>
        </details>
      )}
    </div>
  );
}
