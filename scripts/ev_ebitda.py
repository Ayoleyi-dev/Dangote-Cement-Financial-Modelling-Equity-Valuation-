#!/usr/bin/env python3
"""Transparent EV/EBITDA comparison: 2025 balance sheets; 7 Oct 2026 stock prices.

No external packages required. Values are NGN millions unless indicated.
Prices and historical reported results refer to DIFFERENT dates; outputs are
illustrative retrospective cross-checks, not contemporaneous fair values.
"""
import argparse
import csv
from pathlib import Path
from statistics import mean, median

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/peers/ev_ebitda_inputs.csv"
RESULTS = ROOT / "data/peers/ev_ebitda_results.csv"
SUMMARY = ROOT / "data/peers/ev_ebitda_summary.csv"
FIELDS = ["ticker", "company", "price_date", "balance_date",
          "market_cap_ngn_m", "interest_debt_ngn_m", "lease_liabilities_ngn_m",
          "unrestricted_cash_ngn_m", "nci_ngn_m", "ev_ngn_m",
          "ebitda_ngn_m", "ev_ebitda"]

def load():
    with SOURCE.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def calc():
    rows = load()
    assert {x["ticker"] for x in rows} == {"DANGCEM", "BUACEMENT", "LAFARGE"}
    out = []
    for r in rows:
        assert r["price_date"] == "2026-10-07"
        assert r["ebitda_date"] == "2025-12-31"
        assert r["balance_date"] == "2025-12-31"
        num = lambda name: float(r[name])
        assert num("shares_million") > 0 and num("ebitda_ngn_m") > 0
        assert num("cash_and_equivalents_ngn_m") >= num("restricted_cash_ngn_m")
        cap = num("price_ngn") * num("shares_million")
        liquid_cash = num("cash_and_equivalents_ngn_m") - num("restricted_cash_ngn_m")
        ev = cap + num("interest_debt_ngn_m") + num("lease_liabilities_ngn_m") - liquid_cash + num("nci_ngn_m")
        assert ev > 0
        out.append({
            "ticker": r["ticker"], "company": r["company"],
            "price_date": r["price_date"], "balance_date": r["balance_date"],
            "market_cap_ngn_m": cap, "interest_debt_ngn_m": num("interest_debt_ngn_m"),
            "lease_liabilities_ngn_m": num("lease_liabilities_ngn_m"),
            "unrestricted_cash_ngn_m": liquid_cash,
            "nci_ngn_m": num("nci_ngn_m"), "ev_ngn_m": ev,
            "ebitda_ngn_m": num("ebitda_ngn_m"), "ev_ebitda": ev/num("ebitda_ngn_m")
        })
    peers = [r for r in out if r["ticker"] != "DANGCEM"]
    target = next(r for r in out if r["ticker"] == "DANGCEM")
    median_multiple = median(p["ev_ebitda"] for p in peers)
    mean_multiple = mean(p["ev_ebitda"] for p in peers)
    implied_ev = median_multiple * target["ebitda_ngn_m"]
    implied_equity = (implied_ev - target["interest_debt_ngn_m"] -
                      target["lease_liabilities_ngn_m"] + target["unrestricted_cash_ngn_m"] -
                      target["nci_ngn_m"])
    shares = next(float(r["shares_million"]) for r in rows if r["ticker"] == "DANGCEM")
    summary = [
        ("peer_count",len(peers)), ("peer_mean_multiple",mean_multiple),
        ("peer_median_multiple",median_multiple),
        ("dangcem_ev_implied_ngn_m",implied_ev),
        ("dangcem_equity_implied_ngn_m",implied_equity),
        ("dangcem_indicative_per_share_ngn",implied_equity/shares)
    ]
    return out, summary

def write(path,headers,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",newline="",encoding="utf-8") as file:
        w = csv.DictWriter(file,fieldnames=headers)
        w.writeheader()
        for row in rows:
            w.writerow({k: f"{row[k]:.6f}" if isinstance(row[k],float) else row[k] for k in headers})

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--check",action="store_true")
    ap.add_argument("--export",action="store_true")
    args=ap.parse_args()
    rows, summary=calc()
    for r in rows:
        print(f"{r['ticker']:10s} EV/EBITDA {r['ev_ebitda']:.3f}x")
    for k,v in summary: print(f"{k}: {v:,.3f}")
    if args.check:
        m={r["ticker"]:r for r in rows}
        assert abs(m["LAFARGE"]["ebitda_ngn_m"]-(392099.733+34784.416+40.793))<0.001
        assert abs(m["LAFARGE"]["unrestricted_cash_ngn_m"]-(388067.308-3205.328))<0.001
        assert abs(m["BUACEMENT"]["interest_debt_ngn_m"]-
                   (156303.553+313072.476+57254.261))<0.001
        assert abs(m["DANGCEM"]["interest_debt_ngn_m"]-
                   m["DANGCEM"]["unrestricted_cash_ngn_m"]-682921)<0.001
        assert m["BUACEMENT"]["ev_ebitda"]>m["LAFARGE"]["ev_ebitda"]
        assert 0<len(rows)==3
        print("PASS EV bridge, balance dates, and source-component reconciliations")
    if args.export:
        write(RESULTS,FIELDS,rows)
        write(SUMMARY,["metric","value"],[{"metric":k,"value":v} for k,v in summary])
if __name__=="__main__":
    main()
