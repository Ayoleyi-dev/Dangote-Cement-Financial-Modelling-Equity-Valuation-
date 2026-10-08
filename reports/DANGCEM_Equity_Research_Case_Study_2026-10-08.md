# Dangote Cement Plc | Equity Research Case Study

**NGX:** DANGCEM · **Research date:** 8 October 2026 · **Status:** Working research draft

**Author:** Ayoleyi Gbenga-Ayodeji · Independent portfolio research

> I wrote this report to bring the work in my financial model into one place: what Dangote Cement reported, what changed in the business, and what the numbers might mean for a valuation. Historical results are sourced from company disclosures. Forecasts and valuations are my own scenarios, not company guidance. I am not assigning a BUY, HOLD or SELL rating because several important assumptions still need validation.

## 1. What I found

Dangote Cement had a striking FY2025. Group revenue reached **₦4,306.7bn**, up **20.3%**, while profit after tax more than doubled to **₦1,014.9bn**. Operating profit was **₦1,765.3bn**, and the company reported EBITDA of about **₦1,981.1bn**, a **46.0% margin**. Yet Group cement and clinker volumes edged down **0.9%** to **27.5 million tonnes**. That tells me the year deserves a closer look at pricing, operating costs, product mix and financing—not just sales volumes. [S1–S2]

The balance sheet also changed: Group assets stood at **₦6,040.7bn**, liabilities at **₦3,420.6bn**, and equity at **₦2,620.1bn** at December 2025. The business generated **₦1,710.8bn in operating cash flow**. It paid **₦497.4bn** in cash for property, plant and equipment, which is different from the value of PPE additions booked in the accounts. [S1]

By June 2026, the company reported **H1 revenue of ₦2,513.9bn**, **EBITDA of ₦1,188.3bn**, **profit after tax of ₦638.5bn** and **net cash of ₦215.2bn**. These are interim figures. They help me challenge the forecasts, but they do not tell me what the full year will look like on their own. [S3]

### Questions I still need to answer

- Can operating margins and the mix of Nigeria versus Pan-Africa earnings be maintained through energy and foreign-exchange changes?
- How much cash will maintenance, expansion, debt service and working capital require?
- Why does my provisional DCF imply much lower equity values than my two-peer historical-multiple cross-checks?
- What new segment, market and balance-sheet evidence would close the valuation gaps?

## 2. Business and operating context

Dangote Cement operates a multi-country cement business with reported installed capacity of **55.0 million tonnes per annum** and operations in multiple African markets. It commissioned a **3Mta Côte d'Ivoire grinding facility** in 2025. The FY2025 results release attributes growth partly to pricing discipline, improved energy mix, operational cost control and exports, including an **18.6%** increase in Nigeria cement and clinker export volumes. [S2, S4]

There are reasons to be constructive about the business: established capacity, export routes and stronger Nigerian operations can support future cash generation. There are also reasons to be careful. Cement demand moves with construction activity, energy and distribution costs can rise quickly, and new plants take cash before they earn it back. I would not carry the FY2025 margin straight into every forecast year without testing those pressures.

## 3. Historical financial analysis

| Consolidated Group metric | FY2023 | FY2024 | FY2025 |
|---|---:|---:|---:|
| Revenue (₦bn) | 2,208.1 | 3,580.6 | **4,306.7** |
| Operating profit (₦bn) | 734.3 | 1,152.0 | **1,765.3** |
| Profit after tax (₦bn) | 455.6 | 503.2 | **1,014.9** |
| Gross margin | 54.4% | 54.0% | **62.0%** |
| Operating margin | 33.3% | 32.2% | **41.0%** |
| Net margin | 20.6% | 14.1% | **23.6%** |

*I computed margins from the source-linked historical model. FY2023 income data are taken from the 2024 annual report's comparison; FY2024–2025 from audited Group statements. Values rounded.* [S1, S5]

The FY2025 income statement shows **₦2,672.3bn** gross profit, **₦1,532.7bn** profit before tax and **₦517.7bn** income tax expense. Finance costs dropped from **₦700.3bn in 2024 to ₦351.5bn in 2025**. Together, improved gross profit and lower finance costs help explain the jump in after-tax profit. But I still need to separate what looks repeatable from what reflects financing, prices and other conditions specific to that year. [S1]

### Cash conversion and capital investment

FY2025 operating cash flow was **₦1,710.8bn**, versus FY2024 **₦821.2bn**. FY2025 investing cash flow was positive **₦620.4bn**, including related-party loan cash movements; this must **not** be mistaken for the absence of capex. **Cash PPE purchases were ₦497.4bn**, whereas accounting PPE additions were **₦861.1bn**: supplier credit and prepayments help reconcile them. [S1]

The FY2025 cash-flow statement ended with **₦362.6bn cash equivalents**, while the balance sheet reported **₦397.6bn cash**, reconciled through **₦35.0bn** cash-management overdrafts. I retain the two accounting definitions and do not force equality without the overdraft adjustment. [S1]

## 4. Operating forecast framework (illustrative)

To explore the next five years, I built three scenarios starting from the FY2025 audited accounts. The inputs in `assumptions/scenarios.csv` control sales growth, operating margin, capital spending, depreciation, taxes, interest, dividends and working capital. The projected statements reconcile with one another, but the model is still deliberately simplified. It does not yet predict volumes and prices separately for Nigeria and the rest of Africa.

| Scenario | FY2026E revenue (₦tn) | FY2026E PAT (₦tn) | FY2030E revenue (₦tn) |
|---|---:|---:|---:|
| Downside | 4.82 | ~1.04 | 6.03 |
| Base | 5.17 | 1.30 | 7.36 |
| Upside | 5.34 | ~1.45 | 8.70 |

Historical and forecast values are explicitly separated in the CSVs and dashboard. The forecast model balances Assets = Liabilities + Equity, but that identity alone cannot validate its economic assumptions. I hold other assets/liabilities and debt flat in simplified form, model capex paid as additions, and use broad accounting working-capital categories; these are substantive limitations.

## 5. DCF valuation (prototype, not price target)

I estimate unlevered free cash flow using:

`FCFF = EBIT × (1 − assumed tax rate) + depreciation & amortisation − cash capex − Δworking capital`.

I discount forecast cash flows at an illustrative **23.57% nominal NGN WACC**, assume **4.0%** nominal terminal growth, and include only an approximate **84/365-year** remaining-FY2026 cash-flow stub. Cost of equity is modeled as a 15.951% 6 October 2026 government yield plus **1.0 × 8.0%** equity risk premium. The **beta, ERP, 18% pre-tax debt cost and 4% perpetual growth** are assumption inputs, not calibrated market estimates. [S6]

The equity bridge uses **June 2026 net cash ₦215.2bn**, book non-controlling interest and shares outstanding, although the valuation has an October market-date reference. This **date mismatch is material**. [S3]

| DCF scenario | Enterprise value (₦tn) | Indicative equity value/share |
|---|---:|---:|
| Downside | 3.71 | ₦228.68 |
| Base | **6.41** | **₦389.64** |
| Upside | 8.21 | ₦497.04 |

For the Base scenario, about **51.5% of discounted enterprise value comes from terminal value**, meaning long-run cash flow and WACC assumptions have substantial influence. My 25-cell WACC/terminal-growth sensitivity table is published in `data/valuations/sensitivity_base.csv`.

**What limits this DCF:** the beta and borrowing-cost estimates are not calibrated; the 2026 remaining-year cash flow is prorated; debt maturities, operating working capital and maintenance versus expansion capex need more detail. I also used book value for non-controlling interests and June balance-sheet data against an October market reference. For these reasons, **₦389.64 is a model result—not a fair-value conclusion**.

## 6. Relative valuation (historical peer comparison)

I use the NGX-listed **BUA Cement** and **Lafarge Africa** as an initial local peer set, and exclude Dangote Cement from the two-peer mean. I use **7 October 2026 reference share prices**, **FY2025 audited EPS** and FY2025 EBITDA/balance-sheet inputs. Thus these metrics are not synchronized contemporary trailing-twelve-month multiples. [S7–S9]

| Company | FY2025 earnings P/E | EV / FY2025 EBITDA |
|---|---:|---:|
| Dangote Cement | 17.82× | 9.42× |
| BUA Cement | 28.26× | 18.61× |
| Lafarge Africa | 20.93× | 12.50× |
| **Peer mean (excluding Dangote)** | **24.60×** | **15.55×** |

Applying the two-peer average P/E to Dangote Cement's FY2025 EPS gives **₦1,472.27 per share**. Using the peer EV/EBITDA average and then adjusting for Dangote's historical financial liabilities, cash and non-controlling interests gives **₦1,792.57 per share**. I view both as cross-checks, not targets. Two peers cannot capture every difference in geography, growth, balance sheets or accounting policies.

BUA FY2025 EBITDA remains sourced to a third-party provider pending a line-by-line audit; Lafarge EBITDA is reconstructed as operating profit plus depreciation and amortisation, not a harmonized management-adjusted measure. See `docs/ev_ebitda_research.md` for line-item provenance and caveats. [S8–S9]

## 7. Interpretation and risks

**Observed strengths:** expanding FY2025 gross and operating margins; substantially improved operating cash flow; company-reported progress in Nigerian production energy mix; lower June 2026 reported Group net debt / net cash. [S1–S3]

**Risks to monitor:** (i) domestic demand and pricing pressure; (ii) diesel, gas, electricity and logistics costs; (iii) foreign-exchange translation and Pan-Africa operating performance; (iv) execution, timing and financing of expansion capex; (v) debt and tax treatments; (vi) environmental and emissions regulations; (vii) market data vendor differences, beta estimation and liquidity; and (viii) inconsistent peer EBITDA definitions.

**Why the methods disagree:** the DCF depends heavily on a provisional discount rate and future reinvestment assumptions. The multiples reflect what investors were paying for other businesses' historical earnings, each with its own outlook and risks. The disagreement makes me less confident in a single-point estimate, not more confident that the market has made a mistake.

## 8. Research decision and next validation gates

**My conclusion:** I am not making a formal investment recommendation yet. I have a working analytical framework and clear questions to investigate, but the evidence is not strong enough to support a buy-or-sell decision.

Before issuing a share-price target, I would:
1. Reconcile FY2026 nine-month financials and refresh the balance-sheet and market-price dates.
2. Build segment volume × realized-price forecasts and evaluate cost/energy assumptions.
3. Model maintenance/expansion capex, depreciation, financing and normalized operating working capital.
4. Derive cost of debt from actual debt instruments, beta from transparent return samples, and a justified NGN equity-risk premium.
5. Rebuild BUA/Lafarge multiples on matched TTM, balance-sheet and EBITDA accounting bases; broaden the peer set.
6. Document repeatable tests, review dashboard representations and sign off a separate risk/recommendation memorandum.

## 9. Reproducibility

The GitHub `development` branch contains raw financial statement CSVs, analyst scenario inputs, Python scripts (`validate.py`, `forecast.py`, `valuation.py`, `comparables.py`, `ev_ebitda.py`, `assumption_stress.py`), source audits and the Power BI-ready dashboard import kit. Source files are versioned, assumptions are labelled and downstream figures are reproducible. The report should be reviewed against the exact branch commit before publication.

## Sources and source periods

- **[S1]** Dangote Cement FY2025 audited consolidated statements (31 Dec 2025), NGX: https://doclib.ngxgroup.com/Financial_NewsDocs/DANGOTE_CEMENT_PLC_-_2025_AUDITED_FINANCIAL_STATEMENTS.pdf
- **[S2]** Dangote Cement FY2025 audited earnings release (28 Feb 2026): https://doclib.ngxgroup.com/Financial_NewsDocs/DANGOTE_CEMENT_EARNINGS_RELEASE_FOR_FULL_YEAR_2025.pdf
- **[S3]** Dangote investor financial centre H1 2026, unaudited (30 Jun 2026): https://investors.dangote.com/financials
- **[S4]** Dangote Cement company overview and capacity: https://cement.dangote.com/about-us-2/
- **[S5]** Dangote Cement FY2024 Annual Report, comparative FY2023 Group income statement: https://cement.dangote.com/wp-content/uploads/2025/05/Dangote-Cement-FY-2024-Annual-Report.pdf
- **[S6]** Nigeria 10-year sovereign yield quote for 6 Oct 2026: https://ng.investing.com/rates-bonds/nigeria-10-year-historical-data
- **[S7]** DANGCEM reference share-price history: https://www.investing.com/equities/dangcem-historical-data
- **[S8]** BUA Cement FY2025 audited financial-report archive: https://www.buacement.com/financialreport/
- **[S9]** Lafarge Africa FY2025 audited annual reports: https://www.lafarge.com.ng/financial-reports
- **[S10]** Underlying portfolio model and peer source flags: `data/`, `assumptions/`, `docs/valuation_methodology.md`, `docs/ev_ebitda_research.md` (same repository).

---

*Independent portfolio research. The models are illustrative and have not been independently reviewed; this report is not investment advice.*
