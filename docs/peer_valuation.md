# Comparing Dangote Cement with two listed peers
I used the **7 October 2026 share prices** and **FY2025 audited earnings per share** for Dangote Cement, BUA Cement and Lafarge Africa. This gives a historical-earnings comparison; it is **not** an October 2026 trailing-twelve-month P/E.

| Ticker | Price (₦) | FY2025 audited EPS (₦) | Retrospective P/E |
|---|---:|---:|---:|
| DANGCEM | 1,066.70 | 59.86 | 17.82× |
| BUACEMENT | 297.00 | 10.51 | 28.26× |
| LAFARGE | 355.00 | 16.96 | 20.93× |

The two-peer average P/E is **24.60×**. Applying it to Dangote Cement's FY2025 EPS gives an indicative figure of **₦1,472.27 per share**. My first pass used rounded EPS for BUA and Lafarge; I replaced those with the audited figures of **₦10.51** and **₦16.96** after checking the statements. With only two peers—and differences in business mix, size and capital structure—I would not use this result alone as a price target.

- BUA audited FY2025 EPS ₦10.51 (Note 28): https://www.buacement.com/documents/BUA%20Cement%20Full%20Year%202025%20Audited%20Report%20and%20Financial%20Statements2026030205175520260310051655.pdf
- Lafarge Group basic EPS 1,696 kobo = ₦16.96 (Note 25): https://fliphtml5.com/wsea/rfux/Lafarge_Africa_Plc_-_2025_Lafarge_Annual_Report_and_Accounts/
- Dangote audited FY2025 Group EPS ₦59.86: https://doclib.ngxgroup.com/Financial_NewsDocs/DANGOTE_CEMENT_PLC_-_2025_AUDITED_FINANCIAL_STATEMENTS.pdf
- Reference prices recorded in `data/peers/issuer_prices_earnings.csv`.

I have now separately developed a [dated EV/EBITDA cross-check](ev_ebitda_research.md) with cash, borrowing and lease entries and an explicit EBITDA-definition audit. Comparing two approaches is useful, but they are both affected by historical period selection and the small peer set.
