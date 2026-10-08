#!/usr/bin/env python3
"""Compute simple historical financial metrics from audited Group CSV files.

This analysis contains no forecast, fair value or security recommendation.
Usage: python scripts/analyze.py [--check]
"""
import argparse
import csv
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"

def load(filename):
    with (DATA / filename).open(newline="", encoding="utf-8") as handle:
        return {r["metric"]: r for r in csv.DictReader(handle)}

I, B, C = (
    load("income_statement.csv"),
    load("balance_sheet.csv"),
    load("cash_flow.csv"),
)

def n(table, name, year):
    return float(table[name][f"FY{year}"])

def metric_values(year):
    revenue = n(I, "Revenue", year)
    profit = n(I, "Profit after tax", year)
    operating_cash = n(C, "Net operating cash flow", year)
    return {
        "gross_margin_pct": 100 * n(I, "Gross profit", year) / revenue,
        "operating_margin_pct": 100 * n(I, "Operating profit", year) / revenue,
        "net_margin_pct": 100 * profit / revenue,
        "effective_tax_rate_pct": -100 * n(I, "Income tax expense", year) / n(I, "Profit before tax", year),
        "finance_cost_to_revenue_pct": -100 * n(I, "Finance costs", year) / revenue,
        "cfo_to_profit": operating_cash / profit,
        "current_ratio": n(B, "Total current assets", year) / n(B, "Total current liabilities", year),
        # For historical analysis ONLY. Not FCFF suitable for discounting in an EV DCF.
        "post_capex_cash_proxy_ngn_m": (
            operating_cash + n(C, "Cash purchase of PPE", year) +
            n(C, "Intangible asset purchases", year)
        ),
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="assert historical benchmark figures")
    args = parser.parse_args()
    rows = {year: metric_values(year) for year in (2024, 2025)}
    for name in rows[2024]:
        suffix = "%" if name.endswith("_pct") else (" ₦m" if name.endswith("_ngn_m") else "x")
        print(f"{name:36s} {rows[2024][name]:12,.2f}{suffix} | {rows[2025][name]:12,.2f}{suffix}")
    revenue_growth = 100 * (n(I, "Revenue", 2025) / n(I, "Revenue", 2024) - 1)
    profit_growth = 100 * (n(I, "Profit after tax", 2025) / n(I, "Profit after tax", 2024) - 1)
    print(f"Revenue growth (2025): {revenue_growth:.2f}%")
    print(f"Profit growth (2025): {profit_growth:.2f}%")
    if args.check:
        benchmarks = {
            (2024, "gross_margin_pct"): 54.0391559956,
            (2025, "gross_margin_pct"): 62.0491679948,
            (2024, "net_margin_pct"): 14.0550194802,
            (2025, "net_margin_pct"): 23.5660728018,
            (2024, "post_capex_cash_proxy_ngn_m"): 397730,
            (2025, "post_capex_cash_proxy_ngn_m"): 1213036,
        }
        for (year, metric), expected in benchmarks.items():
            assert abs(rows[year][metric] - expected) < 0.0001, f"{year} {metric} did not reconcile"
        assert round(revenue_growth, 2) == 20.28
        assert round(profit_growth, 2) == 101.67
        print("PASS: historical metric checks")

if __name__ == "__main__":
    main()
