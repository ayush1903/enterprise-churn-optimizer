-- ==========================================================
-- Enterprise Churn Analysis Queries
-- Dataset: Telco Customer Churn
-- ==========================================================

-- Query 1: Overall Churn Rate & Customer Volume
SELECT 
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS overall_churn_rate_pct
FROM telco_churn;

-- Query 2: Churn Rate and Revenue by Contract Type
SELECT 
    Contract,
    COUNT(*) AS total_accounts,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_accounts,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct,
    ROUND(SUM(MonthlyCharges), 2) AS total_monthly_revenue,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END), 2) AS lost_monthly_revenue
FROM telco_churn
GROUP BY Contract
ORDER BY churn_rate_pct DESC;

-- Query 3: Churn Risk by Payment Method
SELECT 
    PaymentMethod,
    COUNT(*) AS customer_count,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_count,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM telco_churn
GROUP BY PaymentMethod
ORDER BY churn_rate_pct DESC;

-- Query 4: Tenure Cohort Risk Distribution
SELECT 
    CASE 
        WHEN tenure <= 12 THEN '0-1 Year (High Risk Cohort)'
        WHEN tenure <= 24 THEN '1-2 Years'
        WHEN tenure <= 48 THEN '2-4 Years'
        ELSE '4+ Years (Loyal)'
    END AS tenure_cohort,
    COUNT(*) AS customer_count,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS cohort_churn_rate_pct,
    ROUND(SUM(MonthlyCharges), 2) AS cohort_mrr
FROM telco_churn
GROUP BY tenure_cohort
ORDER BY cohort_churn_rate_pct DESC;

-- Query 5: Monthly Revenue at Immediate Risk (Month-to-Month + Electronic Check)
SELECT 
    COUNT(*) AS vulnerable_customer_count,
    ROUND(SUM(MonthlyCharges), 2) AS total_mrr_at_immediate_risk,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_spend
FROM telco_churn
WHERE Contract = 'Month-to-month' 
  AND PaymentMethod = 'Electronic check'
  AND Churn = 'No';