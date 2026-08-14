import pandas as pd
import numpy as np

def run_data_pipeline():
    # 1. Load Dataset
    csv_path = "02_Data_Analytics/WA_Fn-UseC_-Telco-Customer-Churn.csv"
    df = pd.read_csv(csv_path)
    print(f"[*] Dataset Loaded: {df.shape[0]} rows, {df.shape[1]} columns")

    # 2. Data Cleaning: Fix blank spaces in TotalCharges
    df['TotalCharges'] = df['TotalCharges'].replace(' ', np.nan)
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'])
    
    # Fill remaining NaNs with 0 for new tenure=0 customers
    df['TotalCharges'] = df['TotalCharges'].fillna(0.0)
    print(f"[*] TotalCharges successfully converted to numeric. Missing values handled: {df['TotalCharges'].isnull().sum()}")

    # 3. Feature Engineering: Risk Scoring Logic
    # Rules-based heuristic risk scoring (0 to 100)
    def calculate_risk(row):
        score = 0
        if row['Contract'] == 'Month-to-month':
            score += 40
        elif row['Contract'] == 'One year':
            score += 15
            
        if row['PaymentMethod'] == 'Electronic check':
            score += 25
            
        if row['tenure'] <= 12:
            score += 25
        elif row['tenure'] <= 24:
            score += 10
            
        if row['InternetService'] == 'Fiber optic':
            score += 10
            
        return min(score, 100)

    df['RiskScore'] = df.apply(calculate_risk, axis=1)

    # 4. Segment into Risk Tiers
    df['RiskTier'] = pd.cut(
        df['RiskScore'],
        bins=[-1, 39, 69, 100],
        labels=['Low Risk', 'Medium Risk', 'High Risk']
    )

    # 5. Save Cleaned & Enriched Dataset
    output_path = "02_Data_Analytics/cleaned_churn_data.csv"
    df.to_csv(output_path, index=False)
    print(f"[*] Cleaned & Enriched data saved to: {output_path}")
    print("\n--- Risk Tier Distribution ---")
    print(df['RiskTier'].value_counts())

if __name__ == "__main__":
    run_data_pipeline()