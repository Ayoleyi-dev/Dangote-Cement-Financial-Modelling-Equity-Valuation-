# Dangote Cement: Financial Modelling & Equity Valuation

**An independent investment research project by Ayoleyi Gbenga-Ayodeji**  
**Company:** Dangote Cement Plc (NGX: DANGCEM)  
**Research date:** 8 October 2026 · **Development status:** review in progress

I built this project to see how far I could take publicly reported company results: from cleaning the financial statements and understanding what changed, to forecasting cash flow and testing what the business might be worth.

My background is in data analytics, so I approached the work the way I would approach any serious analysis: keep the source records, make the calculations repeatable, check what the numbers mean, and explain where the assumptions are doing the heavy lifting.

This is a **portfolio case study**, not investment advice. The valuation figures below are model outputs, not investment recommendations or independently verified price targets.

## What stood out

Dangote Cement reported **₦4.31 trillion in Group revenue** and **₦1.01 trillion in profit after tax** for FY2025. Revenue grew about **20.3%**, while profit after tax rose about **101.7%**. The difference made me look beyond sales growth: gross margins improved and finance costs declined sharply. The company also generated **₦1.71 trillion in operating cash flow**. [FY2025 audited results](https://doclib.ngxgroup.com/Financial_NewsDocs/DANGOTE_CEMENT_PLC_-_2025_AUDITED_FINANCIAL_STATEMENTS.pdf)

A second interesting finding came from the valuation work. The discounted cash-flow model and the two-company peer comparisons produce very different figures:

| Method | Illustrative value per share | How to read it |
|---|---:|---|
| DCF — downside | ₦228.68 | Cash-flow model under conservative assumptions |
| DCF — base | ₦389.64 | Highly sensitive to the provisional discount rate |
| DCF — upside | ₦497.04 | Stronger operating assumptions |
| Peer P/E | ₦1,472.27 | Two local peers' FY2025 earnings multiples |
| Peer EV/EBITDA | ₦1,792.57 | Two local peers' FY2025 EBITDA multiples |

I **have not averaged these into a price target**. The DCF uses assumptions that need better calibration; the peer group is small, EBITDA definitions differ, and market prices and financial statements are from different dates. The gap is a question for further research, not proof that the stock is mispriced.

## What's in the repository

| Folder | Contents |
|---|---|
| [data](data/) | Reported financial statements and model outputs, including scenario and peer valuation CSVs |
| [assumptions](assumptions/) | Editable forecast and DCF inputs, with source dates |
| [scripts](scripts/) | Historical checks, financial analysis, forecasts, DCF and peer comparison calculations |
| [docs](docs/) | Source register, accounting explanations, input audits and methodology |
| [dashboard](dashboard/) | Power BI import tables, DAX measures, report theme and an interactive browser preview |
| [reports](reports/) | The [equity research case study](reports/DANGCEM_Equity_Research_Case_Study_2026-10-08.md) |

All monetary CSV values are in **₦ million** unless a file explicitly says otherwise. The historical income statement covers FY2023–FY2025; the historical balance sheet and cash flow cover FY2024–FY2025. FY2026–FY2030 values are scenario forecasts, not reported actuals.

### Reproduce the results

The calculation scripts use Python's standard library; no API key or private dataset is required.

```bash
python scripts/validate.py
python scripts/analyze.py --check
python scripts/forecast.py --check
python scripts/valuation.py --check
python scripts/comparables.py --check
python scripts/ev_ebitda.py --check
python scripts/assumption_stress.py --check
python dashboard/scripts/build_data.py
python dashboard/scripts/test_data.py
python scripts/qc_release.py
```

The source register is in [docs/sources.md](docs/sources.md), and the valuation inputs are explained in [docs/valuation_methodology.md](docs/valuation_methodology.md). To see the dashboard, open [the browser preview](dashboard/preview/index.html) or follow the [Power BI Desktop build guide](dashboard/README.md). The browser preview is **not** a Power BI `.pbix` file.

## How I worked through the analysis

**1. Start with the accounts.** I extracted the Group figures, checked the subtotals, and reconciled the difference between balance-sheet cash and cash in the cash-flow statement. That difference relates to overdrafts included in the cash-flow cash definition.

**2. Understand performance.** I examined profitability, finance costs, operating cash, debt and capital spending. I kept cash paid for equipment separate from accounting additions to property, plant and equipment.

**3. Build scenarios.** I developed three FY2026–FY2030 cases. They connect profit, balance sheet and cash movements, with explicit assumptions for growth, operating margin, tax, depreciation, working capital and capex.

**4. Explore valuation.** I built a free-cash-flow DCF with WACC and terminal-growth sensitivities, then checked the result against BUA Cement and Lafarge Africa using P/E and EV/EBITDA.

**5. Present the findings.** I prepared a research report and Power BI-ready dashboard tables. The native Power BI report still needs to be assembled and tested in Desktop.

## What remains open

The numbers are reproducible, but reproducibility does not make the assumptions correct. Before calling this an investment-grade valuation, I need to improve the cost-of-capital inputs, model cement volumes and selling prices by segment, separate maintenance from expansion capex, reconcile peer EBITDA definitions, and put market prices, cash and debt on a consistent valuation date.

The latest progress and any issues that should block the release are recorded in [the quality-control review](docs/QUALITY_CONTROL.md).

## Branch and review policy

I am keeping this work on **`development`** until the source checks, calculations, report and dashboard have been reviewed. **Nothing has been merged into `main`.**

---

**Research and analysis:** Ayoleyi Gbenga-Ayodeji  
[GitHub profile](https://github.com/Ayoleyi-dev) · [Portfolio](https://ayoleyi-portfolio.vercel.app)

*Independent educational research. No securities recommendation.*
