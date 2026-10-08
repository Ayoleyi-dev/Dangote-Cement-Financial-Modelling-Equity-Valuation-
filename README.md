# Dangote Cement | Financial Modelling & Equity Valuation

**Portfolio research project · NGX: DANGCEM · Nigerian naira**

I'm building this project to demonstrate how I move from historical company accounts to an evidence-based equity valuation. My background is in data analytics, so I am deliberately treating financial reporting as a data-quality problem first: source the numbers, reproduce the statements, reconcile them, and *only then* forecast or value the business.

> **Status as of 8 October 2026:** Historical financials and first-stage reconciliations complete for **FY2024–FY2025** (plus FY2023 income statement). Forecasts, discount-rate estimates and an equity valuation are **not yet completed**. Nothing in this repository is investment advice.

## What I've built

- **Historical income statement:** FY2023–FY2025 Group figures (NGN millions except EPS).
- **Historical balance sheet:** FY2024–FY2025 consolidated Group assets, liabilities and equity.
- **Historical cash flow:** FY2024–FY2025 operating, investing and financing activities.
- **Reconciliation checks:** accounting equation, cash bridge, financing and capital expenditure classifications.
- **Source register:** primary company filings and corresponding page numbers.
- **Validation script:** repeatable, standard-library-only assertions for the main statement totals.

## A few findings from the accounts

| Metric (₦ billion unless stated) | FY2024 | FY2025 |
| --- | ---: | ---: |
| Group revenue | 3,580.6 | 4,306.7 |
| Group profit after tax | 503.2 | 1,014.9 |
| Total assets | 6,403.2 | 6,040.7 |
| Total equity | 2,175.2 | 2,620.1 |
| Net operating cash flow | 821.2 | 1,710.8 |
| Management-defined net debt | 2,061.9 | 682.9 |

These are **historical reported values, not forecasts**. Revenue grew by about 20% in FY2025, while profit grew faster; I will investigate the underlying drivers before setting any future assumptions.

## Repo layout

```text
data/
  income_statement.csv     FY2023–FY2025 Group history
  balance_sheet.csv        FY2024–FY2025 Group history
  cash_flow.csv            FY2024–FY2025 Group history
docs/
  sources.md               exact source links + interpretation notes
  learning_notes.md        explanation of what each reconciliation means
scripts/
  validate.py              reproducible data checks, Python standard library
.github/workflows/
  validate.yml             CI runs checks when changed
```

## Reproduce the checks

```bash
python scripts/validate.py
```

No credentials or paid datasets are needed. The model is constructed from the audited public disclosures. Data in the CSV files are integers in **₦ million**, except earnings per share (₦ per share).

## My next milestones

1. **Historical statements & checks — COMPLETE for FY2024–FY2025**. FY2023 profit or loss is present; FY2023 balance sheet and cash flow remain to be added.
2. **Financial performance analysis — IN PROGRESS**. Examine margins, working capital, net debt, cash generation and one-off items.
3. **Forecast assumptions & three-statement model — PLANNED**. Research operating assumptions, tie the statements and show scenarios.
4. **Equity valuation — PLANNED**. FCFF DCF, discount rate assumptions, enterprise-to-equity bridge and sensitivity.
5. **Investment note and dashboard — PLANNED**. Communicate investment thesis, risks, limitations and scenarios.

## Sources & research discipline

My principal source is the **[FY2025 audited consolidated filing (NGX Document Library)](https://doclib.ngxgroup.com/Financial_NewsDocs/DANGOTE_CEMENT_PLC_-_2025_AUDITED_FINANCIAL_STATEMENTS.pdf)**. FY2024 comparatives are reported in that document. For FY2023, I used the **[FY2024 Annual Report](https://cement.dangote.com/wp-content/uploads/2025/05/Dangote-Cement-FY-2024-Annual-Report.pdf)**. See [my source and interpretation register](docs/sources.md) for line-item provenance, including the cash/overdraft bridge.

I keep reported numbers separate from analytical definitions. For example, the simple `operating cash flow - cash PPE - cash intangibles` calculation is a **cash-flow proxy**, not unlevered free cash flow available to the firm. I won't present it as a completed DCF.

---

**Author:** [Ayoleyi-dev](https://github.com/Ayoleyi-dev) · Research / educational portfolio only.
