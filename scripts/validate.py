#!/usr/bin/env python3
"""Checks for Dangote Cement's published historical Group figures.

Only Python's standard library is required. Reported figures are sourced
from the NGX-hosted FY2025 audited accounts and its FY2024 comparatives.
No valuation or forecast is claimed here.
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "data"

def load(name):
    with (ROOT / name).open(encoding="utf-8", newline="") as f:
        data = list(csv.DictReader(f))
    assert data, f"Empty input: {name}"
    assert len(set(d["metric"] for d in data)) == len(data), f"Duplicated metric in {name}"
    return {row["metric"]: row for row in data}

I, B, C = [load(file) for file in (
    "income_statement.csv", "balance_sheet.csv", "cash_flow.csv"
)]

def x(table, label, year):
    return float(table[label][f"FY{year}"])

def check_eq(name, a, b):
    assert abs(a-b) < 0.001, f"{name}: expected {b:,.2f}, received {a:,.2f}"
    print(f"PASS  {name}: {a:,.2f}")

for yr in (2023, 2024, 2025):
    check_eq(f"{yr} gross profit", x(I,"Revenue",yr)+x(I,"Production cost of sales",yr), x(I,"Gross profit",yr))
    check_eq(f"{yr} operating profit",sum(x(I,n,yr) for n in (
        "Gross profit","Administrative expenses","Selling and distribution expenses","Other income","Impairment of financial assets"
    )),x(I,"Operating profit",yr))
    check_eq(f"{yr} profit before tax",sum(x(I,n,yr) for n in (
        "Operating profit","Finance income","Finance costs","Net monetary position gain","Share of profit from associate"
    )),x(I,"Profit before tax",yr))
    check_eq(f"{yr} profit after tax",x(I,"Profit before tax",yr)+x(I,"Income tax expense",yr),x(I,"Profit after tax",yr))

for yr in (2024, 2025):
    check_eq(f"{yr} noncurrent assets",sum(x(B,n,yr) for n in (
        "PPE","Intangible assets","Right-of-use assets","Investment in associate",
        "Non-current lease receivables","Deferred tax assets","Non-current prepayments",
        "Non-current related-party receivables")),x(B,"Total non-current assets",yr))
    check_eq(f"{yr} current assets",sum(x(B,n,yr) for n in (
        "Inventories","Trade and other receivables","Current prepayments and other assets",
        "Current lease receivables","Current tax assets","Cash and cash equivalents (balance sheet)")),x(B,"Total current assets",yr))
    check_eq(f"{yr} asset subtotals",x(B,"Total non-current assets",yr)+x(B,"Total current assets",yr),x(B,"Total assets",yr))
    check_eq(f"{yr} current liabilities",sum(x(B,n,yr) for n in (
        "Trade and other payables","Current lease liabilities","Current tax liabilities",
        "Current financial liabilities","Other current liabilities")),x(B,"Total current liabilities",yr))
    check_eq(f"{yr} noncurrent liabilities",sum(x(B,n,yr) for n in (
        "Deferred tax liabilities","Non-current financial liabilities","Non-current lease liabilities",
        "Provisions","Deferred revenue","Employee benefit obligations")),x(B,"Total non-current liabilities",yr))
    check_eq(f"{yr} liabilities subtotal",x(B,"Total current liabilities",yr)+x(B,"Total non-current liabilities",yr),x(B,"Total liabilities",yr))
    check_eq(f"{yr} balance sheet equation",x(B,"Total liabilities",yr)+x(B,"Total equity",yr),x(B,"Total assets",yr))
    check_eq(f"{yr} pre-working capital",sum(x(C,n,yr) for n in (
        "Profit before tax","Depreciation and amortisation","Write-offs and impairments",
        "Interest expenses","Interest and dividend income","Net exchange loss or gain",
        "Net monetary gain","Share of associate income","Deferred revenue adjustment",
        "Provisions","Employee benefits provisions","Gain on disposals"
    )),x(C,"Cash before working capital",yr))
    check_eq(f"{yr} pre-tax cash generated",x(C,"Cash before working capital",yr)+sum(x(C,n,yr) for n in (
        "Change in inventories","Change in receivables","Change in payables","Change in prepayments",
        "Change in other current liabilities","Change in lease receivables")),x(C,"Cash generated before tax",yr))
    check_eq(f"{yr} operating cash",x(C,"Cash generated before tax",yr)+x(C,"Income tax paid",yr),x(C,"Net operating cash flow",yr))
    check_eq(f"{yr} investing cash",sum(x(C,n,yr) for n in (
        "Interest received","Dividend income received","Intangible asset purchases","Net parent company loans",
        "Asset disposal proceeds","Cash purchase of PPE")),x(C,"Net investing cash flow",yr))
    check_eq(f"{yr} PPE capex bridge",sum(x(C,n,yr) for n in (
        "PPE additions (non-cash-inclusive memo)","Change in non-current prepayments (memo)",
        "Suppliers credit unpaid (memo)")),x(C,"Cash purchase of PPE",yr))
    check_eq(f"{yr} financing cash",sum(x(C,n,yr) for n in (
        "Interest paid","Principal lease payments","Dividends paid","Loans obtained","Loans repaid"
    )),x(C,"Net financing cash flow",yr))
    check_eq(f"{yr} change in cash",sum(x(C,n,yr) for n in (
        "Net operating cash flow","Net investing cash flow","Net financing cash flow")),x(C,"Change in cash",yr))
    check_eq(f"{yr} closing cash by cash movements",sum(x(C,n,yr) for n in (
        "Change in cash","Cash at beginning of year","FX effect on cash")),x(C,"Cash at end of year (cash flow)",yr))
    check_eq(f"{yr} note 32.1 overdraft bridge",x(C,"Cash at end of year (balance sheet)")+x(C,"Bank overdrafts for cash management",yr),x(C,"Cash at end of year (cash flow)",yr))

print("\nAll historical statement checks passed. No forward-looking valuation performed.")
