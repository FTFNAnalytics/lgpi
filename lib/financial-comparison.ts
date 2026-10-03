import type { FinancialObservation } from "./lgpi-data";

export const coreMetricKeys = ["total_revenue", "total_expenditure", "long_term_debt", "capital_assets"];

type FinancialChange = {
  changeThousands: number | null;
  percentChange: number | null;
  explanation: string | null;
};

/** Compare accepted, consecutive annual observations on the same municipality/metric. */
export function getFinancialChange(
  prior: FinancialObservation | undefined,
  current: FinancialObservation | undefined,
): FinancialChange {
  const withheld = (explanation: string): FinancialChange => ({
    changeThousands: null, percentChange: null, explanation,
  });
  if (!prior || !current) return withheld("Both years need a reported value to calculate change.");
  if (prior.municipalitySlug !== current.municipalitySlug || prior.metric !== current.metric || current.year !== prior.year + 1) {
    return withheld("Year-over-year change requires the same municipality and metric in consecutive years.");
  }
  if (prior.status === "pending_review" || current.status === "pending_review") {
    return withheld("Mapping under review — change withheld.");
  }
  if (prior.status !== "reported" || current.status !== "reported" ||
      prior.valueThousands === null || current.valueThousands === null ||
      !Number.isFinite(prior.valueThousands) || !Number.isFinite(current.valueThousands)) {
    return withheld("Both years need a reported value to calculate change.");
  }
  const changeThousands = current.valueThousands - prior.valueThousands;
  return {
    changeThousands,
    percentChange: prior.valueThousands > 0 ? changeThousands / prior.valueThousands * 100 : null,
    explanation: prior.valueThousands === 0
      ? "Percentage change is undefined from a zero baseline."
      : prior.valueThousands < 0
        ? "Percentage change is not shown for a negative baseline."
        : null,
  };
}
