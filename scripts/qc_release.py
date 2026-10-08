#!/usr/bin/env python3
"""Release checks for the Dangote Cement research project.

This script catches presentation/data drift across outputs and documentation.
It does not validate forecast assumptions or guarantee market-price accuracy.
Run from anywhere: python scripts/qc_release.py
"""
from pathlib import Path
import csv
import math
import re

ROOT = Path(__file__).resolve().parents[1]

def load(relative):
    with (ROOT / relative).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def unique(rows, key, label):
    seen = [tuple(r[k] for k in key) for r in rows]
    assert len(seen) == len(set(seen)), f"Duplicate {label}"

def almost(a, b, label, tol=0.02):
    assert math.isclose(float(a), float(b), rel_tol=0, abs_tol=tol), f"{label}: {a} != {b}"

def main():
    checked = 0
    inc = load("data/income_statement.csv")
    bs = load("data/balance_sheet.csv")
    cf = load("data/cash_flow.csv")
    f = {r["metric"]: r for r in inc}
    b = {r["metric"]: r for r in bs}
    c = {r["metric"]: r for r in cf}
    for year in (2023, 2024, 2025):
        y = "FY"+str(year)
        almost(float(f["Revenue"][y]) + float(f["Production cost of sales"][y]),
               f["Gross profit"][y], f"{year} gross profit")
        almost(float(f["Profit before tax"][y]) + float(f["Income tax expense"][y]),
               f["Profit after tax"][y], f"{year} net profit")
        checked += 2
    for year in (2024, 2025):
        y = "FY"+str(year)
        almost(float(b["Total assets"][y])-float(b["Total liabilities"][y]),
               b["Total equity"][y], f"{year} balance sheet")
        almost(float(c["Cash at end of year (balance sheet)"][y]) +
               float(c["Bank overdrafts for cash management"][y]),
               c["Cash at end of year (cash flow)"][y], f"{year} cash bridge")
        checked += 2

    revenue = float(f["Revenue"]["FY2025"])
    profit = float(f["Profit after tax"]["FY2025"])
    almost(revenue, 4306704, "audited 2025 revenue")
    almost(profit, 1014921, "audited 2025 profit")
    checked += 2

    # Valuation bridge and scenario calculations
    vals = load("data/valuations/valuation_scenarios.csv")
    unique(vals, ["scenario"], "DCF scenarios")
    assert {r["scenario"] for r in vals} == {"Base", "Downside", "Upside"}
    for r in vals:
        almost(float(r["pv_fcff"])+float(r["pv_terminal"]),
               r["enterprise_value"], f"{r['scenario']} enterprise value")
        almost((float(r["enterprise_value"])+float(r["net_cash"]) -
                float(r["noncontrolling_equity"])), r["equity_value"],
               f"{r['scenario']} equity value")
        almost(float(r["equity_value"])/float(r["shares_million"]),
               r["value_per_share"], f"{r['scenario']} per share", tol=0.0002)
        checked += 3
    base = next(r for r in vals if r["scenario"] == "Base")
    almost(base["value_per_share"], 389.640961, "base DCF per share", tol=0.001)
    checked += 1

    # Quoted October prices are historical market snapshots, not FY2025 dates.
    peers = load("data/peers/comparable_results.csv")
    unique(peers, ["ticker"], "peer tickers")
    assert {r["ticker"] for r in peers} == {"DANGCEM", "BUACEMENT", "LAFARGE"}
    for r in peers:
        assert r["price_date"] == "2026-10-07"
        almost(float(r["price_ngn"])/float(r["fy2025_eps_ngn"]),
               r["trailing_fy2025_pe"], f"{r['ticker']} trailing P/E", tol=0.0002)
        checked += 2
    ev = load("data/peers/ev_ebitda_results.csv")
    unique(ev, ["ticker"], "EV/EBITDA peers")
    for r in ev:
        almost(float(r["market_cap_ngn_m"])+float(r["interest_debt_ngn_m"]) +
               float(r["lease_liabilities_ngn_m"]) -
               float(r["unrestricted_cash_ngn_m"]) +
               float(r["nci_ngn_m"]), r["ev_ngn_m"], f"{r['ticker']} EV")
        almost(float(r["ev_ngn_m"])/float(r["ebitda_ngn_m"]),
               r["ev_ebitda"], f"{r['ticker']} EV/EBITDA", tol=0.0002)
        assert r["balance_date"] == "2025-12-31"
        checked += 3

    facts = load("dashboard/data/FactFinancial.csv")
    unique(facts, ["Year", "Scenario", "MetricKey"], "dashboard financial facts")
    assert all((int(r["Year"]) <= 2025) == (r["Scenario"] == "Actual") for r in facts)
    check_fact = lambda year, scenario, key: float(next(r["ValueNGNm"] for r in facts
        if r["Year"] == str(year) and r["Scenario"] == scenario and r["MetricKey"] == key))
    almost(check_fact(2025, "Actual", "Revenue"), revenue, "dashboard FY2025 revenue")
    almost(check_fact(2025, "Actual", "PAT"), profit, "dashboard FY2025 profit")
    for scenario in ("Base", "Downside", "Upside"):
        forecasts = load("data/forecasts/" + scenario.lower() + ".csv")
        for r in forecasts:
            almost(check_fact(int(r["year"]),scenario,"Revenue"),
                   r["revenue"], f"dashboard {scenario} {r['year']} revenue")
            almost(float(r["total_assets"]) - float(r["total_liabilities"]),
                   r["equity"], f"forecast {scenario} {r['year']} balance", tol=0.04)
            almost(float(r["cash_close"])-float(r["cash_open"]),
                   float(r["operating_cash_flow"])+float(r["investing_cash_flow"]) +
                   float(r["financing_cash_flow"]), f"forecast {scenario} {r['year']} cash", tol=0.04)
            checked += 3

    dashboard_peers = load("dashboard/data/FactPeer.csv")
    for r in dashboard_peers:
        matched=next(p for p in peers if p["ticker"] == r["Ticker"])
        almost(r["PE"], matched["trailing_fy2025_pe"], f"dashboard {r['Ticker']} P/E",tol=0.0002)
        almost(r["PriceNGN"], matched["price_ngn"], f"dashboard {r['Ticker']} price",tol=0.0002)
        checked += 2
    sensitivity = load("dashboard/data/FactSensitivity.csv")
    assert len(sensitivity) == 25, "expected 25 DCF sensitivity observations"
    assert len(load("dashboard/data/FactValuation.csv")) == 3
    checked += 2

    # Reproducible editorial claims.
    readme=(ROOT/"README.md").read_text(encoding="utf-8")
    report=(ROOT/"reports/DANGCEM_Equity_Research_Case_Study_2026-10-08.md").read_text(encoding="utf-8")
    guide=(ROOT/"dashboard/README.md").read_text(encoding="utf-8")
    for keyword in ("₦389.64","₦1,472.27","₦1,792.57"):
        assert keyword in readme, "README missing expected illustrative model figure: " + keyword
    for keyword in ("₦389.64","₦1,472.27","₦1,792.57"):
        assert keyword in report, "Research report missing matching model figure: " + keyword
    assert "not" in guide.lower() and ".pbix" in guide, "Native Power BI limitation must be stated"
    assert "BUY" in report or "buy" in report.lower(), "Research conclusion should state recommendation status"
    assert "FY2025" in readme and "FY2026" in readme
    checked += 9

    # Verify tracked Markdown links that point to repository files.
    docs=[ROOT/"README.md",ROOT/"dashboard/README.md",
          ROOT/"reports/DANGCEM_Equity_Research_Case_Study_2026-10-08.md"]
    for p in docs:
        text=p.read_text(encoding="utf-8")
        for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)",text):
            href=match.group(1).split("#")[0]
            if href and not href.startswith(("http://","https://","mailto:","#")):
                assert (p.parent/href).exists(), f"Broken relative link: {p}: {href}"
                checked += 1
    print(f"PASS: {checked} independent release assertions and internal-link checks.")
    print("Open items: cost-of-capital calibration, latest balance date, peer EBITDA normalization, native PBIX review.")
    print("No automated test can certify investment forecast assumptions.")

if __name__=="__main__":
    main()
