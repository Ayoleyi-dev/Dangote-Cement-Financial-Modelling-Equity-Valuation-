# Financial performance: what changed between 2024 and 2025?

I started with the audited Group accounts because I wanted to understand the business before forecasting it. The tables below keep the figures in **₦ million**, unless I say otherwise. I calculate ratios directly from those figures rather than copying rounded percentages from a presentation.

## Profitability

| Measure | FY2024 | FY2025 | How I calculate it |
|---|---:|---:|---|
| Revenue | 3,580,550 | 4,306,704 | Published income statement |
| Profit after tax | 503,247 | 1,014,921 | Published income statement |
| Gross margin | 54.04% | 62.05% | Gross profit / revenue |
| Operating margin | 32.18% | 40.99% | Operating profit / revenue |
| Net profit margin | 14.06% | 23.57% | Profit after tax / revenue |
| Effective tax rate | 31.30% | 33.78% | Tax expense / profit before tax |
| Finance costs / revenue | 19.56% | 8.16% | Absolute finance costs / revenue |

Revenue increased **20.28%**, but after-tax profit grew **101.67%**. I traced some of that gap to stronger gross and operating margins. Finance costs also declined from **₦700,299m** to **₦351,504m**, lifting profit further.

The next question is how much of that improvement can last. Pricing, fuel, logistics, financing and foreign-exchange movements could all change. That's why my forecast uses alternative margin assumptions rather than carrying one year's result forward unchanged.

## Liquidity, cash and capital allocation

| Measure | FY2024 | FY2025 | Interpretation |
|---|---:|---:|---|
| Operating cash flow (₦m) | 821,184 | 1,710,762 | Cash from operating activities |
| Operating cash flow / profit after tax | 1.63× | 1.69× | Simple cash conversion proxy |
| Current ratio | 0.74× | 0.76× | Current assets / current liabilities |
| Cash PPE purchases (₦m) | 423,149 | 497,428 | Cash capex, not accounting additions |
| Simple post-capex operating cash proxy (₦m) | 397,730 | 1,213,036 | CFO − cash PPE − cash intangible purchases |
| Reported net debt (₦m) | 2,061,948 | 682,921 | Note 30.1 company-defined net debt |

**What I would not infer from these figures:**

1. The *simple post-capex cash proxy* is **not FCFF** (free cash flow to the firm). Interest classification, taxes, operating working capital and other cash movements require care in a DCF.
2. FY2025 investing cash flow was **positive ₦620,354m**, driven in part by a **₦1,037,232m net parent-company-related loan inflow**. Positive investing cash flow alone does **not** mean the company stopped investing in its plants.
3. FY2025 total current liabilities exceed current assets (current ratio below 1), which is a reason to inspect the debt maturity and working-capital notes—not sufficient grounds by itself to conclude financial distress.
4. Bank overdrafts used for cash management are deducted in the statement-of-cash-flows cash reconciliation (see [source register](sources.md)). I did not treat the difference between cash definitions as a data error.
5. The company's **reported net debt** is based on its notes, not an invented aggregation of every financial-liability caption on the balance sheet.

## Why this matters for the eventual valuation

A **DCF is sensitive to margin assumptions and reinvestment needs**. If I simply extrapolate 2025's net margin indefinitely, I could substantially overstate a valuation. Before modelling future free cash flows, I will assess the durability of price increases, production input costs, working-capital investment and the capital expenditure pipeline.

## Repeat the analysis

```bash
python scripts/validate.py
python scripts/analyze.py
python scripts/analyze.py --check
```

The analysis script reads the committed CSVs and computes each ratio. `--check` verifies selected calculations against the published totals and expected first-stage ratios.

**Sources:** [FY2025 audited accounts (NGX)](https://doclib.ngxgroup.com/Financial_NewsDocs/DANGOTE_CEMENT_PLC_-_2025_AUDITED_FINANCIAL_STATEMENTS.pdf), consolidated Group statements and Notes 30.1 and 32.1.
