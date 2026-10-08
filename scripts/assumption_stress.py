#!/usr/bin/env python3
"""Explicitly UNCALIBRATED WACC and capex stress tests on the Base DCF.

This is a modelling sensitivity, not revised market-based cost-of-capital research.
Run: python scripts/assumption_stress.py --check [--export]
"""
import argparse
import csv
from pathlib import Path
from valuation import params, discount_rate, dcf, cashflows, read_csv

ROOT = Path(__file__).resolve().parents[1]

def rows_for_stress():
    p = params()
    table = []
    baseline=dcf("Base",p)
    for beta in (0.8,1.0,1.2,2.308):
        q=dict(p);q["levered_beta"]=beta
        w=discount_rate(q)["wacc"]
        val=dcf("Base",q,wacc=w)
        table.append({"test":"beta","input_value":beta,
                      "wacc":w,"share_value_ngn":val["value_per_share"],
                      "difference_from_base_ngn":val["value_per_share"]-baseline["value_per_share"]})
    # Incremental capex in each forecast year: apply to annual FCFF, NOT
    # to a rerun of balance sheet; this is a static valuation-only shock.
    base_cf=cashflows("Base",p)
    rev={int(r["year"]):float(r["revenue"]) for r in read_csv("data/forecasts/base.csv")}
    w=baseline["wacc"];g=p["terminal_growth"]
    for capex_pct_shift in (-0.01,0,0.01,0.02):
        pv=0;last_fcff=None;tv_pv=None
        for i,r in enumerate(base_cf):
            new_annual=r["annual_fcff"]-capex_pct_shift*rev[r["year"]]
            fraction=p["stub_days_remaining_2026"]/p["days_per_year"] if i==0 else 1
            pv += new_annual*fraction/(1+w)**r["discount_exponent"]
            if i==len(base_cf)-1:
                last_fcff=new_annual
                tv_pv=last_fcff*(1+g)/(w-g)/(1+w)**r["discount_exponent"]
        ev=pv+tv_pv
        equity=ev-p["gross_financial_debt_ngn_m"]+p["cash_ngn_m"]-p["noncontrolling_equity_ngn_m"]+p["other_nonoperating_adjustments_ngn_m"]
        val=equity/p["shares_outstanding_million"]
        table.append({"test":"capex_as_share_of_revenue_delta",
                      "input_value":capex_pct_shift,"wacc":w,"share_value_ngn":val,
                      "difference_from_base_ngn":val-baseline["value_per_share"]})
    return table, baseline["value_per_share"]

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--check",action="store_true");p.add_argument("--export",action="store_true")
    args=p.parse_args()
    rows,base=rows_for_stress()
    for r in rows:print(f"{r['test']}: {r['input_value']:.4f} | WACC={r['wacc']:.3%} | ₦{r['share_value_ngn']:.2f}/share")
    if args.check:
        beta=[r for r in rows if r["test"]=="beta"]
        capex=[r for r in rows if r["test"]=="capex_as_share_of_revenue_delta"]
        assert all(x["share_value_ngn"]>y["share_value_ngn"] for x,y in zip(beta,beta[1:]))
        assert all(x["share_value_ngn"]>y["share_value_ngn"] for x,y in zip(capex,capex[1:]))
        assert abs(capex[1]["share_value_ngn"]-base)<0.01
        assert abs(beta[1]["share_value_ngn"]-base)<0.01
        print("PASS: WACC/beta/capex monotonic sensitivities; baseline bridge")
    if args.export:
        path=ROOT/"data/valuations/assumption_stress.csv"
        with path.open("w",newline="",encoding="utf-8") as f:
            columns=["test","input_value","wacc","share_value_ngn","difference_from_base_ngn"]
            writer=csv.DictWriter(f,fieldnames=columns);writer.writeheader()
            for r in rows:writer.writerow({k:f"{r[k]:.6f}" if isinstance(r[k],float) else r[k] for k in columns})
        print("Exported",path)
if __name__=="__main__":main()
