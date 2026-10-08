#!/usr/bin/env python3
"""Validate the materialized Power BI CSV star-model outputs and source ties."""
from pathlib import Path
import csv
ROOT=Path(__file__).resolve().parents[2]

def load(p):
    with (ROOT/p).open(newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))
fact=load("dashboard/data/FactFinancial.csv")
year=load("dashboard/data/DimYear.csv")
metric=load("dashboard/data/DimMetric.csv")
scenario=load("dashboard/data/DimScenario.csv")
valuation=load("dashboard/data/FactValuation.csv")
peers=load("dashboard/data/FactPeer.csv")
sense=load("dashboard/data/FactSensitivity.csv")
fcff=load("dashboard/data/FactFCFF.csv")
M={r["MetricKey"] for r in metric};Y={r["Year"] for r in year};S={r["Scenario"] for r in scenario}
assert len(year)==8 and len(metric)==16 and len(scenario)==3
assert len(fact)==len({(r["Year"],r["Scenario"],r["MetricKey"]) for r in fact}),"Duplicated facts"
assert all(r["MetricKey"] in M and r["Year"] in Y and r["Scenario"] in S|{"Actual"} for r in fact)
assert all((int(r["Year"])<=2025)==(r["Scenario"]=="Actual") for r in fact)
assert all(r["Basis"].startswith("Illustrative") for r in fact if r["Scenario"]!="Actual")
assert not any(r["Year"]=="2023" and r["MetricKey"]=="Assets" for r in fact),"Never impute FY2023 balance"
def value(y,s,m):
    return float(next(r["ValueNGNm"] for r in fact if int(r["Year"])==y and r["Scenario"]==s and r["MetricKey"]==m))
assert value(2025,"Actual","Revenue")==4306704
assert value(2025,"Actual","PAT")==1014921
assert abs(value(2026,"Base","Revenue")-5168044.8)<1
assert abs(value(2030,"Base","Revenue")-7357741.2473)<1
assert len(valuation)==3 and len(sense)==25 and len(fcff)==15 and len(peers)==3
assert {x["Scenario"] for x in valuation}==S
assert abs(float(next(r["ValuePerShareNGN"] for r in valuation if r["Scenario"]=="Base"))-389.640961)<.001
assert abs(float(next(r["PriceNGN"] for r in peers if r["Ticker"]=="BUACEMENT"))-297)<.001
assert abs(float(next(r["PE"] for r in peers if r["Ticker"]=="BUACEMENT"))-297/10.51)<.0001
assert abs(float(next(r["EVtoEBITDA"] for r in peers if r["Ticker"]=="DANGCEM"))-9.415145)<.001
for r in valuation:
    assert r["Status"]=="Illustrative only" and r["BridgeBalanceAsOf"]=="2026-06-30"
for r in fcff:
    assert abs(float(r["FCFFNGNm"])-value(int(r["Year"]),r["Scenario"],"FCFF"))<.01
print(f"PASS dashboard: 8 tables; {len(fact)} financial points, {len(peers)} peers, {len(fcff)} FCFF rows, {len(sense)} sensitivity cells")
print("PASS provenance: Actual FY2025 audited vs FY2026 onward illustrative; dates and units consistent")
