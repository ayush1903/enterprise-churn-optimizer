import pandas as pd
import numpy as np

np.random.seed(42)
n_records = 5000

# 1. Base Variables
carriers = np.random.choice(['Apex Freight', 'BlueDart Express', 'SwiftLogix', 'TransGlobal'], n_records, p=[0.35, 0.25, 0.20, 0.20])
transport_modes = np.random.choice(['Air', 'Ocean', 'Road', 'Rail'], n_records, p=[0.25, 0.30, 0.35, 0.10])
shipment_weight = np.random.uniform(5.0, 1500.0, n_records).round(2)
freight_cost = (shipment_weight * np.random.uniform(1.8, 3.5, n_records) + np.random.uniform(50, 300, n_records)).round(2)
transit_days = np.random.randint(1, 45, n_records)

# 2. Risk Target: Delay / Incident (Yes/No)
risk_prob = np.where(transit_days > 20, 0.45, 0.12)
incident_flag = np.where(np.random.rand(n_records) < risk_prob, 'Yes', 'No')

# 3. Assemble Dirty Enterprise Dataframe
df = pd.DataFrame({
    ' Shipment_ID ': [f"SHP-{10000 + i}" for i in range(n_records)], # Whitespace in header
    'Carrier_Partner': carriers,
    'Transport_Mode': transport_modes,
    'Weight_KG': shipment_weight,
    'Freight_Charges_USD': freight_cost.astype(str), # Disguised numeric as string
    'Transit_Days': transit_days,
    'Incident_Risk': incident_flag
})

# 4. Inject SIT Edge Cases
# A. Inject whitespace blanks into disguised string column
df.loc[np.random.choice(n_records, 45, replace=False), 'Freight_Charges_USD'] = "   "

# B. Inject pure Null values into categorical and numerical columns
df.loc[np.random.choice(n_records, 30, replace=False), 'Carrier_Partner'] = np.nan
df.loc[np.random.choice(n_records, 20, replace=False), 'Weight_KG'] = np.nan

# C. Inject Duplicate tracking records (25 exact duplicates)
duplicate_rows = df.iloc[:25]
df = pd.concat([df, duplicate_rows], ignore_index=True)

# 5. Export to CSV
output_path = "02_Data_Analytics/logistics_stress_test.csv"
df.to_csv(output_path, index=False)
print(f"✓ Successfully generated SIT Stress-Test Dataset: '{output_path}' ({len(df)} rows)")