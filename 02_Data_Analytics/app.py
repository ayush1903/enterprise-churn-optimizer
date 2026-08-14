import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="Telco Customer Churn Dashboard",
    page_icon="📊",
    layout="wide"
)

# --- 2. Custom Modern SaaS Styling ---
st.markdown("""
<style>
    /* Dark Theme Background */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #1e293b;
        border-right: 1px solid #334155;
    }

    /* Metric Cards Styling */
    div[data-testid="stMetric"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        padding: 16px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        border-left: 5px solid #0284c7;
    }
    
    div[data-testid="stMetric"] label {
        font-size: 0.9rem !important;
        color: #94a3b8 !important;
        font-weight: 600;
    }
    
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 700;
        color: #f8fafc !important;
    }

    /* Headers */
    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. Load & Clean Data ---
@st.cache_data
def load_data():
    file_name = "WA_Fn-UseC_-Telco-Customer-Churn.csv"
    try:
        df = pd.read_csv(file_name)
    except FileNotFoundError:
        df = pd.read_csv("02_Data_Analytics/" + file_name)
        
    # Clean TotalCharges
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"].replace(" ", None), errors="coerce")
    df["TotalCharges"] = df["TotalCharges"].fillna(0)
    
    # Create Churn flag (0 or 1)
    df["Churn_Flag"] = df["Churn"].apply(lambda x: 1 if x == "Yes" else 0)
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading dataset: {e}. Please ensure 'WA_Fn-UseC_-Telco-Customer-Churn.csv' is in 02_Data_Analytics folder.")
    st.stop()

# --- 4. Sidebar Filters ---
st.sidebar.header("🔍 Filter Options")

contract_options = ["All"] + sorted(list(df["Contract"].dropna().unique()))
selected_contract = st.sidebar.selectbox("Contract Type", contract_options)

internet_options = ["All"] + sorted(list(df["InternetService"].dropna().unique()))
selected_internet = st.sidebar.selectbox("Internet Service", internet_options)

# Filter Application
filtered_df = df.copy()
if selected_contract != "All":
    filtered_df = filtered_df[filtered_df["Contract"] == selected_contract]
if selected_internet != "All":
    filtered_df = filtered_df[filtered_df["InternetService"] == selected_internet]

# --- 5. Dashboard Header ---
st.title("📊 Telco Customer Churn & Revenue Analytics")
st.markdown("Interactive insights dashboard to monitor churn rate, risk segments, and revenue.")
st.divider()

# --- 6. Key Metrics (KPIs) ---
total_customers = len(filtered_df)
churn_count = filtered_df["Churn_Flag"].sum()
churn_rate = (churn_count / total_customers * 100) if total_customers > 0 else 0
total_mrr = filtered_df["MonthlyCharges"].sum()
revenue_at_risk = filtered_df[filtered_df["Churn"] == "Yes"]["MonthlyCharges"].sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="👥 Total Customers", value=f"{total_customers:,}")

with col2:
    st.metric(label="⚠️ Churn Rate", value=f"{churn_rate:.1f}%")

with col3:
    st.metric(label="💰 Total MRR", value=f"${total_mrr:,.2f}")

with col4:
    st.metric(label="🚨 Monthly Revenue at Risk", value=f"${revenue_at_risk:,.2f}")

st.divider()

# --- 7. Visualizations ---
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    # Visual 1: Churn by Contract Type
    st.subheader("📋 Churn by Contract Type")
    contract_churn = filtered_df.groupby(["Contract", "Churn"]).size().reset_index(name="Count")
    fig_contract = px.bar(
        contract_churn,
        x="Contract",
        y="Count",
        color="Churn",
        barmode="group",
        color_discrete_map={"Yes": "#ef4444", "No": "#3b82f6"},
        template="plotly_dark"
    )
    fig_contract.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig_contract, use_container_width=True)

with row1_col2:
    # Visual 2: Revenue Distribution by Internet Service
    st.subheader("🌐 MRR Distribution by Internet Service")
    fig_rev = px.histogram(
        filtered_df,
        x="InternetService",
        y="MonthlyCharges",
        color="Churn",
        barmode="stack",
        color_discrete_map={"Yes": "#ef4444", "No": "#3b82f6"},
        template="plotly_dark",
        labels={"MonthlyCharges": "Total Monthly Charges ($)"}
    )
    fig_rev.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig_rev, use_container_width=True)

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    # Visual 3: Tenure vs Churn Distribution
    st.subheader("⏳ Tenure (Months) vs Churn")
    fig_tenure = px.box(
        filtered_df,
        x="Churn",
        y="tenure",
        color="Churn",
        color_discrete_map={"Yes": "#ef4444", "No": "#3b82f6"},
        template="plotly_dark",
        labels={"tenure": "Tenure (Months)"}
    )
    fig_tenure.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=30, b=20),
        showlegend=False
    )
    st.plotly_chart(fig_tenure, use_container_width=True)

with row2_col2:
    # Visual 4: Payment Method Distribution
    st.subheader("💳 Churn by Payment Method")
    fig_pay = px.histogram(
        filtered_df,
        x="PaymentMethod",
        color="Churn",
        barmode="group",
        color_discrete_map={"Yes": "#ef4444", "No": "#3b82f6"},
        template="plotly_dark",
        labels={"PaymentMethod": "Payment Method", "count": "Customer Count"}
    )
    fig_pay.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_tickangle=-25,
        margin=dict(l=20, r=20, t=30, b=20),
        yaxis_title="Customer Count"
    )
    st.plotly_chart(fig_pay, use_container_width=True)

# --- 8. Data Preview Expander ---
with st.expander("📄 View Filtered Raw Data"):
    st.dataframe(filtered_df, use_container_width=True)