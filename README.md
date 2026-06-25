# Mutual Fund Analytics Capstone Project

## Overview

The **Mutual Fund Analytics Capstone Project** is an end-to-end data analytics solution developed to analyze mutual fund performance, investor behavior, and financial risk. The project demonstrates the complete analytics lifecycle, including data ingestion, data cleaning, exploratory data analysis (EDA), performance analytics, Power BI dashboard development, and advanced risk analytics.

---

# Objectives

* Build an automated ETL pipeline.
* Clean and validate mutual fund datasets.
* Store structured data using SQLite.
* Perform exploratory data analysis.
* Calculate financial performance metrics.
* Develop an interactive Power BI dashboard.
* Perform advanced analytics such as VaR, CVaR, and Rolling Sharpe Ratio.
* Recommend suitable mutual funds based on investor risk profile.

---

# Project Features

* Automated Data Ingestion
* Data Cleaning & Validation
* Exploratory Data Analysis (EDA)
* Performance Analytics
* Interactive Power BI Dashboard
* Historical VaR & CVaR Analysis
* Rolling Sharpe Ratio
* Investor Cohort Analysis
* SIP Continuity Analysis
* Fund Recommendation Engine

---

# Technologies Used

### Programming Language

* Python 3.x

### Python Libraries

* Pandas
* NumPy
* Matplotlib
* Requests

### Database

* SQLite

### Data Visualization

* Power BI Desktop

### Version Control

* Git
* GitHub

---

# Project Structure

```text
mutual_fund_analytics/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── db/
│
├── notebooks/
│   ├── 01_data_ingestion.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda_analysis.ipynb
│   ├── 04_performance_analytics.ipynb
│   └── 05_advanced_analytics.ipynb
│
├── scripts/
│   ├── etl_pipeline.py
│   ├── data_ingestion.py
│   ├── live_nav_fetch.py
│   ├── clean_data.py
│   ├── compute_metrics.py
│   ├── Advanced_Analytics.py
│   └── recommender.py
│
├── sql/
│   ├── schema.sql
│   └── queries.sql
│
├── dashboard/
│   └── bluestock_mf_dashboard.pbix
│
├── reports/
│   ├── Final_Report.pdf
│   ├── Presentation.pptx
│   ├── data_dictionary.md
│   ├── fund_scorecard.csv
│   ├── var_cvar_report.csv
│   └── rolling_sharpe_chart.png
│
├── README.md
└── requirements.txt
```

---

# Datasets Used

The project uses four datasets.

| Dataset                   | Purpose                      |
| ------------------------- | ---------------------------- |
| fund_master.csv           | Mutual Fund Master Data      |
| nav_history.csv           | Historical NAV Data          |
| scheme_performance.csv    | Fund Performance Metrics     |
| investor_transactions.csv | Investor Transaction Records |

---

# Installation

Clone the repository:

```bash
git clone https://github.com/YashPise07/mutual-fund-analytics.git
```

Move into the project folder:

```bash
cd mutual-fund-analytics
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Running the Project

### Run ETL Pipeline

```bash
python scripts/etl_pipeline.py
```

### Run Data Cleaning

```bash
python scripts/clean_data.py
```

### Compute Performance Metrics

```bash
python scripts/compute_metrics.py
```

### Run Advanced Analytics

```bash
python scripts/Advanced_Analytics.py
```

### Run Fund Recommendation System

```bash
python scripts/recommender.py
```

---

# Power BI Dashboard

The dashboard consists of four interactive pages:

1. Industry Overview
2. Fund Performance
3. Investor Analytics
4. SIP & Market Trends

Features include:

* KPI Cards
* Interactive Filters
* Dynamic Charts
* Risk vs Return Analysis
* Investment Trend Analysis

---

# Advanced Analytics

The project includes:

* Historical Value at Risk (VaR)
* Conditional Value at Risk (CVaR)
* Rolling Sharpe Ratio
* Investor Cohort Analysis
* SIP Continuity Analysis
* Fund Recommendation Engine

Generated outputs:

* fund_scorecard.csv
* var_cvar_report.csv
* rolling_sharpe_chart.png

---

# Results

* Successfully processed and cleaned mutual fund datasets.
* Developed a complete ETL pipeline.
* Built an interactive Power BI dashboard.
* Calculated key financial performance metrics.
* Implemented advanced risk analytics.
* Generated investment insights using historical data.

---

# Future Enhancements

* Live AMFI API Integration
* Streamlit Web Application
* Machine Learning Recommendation System
* Portfolio Optimization
* Automated Email Reports

---

# Author

**Shreyash Pise**

GitHub:
https://github.com/YashPise07

LinkedIn:
https://www.linkedin.com/in/shreyash-pise-342805318

---

# License

This project was developed as part of the **Bluestock Mutual Fund Analytics Capstone Project** for educational purposes.
