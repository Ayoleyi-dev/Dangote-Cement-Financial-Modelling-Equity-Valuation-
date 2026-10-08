# Financial sources and accounting choices

I work from the **consolidated Group** results throughout the historical model. The annual filings also contain separate figures for the Nigerian parent company; mixing the two would make the analysis unreliable. I note the source document and page for every major statement.

| ID | Filing | Group data | Page(s) |
|---|---|---|---|
| S01 | [FY2025 audited financial statements, NGX-hosted](https://doclib.ngxgroup.com/Financial_NewsDocs/DANGOTE_CEMENT_PLC_-_2025_AUDITED_FINANCIAL_STATEMENTS.pdf) | FY2025 and FY2024 financial figures | PDF p20 (income), p22 (balance sheet), p25 (cash flow) |
| S02 | [FY2024 annual report](https://cement.dangote.com/wp-content/uploads/2025/05/Dangote-Cement-FY-2024-Annual-Report.pdf) | FY2023 comparison for the income statement | printed p151 |
| S03 | [Same FY2025 audited statements](https://doclib.ngxgroup.com/Financial_NewsDocs/DANGOTE_CEMENT_PLC_-_2025_AUDITED_FINANCIAL_STATEMENTS.pdf) | Net debt definition | p75, Note 30.1 |
| S04 | [Same FY2025 audited statements](https://doclib.ngxgroup.com/Financial_NewsDocs/DANGOTE_CEMENT_PLC_-_2025_AUDITED_FINANCIAL_STATEMENTS.pdf) | Balance sheet vs cash flow cash bridge | p85, Note 32.1 |
| S05 | [Official results archive](https://cement.dangote.com/results-and-presentation-for-shares/) | Interim 2026 filings for later use | next milestone |

## Rules I followed

- **Units:** NGN millions, except per-share earnings. I store expenses and cash outflows as negative values in CSVs.
- **Reporting period:** FY2024 and FY2025 are fiscal years ending 31 December.
- **Scope:** Group historicals include subsidiaries; parent-only columns have deliberately been excluded.
- **Presentation:** published subtotals are retained verbatim; the validator independently recomputes them.
- **Missing data:** the FY2023 balance sheet and cash flow are **not yet populated**; they are not inferred from FY2024.
- **2026 interim data:** not mixed with full-year annual values.

## Subtleties from the filing

### Why isn't cash on the balance sheet equal to cash at the bottom of the cash flow?

Note 32.1 includes certain **bank overdrafts repayable on demand that are used for cash management** in the statement-of-cash-flows definition.

```
                                       FY2024       FY2025
Balance sheet cash (₦m)                 449,831      397,569
Bank overdrafts                        (318,115)     (34,983)
Cash-flow statement cash                131,716      362,586
```

These quantities reconcile exactly. I keep the overdraft as its own input, rather than treating the difference as an error.

### Why are PPE additions and cash purchases different?

The investing cash-flow presentation includes an explanatory bridge. **FY2025 PPE additions (₦861,089m)** were not identical to cash paid to acquire PPE (**₦497,428m**): non-current prepayments and unpaid supplier credit adjusted the cash figure. The notes are not *additional investing cash flows* and must not be double-counted.

### Net debt

Group **financial liabilities (Note 26)** less balance-sheet cash equals the management-defined net debt:

- FY2024: ₦2,511,779m − ₦449,831m = **₦2,061,948m**
- FY2025: ₦1,080,490m − ₦397,569m = **₦682,921m**

Note this is not the same as taking every balance-sheet financial-liability caption indiscriminately: the reported Note 26 definition is the anchor.

### Notes about source accessibility

The NGX document-library PDF is the version I relied on for FY2025 and FY2024. Some older company-hosted URLs have intermittently returned errors, so historical figures should always be checked against the named audited filing; I have not guessed unsupported FY2023 balance-sheet or cash-flow values.
