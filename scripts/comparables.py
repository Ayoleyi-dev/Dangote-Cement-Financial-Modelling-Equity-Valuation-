#!/usr/bin/env python3
"""Reproducible FY2025 EPS vs October 2026 peer P/E cross-check.

Uses dated public inputs from data/peers/issuer_prices_earnings.csv.
Uses audited FY2025 per-share earnings; EV/EBITDA is in ev_ebitda.py.\nDoes not mislabel FY2025 annual EPS as an October 2026 TTM denominator.
"""
import argparse
import csv
from pathlib import Path
from statistics import mean, median
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data/peers/issuer_prices_earnings.csv"
def load():
    with SOURCE.open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f))
def assess():
    rows=load()
    assert {x["ticker"] for x in rows}=={"DANGCEM","BUACEMENT","LAFARGE"}
    assert len({x["ticker"] for x in rows})==len(rows)
    for x in rows:
        assert x["price_date"]=="2026-10-07"
        assert float(x["fy2025_eps_ngn"])>0 and float(x["price_ngn"])>0
        x["trailing_fy2025_pe"]=float(x["price_ngn"])/float(x["fy2025_eps_ngn"])
    peers=[r for r in rows if r["ticker"]!="DANGCEM"]
    target=next(r for r in rows if r["ticker"]=="DANGCEM")
    avg=mean(r["trailing_fy2025_pe"] for r in peers)
    med=median(r["trailing_fy2025_pe"] for r in peers)
    return rows, {"peer_mean_pe":avg,"peer_median_pe":med,
                  "dangcem_fy2025_pe":target["trailing_fy2025_pe"],
                  "indicative_mean_value_ngn":avg*float(target["fy2025_eps_ngn"]),
                  "indicative_median_value_ngn":med*float(target["fy2025_eps_ngn"])}
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--check",action="store_true")
    ap.add_argument("--export",action="store_true")
    args=ap.parse_args()
    rows,r=assess()
    for x in rows:
        print(f"{x['ticker']}: ₦{float(x['price_ngn']):.2f}/₦{float(x['fy2025_eps_ngn']):.2f} = {x['trailing_fy2025_pe']:.2f}x")
    for k,v in r.items(): print(f"{k}: {v:.3f}")
    if args.check:
        assert abs(next(x["trailing_fy2025_pe"] for x in rows if x["ticker"]=="BUACEMENT")-297/10.51)<1e-9
        assert abs(next(x["trailing_fy2025_pe"] for x in rows if x["ticker"]=="LAFARGE")-355/16.96)<1e-9
        assert len([x for x in rows if x["ticker"]!="DANGCEM"])==2
        assert r["peer_mean_pe"]==r["peer_median_pe"]
        print("PASS: dated prices, two-peer exclusion, EPS formulas")
    if args.export:
        path=ROOT/"data/peers/comparable_results.csv"
        with path.open("w",newline="",encoding="utf-8") as f:
            w=csv.DictWriter(f,fieldnames=["ticker","company","price_date","price_ngn","fy2025_eps_ngn","trailing_fy2025_pe","eps_quality"])
            w.writeheader()
            for x in rows: w.writerow({k:x[k] for k in w.fieldnames})
        print("Wrote",path)
if __name__=="__main__":main()
