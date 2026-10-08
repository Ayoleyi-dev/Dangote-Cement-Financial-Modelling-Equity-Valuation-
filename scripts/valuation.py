#!/usr/bin/env python3
"""Illustrative dated enterprise DCF for DANGCEM; not an investment recommendation.

Inputs: dated assumptions/valuation_inputs.csv and existing historical-scenario
forecasts in data/forecasts/*.csv. Dates and stale information are explicit.
No dependencies outside the Python standard library.
"""
import argparse
import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read_csv(path):
    with (ROOT / path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))

def params():
    rows = read_csv("assumptions/valuation_inputs.csv")
    assert len(rows) == len({row["key"] for row in rows})
    return {row["key"]: float(row["value"]) for row in rows}

def discount_rate(p):
    cost_equity = p["ngn_10y_yield"] + p["levered_beta"] * p["equity_risk_premium"] + p["additional_country_premium"]
    reference_market_cap = p["share_price_ngn"] * p["shares_outstanding_million"]
    debt = p["gross_financial_debt_ngn_m"]
    w_e = reference_market_cap / (reference_market_cap + debt)
    w_d = 1 - w_e
    wacc = w_e * cost_equity + w_d * p["pre_tax_cost_of_debt"] * (1-p["debt_tax_shield_rate"])
    return {"cost_of_equity": cost_equity, "wacc": wacc,
            "market_cap_ngn_m": reference_market_cap, "equity_weight": w_e,
            "debt_weight": w_d}

def cashflows(scenario, p):
    rows = read_csv(f"data/forecasts/{scenario.lower()}.csv")
    assert [int(x["year"]) for x in rows] == list(range(2026, 2031))
    fraction = p["stub_days_remaining_2026"] / p["days_per_year"]
    assert 0 < fraction < 1
    result = []
    for idx,r in enumerate(rows):
        # FCFF = EBIT*(1-tax) + D&A - capex - delta NWC
        a = {k:float(r[k]) for k in ("ebit","depreciation","cash_capex","change_in_nwc")}
        # Take scenario-year-specific tax assumption, not effective historical PAT rate
        assumptions = [z for z in read_csv("assumptions/scenarios.csv")
                       if z["scenario"] == r["scenario"] and z["year"] == r["year"]]
        assert len(assumptions) == 1
        tax = float(assumptions[0]["tax_rate"])
        nopat = a["ebit"] * (1-tax)
        fcff = nopat + a["depreciation"] - a["cash_capex"] - a["change_in_nwc"]
        # No Q3 data available yet. Simple pro-rata annual FCFF for 2026 stub.
        valuation_cash_flow = fcff * fraction if idx == 0 else fcff
        exponent = fraction + idx
        result.append({"year":int(r["year"]), "nopat":nopat, "depreciation":a["depreciation"],
                       "capex":a["cash_capex"], "change_in_nwc":a["change_in_nwc"],
                       "annual_fcff":fcff, "cash_flow_for_dcf":valuation_cash_flow,
                       "discount_exponent":exponent})
    return result

def dcf(scenario, p, wacc=None, terminal_growth=None):
    flows = cashflows(scenario,p)
    dr = discount_rate(p)
    wacc = dr["wacc"] if wacc is None else wacc
    g = p["terminal_growth"] if terminal_growth is None else terminal_growth
    if not (wacc > g and wacc > -1 and g > -1):
        raise ValueError("WACC must be greater than perpetual growth")
    for r in flows:
        r["discount_factor"] = (1+wacc)**(-r["discount_exponent"])
        r["pv_fcff"] = r["cash_flow_for_dcf"]*r["discount_factor"]
    terminal_fcff = flows[-1]["annual_fcff"] * (1+g)
    terminal_value = terminal_fcff / (wacc-g)
    pv_terminal = terminal_value * flows[-1]["discount_factor"]
    pv_explicit = sum(r["pv_fcff"] for r in flows)
    ev = pv_explicit + pv_terminal
    # Use H1 2026 balance sheet even though valuation snapshot is Oct 2026.
    equity = (ev - p["gross_financial_debt_ngn_m"] + p["cash_ngn_m"]
              - p["noncontrolling_equity_ngn_m"] +
              p["other_nonoperating_adjustments_ngn_m"])
    share_value = equity / p["shares_outstanding_million"]
    return {"scenario":scenario, "wacc":wacc, "terminal_growth":g,
            "pv_fcff":pv_explicit, "pv_terminal":pv_terminal,
            "enterprise_value":ev, "net_cash":p["cash_ngn_m"]-p["gross_financial_debt_ngn_m"],
            "noncontrolling_equity":p["noncontrolling_equity_ngn_m"],
            "equity_value":equity,"shares_million":p["shares_outstanding_million"],
            "value_per_share":share_value,"reference_price":p["share_price_ngn"],
            "fraction_terminal_value":pv_terminal/ev, "cashflows":flows}

def write_csv(path, fieldnames, data):
    dest = ROOT/path
    dest.parent.mkdir(parents=True,exist_ok=True)
    with dest.open("w",newline="",encoding="utf-8") as handle:
        wr = csv.DictWriter(handle,fieldnames=fieldnames)
        wr.writeheader()
        for row in data:
            wr.writerow({k: (f"{row[k]:.6f}" if isinstance(row[k],float) else row[k]) for k in fieldnames})

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--check",action="store_true")
    ap.add_argument("--export",action="store_true")
    args=ap.parse_args()
    p=params()
    w=discount_rate(p)
    cases = [dcf(name,p) for name in ("Downside","Base","Upside")]
    print(f"Cost of equity: {w['cost_of_equity']:.4%} | WACC: {w['wacc']:.4%}")
    for r in cases:
        print(f"{r['scenario']:9s} EV={r['enterprise_value']:,.2f} (₦m); equity={r['equity_value']:,.2f} (₦m); per share=₦{r['value_per_share']:,.2f}; TV/EV={r['fraction_terminal_value']:.1%}")
    if args.check:
        assert all(0<r["fraction_terminal_value"]<1 for r in cases)
        assert cases[0]["value_per_share"] < cases[1]["value_per_share"] < cases[2]["value_per_share"]
        assert all(abs((r["pv_fcff"] + r["pv_terminal"]) - r["enterprise_value"])<0.01 for r in cases)
        assert all(abs(r["equity_value"]-(r["enterprise_value"]+r["net_cash"]-r["noncontrolling_equity"]))<0.01 for r in cases)
        # This baseline helps catch accidental drifts relative to the independently made Excel model.
        # Do not assert a fixed value/share: editable scenario inputs can legitimately change.
        for growth in (0.02,0.03,0.04,0.05,0.06):
            values=[dcf("Base",p,wacc=w["wacc"]+delta,terminal_growth=growth)["value_per_share"]
                    for delta in (-0.04,-0.02,0,0.02,0.04)]
            assert all(a>b for a,b in zip(values,values[1:])), "Higher WACC should reduce valuation"
        print("PASS: enterprise-to-equity bridge, scenario ordering and WACC sensitivity")
    if args.export:
        lines=[{k:r[k] for k in ("scenario","wacc","terminal_growth","pv_fcff","pv_terminal",
            "enterprise_value","net_cash","noncontrolling_equity","equity_value","shares_million",
            "value_per_share","reference_price","fraction_terminal_value")} for r in cases]
        write_csv("data/valuations/valuation_scenarios.csv",list(lines[0]),lines)
        fc=[{"scenario":r["scenario"],**f} for r in cases for f in r["cashflows"]]
        write_csv("data/valuations/fcff_schedule.csv",list(fc[0]),fc)
        sens=[{"terminal_growth":g, "wacc":w["wacc"]+d,
               "model_value_per_share":dcf("Base",p,wacc=w["wacc"]+d,terminal_growth=g)["value_per_share"]}
               for g in (0.02,0.03,0.04,0.05,0.06)
               for d in (-0.04,-0.02,0,0.02,0.04)]
        write_csv("data/valuations/sensitivity_base.csv",list(sens[0]),sens)
        print("Exported 3 inspectable valuation CSVs.")
if __name__=="__main__":
    main()
