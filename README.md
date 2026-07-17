# Nifty 100 Financial Analytics Platform

## Project Overview

The **Nifty 100 Financial Analytics Platform** is an end-to-end data engineering project that processes financial data of Nifty 100 companies. The project builds a robust ETL pipeline to extract, transform, validate, and load financial datasets into a SQLite database. The validated data serves as the foundation for financial analytics, reporting, and Power BI dashboards.

---

# Project Objectives

* Build a scalable ETL pipeline for financial datasets.
* Standardize financial year and stock ticker formats.
* Validate data using Data Quality (DQ) rules.
* Store validated data in a SQLite database.
* Prepare data for financial analytics and dashboard development.
* Generate validation and load audit reports.

---
# Sprint Progress

| Sprint | Status |
|---------|--------|
| Sprint 1 – Data Foundation | Completed |
| Sprint 2 – Financial Ratio Engine | Completed |
| Sprint 3 – Screener & Peer Comparison | Completed|
| Sprint 4 – DASHBOARD & VALUATION MODULE | Completed |
| Sprint 5 – QA, Documentation & Deployment | In Progress |

---
# Sprint 1 – Data Foundation

## Day 1 – Environment Setup 

* Created the project directory structure.
* Configured the Python virtual environment.
* Installed required Python libraries.
* Added `.env`, `.gitignore`, `requirements.txt`, and `Makefile`.
* Initialized the Git repository.
* Created the initial project documentation.

---

## Day 2 – Excel Loader & Normaliser 

* Developed `loader.py` to load Excel datasets using Pandas.
* Implemented `normalize_year()` to standardize financial year formats.
* Implemented `normalize_ticker()` to standardize stock ticker symbols.
* Successfully loaded sample datasets from the `data/raw` directory.
* Added unit tests for loader and normaliser modules.

---

## Day 3 – Schema Validator & Data Quality Checks 

* Developed `validator.py`.
* Implemented Required Columns validation.
* Implemented Missing Values validation.
* Implemented Duplicate Rows validation.
* Implemented Year validation.
* Implemented Ticker validation.
* Generated `validation_report.csv`.
* Successfully passed all ETL unit tests.

### Validation Summary

* Required Columns – Passed
* Missing Values – Passed
* Duplicate Rows – Passed

---

## Day 4 – SQLite Database Schema 

* Created `schema.sql`.
* Developed `database.py`.
* Created SQLite database (`nifty100.db`).
* Enabled SQLite Foreign Key support.
* Created database tables.
* Verified database creation.
* Added database unit tests.

---

## Day 5 – ETL Data Loading & Database Integration 

* Developed `insert_data.py` to load validated Excel datasets into SQLite.
* Automated loading of all project datasets into database tables.
* Implemented reusable SQLite database connection.
* Generated **Load Audit Report (`load_audit.csv`)**.
* Created `verify_row_counts.py` to verify records loaded into database tables.
* Verified successful data loading into SQLite.
* Added database insertion and verification unit tests.
* Completed end-to-end ETL pipeline from Excel files to SQLite database.

---
## Day 6 Data Quality Manual Review 

- Verified all SQLite database tables.
- Confirmed row counts for all datasets.
- Performed manual review of five companies.
- Verified year coverage across financial datasets.
- Identified JIOFIN as the only company with less than five years of financial data.
- Checked for missing values and duplicate records.
- Verified foreign key integrity.
- Generated a Data Quality Review report.
- Successfully completed all unit tests.

----
## Day 7 – Sprint Wrap-Up & Review 

- Created exploratory SQL queries for data analysis.
- Verified all SQLite database tables.
- Confirmed row counts for all datasets.
- Executed data quality verification scripts.
- Ran all unit tests successfully.
- Reviewed Sprint 1 deliverables.
- Updated project documentation.
- Successfully completed Sprint 1 – Data Foundation.
---------
## SPRINT 2 — Financial Ratio Engine
## Day 8 – Profitability Ratio Engine 

- Created the `analytics` module.
- Loaded Profit & Loss and Balance Sheet data from SQLite.
- Merged financial datasets using company ID and year.
- Calculated Net Profit Margin (NPM).
- Calculated Operating Profit Margin (OPM).
- Calculated Return on Equity (ROE).
- Calculated Return on Capital Employed (ROCE).
- Generated `profitability_validation.csv`.
- Added unit tests for all profitability ratios.
-----
## Day 9 – Leverage & Efficiency Ratio Engine 

- Implemented Debt-to-Equity (D/E) Ratio.
- Implemented Interest Coverage Ratio (ICR).
- Implemented Asset Turnover Ratio.
- Handled division-by-zero and missing-value edge cases.
- Added unit tests for leverage and efficiency ratios.
- Validated calculated ratios against financial statements.
---
## Day 10 – CAGR Engine 

- Implemented Revenue CAGR.
- Implemented PAT CAGR.
- Implemented EPS CAGR.
- Added reusable CAGR calculation function.
- Added edge case handling.
- Added unit tests.
- Generated cagr_validation.csv.

---
## Day 11 – Cash Flow KPIs & Capital Allocation 

- Implemented Free Cash Flow.
- Implemented CFO Quality Score.
- Implemented CapEx Intensity.
- Implemented FCF Conversion.
- Implemented Capital Allocation Pattern Classifier.
- Generated capital_allocation.csv.
- Added unit tests.
---
## Day 12 – Financial Ratios Population 

- Merged Profit & Loss, Balance Sheet, and Cash Flow tables.
- Calculated 19 financial KPI columns.
- Populated the financial_ratios table in SQLite.
- Generated financial_ratios_validation.csv.
- Verified row count (1184 rows).

---
## Day 13 – Ratio Validation & Edge Case Analysis 

- Validated computed ROE against source data.
- Compared calculated ROE values with source ROE values.
- Generated `ratio_edge_cases.log`.
- Documented formula differences for further review.
- Verified the `financial_ratios` table contains all calculated KPI records.
---
## Day 14 – Tests & Sprint Review 

- Executed all KPI unit tests.      
- Reviewed ratio_edge_cases.log.
- Verified financial_ratios table.
- Ran screener preview.
- Completed Sprint 2 retrospective.
- Demonstrated financial_ratios table.
---
## SPRINT 3 — Screener & Peer Comparison Engine
## Day 15 – Financial Screener Filter Engine

- Created the Financial Screener Filter Engine.
- Loaded financial ratios from the SQLite database.
- Implemented configurable screening thresholds using a YAML configuration file.
- Applied filters based on Return on Equity (ROE), Debt-to-Equity (D/E), and Free Cash Flow (FCF).
- Retrieved the latest financial record for each company before screening.
- Sorted filtered companies using the Composite Quality Score.
- Generated the `day15_filter_results.csv` report for screened companies.
---
## Day 16 – Preset Screeners

- Implemented six predefined financial screener presets.
- Applied preset-specific filtering rules using financial ratios.
- Screened the latest financial data for all companies.
- Ranked companies using the Composite Quality Score.
- Exported screening results to `output/screener_output.xlsx`.
- Validated preset outputs and reviewed the shortlisted companies.
---
## Day 17 – Composite Score & Screener Export

- Implemented Composite Quality Score calculation.
- Applied P10/P90 winsorization for metric normalization.
- Computed sector-relative performance scores.
- Generated multi-sheet `screener_output.xlsx`.
- Added conditional formatting for financial thresholds.
- Ranked companies using Composite Quality Score.
- Validated generated screener reports.
---
## Day 18 – Peer Percentile Rankings

- Developed Peer Percentile Ranking Engine.
- Computed percentile rankings for financial metrics.
- Inverted Debt-to-Equity ranking (lower is better).
- Created `peer_percentiles` table in SQLite.
- Generated `peer_comparison.xlsx` with peer-wise sheets.
- Applied conditional formatting and benchmark highlighting.
---
## Day 19 – Radar Chart Generation

- Developed a radar chart engine for visualizing company financial performance.
- Compared each company against its peer group average across eight financial metrics.
- Generated radar charts using Matplotlib polar plots.
- Created standalone radar charts for companies without peer groups using the Nifty 100 average.
- Exported all radar charts as PNG files to `reports/radar_charts/`.
- Automated chart generation for all companies in the dataset.
---
## Day 20 – Peer Comparison Excel Report

- Generated peer_comparison.xlsx with one worksheet for each peer group.
- Added company financial KPIs and percentile rankings.
- Applied conditional formatting to percentile values.
- Highlighted benchmark companies using gold formatting.
- Added peer-group median summary rows.
- Automated Excel report generation using OpenPyXL.
---
## Day 21 – Sprint 3 Review & Testing

- Executed Data Quality unit tests.
- Verified Quality Compounder screener output.
- Validated peer percentile rankings.
- Reviewed generated Excel reports.
- Verified radar chart generation.
- Completed Sprint 3 retrospective and project demonstration.
---
## Sprint 4 – Day 22: Streamlit Dashboard Scaffold

### Day 22 – Streamlit Dashboard Scaffold

- Developed the initial Streamlit dashboard framework with multi-page navigation and a responsive wide-layout interface.
- Implemented a reusable SQLite database utility module with cached data loading for efficient access to company and financial data.
- Created the dashboard structure with eight placeholder screens covering Home, Company Profile, Screener, Peer Comparison, Trends, Sectors, Capital Allocation, and Reports.
- Verified successful application startup, sidebar navigation, and database connectivity to support upcoming dashboard features.

## Day 23-Home Screen & Company Profile Screen

- Developed the Home Dashboard with KPI cards, sector-wise donut chart, and Top-5 companies table.
- Implemented the Company Profile page with company search, financial KPI cards, charts, and Pros & Cons section.
- Integrated the dashboard with the SQLite database and added handling for missing data.

## Day 24-Screener Screen & Peer Comparison Screen

- Developed the Stock Screener with financial metric filters, preset screening options, and CSV export.
- Implemented the Peer Comparison page with radar chart and KPI comparison table.
- Integrated dynamic filtering and peer analysis using SQLite database data.

## Day 25-Remaining 4 Screens

- Implemented Trend Analysis with multi-metric comparison and 10-year financial trends.
- Developed Sector Analysis with bubble chart and sector median KPI visualization.
- Built Capital Allocation Map using Plotly treemap and company pattern classification.
- Added Annual Reports page with searchable company reports and downloadable PDF links.

# Day 26-Valuation Analytics Module

- Integrated company, financial ratio, market capitalization, and sector data for valuation analysis.
- Calculated FCF Yield, Sector Median P/E, and P/E vs Sector Median percentage for all companies.
- Classified companies as **Caution**, **Discount**, or **Fair** based on valuation rules.
- Generated `valuation_summary.xlsx` and `valuation_flags.csv` reports for further analysis.

# Day 27-Integration QA & Bug Fixes

- Tested the Streamlit dashboard using multiple companies across different sectors and validated handling of partial data.
- Performed QA checks for missing values, generated QA reports, and verified application stability under different scenarios.
- Created QA artifacts including sample companies, missing data summary, QA checklist, and QA summary report.
- Improved application reliability by validating edge cases and preparing the project for final integration testing.
---
# Project Structure

```text
nifty100_financial_analytics/
│
├── config/
│   └── screener_config.yaml
│
├── data/
│   ├── raw/
│   │   ├── analysis.xlsx
│   │   ├── balancesheet.xlsx
│   │   ├── cashflow.xlsx
│   │   ├── companies.xlsx
│   │   ├── documents.xlsx
│   │   ├── financial_ratios.xlsx
│   │   ├── market_cap.xlsx
│   │   ├── peer_groups.xlsx
│   │   ├── profitandloss.xlsx
│   │   ├── prosandcons.xlsx
│   │   ├── sectors.xlsx
│   │   └── stock_prices.xlsx
│   │
│   └── processed/
│
├── db/
│   ├── nifty100.db
│   ├── check_schema.py
│   └── check_excel_headers.py
│
├── output/
│   ├── screener_output.xlsx
│   ├── peer_comparison.xlsx
│   └── valuation_summary.xlsx        (Day 26)
│
├── reports/
│   └── radar_charts/
│       ├── ABB_radar.png
│       ├── TCS_radar.png
│       ├── LT_radar.png
│       └── ...
│
├── src/
│   │
│   ├── analytics/
│   │   ├── __init__.py
│   │   ├── composite_score.py
│   │   ├── peer.py
│   │   ├── radar_chart.py
│   │   ├── peer_comparison_report.py
│   │   └── valuation.py              (Day 26)
│   │
│   ├── dashboard/
│   │   ├── __init__.py
│   │   ├── app.py
│   │   │
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   └── db.py
│   │   │
│   │   ├── pages/
│   │   │   ├── __init__.py
│   │   │   ├── 01_home.py
│   │   │   ├── 02_profile.py
│   │   │   ├── 03_screener.py
│   │   │   ├── 04_peers.py
│   │   │   ├── 05_trends.py
│   │   │   ├── 06_sectors.py
│   │   │   ├── 07_capital.py
│   │   │   └── 08_reports.py
│   │   │
│   │   └── test_db.py
│   │
│   ├── db/
│   │   ├── check_schema.py
│   │   ├── check_excel_headers.py
│   │   └── verify_sqlite.py
│   │
│   └── screener/
│       ├── __init__.py
│       ├── engine.py
│       ├── presets.py
│       ├── export_presets.py
│       └── composite_score.py
│
├── tests/
│   ├── test_dq_rules.py
│   └── day21_verification.py
│
├── venv/
│
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE
```

---

# ETL Workflow

```text
Excel Files
      │
      ▼
Loader Module
      │
      ▼
Data Normalisation
      │
      ▼
Schema Validation
      │
      ▼
SQLite Database
      │
      ▼
ETL Data Loading
      │
      ▼
Load Audit Report
      │
      ▼
Financial Analytics
      │
      ▼
Power BI Dashboard
```

---

# Technologies Used

- Python 3.12
- Pandas
- NumPy
- SQLite
- PyYAML
- OpenPyXL
- Pytest
- Git & GitHub
- VS Code
- Power BI

---

# Modules

## Loader Module (`loader.py`)

* Reads Excel datasets.
* Loads Excel files into Pandas DataFrames.
* Handles loading errors.
* Displays dataset statistics.

---

## Normaliser Module (`normaliser.py`)

* Standardizes financial year values.
* Standardizes stock ticker symbols.
* Removes extra whitespace.
* Converts ticker values to uppercase.

---

## Validator Module (`validator.py`)

Implements Data Quality (DQ) validation before loading data into SQLite.

### Validation Rules

* Required Columns Validation
* Missing Values Validation
* Duplicate Rows Validation
* Year Validation
* Ticker Validation

### Validation Output

* `output/validation_report.csv`

---

## Database Module (`database.py`)

Responsible for:

* Creating SQLite database
* Executing `schema.sql`
* Creating database tables
* Enabling foreign keys

---

## ETL Loader Module (`insert_data.py`)

Responsible for:

* Loading validated Excel datasets into SQLite
* Managing database connections
* Inserting records into database tables
* Generating load audit reports

### Output

* `output/load_audit.csv`

---

## Database Verification (`verify_row_counts.py`)

Responsible for:

* Verifying row counts for all database tables
* Confirming successful ETL execution

---
# Dashboard Screens

## 1. Home Dashboard

![Home Dashboard](screenshots/home.png)

Displays the overall dashboard with KPI cards, sector distribution, and top-performing companies.

---

## 2. Company Profile

### Company Overview

![Company Profile](screenshots/profile2.png)

### Financial Details

![Company Profile Continued](screenshots/profile3.png)

Displays company information, financial KPIs, charts, and annual reports.

---

## 3. Stock Screener

### Screener Filters

![Stock Screener](screenshots/screener.png)

### Screener Results

![Stock Screener Results](screenshots/screener2.png)

Filters companies based on financial metrics and preset screeners.

---

## 4. Peer Comparison

![Peer Comparison](screenshots/peer.png)

Compares companies using radar charts and KPI tables.

---

## 5. Trend Analysis

### Trend Charts

![Trend Analysis](screenshots/trends.png)

### Additional Trends

![Trend Analysis Continued](screenshots/trends2.png)

Displays multi-year financial performance.

---

## 6. Sector Analysis

![Sector Analysis](screenshots/sector.png)

Shows sector-wise comparisons and median metrics.

---

## 7. Capital Allocation

![Capital Allocation](screenshots/Capital.png)

Visualizes capital allocation patterns using a treemap.

---

## 8. Annual Reports

![Annual Reports](screenshots/report.png)

Provides searchable annual report links for companies.
---

# Current Progress

## Sprint 1 – Data Foundation

- Environment Setup
- ETL Pipeline
- Data Validation
- SQLite Database
- ETL Data Loading
- Database Verification
- Sprint Review

## Sprint 2 – Financial Ratio Engine

- Profitability Ratio Engine
- Leverage Ratio Engine
- Efficiency Ratio Engine
- CAGR Engine
- Cash Flow KPI Engine
- Capital Allocation
- Financial Ratios Population
- Ratio Validation
- KPI Unit Tests

## Sprint 3 – Screener & Peer Comparison

- Day 15 – Financial Screener Filter Engine
- Day 16 – Preset Screeners
- Composite Quality Score
- Peer Comparison Engine
- Radar Charts
- Excel Reports

---

# How to Run

```bash
# Activate Virtual Environment
venv\Scripts\activate

# Install Dependencies
pip install -r requirements.txt

# Run ETL Pipeline
python src/etl/loader.py
python src/etl/normaliser.py
python src/etl/validator.py

# Create Database
python src/db/database.py

# Load Data into SQLite
python -m src.db.insert_data

# Verify Database
python src/db/check_database.py
python src/db/verify_row_counts.py

# Populate Financial Ratios
python -m src.analytics.populate_financial_ratios

# Validate Financial Ratios
python -m src.analytics.ratio_validation

# Run Financial Screener Engine
python -m src.screener.engine

# Run Preset Screeners
python -m src.screener.presets

# Execute All Unit Tests
python -m pytest
## Run the Streamlit Dashboard

Activate the virtual environment:

```bash
venv\Scripts\activate
```

Launch the dashboard:

```bash
streamlit run src/dashboard/app.py
```

The dashboard will open in your default web browser.
---

# Deliverables

## Database

- SQLite Database (`nifty100.db`)
- Financial Ratios Table

## Reports

- validation_report.csv
- load_audit.csv
- profitability_validation.csv
- cagr_validation.csv
- capital_allocation.csv
- financial_ratios_validation.csv
- ratio_edge_cases.log
- day15_filter_results.csv

## Analytics Modules

- Profitability Engine
- Leverage Engine
- Efficiency Engine
- CAGR Engine
- Cash Flow KPI Engine
- Financial Screener Engine

## Testing

- ETL Unit Tests
- KPI Unit Tests

## Documentation

- README
- Sprint Documentation

---

# Author

**Sricharan Medaboina**

**Nifty 100 Financial Analytics Platform**

**Sprint 1 – Data Foundation**
**Sprint 2 - Financial Ratio Engine**
**Sprint 3 – Screener & Peer Comparison**
**Sprint 4 – DASHBOARD & VALUATION MODULE**