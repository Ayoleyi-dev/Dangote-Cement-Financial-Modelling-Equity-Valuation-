# Input-audit register (8 October 2026)

This is an **audit of the existing inputs**, not evidence that every input has been verified.

| DCF input | Existing value | Status | Action |
|---|---:|---|---|
| NGN government 10-year yield | 15.951% | **Independently cross-checked** against dated 6 Oct 2026 historical quote | Keep dated market observation; investigate bond duration and taxable curve |
| DANGCEM price | ₦1,066.70 | **Cross-checked** with 7 Oct 2026 history; FT shows an alternative closing convention of ₦1,055 | Retain dated reference, disclose vendor discrepancy; don't label as 8 Oct closing |
| Equity risk premium | 8.0% | **Not validated**: pure analyst scenario input | Derive from market implied premium or peer research |
| Beta | 1.0 | **Not validated**: placeholder | FT vendor lists beta 2.308 on its DANGCEM tear sheet; that is **not automatically substitutable** without knowing frequency/index/levering |
| Cost of debt | 18.0% | **Not validated**: placeholder | Calculate weighted current debt cost from notes and yields rather than equate with accounting finance cost |
| WACC | 23.57% | **Reproducible mechanically**, not research-validated | Calibrate beta/ERP, debt yield and equity/debt weights |
| Long-run growth | 4.0% | **Not validated**: assumption | Test NGN nominal growth vs sustainable reinvestment/ROIC |
| H1 net cash | ₦215.232bn | **Source-backed** at 30 Jun 2026 | Roll to valuation date when Q3 data available |
| Share count | 16.752bn excluding treasury | **Source-backed** at 30 Jun 2026 | Check corporate actions through 8 October |
| FY2026 stub | 84/365 | **Simplified timing** | Replace with actual 9M performance and accurate remaining-year forecast |
| FCFF working capital | broad accounting captions | **Proxy only** | Exclude financing/other non-operating balances and reconcile operating NWC |
| Minority interest bridge | book value | **Approximation** | Value noncontrolling interests and other non-operating items separately |

## Source URLs
- Historical sovereign yield: https://www.investing.com/rates-bonds/nigeria-10-year-historical-data
- DANGCEM historical closing price: https://ng.investing.com/equities/dangcem-historical-data
- Alternative FT close and vendor beta: https://markets.ft.markitdigital.com/data/equities/tearsheet/historical?s=DANGCEM%3ALAG
- DANGCEM H1 official investor centre: https://investors.dangote.com/financials

**Decision:** I have intentionally **not silently changed** the existing beta, equity risk premium, cost of debt, or terminal growth. Replacing one arbitrary value with another can create false precision. The sensitivity schedule quantifies uncertainty while the input research is incomplete.
