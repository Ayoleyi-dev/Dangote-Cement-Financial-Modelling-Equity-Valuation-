# Dangote Cement | Power BI Investment Dashboard

**Status:** data model + DAX + theme + reproducible browser preview.
**This is not a .pbix or a Power BI Desktop-tested .pbip file.** Power BI Desktop is required to assemble, open and save the native report. The GitHub repository remains on **development**.

## What I made

| Asset | Role |
|---|---|
| data/DimYear.csv, DimScenario.csv, DimMetric.csv | Reporting dimensions, analyst scenario slicer and metric catalog |
| data/FactFinancial.csv | Historical actuals and scenario projections, **all values ₦ million** |
| data/FactPeer.csv | FY2025 peer P/E and EV/EBITDA, October 2026 reference prices |
| data/FactValuation.csv | DCF scenario values with source-date caveats |
| data/FactSensitivity.csv | 25 combinations of WACC and long-run growth |
| data/FactFCFF.csv | Five forecast years × three scenarios: unlevered FCFF |
| powerbi/measures.dax | Individually copyable named measures |
| powerbi/theme.json | Importable dark report theme |
| preview/index.html | Self-contained browser prototype: no network or Power BI needed |
| scripts/build_data.py, scripts/test_data.py | Rebuild and check table consistency |

Rebuild from the underlying existing Python model:

\`\`\`sh
python scripts/validate.py
python scripts/forecast.py --check
python scripts/valuation.py --check
python scripts/comparables.py --check
python scripts/ev_ebitda.py --check
python dashboard/scripts/build_data.py
python dashboard/scripts/test_data.py
\`\`\`

## Power BI Desktop steps

1. On Windows, open Power BI Desktop. Use **Home → Get data → Text/CSV** to import **each of the eight CSV files** in \`dashboard/data/\`. See Microsoft's official [Text/CSV connector guide](https://learn.microsoft.com/en-us/power-query/connectors/text-csv).
2. In Power Query verify **Year** and **SortOrder** are Whole Number; the NGNm/ratio/share-price columns are Decimal Number; date-status columns are Text. Keep company tickers and date-as-of fields as **Text** for this snapshot. Select **Close & Apply**.
3. In **Model view**, create the relationships **DimYear[Year] (1) → FactFinancial[Year] (*)** and **DimYear[Year] (1) → FactFCFF[Year] (*)**, both single-direction. Then **DimMetric[MetricKey] (1) → FactFinancial[MetricKey] (*)**. Leave **DimScenario disconnected**, otherwise selecting Base would filter away audited historical actuals. FactPeer, FactValuation and FactSensitivity are independent snapshot tables. Do **not** make accidental many-to-many relationships.
4. Under **View → Themes → Browse for themes**, import \`dashboard/powerbi/theme.json\` (Microsoft [report theme documentation](https://learn.microsoft.com/power-bi/create-reports/report-themes-create-custom)).
5. Add each definition from \`powerbi/measures.dax\` as a distinct **New measure**. Place the \`DimScenario[Scenario]\` slicer on scenario-sensitive report pages with single-select and default **Base**.
6. Build the following pages, then save as \`Dangote_Cement_Investment_Dashboard.pbix\` **on your computer**. The source-controlled assets remain in the repo.

### Page 1 — Executive overview

- Header: **Dangote Cement | Equity Research**, badge: "AUDITED FY2025 / ASSUMPTION-DRIVEN FY2026–30".
- Cards: FY2025 revenue, FY2025 net profit, FY2025 net margin, FY2025 operating cash flow. Use a **Year = 2025 visual filter** on each historical KPI card.
- Combination or line chart: **DimYear[Year]** vs [Revenue (NGNm)], [Net Profit (NGNm)]. Display 2023–2030, set dashed line/annotation at FY2025 vs FY2026 boundary. Do not present forecast years as actual.
- Historical gross, operating and net margins for FY2023–2025. Operating and net margins for later years are scenario forecasts.

### Page 2 — Forecast and free cash flow

- Slicer \`DimScenario[Scenario]\`: Base / Downside / Upside.
- Area or line visual: FY2026–2030 revenue and operating profit via measures.
- Column chart: \`DimYear[Year]\` and [FCFF (NGNm)] (FY2026–2030 only).
- Small multiples: capex, operating cash flow, profit after tax.
- Note: the 2026 stub in DCF does **not** equal full FY2026 projected FCFF.

### Page 3 — DCF and peer valuation

- DCF share estimate card: [DCF per Share (NGN)]. WACC card: [DCF WACC %]. WACC and terminal growth are **analyst assumptions**.
- Peer bar chart: \`FactPeer[Company]\` and \`FactPeer[PE]\`; second visual for \`FactPeer[EVtoEBITDA]\`.
- Sensitivity matrix: \`FactSensitivity[WACC]\` rows, \`FactSensitivity[TerminalGrowth]\` columns, \`[DCF Sensitivity Share (NGN)]\` values. Color scale optional.
- Do not show the model's ₦/share as an actionable price target or conceal date mismatches.

### Page 4 — Research integrity

- Source table showing \`FactPeer[PriceDate]\`, \`FactPeer[BalanceAsOf]\`, \`FactPeer[EBITDABasis]\`.
- Narrative box: "H1 2026 cash/debt bridge; October market price; FY2025 operating results. Mixed dates."
- Open audit items: market beta, ERP, corporate debt coupon/yield, capex commitments, operating working-capital normalization, vendor BUA EBITDA definition.
- Clarify: model shares are **educational valuation outputs**, not investment advice.

## Design system

- Canvas: dark navy \`#0B1424\`, card \`#14243A\`, text \`#F2F5FC\`, subdued text \`#A9B6CB\`.
- Actual = mint \`#53D0B1\`; projected base = sky \`#3D7EFF\`; downside = coral \`#E66B70\`; upside = amber \`#FDAF54\`.
- Top-level cards large with units: **₦ trillion** or **₦ billion** explicitly. Native model stays in ₦ million.
- Footers: "Historical FY2023–25 / projected FY2026–30 | reference market date 7 Oct 2026 | educational research model".

## Open limitations

- The preview is **not** a Power BI report, and does not contain the genuine Power BI filter engine or Desktop visuals. It is a visual companion to the actual CSV+DAX import kit.
- The DCF/WACC model still contains uncalibrated cost-of-capital and reinvestment assumptions.
- BUA's FY2025 EBITDA is a third-party dataset; Lafarge EBITDA is a reconstructed proxy, not harmonized management EBITDA.
- Cash, debt and share price are from different dates; the report calls this out.
- Native PBIR/PBIP project files should be generated and verified in Desktop. Microsoft [PBIR/PBIP guidance](https://learn.microsoft.com/power-bi/developer/projects/projects-report) explains why programmatically generating an untested "ready-to-open" file is risky.

## Suggested next stage

Audit output visuals and assumptions, connect a native PBIX, gather new peer/segment financial evidence, and draft the investment research report. **No merge into main without review.**
