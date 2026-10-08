# Phase 2 — Assumption-led operating forecast (FY2026–FY2030)

I am moving from **audited actuals** to a basic three-statement *teaching model*. I deliberately separate source figures from analyst **assumptions**; forecasts are **not Dangote Cement guidance** or investment recommendations.

## Source anchors

- [Audited FY2025 consolidated statements, NGX PDF](https://doclib.ngxgroup.com/Financial_NewsDocs/DANGOTE_CEMENT_PLC_-_2025_AUDITED_FINANCIAL_STATEMENTS.pdf) — consolidated profit or loss p20, financial position p22, cash flow p25 (printed pages).
- [Company's official H1 2026 investor centre](https://doclib.ngxgroup.com/Financial_NewsDocs/47629_DANGOTE_CEMENT_PLC-H1_2026_EARNINGS_RELEASE_CORPORATE_ACTIONS_JULY_2026.pdf) — H1 2026 *unaudited* figures: revenue about ₦2,513.9bn, EBITDA ₦1,188.3bn, PAT ₦638.5bn. Rounded presentation figures; not inputs to the audited FY2025 base.
- [FY2025 ratio review](financial_performance.md) and the [source register](sources.md).

## Why the model is 'three statement'

The forecast simultaneously generates:
1. **Income statement:** projected revenue, operating profit (EBIT), finance interest, tax and profit.
2. **Cash flow:** projected CFO, capex, debt financing, dividends and closing cash.
3. **Balance sheet:** PPE, working-capital assets and liabilities, outstanding debt, cash and shareholders' equity.

I test both **Assets − Liabilities − Equity = 0** and the **cash flow movement check = 0** each year, scenario by scenario.

## Editable analyst assumptions — NOT sourced company guidance

All rows of [assumptions/scenarios.csv](../assumptions/scenarios.csv) are *illustrative*. They are distinct from audited data. These should be revisited before any valuation.

| Key driver | FY2026 base assumption | Logic | Important limitation |
|---|---:|---|---|
| Revenue growth | 20.0% | Starting point close to FY2025's 20.3% growth and H1 2026's positive trajectory | FY2026 H1 performance cannot simply be annualised |
| Operating margin | 41.0% | Broadly near FY2025's 40.99% | Margins affected by fuel, FX, pricing and costs |
| Cash capex / revenue | 14.0% | Conservative expansion allowance above FY2025 cash capex/revenue (~11.55%) | Cash capex differs from reported additions; actual projects need separate schedule |
| D&A / revenue | 5.0% | Roughly FY2025's 4.99% | Simplifies intangible amortisation and PPE mix |
| Effective cash tax rate | 34.0% | Around FY2025 effective tax expense/PBT ~33.78% | Cash taxes and accrual taxes were very different in FY2025 |
| Interest cost on opening debt | 13.0% | Placeholder scenario assumption | Not a company disclosed cost of debt; actual financing / FX effects differ |
| Dividend payout / PAT | 50.0% | Illustrative cash distribution | NOT the board's declared dividend, and ignores precise share count |
| Debt draw/repayment | 0 | Neutral teaching simplification | Actual debt maturities and new borrowings MUST be modelled |
| Working-capital lines / revenue | Fixed profile | Based loosely on the FY2025 balance-sheet mix | IFRS categories include non-operating items |

*The downside, base and upside variants differ in revenue growth, margins, capex intensity, taxes, interest and payout. None is probability-weighted.*

### Revenue assumptions (% per year)

| Scenario | 2026 | 2027 | 2028 | 2029 | 2030 |
|---|---:|---:|---:|---:|---:|
| Downside | 12% | 8% | 6% | 5% | 4% |
| Base | 20% | 12% | 10% | 8% | 7% |
| Upside | 24% | 16% | 14% | 12% | 10% |

These values are used to **test sensitivity**, not to assert an actual future outcome.

## Accounting mechanics and modelling caveats

- I start at the **FY2025 audited Group balance sheet**. Opening debt means the *current and non-current financial liabilities* (not 'all current liabilities'), as reported on p22. This is different from the separate company-defined 'net debt' measure in Note 30.1.
- **Operating NWC** = inventories + trade & other receivables + current prepayments/other assets − trade & other payables − other current liabilities. This is an **approximation**, not pure operating-only working capital.
- **Cash flow from operations** = projected net profit + depreciation + interest added back − change in NWC. I deduct **cash interest in financing** to follow the presentation adopted by the company's 2025 cash-flow statement.
- **Cash flow from investing** = −cash capex. No asset disposals, dividends received, intercompany financing inflows or acquisitions are assumed.
- **Cash flow from financing** = new debt − cash interest − cash dividends.
- **PPE close** = opening PPE + forecast cash capex − total D&A. This assumes capex paid equals capitalised additions and treats all D&A as PPE depreciation; simplifying **not a statutory accounting prediction**.
- **Other assets and other liabilities remain unchanged** across years. No FX translation reserve, OCI, lease accounting, deferred taxes or inflation restatements are projected. Equity = opening equity + profit − dividends.
- I **do not** use the simplified cash flow output as a fair-value estimate. Discounting FCFF, terminal value, WACC, non-controlling interests, minority share bridge and current market price still require separate defensible research.

## Reproduce

```shell
python scripts/validate.py
python scripts/analyze.py --check
python scripts/forecast.py --check
python scripts/forecast.py --export
```

The last command creates CSV outputs in `data/forecasts/`. Every scenario should pass accounting and cash-bridge checks. This is a deliberately simple learning version, not a production-ready investment bank model.

## Questions before any DCF

- Separate cement and clinker **volumes, realised prices and geographic contributions**.
- Reconcile FY2025 management EBITDA definition with operating profit plus D&A.
- Build an evidence-led **plant expansion capex and depreciation schedule**.
- Resolve actual FY2026/2027 debt maturity and interest schedule.
- Model non-controlling interests, deferred taxes, dividends and capital structure more accurately.
- Estimate WACC from supportable market and debt inputs, with source date and sensitivity.

*My research status: Phase 2 modelling framework, 8 October 2026. No security recommendation.*
