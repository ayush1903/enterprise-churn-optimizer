# GenAI Prompt Engineering Library & Productivity Audit

**Project:** Enterprise AI-Driven Customer Retention & Churn Reduction System  
**Objective:** Document exact prompt engineering methodologies, structured role-based prompts, and measurable productivity gains across Business Analysis, Data Analytics, and Project Management tracks.

---

## 1. GenAI Productivity Audit & Time-Savings Summary

| Project Milestone / Task | Traditional Baseline Effort | GenAI-Augmented Effort | Time Saved (%) | Primary AI Acceleration Value |
| :--- | :---: | :---: | :---: | :--- |
| **BRD & Requirements Framing** | 8.0 Hours | 1.5 Hours | **81%** | Standardized structure, auto-formulated KPIs, and Gherkin criteria. |
| **Process Flow Mapping (Mermaid.js)** | 4.0 Hours | 0.5 Hours | **88%** | Instant generation of As-Is / To-Be declarative diagram syntax. |
| **Data Cleaning & Risk Scoring Script** | 10.0 Hours | 2.0 Hours | **80%** | Auto-generation of type coercion, null handlers, and scoring functions. |
| **SQL Queries & Cohort Analysis** | 5.0 Hours | 1.0 Hours | **80%** | Rapid aggregation and cohort-level metric formulation. |
| **Interactive Streamlit Dashboard** | 12.0 Hours | 2.5 Hours | **79%** | Instant Plotly UI composition and layout structuring. |
| **Agile Backlog & Risk Register** | 6.0 Hours | 1.0 Hours | **83%** | Rapid breakdown into epics, user stories, and severity scoring. |
| **Total Project Delivery Time** | **45.0 Hours** | **8.5 Hours** | **~81% Saved** | **Focus shifted from syntax/boilerplate to strategic decision-making.** |

---

## 2. Complete Prompt Library Catalog

### Prompt 1: Business Requirements Document (BRD) Generation
* **Role / Context:** Senior Business Analyst in SaaS Operations
* **Target Deliverable:** `01_Business_Analysis/BRD_Customer_Retention.md`
* **Prompt Used:**
> *"Act as a Senior Business Analyst in SaaS Ops. Write a professional Business Requirements Document (BRD) for an 'AI-Driven Churn Reduction & Retention System'. Include: Executive Summary, Business Drivers, In-Scope/Out-of-Scope items, Functional Requirements (FR1 to FR5), Non-Functional Requirements, and Key Performance Indicators (KPIs)."*

---

### Prompt 2: As-Is vs. To-Be Process Flow Modeling
* **Role / Context:** Lead Business Process Engineer
* **Target Deliverable:** `01_Business_Analysis/AsIs_ToBe_Process_Flows.png`
* **Prompt Used:**
> *"Generate Mermaid.js syntax for two flowcharts: 1) As-Is Process: Manual and reactive churn handling when a customer cancels. 2) To-Be Process: Automated GenAI-driven risk scoring, instant retention offers, and automated ticket escalation."*

---

### Prompt 3: Data Cleaning, Risk Scoring & SQL Query Suite
* **Role / Context:** Senior Data Analyst & Analytics Engineer
* **Target Deliverable:** `02_Data_Analytics/churn_queries.sql` & `eda_and_cleaning.py`
* **Prompt Used:**
> *"I have a Telco Churn CSV with columns: customerID, tenure, Contract, PaymentMethod, MonthlyCharges, TotalCharges, Churn. Write 5 analytical SQL queries to find: 1) Churn rate by contract type, 2) Monthly revenue lost to churn, 3) Top payment methods with high churn. Also, write a Python Pandas script to clean missing values in TotalCharges and create risk categories."*

---

### Prompt 4: Interactive Low-Code Dashboard Architecture
* **Role / Context:** Data Visualization Engineer / BI Developer
* **Target Deliverable:** `02_Data_Analytics/app.py`
* **Prompt Used:**
> *"Write a complete Python Streamlit app using Plotly to analyze 'WA_Fn-UseC_-Telco-Customer-Churn.csv'. Add key metric callouts for Total Customers, Churn Rate %, Total MRR, and interactive charts filtering by Contract type and Internet Service."*

---

### Prompt 5: Agile Backlog & Gherkin User Story Formulation
* **Role / Context:** Technical Project Manager / Scrum Master
* **Target Deliverable:** `03_Project_Management/Jira_Backlog_Export.csv`
* **Prompt Used:**
> *"Create an Agile Backlog in CSV format with columns: Issue Type, Summary, Description, Story Points, Sprint (Sprint 1 to 4). Include 12 user stories written in Gherkin format (Given-When-Then) covering Data Ingestion, Risk Modeling, Dashboard UI, and Retention Workflows."*

---

### Prompt 6: Risk Governance Matrix & Project RACI Matrix
* **Role / Context:** Enterprise Project Governance Lead
* **Target Deliverable:** `03_Project_Management/Risk_Register_and_Mitigation.csv` & `Project_Charter_RACI.md`
* **Prompt Used:**
> *"Generate a comprehensive Project Charter, a RACI Matrix, and a Risk Register with columns: Risk ID, Category, Description, Likelihood (1-5), Impact (1-5), Severity Score, Risk Owner, and Mitigation Strategies for an enterprise analytics deployment."*

---

## 3. Human-in-the-Loop (HITL) Validation Insights
While GenAI accelerated boilerplate scaffolding, critical human validation was required to maintain production quality:
1. **Plotly Syntax Correction:** Caught and resolved runtime enum incompatibilities (`barnorm="percent"` vs `barmode`) that standard LLM generation overlooked.
2. **Data Boundary Enforcement:** Verified numeric conversions on `TotalCharges` to ensure zero-tenure records did not drop from aggregation calculations.
3. **Strategic Metric Alignment:** Refined churn risk thresholds to ensure high-value accounts received priority intervention SLAs.
