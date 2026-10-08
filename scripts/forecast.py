#!/usr/bin/env python3
"""Illustrative consolidated forecast FY2026–FY2030, not company guidance.

Starting figures are the audited FY2025 Group numbers in /data.
Forecast drivers live in assumptions/scenarios.csv; nothing is hidden in code.
No share-price targets, WACC, terminal value or security recommendations here.

Run:
    python scripts/forecast.py
    python scripts/forecast.py --check
    python scripts/forecast.py --export
"""
import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read_rows(relative_path):
    with (ROOT / relative_path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

def history(relative_path, metric, year=2025):
    rows = read_rows(relative_path)
    matches = [r for r in rows if r["metric"] == metric]
    assert len(matches) == 1, "Missing or duplicate historical row: " + metric
    return float(matches[0][f"FY{year}"])

I = "data/income_statement.csv"
B = "data/balance_sheet.csv"
C = "data/cash_flow.csv"

def h(table, key):
    return history(table, key)

START = {
    "revenue": h(I, "Revenue"),
    "ppe": h(B, "PPE"),
    "inventory": h(B, "Inventories"),
    "receivables": h(B, "Trade and other receivables"),
    "prepayments": h(B, "Current prepayments and other assets"),
    "payables": h(B, "Trade and other payables"),
    "other_current_liabilities": h(B, "Other current liabilities"),
    "debt": h(B, "Current financial liabilities") + h(B, "Non-current financial liabilities"),
    "cash": h(B, "Cash and cash equivalents (balance sheet)"),
    "equity": h(B, "Total equity"),
}

# Asset/liability residuals hold OTHER balance-sheet categories constant
# so the simplified 3-statement template is internally balanced.
START["other_assets"] = h(B, "Total assets") - sum(START[k] for k in (
    "ppe", "inventory", "receivables", "prepayments", "cash"
))
START["other_liabilities"] = h(B, "Total liabilities") - sum(START[k] for k in (
    "payables", "other_current_liabilities", "debt"
))
assert abs(h(B, "Total assets") - (h(B, "Total liabilities") + h(B, "Total equity"))) < 0.001

def forecast_scenario(inputs):
    state = dict(START)
    results = []
    for row in inputs:
        year = int(row["year"])
        p = {k: float(v) for k, v in row.items() if k not in ("scenario", "year")}
        assert 0 <= p["tax_rate"] <= 1
        assert 0 <= p["dividend_payout"] <= 1
        assert p["depreciation_pct_revenue"] >= 0 and p["cash_capex_pct_revenue"] >= 0
        revenue = state["revenue"] * (1 + p["revenue_growth"])
        ebit = revenue * p["operating_margin"]
        interest = state["debt"] * p["interest_rate_on_debt"]
        profit_before_tax = ebit - interest
        cash_tax = max(profit_before_tax, 0) * p["tax_rate"]
        profit = profit_before_tax - cash_tax
        da = revenue * p["depreciation_pct_revenue"]
        capex = revenue * p["cash_capex_pct_revenue"]
        dividends = max(profit, 0) * p["dividend_payout"]

        prev_nwc = (state["inventory"] + state["receivables"] +
                    state["prepayments"] - state["payables"] -
                    state["other_current_liabilities"])
        inventory = revenue * p["inventory_pct_revenue"]
        receivables = revenue * p["receivables_pct_revenue"]
        prepayments = revenue * p["prepayments_pct_revenue"]
        payables = revenue * p["payables_pct_revenue"]
        other_cl = revenue * p["other_current_liabilities_pct_revenue"]
        nwc = inventory + receivables + prepayments - payables - other_cl
        delta_nwc = nwc - prev_nwc

        # CFO adds interest back because financing cash flow includes interest paid.
        # Forecast assumes no FX, OCI, deferred tax or non-cash loan additions.
        cfo = profit + da + interest - delta_nwc
        cfi = -capex
        cff = -interest - dividends + p["debt_change_ngn_m"]
        change_cash = cfo + cfi + cff
        closing_cash = state["cash"] + change_cash
        ppe = state["ppe"] + capex - da
        debt = state["debt"] + p["debt_change_ngn_m"]
        equity = state["equity"] + profit - dividends

        assets = (ppe + inventory + receivables + prepayments
                  + state["other_assets"] + closing_cash)
        liabilities = (debt + payables + other_cl +
                       state["other_liabilities"])
        bs_check = assets - liabilities - equity
        cash_check = closing_cash - state["cash"] - cfo - cfi - cff

        result = {
            "scenario": row["scenario"], "year": year,
            "revenue": revenue, "ebit": ebit,
            "interest_cost": interest, "profit_before_tax": profit_before_tax,
            "tax": cash_tax, "profit_after_tax": profit,
            "depreciation": da, "cash_capex": capex,
            "inventory": inventory, "receivables": receivables,
            "prepayments": prepayments, "payables": payables,
            "other_current_liabilities": other_cl,
            "net_working_capital": nwc, "change_in_nwc": delta_nwc,
            "dividends": dividends, "operating_cash_flow": cfo,
            "investing_cash_flow": cfi, "financing_cash_flow": cff,
            "cash_open": state["cash"], "cash_close": closing_cash,
            "ppe": ppe, "debt": debt, "equity": equity,
            "other_assets_constant": state["other_assets"],
            "other_liabilities_constant": state["other_liabilities"],
            "total_assets": assets, "total_liabilities": liabilities,
            "balance_sheet_check": bs_check, "cash_flow_check": cash_check,
        }
        assert abs(bs_check) < 0.00001 * max(1, assets), f"{year} balance sheet out of balance"
        assert abs(cash_check) < 0.00001 * max(1, abs(closing_cash)), f"{year} cash bridge failure"
        if closing_cash < 0:
            raise ValueError(f"{row['scenario']} {year}: negative cash requires financing assumptions")
        results.append(result)
        state.update({
            "revenue": revenue, "ppe": ppe, "inventory": inventory,
            "receivables": receivables, "prepayments": prepayments,
            "payables": payables, "other_current_liabilities": other_cl,
            "debt": debt, "cash": closing_cash, "equity": equity
        })
    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="run projection invariants")
    parser.add_argument("--export", action="store_true", help="write scenario output CSV files")
    args = parser.parse_args()
    rows = read_rows("assumptions/scenarios.csv")
    scenarios = sorted(set(row["scenario"] for row in rows))
    assert len(rows) == len(set((row["scenario"], row["year"]) for row in rows))
    for scenario in scenarios:
        group = sorted((r for r in rows if r["scenario"] == scenario), key=lambda r: int(r["year"]))
        assert [int(r["year"]) for r in group] == list(range(2026, 2031))
        forecast = forecast_scenario(group)
        print("\n" + scenario.upper() + " | illustrative Group forecast (NGN million)")
        for row in forecast:
            print(f"{row['year']} revenue={row['revenue']:,.0f} PAT={row['profit_after_tax']:,.0f} cash={row['cash_close']:,.0f} BS gap={row['balance_sheet_check']:.5f}")
        if args.export:
            folder = ROOT / "data" / "forecasts"
            folder.mkdir(parents=True, exist_ok=True)
            path = folder / (scenario.lower() + ".csv")
            with path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=list(forecast[0]))
                writer.writeheader()
                writer.writerows({k: f"{v:.4f}" if isinstance(v, float) else v for k, v in r.items()} for r in forecast)
        if args.check:
            for row in forecast:
                assert abs(row["balance_sheet_check"]) < 0.01
                assert abs(row["cash_flow_check"]) < 0.01
                assert row["cash_close"] >= 0
            print("PASS: balance sheet / cash flow / positive cash checks")
    if args.check:
        print("\nALL SCENARIO CHECKS PASSED. THESE ARE ASSUMPTIONS, NOT PRICE TARGETS.")

if __name__ == "__main__":
    main()
