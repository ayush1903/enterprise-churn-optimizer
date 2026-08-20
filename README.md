# enterprise-churn-optimizer
# 📊 Enterprise AI-Driven Customer Retention & Churn Optimization Engine

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive_BI-3F4F75.svg?logo=plotly&logoColor=white)](https://plotly.com)
[![Pandas](https://img.shields.io/badge/Pandas-Data_Engineering-150458.svg?logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Agile](https://img.shields.io/badge/Methodology-Agile_Scrum-0052CC.svg?logo=jira&logoColor=white)](https://atlassian.com/jira)

> An end-to-end enterprise solution bridging **Business Analysis**, **Predictive Risk Analytics**, **Low-Code Interactive BI**, and **Agile Project Governance** to proactively detect and mitigate customer churn before revenue leakage occurs.

---

## 🎯 Executive Summary & Problem Statement

Customer churn represents one of the largest revenue vulnerabilities for subscription and recurring revenue business models. Relying purely on **reactive** cancellation handling results in delayed intervention, low customer save rates, and lost Monthly Recurring Revenue (MRR).

This project designs and deploys an automated, full-cycle retention intelligence pipeline:
* **Identifies at-risk cohorts 30 days prior** to cancellation.
* **Quantifies monthly revenue exposure** ($139k+ at immediate risk).
* **Automates tailored retention playbooks** for Customer Success teams to protect customer lifetime value (CLV).

---

## 💼 Core Deliverables by Track
enterprise-churn-optimizer/
├── 01_Business_Analysis/
│   ├── BRD_Customer_Retention.md       # Full Business Requirements Document (FR1-FR5, KPIs)
│   └── AsIs_ToBe_Process_Flows.png     # As-Is (Reactive) vs To-Be (Automated AI) Workflows
├── 02_Data_Analytics/
│   ├── WA_Fn-UseC_-Telco-Customer-Churn.csv  # 7,043 Raw Customer Records
│   ├── eda_and_cleaning.py             # Automated ETL & Heuristic Risk Scoring Engine
│   ├── cleaned_churn_data.csv          # Segmented Customer Data with Risk Tiers
│   ├── churn_queries.sql               # Analytical SQL Suite (Cohorts, Revenue at Risk)
│   └── app.py                          # Streamlit Low-Code BI Dashboard
├── 03_Project_Management/
│   ├── Jira_Backlog_Export.csv         # 4-Sprint Agile Backlog (12 User Stories in Gherkin)
│   ├── Risk_Register_and_Mitigation.csv# 5x5 Likelihood/Impact Risk Governance Matrix
│   └── Project_Charter_RACI.md         # Milestone Roadmap & RACI Stakeholder Matrix
├── 04_GenAI_Workflows/
│   └── prompt_library_used.md          # Full Prompt Catalog & 81% Time-Savings Audit
└── README.md                           # Executive Project Portfolio Overview


---

## 📈 Key Metrics & Analytical Findings

From analyzing **7,043 customer accounts** representing **$456,116.60 in Total MRR**:

| Metric Indicator | Dataset Finding | Strategic Takeaway |
| :--- | :---: | :--- |
| **Gross Churn Rate** | **26.5%** | Baseline benchmark for retention intervention workflows. |
| **Monthly Revenue at Risk** | **$139,130.85** | High-priority revenue exposed to immediate cancellation. |
| **Highest Risk Contract Type** | **Month-to-Month (42.7%)** | Primary driver; target with 1-year conversion incentives. |
| **Highest Risk Payment Method** | **Electronic Check (45.3%)** | Target with autopay / credit card migration promos. |
| **Tenure Cliff** | **Months 1–12** | Highest churn concentration; requires automated onboarding check-ins. |

---

## 🖥️ Low-Code Interactive BI Dashboard

The interactive Streamlit dashboard (`02_Data_Analytics/app.py`) provides Customer Success and Operations leaders with real-time risk visibility:
* **Dynamic KPI Callouts:** Total Customers, Churn Rate %, Total MRR, and Monthly Revenue at Risk.
* **Interactive Slicers:** Filter instantly by Contract Type and Internet Service tier.
* **Risk Distribution Charts:** Plotly visualizers for Tenure vs. Churn, Payment Methods, and Contract categories.
* **Customer Drill-Down Drawer:** Filterable raw data inspection table for immediate CRM actions.

---

## 🚀 How to Run the Project Locally

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/enterprise-churn-optimizer.git](https://github.com/your-username/enterprise-churn-optimizer.git)
cd enterprise-churn-optimizer

2. Install Required Dependencies
Bash
pip install streamlit plotly pandas numpy
3. Run the Data Pipeline & Risk Scoring
Bash
python 02_Data_Analytics/eda_and_cleaning.py
4. Launch the Streamlit Dashboard
Bash
streamlit run 02_Data_Analytics/app.py
Access the local web dashboard at http://localhost:8501.

🤖 GenAI Productivity Audit
By leveraging structured, role-based Generative AI prompt engineering alongside rigorous Human-in-the-Loop (HITL) quality validation, total project turnaround was accelerated significantly:

Traditional Baseline Effort: ~45.0 Hours

GenAI-Augmented Delivery: 8.5 Hours

Net Productivity Gain: ~81% Time Saved (Scaffolding, boilerplate syntax, and structural formatting automated).

See 04_GenAI_Workflows/prompt_library_used.md for full prompt documentation and audit breakdown.


---

# 🌐 Universal Multi-Domain Analytics & Intelligence Platform

An enterprise-grade, domain-agnostic data analytics and visualization suite built with **Streamlit**, **Pandas**, and **Plotly**. Designed to ingest, cleanse, profile, and visualize datasets across multiple industries—from customer churn and risk monitoring to operational KPIs and telemetry data—with zero runtime crashes.

---

## 🚀 Key Features

* **Universal CSV Ingestion & Fallback Guarantee:** Ingest any standard CSV dataset or fall back safely to benchmark data without cold-start errors.
* **Automated Health Audit & Quality Gate:** Instantly detects missing/null entries, blank whitespace, duplicate records, and disguised numerical fields, providing interactive 1-click automated remediation.
* **Smart Data Profiler:** Automatically classifies dataframe columns into discrete categorical groups ($\le 10$ unique values) and continuous metrics ($> 10$ unique values).
* **Adaptive Intelligence Modes:**
  * **🚨 Event & Binary Risk Analysis:** Quantifies occurrence rates, financial exposure, and category breakdowns (e.g., Churn, Fraud, Safety Incidents).
  * **📈 Continuous Metrics & Trends:** Evaluates distribution histograms, multi-metric scatter trendlines, five-number summary box plots, and 2D density heatmaps (e.g., Airbnb operations, sensor telemetry).
  * **🔗 Correlation & Driver Explorer:** Generates interactive multi-variable correlation heatmaps with matrix dimension and peak correlation metrics.
* **Cardinality Safeguards:** Automatically switches high-cardinality dimensions into continuous binned distributions to prevent cluttered, unreadable charts.
* **Export Facility:** Integrated 1-click export to download cleansed and filtered datasets directly as CSV.

---

## 🛠️ Tech Stack

* **Frontend & Engine:** Python 3.12, Streamlit
* **Data Processing & Auditing:** Pandas, NumPy
* **Interactive Visualizations:** Plotly Express, Statsmodels (OLS Regression)

---

## 💻 Quick Start

### 1. Clone Repository & Install Dependencies
```bash
git clone <your-repository-url>
cd enterprise-churn-optimizer
pip install -r requirements.txt
2. Launch Dashboard
Bash
streamlit run 02_Data_Analytics/app.py

---

cat << 'EOF' >> README.md

## 🚀 Supported Ingestion Formats & Features
| Ingestion Format | Supported Engine | Automated Cleaning | HTML Briefing Export |
| :--- | :--- | :---: | :---: |
| **CSV (`.csv`)** | Native Pandas Delimited | ✅ | ✅ |
| **Excel (`.xlsx`, `.xls`)** | OpenPyXL Engine | ✅ | ✅ |
| **Apache Parquet (`.parquet`)** | PyArrow Columnar | ✅ | ✅ |
| **JSON (`.json`)** | Pandas Structured Parser | ✅ | ✅ |
EOF




