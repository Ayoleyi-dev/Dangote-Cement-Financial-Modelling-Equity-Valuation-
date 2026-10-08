#!/usr/bin/env python3
"""Build Power BI-importable dashboard tables from version-controlled source CSVs.

No third-party dependencies. Run from any directory:
    python dashboard/scripts/build_data.py
    python dashboard/scripts/test_data.py
Do not manually alter dashboard/data generated files; change documented source
inputs and regenerate them. Reporting units are NGN *millions*.
"""
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / "dashboard" / "data"
DEST.mkdir(parents=True, exist_ok=True)

METRICS = [
 ("Revenue","Revenue","Income"), ("GrossProfit","Gross profit","Income"),
 ("EBIT","Operating profit (EBIT)","Income"), ("PAT","Profit after tax","Income"),
 ("PBT","Profit before tax","Income"), ("CFO","Operating cash flow","Cash flow"),
 ("Cash","Cash and equivalents (balance sheet)","Balance sheet"),
 ("Debt","Current + noncurrent financial liabilities","Balance sheet"),
 ("Equity","Total shareholders' equity (including NCI)","Balance sheet"),
 ("Assets","Total assets","Balance sheet"),
 ("Liabilities","Total liabilities","Balance sheet"),
 ("CashCapex","Cash payments for PPE + intangible purchases","Cash flow"),
 ("DandA","Depreciation & amortisation","Cash flow"),
 ("FCFF","Analyst-estimated unlevered free cash flow","Valuation"),
 ("NWC","Simplified net working capital","Forecast"),
 ("ChangeNWC","Change in simplified net working capital","Forecast")
]
SCENARIOS = ("Base","Downside","Upside")

def read(path):
    with (ROOT/path).open(newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write(name, headers, rows):
    with (DEST/name).open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    print(f"{name}: {len(rows)} rows")

def metric(actual,name,year):
    row=next(r for r in actual if r["metric"]==name)
    return row.get("FY"+str(year)) or None

income=read("data/income_statement.csv")
balance=read("data/balance_sheet.csv")
cash=read("data/cash_flow.csv")
facts=[]
def add(year,scenario,key,value,basis,source):
    if value in (None,""): return
    amount=float(value)
    facts.append(dict(Year=int(year),Scenario=scenario,MetricKey=key,
                      ValueNGNm=round(amount,4),Basis=basis,Source=source))

for year in (2023,2024,2025):
    for code,label in (
       ("Revenue","Revenue"),("GrossProfit","Gross profit"),("EBIT","Operating profit"),
       ("PAT","Profit after tax"),("PBT","Profit before tax")):
        add(year,"Actual",code,metric(income,label,year),"Reported",
            "FY2025 audited Group accounts / FY2024 annual report")
    if year>=2024:
        for code,label in (
          ("Cash","Cash and cash equivalents (balance sheet)"),("Equity","Total equity"),
          ("Assets","Total assets"),("Liabilities","Total liabilities")):
            add(year,"Actual",code,metric(balance,label,year),"Reported","FY2025 audited Group accounts")
        debt=float(metric(balance,"Current financial liabilities",year))+float(metric(balance,"Non-current financial liabilities",year))
        add(year,"Actual","Debt",debt,"Computed reported captions","Audited balance sheet financial-liability captions")
        add(year,"Actual","CFO",metric(cash,"Net operating cash flow",year),"Reported","Audited Group cash flow")
        capex=-float(metric(cash,"Cash purchase of PPE",year))-float(metric(cash,"Intangible asset purchases",year))
        add(year,"Actual","CashCapex",capex,"Derived positive cash spending","Audited Group cash flow")
        add(year,"Actual","DandA",metric(cash,"Depreciation and amortisation",year),"Reported","Audited Group cash flow")

forecast_map = (
 ("Revenue","revenue"),("EBIT","ebit"),("PAT","profit_after_tax"),
 ("PBT","profit_before_tax"),("CFO","operating_cash_flow"),
 ("Cash","cash_close"),("Debt","debt"),("Equity","equity"),
 ("Assets","total_assets"),("Liabilities","total_liabilities"),
 ("CashCapex","cash_capex"),("DandA","depreciation"),
 ("NWC","net_working_capital"),("ChangeNWC","change_in_nwc")
)
for scenario in SCENARIOS:
    for r in read(f"data/forecasts/{scenario.lower()}.csv"):
        for code,column in forecast_map:
            add(r["year"],scenario,code,r[column],"Illustrative analyst forecast","forecast.py scenario assumptions")

fcff=read("data/valuations/fcff_schedule.csv")
for r in fcff:
    add(r["year"],r["scenario"],"FCFF",r["annual_fcff"],"Illustrative DCF FCFF","valuation.py, with documented limitations")

write("DimYear.csv",["Year","Period","PeriodType"],[
   dict(Year=year,Period=f"FY{year}",PeriodType="Historical" if year<=2025 else "Forecast")
   for year in range(2023,2031)])
write("DimScenario.csv",["Scenario","SortOrder"],[
    dict(Scenario=scenario,SortOrder=i) for i,scenario in enumerate(SCENARIOS,1)])
write("DimMetric.csv",["MetricKey","MetricLabel","Category","Unit"],[
    dict(MetricKey=code,MetricLabel=label,Category=category,Unit="NGN million") for code,label,category in METRICS])
write("FactFinancial.csv",["Year","Scenario","MetricKey","ValueNGNm","Basis","Source"],facts)

pr=read("data/peers/comparable_results.csv")
peer=[]
for ev in read("data/peers/ev_ebitda_results.csv"):
    p=next(z for z in pr if z["ticker"]==ev["ticker"])
    ticker=ev["ticker"]
    basis=("Vendor-provided FY2025 EBITDA; audited bridge pending"
           if ticker=="BUACEMENT" else
           "IFRS-reconstructed EBITDA proxy" if ticker=="LAFARGE" else
           "Issuer-rounded Group EBITDA")
    peer.append(dict(
        Ticker=ticker,Company=ev["company"],PriceDate=ev["price_date"],
        PriceNGN=p["price_ngn"],FY2025EPSNGN=p["fy2025_eps_ngn"],
        PE=p["trailing_fy2025_pe"],EVtoEBITDA=ev["ev_ebitda"],
        EnterpriseValueNGNm=ev["ev_ngn_m"],EBITDANGNm=ev["ebitda_ngn_m"],
        BalanceAsOf=ev["balance_date"],EBITDABasis=basis,
        Status="Illustrative historical peer multiple"))
write("FactPeer.csv",list(peer[0]),peer)

valuation=[]
for r in read("data/valuations/valuation_scenarios.csv"):
    valuation.append(dict(
        Scenario=r["scenario"],WACC=r["wacc"],TerminalGrowth=r["terminal_growth"],
        EnterpriseValueNGNm=r["enterprise_value"],EquityValueNGNm=r["equity_value"],
        ValuePerShareNGN=r["value_per_share"],TerminalFraction=r["fraction_terminal_value"],
        ReferencePriceNGN=r["reference_price"],ValuationAsOf="2026-10-08",
        BridgeBalanceAsOf="2026-06-30",Status="Illustrative only"))
write("FactValuation.csv",list(valuation[0]),valuation)

sensitivity=[]
for r in read("data/valuations/sensitivity_base.csv"):
    sensitivity.append(dict(
        WACC=r["wacc"],TerminalGrowth=r["terminal_growth"],
        ValuePerShareNGN=r["model_value_per_share"],Scenario="Base",
        Status="Illustrative DCF sensitivity"))
write("FactSensitivity.csv",list(sensitivity[0]),sensitivity)

fc=[]
for r in fcff:
    fc.append(dict(Year=r["year"],Scenario=r["scenario"],
        NOPATNGNm=r["nopat"],DandANGNm=r["depreciation"],CapexNGNm=r["capex"],
        ChangeNWCNGNm=r["change_in_nwc"],FCFFNGNm=r["annual_fcff"],
        PVFCFFNGNm=r["pv_fcff"],DiscountExponent=r["discount_exponent"]))
write("FactFCFF.csv",list(fc[0]),fc)
