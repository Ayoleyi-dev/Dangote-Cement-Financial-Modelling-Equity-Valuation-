# Phase 3 — Illustrative DCF and WACC methodology

**As-of reference: 8 October 2026.** My DCF is a transparent demonstration of the financial modelling mechanics, **not** a point-in-time institutional research target or a trade signal.

## Inputs, units and date discipline

I read FY2026E–FY2030E EBITDA-related forecast lines from the existing scenario outputs, not from undisclosed vendor estimates. Source and analyst inputs are explicitly labelled in [valuation_inputs.csv](../assumptions/valuation_inputs.csv).

| Input | Value | Source/reporting date | Status |
| --- | ---: | --- | --- |
| NGN sovereign 10-year yield | 15.951% | [Investing.com](https://ng.investing.com/rates-bonds/nigeria-10-year-historical-data), 6 Oct 2026 | indicative market quote |
| Incremental ERP / beta | 8.0% / 1.0× | 8 Oct 2026 | **uncalibrated analyst assumptions** |
| Pre-tax cost of debt | 18% | 8 Oct 2026 | **analyst assumption**, not company's credit pricing |
| Tax shield | 34% | FY2025 effective rate as context | **analyst approximation** |
| Last reference close | ₦1,066.70 | [Investing.com](https://ng.investing.com/equities/dangcem-historical-data), 7 Oct 2026 | prior-day quote |
| Shares outstanding, excluding treasury | 16,752,154,537 shares | [H1 interim financials](https://www.marketscreener.com/news/dangote-cement-quarter-2-financial-statement-for-2026-ce7f51d3db80f226), 30 Jun 2026 | reported |
| Group financial liabilities | ₦581,044m | [H1 2026 official earnings](https://doclib.ngxgroup.com/Financial_NewsDocs/47629_DANGOTE_CEMENT_PLC-H1_2026_EARNINGS_RELEASE_CORPORATE_ACTIONS_JULY_2026.pdf), 30 Jun 2026 | reported |
| Group cash | ₦796,276m | same H1 earnings release | reported |
| Non-controlling interest | ₦97,253m | H1 condensed consolidated statement of financial position | reported **book**, not market |
| Terminal cash flow growth | 4% | 8 Oct 2026 | **analyst assumption** |
| Remaining FY2026 stub | 84/365 year | 8 Oct 2026 | **timing simplification** |

The company was **net cash ₦215,232m** on the reported H1 debt/cash definition (796,276 minus 581,044). This represents a material change from **net debt ₦682,921m at FY2025**. I do **not** mix FY2025 net debt into a valuation using H1 2026 cash.

**Date mismatch:** The latest balance sheet available in this exercise is 30 June 2026; the quoted sovereign yield and reference share price are from early October. A true point-in-time October valuation must obtain/estimate Q3 movements in debt, cash and noncontrolling interests. Until then, these results are provisional.

## Step 1 — Unlevered free cash flow

```
NOPAT_t  = EBIT_t × (1 − marginal cash tax assumption_t)
FCFF_t   = NOPAT_t + D&A_t − cash capital expenditure_t − change in net working capital_t
```

I use the *change in a simplified net-working-capital proxy* from the earlier three-statement model. This includes some balance-sheet captions that are not purely operational, so the result requires a cleaner operational NWC schedule. In addition, financial assets, leases, deferred taxes and other non-cash movements require follow-up work.

As we are already in October, I include only a **84/365 pro-rata stub of FY2026E FCFF**. I do **not** pretend the entire 2026 projected cash flow lies ahead. The remaining years have full-year cash flows. This simplistic pro-rata stub does not replace Q3 actuals / Q4 budget information and creates material uncertainty.

## Step 2 — Weighted-average cost of capital

```
Cost of equity = NGN 10y government yield + beta × incremental ERP + extra country premium
Cost of debt after tax = assumed pre-tax cost of debt × (1 − tax shield)
WACC = equity market weight × cost of equity + debt weight × after-tax debt cost
```

I use 7 Oct 2026 reference price × H1 share count for illustrative market equity weights, and latest H1 2026 financial liabilities for debt weight. This is **not a rigorously tested market beta**; beta = 1.0 and ERP = 8% are placeholders, and a NGN nominal WACC is required when nominal NGN cash flows are discounted. I set additional country premium to **zero** to avoid simplistic double-counting sovereign risk.

## Step 3 — Discount forecast and terminal value

```
PV of FCFF = Σ FCFF_t / (1 + WACC)^t
Terminal value_2030 = FCFF_2030 × (1 + g) / (WACC − g)
Enterprise value = PV of explicit FCFF + PV of terminal value
```

I discount FY2026 stub at 84/365 years, and then 2027–2030 at 1+84/365, 2+84/365 etc. I explicitly require WACC > g.

## Step 4 — EV to equity value attributable to Dangote Cement owners

```
Equity attributable to owners ≈
  Enterprise value
  − June 2026 Group financial liabilities
  + June 2026 Group cash
  − June 2026 non-controlling interest book value
  + other non-operating adjustments (currently zero)
Share value = equity attributable to owners / 16,752.154537 million shares
```

The noncontrolling amount is **book value**, not separately measured fair value. A full analyst bridge needs to consider leases, excess versus operating cash, market valuation of subsidiaries/minorities, pension liabilities and associate investments.

## Sensitivity and investment-thesis limits

My sensitivity table varies WACC by −4 to +4 percentage points and nominal terminal growth from 2% to 6%. Even relatively small changes to the terminal discount rate can dominate share-price outputs.

I intentionally **do not issue a BUY/HOLD/SELL rating**. To make this a stronger portfolio investment thesis I still need to:
- Segment Nigeria and Pan-Africa volumes, realised prices and costs.
- Use the September 2026 Capital Markets Day expansion/capex disclosures and verify costs/timing.
- Refine interest, debt maturity, leases and tax schedules.
- Calibrate market beta, equity risk premium and debt yield to contemporaneous evidence.
- Check peer EV/EBITDA and P/E multiples, minority interest market value and Q3 information.
- Audit assumption reasonableness and write downside risk commentary.

## Reproduce

```bash
python scripts/validate.py
python scripts/forecast.py --check
python scripts/valuation.py --check
python scripts/valuation.py --export
```

Three generated CSVs live in `data/valuations`: case outputs, annual FCFF bridge and WACC/g sensitivity. I maintain scenario drivers in machine-readable files for transparency.

*For educational/portfolio demonstration only. Sources and numbers date-stamped 8 October 2026.*
