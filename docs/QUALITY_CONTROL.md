# Quality-control review

**Project:** Dangote Cement financial modelling and equity valuation  
**Review date:** 8 October 2026  
**Branch:** `development`  
**Decision:** **Hold the merge until final review.**

## What I checked

I went back through the source tables, the forecast model, the valuation outputs and the research documents. My goal was to catch inconsistencies that would be embarrassing—or misleading—once the project is public.

### Data and calculation checks

| Area | Check | Result |
|---|---|---|
| Historical income statements | FY2023–FY2025 revenue/cost/gross profit and tax/profit relationships | Pass |
| Historical balance sheets | FY2024 and FY2025 assets less liabilities equal equity | Pass |
| Historical cash | Balance-sheet cash reconciles to cash-flow cash using the disclosed cash-management overdrafts | Pass |
| Three-statement forecasts | Every 2026–2030 scenario balances assets, liabilities and equity, and reconciles cash movement | Pass |
| DCF | Present value of free cash flows + present value of terminal value equals enterprise value; equity and per-share bridges reconcile | Pass |
| P/E comparables | Share price divided by audited FY2025 EPS; two-peer group excludes Dangote | Pass |
| EV/EBITDA comparables | Market capitalisation, debt, leases, cash and non-controlling interests reconcile to EV | Pass |
| Dashboard | FY2025 historical KPIs, model forecasts, peer multiples, valuation cases and sensitivity grid match committed source CSVs | Pass |
| Report and README | Key figures, forecast periods and valuation caveats agree with model outputs | Pass |

An independent read-through of the committed `development` data passed **605 cross-file assertions** with **zero calculation or data-consistency failures**. The checks covered 256 dashboard financial observations, 3 DCF scenarios, 3 comparable companies and the 25-cell sensitivity grid.

The repository also contains `scripts/qc_release.py` for repeatable release assertions. This should run with all existing calculation and dashboard tests in GitHub Actions. **Hosted CI success must still be confirmed independently**; the 605 checks above were a separate review, not a claimed hosted workflow result.

### External evidence checked

- The FY2025 Group figures match Dangote Cement's audited results and official FY2025 results presentation: revenue **₦4,306,704m**, operating profit **₦1,765,277m**, profit after tax **₦1,014,921m**, reported EBITDA approximately **₦1,981,134m** and Group volumes about **27.5Mt**.
- I kept the company's reported EBITDA separate from IFRS operating profit plus depreciation and amortisation.
- I corrected the peer P/E dataset to use the audited FY2025 EPS figures (**BUA ₦10.51; Lafarge ₦16.96**) instead of press-release rounding.
- Cash paid for PPE and accounting PPE additions are separate rows. The balance-sheet and cash-flow cash differences are explained rather than silently adjusted.

Primary audited financial figures: [Dangote Cement FY2025 results](https://dangotecement.com/wp-content/uploads/2026/03/Dangote-Cement-PLc-Result-Presentation-2025.pdf) and [audited accounts](https://doclib.ngxgroup.com/Financial_NewsDocs/DANGOTE_CEMENT_PLC_-_2025_AUDITED_FINANCIAL_STATEMENTS.pdf).

## Changes made to the writing

I rewrote the [project introduction](../README.md), [research report](../reports/DANGCEM_Equity_Research_Case_Study_2026-10-08.md), dashboard guide and key financial explanations. They now focus on the question, the evidence, the calculation and what I concluded. I removed awkward repeated disclaimers where a clear limitation would suffice, without hiding the limitations themselves.

The technical documentation still includes enough detail to reproduce the work. I used the first person where I describe my decisions and research process, while keeping calculations and source labels objective.

## Items that still need work

These are not failed arithmetic tests; they are evidence or deliverable gaps.

| Priority | Open item | Why it matters |
|---|---|---|
| **High** | Calibrate beta, equity risk premium and company borrowing costs | The DCF's 23.57% WACC is assumption-led rather than empirically validated |
| **High** | Put the latest available interim results, share prices, cash and debt on the same valuation date | Current model bridges use mixed dates |
| **High** | Build a segment-level volume/price and capex forecast | The forecast currently uses broad revenue and capex percentages |
| **High** | Reconcile BUA EBITDA to its audited report and align all three EBITDA definitions | Peer EV/EBITDA comparisons may not be strictly like-for-like |
| **Medium** | Assemble and visually test a native `.pbix` report in Power BI Desktop | The repository contains a data-and-DAX import kit plus HTML preview, not a finished PBIX |
| **Medium** | Verify all financial source links at release time, and capture durable copies where permitted | Public investor links and market data can change |
| **Medium** | Review the formatted PDF/Word report against the version-controlled Markdown | Prevent document versions from drifting apart |

## Final merge conditions

Before merging `development` into `main`, I will:

1. Run the full Python test suite and verify the result of the hosted GitHub Actions workflow.
2. Check the README, report, dashboard and downloadable files against the same source commit.
3. Ensure all reported figures, assumption dates and illustrative outputs are labelled consistently.
4. Review the native Power BI deliverable separately; if it is not ready, label it clearly as outstanding.
5. Get final approval before touching `main`.

**Current status:** the source figures and arithmetic checks are consistent, but the project is **not yet investment-grade**. It is suitable for portfolio review as an explicitly provisional research case study.
