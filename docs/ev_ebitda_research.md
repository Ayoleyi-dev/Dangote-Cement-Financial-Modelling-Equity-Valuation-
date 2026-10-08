# Phase 4.2 — EV/EBITDA comparable-company research

**Analysis snapshot:** 8 October 2026. This is a portfolio-learning analysis, not investment advice. I use the **7 October 2026 reference share prices** and **31 December 2025 balance-sheet / FY2025 EBITDA** inputs. This is not a single-date mark-to-market enterprise value; the mixed dates are openly disclosed. All monetary inputs are **₦ million**, and shares are in **millions**.

## My calculation

```
Market equity value = reference closing price (NGN) × ordinary shares outstanding (million)
Unrestricted cash = reported cash and cash equivalents − restricted cash
EV = market equity value + interest-bearing borrowing + leases − unrestricted cash + non-controlling interests
EV/EBITDA = EV / FY2025 EBITDA
```

I use a common definition of enterprise value, but audited and issuer EBITDA definitions can still differ. I keep an explicit per-company `ebitda_basis` field rather than quietly describing these as identical.

## Source-provenance table

| Company | FY2025 earnings basis | Balance-sheet assumptions | Important caveat |
|---|---|---|---|
| Dangote Cement | Issuer Group EBITDA **₦1,981.1bn**, rounded (FY2025 release) | FY2025 interest-bearing financial liabilities ₦1,080.490bn, cash ₦397.569bn, NCI ₦99.900bn | Share count comes from H1 2026 disclosure; debt may include some leases so no additional lease amount is added. |
| BUA Cement | **₦553.669bn** EBITDA from MarketScreener FY2025 dataset; not yet recreated from every audited note | Audited debt including debt securities ₦526.630bn, cash ₦280.380bn, current lease ₦0.145bn | External EBITDA source; FY2025 accounts source for borrowings/share count; do **not** call EBITDA 'fully audited-reconciled'. |
| Lafarge Africa | **₦426.925bn**, calculated as audited Group operating profit ₦392.100bn + depreciation ₦34.784bn + amortisation ₦0.041bn | Audited Group no bank borrowing, lease liabilities ₦1.308bn, cash ₦388.067bn less restricted ₦3.205bn | This is an IFRS-based *reconstructed EBITDA proxy*, not necessarily management's adjusted EBITDA. |

Sources:
- Dangote official FY2025 results: https://www.dangotecement.com/wp-content/uploads/2026/03/Dangote-Cement-PLc-Result-Presentation-2025.pdf
- Dangote audited FY2025 group statements: https://doclib.ngxgroup.com/Financial_NewsDocs/DANGOTE_CEMENT_PLC_-_2025_AUDITED_FINANCIAL_STATEMENTS.pdf
- BUA audited FY2025 annual statements (Note 27 for share capital; Notes 24/25 for borrowings): https://www.buacement.com/documents/BUA%20Cement%20Full%20Year%202025%20Audited%20Report%20and%20Financial%20Statements2026030205175520260310051655.pdf
- BUA EBITDA vendor data: https://in.marketscreener.com/quote/stock/BUA-CEMENT-PLC-102186380/finances/
- Lafarge FY2025 annual accounts (Group income, balance sheet, Note 14, Note 22/27): https://fliphtml5.com/wsea/rfux/Lafarge_Africa_Plc_-_2025_Lafarge_Annual_Report_and_Accounts/
- DANGCEM dated price source: https://uk.investing.com/equities/dangcem-historical-data
- BUA date-linked share quote: https://in.marketscreener.com/quote/stock/BUA-CEMENT-PLC-102186380/finances/
- Lafarge dated price source: https://ng.investing.com/equities/wapco-historical-data

## How I avoid common mistakes

1. **I exclude Dangote itself** from the peer average. Two-peer mean and median happen to be identical.
2. **I don't mix profit after tax with EV.** EV/EBITDA compares enterprise value to pre-financing operating earnings; P/E remains an equity-only multiple.
3. **I exclude restricted cash** when it is explicitly disclosed (Lafarge, ₦3.205bn).
4. **I don't count BUA's borrowings twice:** bank borrowings plus debt securities are in the ₦526.630bn interest-bearing total; lease liabilities are separate.
5. **I don't silently call EBITDA standards-identical.** Dangote is issuer-adjusted/issuer-reported, Lafarge is IFRS constructed, and BUA uses vendor EBIT/EBITDA data.
6. **I don't call the result a price target.** A two-company premium can reflect scale, growth, liquidity, cross-border exposure and accounting choices rather than undervaluation.

## Pending before an institutional-quality relative valuation

- Reconstruct BUA's D&A and EBITDA line by line from the FY2025 notes.
- Audit Dangote EBITDA vs statutory EBIT + D&A and company non-recurring adjustments.
- Check consistency of 2025 leases / debt and shares across dates.
- Repeat all multiples on synchronized latest-available TTM operating results with matching latest balance sheets.
- Add wider regional and multinational cement peers with currency and accounting adjustments.

Run `python scripts/ev_ebitda.py --check` and `python scripts/ev_ebitda.py --export` to regenerate all outputs. Machine-readable sources are in `data/peers/ev_ebitda_inputs.csv`.
