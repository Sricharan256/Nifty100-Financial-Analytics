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

# Sprint 1 – Data Foundation

## Day 1 – Environment Setup ✅

* Created the project directory structure.
* Configured the Python virtual environment.
* Installed required Python libraries.
* Added `.env`, `.gitignore`, `requirements.txt`, and `Makefile`.
* Initialized the Git repository.
* Created the initial project documentation.

---

## Day 2 – Excel Loader & Normaliser ✅

* Developed `loader.py` to load Excel datasets using Pandas.
* Implemented `normalize_year()` to standardize financial year formats.
* Implemented `normalize_ticker()` to standardize stock ticker symbols.
* Successfully loaded sample datasets from the `data/raw` directory.
* Added unit tests for loader and normaliser modules.

---

## Day 3 – Schema Validator & Data Quality Checks ✅

* Developed `validator.py`.
* Implemented Required Columns validation.
* Implemented Missing Values validation.
* Implemented Duplicate Rows validation.
* Implemented Year validation.
* Implemented Ticker validation.
* Generated `validation_report.csv`.
* Successfully passed all ETL unit tests.

### Validation Summary

* ✅ Required Columns – Passed
* ✅ Missing Values – Passed
* ✅ Duplicate Rows – Passed

---

## Day 4 – SQLite Database Schema ✅

* Created `schema.sql`.
* Developed `database.py`.
* Created SQLite database (`nifty100.db`).
* Enabled SQLite Foreign Key support.
* Created database tables.
* Verified database creation.
* Added database unit tests.

---

## Day 5 – ETL Data Loading & Database Integration ✅

* Developed `insert_data.py` to load validated Excel datasets into SQLite.
* Automated loading of all project datasets into database tables.
* Implemented reusable SQLite database connection.
* Generated **Load Audit Report (`load_audit.csv`)**.
* Created `verify_row_counts.py` to verify records loaded into database tables.
* Verified successful data loading into SQLite.
* Added database insertion and verification unit tests.
* Completed end-to-end ETL pipeline from Excel files to SQLite database.

---

# Project Structure

```text
nifty100_financial_analytics/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── supplementary/
│
├── db/
│   ├── schema.sql
│   └── nifty100.db
│
├── docs/
├── notebooks/
│
├── output/
│   ├── validation_report.csv
│   └── load_audit.csv
│
├── src/
│   ├── db/
│   │   ├── database.py
│   │   ├── insert_data.py
│   │   ├── check_database.py
│   │   └── verify_row_counts.py
│   │
│   ├── etl/
│   │   ├── loader.py
│   │   ├── normaliser.py
│   │   └── validator.py
│   │
│   └── utils/
│
├── tests/
│   ├── db/
│   │   ├── test_database.py
│   │   └── test_insert.py
│   │
│   └── etl/
│       ├── test_loader.py
│       ├── test_normaliser.py
│       └── test_validator.py
│
├── README.md
├── requirements.txt
├── Makefile
├── .env
└── .gitignore
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

* Python 3.12
* Pandas
* NumPy
* OpenPyXL
* SQLite
* Pytest
* Git & GitHub
* Power BI

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

# Current Progress

* ✅ Environment Setup Completed
* ✅ Excel Loader Completed
* ✅ Data Normalisation Completed
* ✅ Schema Validator Completed
* ✅ Validation Report Generated
* ✅ SQLite Database Completed
* ✅ ETL Data Loading Completed
* ✅ Load Audit Report Generated
* ✅ Database Verification Completed
* ✅ Unit Tests Passed
* ⏳ Data Quality Review (Day 6)
* ⏳ Sprint Review & Documentation (Day 7)

---

# How to Run

```bash
# Activate Virtual Environment
venv\Scripts\activate

# Install Dependencies
pip install -r requirements.txt

# Run Loader
python src/etl/loader.py

# Run Normaliser
python src/etl/normaliser.py

# Run Validator
python src/etl/validator.py

# Create Database
python src/db/database.py

# Load Data into SQLite
python -m src.db.insert_data

# Verify Database
python src/db/check_database.py

# Verify Row Counts
python src/db/verify_row_counts.py

# Run All Unit Tests
python -m pytest
```

---

# Deliverables Completed

* Project Structure
* Excel Loader
* Data Normaliser
* Schema Validator
* Validation Report
* SQLite Database
* Database Schema
* ETL Data Loading
* Load Audit Report
* Database Verification
* Row Count Verification
* Unit Tests
* Project Documentation

---

# Author

**Sricharan Medaboina**

**Nifty 100 Financial Analytics Platform**

**Sprint 1 – Data Foundation**
