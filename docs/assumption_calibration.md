# Stress-testing the discount rate and capital spending

I wanted to know which assumptions are driving the wide gap between the DCF and peer valuations. I focused first on the discount rate and cash spending on new plants and equipment. The results show sensitivity; they do **not** turn an uncalibrated DCF into a defensible price target.

## WACC
Existing analyst assumptions: local-government yield 15.951%, incremental equity risk premium 8%, levered beta 1.0, pre-tax debt cost 18%, debt tax shield 34%. The calculated WACC is ~23.57% under the old reference capital weights. The 8% ERP, 1.0 beta and 18% debt cost are **not verified issuer market estimates**.

A market-data vendor showed a beta of **2.308** for DANGCEM. That is useful context, but I could not establish its return window, benchmark or liquidity adjustments from the quote alone. I therefore kept the original beta of **1.0** as an explicit placeholder and tested **0.8, 1.0, 1.2 and 2.308** to see how much the model changes.

Price-vendor warning: FT's 7 October 2026 quote of ₦1,055 differs from Investing.com's ₦1,066.70. The existing Phase 3 model retains a fixed reference source/date. Any future market-backed WACC refresh must select one vendor convention, explain it, and archive the timestamp and data source.

Sources:
- FT share-price and beta screen: https://markets.ft.markitdigital.com/data/equities/tearsheet/historical?s=DANGCEM%3ALAG
- Historical NGN yield series: https://ng.investing.com/rates-bonds/nigeria-10-year-historical-data
- Dangote H1 2026 investor site for debt, cash and interim earnings: https://investors.dangote.com/financials

## Capex: cash disbursement versus asset additions

FY2025 Group reported **₦861.089bn capital additions**, of which Nigeria accounted for **₦729.780bn** and Pan-Africa **₦131.309bn**. Historical investing cash flow reported cash paid for PPE of **₦497.428bn**, plus **₦0.298bn** spent on intangibles. These are **not interchangeable**: advance payments and supplier credit generate a large difference between additions and cash disbursement.

In my FY2026 base case, cash capex is set at **14% of projected revenue**—about **₦723.5bn** against **₦5,168.0bn** in sales. I chose it as a test input, not because Dangote published that exact budget. The distinction matters: even a calculation that sits between two historical figures can still be a poor forecast.

I added a valuation-only stress for a permanent 1 percentage-point increase in capex/revenue (and selected larger/smaller changes). This reduces FCFF each year and terminal FCFF in FY2030; it is **not a full rerun of the three statements**. For future work I need segment capex, contractual commitments, capacity start dates, maintenance/expansion splits and financing.

Management context: Dangote's 3Mtpa Côte d'Ivoire grinding facility commissioned Q3 2025; its Q1 2026 update also discussed Itori and Ethiopia expansion and a long-term capacity goal of 80Mtpa by 2030. *Those are project drivers, not a quantified approved capex schedule.*

Primary sources:
- Dangote FY2025 statement and report: https://www.dangotecement.com/wp-content/uploads/2026/03/Dangote-Cement-PLc-Result-Presentation-2025.pdf
- Dangote FY2025 audited Group cash flows: https://doclib.ngxgroup.com/Financial_NewsDocs/DANGOTE_CEMENT_PLC_-_2025_AUDITED_FINANCIAL_STATEMENTS.pdf
- Côte d'Ivoire capacity update: https://cement.dangote.com/cote-divoire/
- Q1 2026 update: https://cement.dangote.com/wp-content/uploads/2026/04/Dangote-Cement-Q1-2026-Result-Presentation.pdf

## How to reproduce

```sh
python scripts/valuation.py --check
python scripts/assumption_stress.py --check
python scripts/assumption_stress.py --export
```

I will only call the WACC 'calibrated' after verifying the corporate debt instrument rates, treasury yield curve, market/sector beta and incremental ERP. I will only call forecast capex 'evidence-led' after attaching segment/project source assumptions and a PP&E roll-forward.
