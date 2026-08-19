import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import io
from datetime import datetime

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="Universal Multi-Domain Analytics Platform",
    page_icon="📊",
    layout="wide"
)

# --- 2. Custom Modern SaaS Styling ---
st.markdown("""
<style>
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    section[data-testid="stSidebar"] {
        background-color: #1e293b;
        border-right: 1px solid #334155;
    }
    div[data-testid="stMetric"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        padding: 16px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        border-left: 5px solid #0284c7;
    }
    div[data-testid="stMetric"] label {
        font-size: 0.85rem !important;
        color: #94a3b8 !important;
        font-weight: 600;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        font-size: 1.7rem !important;
        font-weight: 700;
        color: #f8fafc !important;
    }
    h1, h2, h3, h4 {
        color: #ffffff !important;
        font-weight: 700;
    }
    .clean-box-warning {
        background-color: #451a03;
        border: 1px solid #b45309;
        border-left: 6px solid #f59e0b;
        padding: 16px 20px;
        border-radius: 8px;
        margin-bottom: 16px;
    }
    .clean-box-success {
        background-color: #052e16;
        border: 1px solid #15803d;
        border-left: 6px solid #22c55e;
        padding: 12px 18px;
        border-radius: 8px;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

PLOT_CONFIG = {
    'scrollZoom': True,
    'displayModeBar': True,
    'displaylogo': False,
    'modeBarButtonsToAdd': ['drawline', 'drawopenpath', 'eraseshape']
}

# --- 3. Multi-Format Ingestion Helper ---
def load_data_from_file(uploaded_file):
    """Loads CSV, XLSX, Parquet, or JSON files into a Pandas DataFrame."""
    file_name = uploaded_file.name.lower()
    if file_name.endswith('.csv'):
        return pd.read_csv(uploaded_file)
    elif file_name.endswith(('.xlsx', '.xls')):
        return pd.read_excel(uploaded_file)
    elif file_name.endswith('.parquet'):
        return pd.read_parquet(uploaded_file)
    elif file_name.endswith('.json'):
        return pd.read_json(uploaded_file)
    else:
        raise ValueError(f"Unsupported file format: {uploaded_file.name}")

# --- 4. Health Audit, Profiling & Auto-Cleaning Functions ---
def run_health_audit(df: pd.DataFrame):
    issues = []
    null_counts = int(df.isnull().sum().sum())
    if null_counts > 0:
        issues.append(f"Found **{null_counts:,}** missing/null values across columns.")
        
    whitespace_count = 0
    for col in df.select_dtypes(include=['object', 'string']).columns:
        ws_in_col = int(df[col].astype(str).str.strip().eq('').sum())
        whitespace_count += ws_in_col
    if whitespace_count > 0:
        issues.append(f"Found **{whitespace_count:,}** blank whitespace entries in text columns.")
        
    dup_count = int(df.duplicated().sum())
    if dup_count > 0:
        issues.append(f"Found **{dup_count:,}** exact duplicate rows.")
        
    is_clean = len(issues) == 0
    return is_clean, issues

def auto_clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    clean_df = df.copy()
    clean_df = clean_df.drop_duplicates()
    
    for col in clean_df.select_dtypes(include=['object', 'string']).columns:
        clean_df[col] = clean_df[col].replace(r'^\s*$', np.nan, regex=True)
        converted = pd.to_numeric(clean_df[col], errors='coerce')
        if len(clean_df) > 0 and (converted.notnull().sum() / len(clean_df)) > 0.8:
            clean_df[col] = converted
            
    for col in clean_df.select_dtypes(include=[np.number]).columns:
        clean_df[col] = clean_df[col].fillna(0)
        
    for col in clean_df.select_dtypes(include=['object', 'string']).columns:
        clean_df[col] = clean_df[col].fillna('Unknown')
        
    return clean_df

def profile_dataset_columns(df: pd.DataFrame):
    """Smart profiler classifying numeric vs categorical features without choking on small datasets."""
    cat_cols = []
    num_cols = []
    for col in df.columns:
        unique_count = df[col].nunique(dropna=True)
        if pd.api.types.is_numeric_dtype(df[col]):
            # If numeric and strictly binary (<=2 unique values e.g. 0/1), treat as categorical/event
            if unique_count <= 2:
                cat_cols.append(col)
            else:
                num_cols.append(col)
        else:
            cat_cols.append(col)
    return cat_cols, num_cols

def detect_recommended_mode(df: pd.DataFrame):
    for col in df.columns:
        u_vals = df[col].dropna().unique()
        if len(u_vals) in [2, 3]:
            str_vals = [str(x).strip().lower() for x in u_vals]
            if any(k in str_vals for k in ['yes', 'no', '1', '0', 'true', 'false', 'churn', 'active', 'left', 'fatal', 'fraud', 'incident']):
                return 0
    return 1

def generate_executive_html_report(df_summary_dict: dict, table_preview_html: str) -> str:
    metrics_cards_html = "".join([
        f"""<div class="metric-card">
            <div class="metric-title">{k}</div>
            <div class="metric-val">{v}</div>
        </div>""" for k, v in df_summary_dict.items()
    ])
    
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Executive Analytics Briefing</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f8fafc; color: #0f172a; margin: 0; padding: 40px; }}
            .container {{ max-width: 960px; margin: 0 auto; background: #ffffff; padding: 36px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border: 1px solid #e2e8f0; }}
            .header {{ border-bottom: 2px solid #0284c7; padding-bottom: 16px; margin-bottom: 24px; }}
            h1 {{ margin: 0 0 8px 0; color: #0f172a; font-size: 24px; }}
            .meta {{ color: #64748b; font-size: 13px; }}
            .grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 28px; }}
            .metric-card {{ background: #f1f5f9; padding: 16px; border-radius: 8px; border-left: 4px solid #0284c7; }}
            .metric-title {{ font-size: 12px; color: #475569; font-weight: 600; text-transform: uppercase; margin-bottom: 4px; }}
            .metric-val {{ font-size: 20px; font-weight: 700; color: #0f172a; }}
            .table-box {{ overflow-x: auto; margin-top: 20px; }}
            table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
            th, td {{ padding: 10px 12px; border: 1px solid #e2e8f0; text-align: left; }}
            th {{ background-color: #f8fafc; font-weight: 600; }}
            .footer {{ margin-top: 36px; padding-top: 16px; border-top: 1px solid #e2e8f0; font-size: 12px; color: #94a3b8; text-align: right; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 Executive Analytics & Data Health Briefing</h1>
                <div class="meta">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Engine: Universal Analytics Platform</div>
            </div>
            <h3>Key Performance Summary</h3>
            <div class="grid">{metrics_cards_html}</div>
            <h3>Data Sample & Structure (Top 10 Records)</h3>
            <div class="table-box">{table_preview_html}</div>
            <div class="footer">Confidential Internal Executive Briefing — Universal Analytics Engine</div>
        </div>
    </body>
    </html>
    """
    return html_template

# --- 5. Sidebar: Multi-Format File Ingestion ---
st.sidebar.header("📁 Ingestion & Formats")

uploaded_file = st.sidebar.file_uploader(
    "Upload Dataset (.csv, .xlsx, .parquet, .json)",
    type=["csv", "xlsx", "xls", "parquet", "json"],
    help="Supports CSV, Excel workbooks, Parquet telemetry, or JSON extracts."
)

if uploaded_file is not None:
    try:
        raw_df = load_data_from_file(uploaded_file)
        source_name = f"Uploaded: {uploaded_file.name}"
    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()
else:
    file_name = "WA_Fn-UseC_-Telco-Customer-Churn.csv"
    try:
        raw_df = pd.read_csv(file_name)
    except FileNotFoundError:
        raw_df = pd.read_csv("02_Data_Analytics/" + file_name)
    source_name = "Default Dataset: Telco Benchmark"

# --- 6. Data Quality Gate ---
is_clean, audit_issues = run_health_audit(raw_df)

if "clean_choice" not in st.session_state:
    st.session_state.clean_choice = "pending"

if "last_source" not in st.session_state or st.session_state.last_source != source_name:
    st.session_state.last_source = source_name
    st.session_state.clean_choice = "pending"
    default_mode_idx = detect_recommended_mode(raw_df)
    st.session_state.current_mode_idx = default_mode_idx

if is_clean or st.session_state.clean_choice == "raw":
    active_df = raw_df.copy()
elif st.session_state.clean_choice == "cleaned":
    active_df = auto_clean_dataset(raw_df)
else:
    active_df = raw_df.copy()

st.title("🌐 Universal Multi-Domain Analytics Engine")
st.caption(f"Active Source: **{source_name}** | Total Observations: **{len(active_df):,}** | Dimensions: **{len(active_df.columns)}**")

if not is_clean and st.session_state.clean_choice == "pending":
    st.markdown("""
    <div class="clean-box-warning">
        <h4 style="margin:0 0 8px 0; color:#fde68a !important;">⚠️ Data Quality Alert: Uncleaned Dataset Detected</h4>
        <p style="margin:0; font-size:0.9rem; color:#fef3c7;">
            The active file contains missing values, blank entries, or formatting issues that may affect analytics accuracy.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("🔍 View Detected Quality Anomalies", expanded=True):
        for issue in audit_issues:
            st.markdown(f"- {issue}")
            
    btn_col1, btn_col2 = st.columns([1, 1])
    with btn_col1:
        if st.button("✨ Clean the file now (Recommended)", type="primary", use_container_width=True):
            st.session_state.clean_choice = "cleaned"
            st.rerun()
    with btn_col2:
        if st.button("⏩ Use the file as it is", use_container_width=True):
            st.session_state.clean_choice = "raw"
            st.rerun()
            
elif st.session_state.clean_choice == "cleaned":
    st.markdown("""
    <div class="clean-box-success">
        <strong style="color:#86efac;">✓ Dataset Cleansed:</strong> Missing entries imputed, whitespace stripped, and datatypes standardized.
    </div>
    """, unsafe_allow_html=True)

# --- 7. Analysis Modes & Dispatcher ---
st.sidebar.markdown("---")
st.sidebar.header("🎯 Analysis Mode")

modes = [
    "🚨 Event & Binary Risk Analysis",
    "📈 Continuous Metrics & Trends",
    "🔗 Correlation & Driver Explorer"
]

if "current_mode_idx" not in st.session_state:
    st.session_state.current_mode_idx = 0

def on_mode_change():
    st.session_state.current_mode_idx = modes.index(st.session_state.mode_radio)

analysis_mode = st.sidebar.radio(
    "Select Intelligence Mode:",
    modes,
    index=st.session_state.current_mode_idx,
    key="mode_radio",
    on_change=on_mode_change
)

all_cols = list(active_df.columns)
cat_cols, num_cols = profile_dataset_columns(active_df)
if not cat_cols:
    cat_cols = all_cols
if not num_cols:
    num_cols = all_cols

def find_default_index(col_list, keywords, fallback_idx=0):
    for idx, col in enumerate(col_list):
        if any(k.lower() in col.lower() for k in keywords):
            return idx
    return fallback_idx if fallback_idx < len(col_list) else 0

st.sidebar.markdown("---")
st.sidebar.header("⚙️ Feature Mapping")

summary_metrics_for_report = {}

if analysis_mode == "🚨 Event & Binary Risk Analysis":
    target_event_col = st.sidebar.selectbox(
        "Event / Risk Column (Target)",
        all_cols,
        index=find_default_index(all_cols, ["churn", "status", "cancel", "fatality", "fraud", "incident", "event"], 1 if len(all_cols)>1 else 0)
    )
    metric_measure_col = st.sidebar.selectbox(
        "Primary Measure / Impact Column",
        num_cols,
        index=find_default_index(num_cols, ["monthly", "charge", "mrr", "spend", "cost", "freight", "sales", "amount"], 0)
    )
    
    slicer_candidates = [c for c in cat_cols if c != target_event_col]
    if not slicer_candidates:
        slicer_candidates = all_cols
        
    category_slicer_1 = st.sidebar.selectbox("Primary Category Slicer", slicer_candidates, index=0)
    category_slicer_2 = st.sidebar.selectbox("Secondary Category Slicer", slicer_candidates, index=1 if len(slicer_candidates)>1 else 0)
    
    def normalize_event(val):
        if pd.isna(val):
            return 0
        s = str(val).strip().lower()
        if s in ['yes', '1', 'true', 'churn', 'churned', 'positive', 'fatal', 'failed', 'left']:
            return 1
        return 0
        
    analysis_df = active_df.copy()
    analysis_df["__Event_Flag__"] = analysis_df[target_event_col].apply(normalize_event)
    analysis_df["__Event_Display__"] = analysis_df["__Event_Flag__"].apply(lambda x: "Event / Risk" if x == 1 else "Baseline / Normal")
    analysis_df[metric_measure_col] = pd.to_numeric(analysis_df[metric_measure_col], errors='coerce').fillna(0)

    total_records = len(analysis_df)
    event_count = int(analysis_df["__Event_Flag__"].sum())
    event_rate = (event_count / total_records * 100) if total_records > 0 else 0
    total_impact = float(analysis_df[metric_measure_col].sum())
    risk_impact = float(analysis_df[analysis_df["__Event_Flag__"] == 1][metric_measure_col].sum())

    summary_metrics_for_report = {
        "Total Observations": f"{total_records:,}",
        "Event / Risk Rate": f"{event_rate:.1f}%",
        f"Total {metric_measure_col}": f"${total_impact:,.2f}",
        f"At-Risk {metric_measure_col}": f"${risk_impact:,.2f}"
    }

    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("📋 Total Records", f"{total_records:,}")
    with c2:
        st.metric("⚠️ Event / Risk Rate", f"{event_rate:.1f}%")
    with c3:
        st.metric(f"📊 Total {metric_measure_col}", f"${total_impact:,.2f}")
    with c4:
        st.metric(f"🚨 At-Risk {metric_measure_col}", f"${risk_impact:,.2f}")
    st.divider()

    row1_c1, row1_c2 = st.columns(2)
    with row1_c1:
        st.subheader(f"📊 Chart 1: Occurrence by {category_slicer_1}")
        num_unique_slicer = analysis_df[category_slicer_1].nunique()
        if num_unique_slicer <= 15:
            grp1 = analysis_df.groupby([category_slicer_1, "__Event_Display__"]).size().reset_index(name="Count")
            fig1 = px.bar(grp1, x=category_slicer_1, y="Count", color="__Event_Display__", barmode="group",
                          color_discrete_map={"Event / Risk": "#ef4444", "Baseline / Normal": "#3b82f6"}, template="plotly_dark")
        else:
            fig1 = px.histogram(analysis_df, x=category_slicer_1, color="__Event_Display__", barmode="group", nbins=25,
                                color_discrete_map={"Event / Risk": "#ef4444", "Baseline / Normal": "#3b82f6"}, template="plotly_dark")
        fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig1, use_container_width=True, config=PLOT_CONFIG)

    with row1_c2:
        st.subheader(f"🌐 Chart 2: {metric_measure_col} Impact by {category_slicer_2}")
        fig2 = px.histogram(analysis_df, x=category_slicer_2, y=metric_measure_col, color="__Event_Display__", barmode="stack",
                            color_discrete_map={"Event / Risk": "#ef4444", "Baseline / Normal": "#3b82f6"}, template="plotly_dark",
                            labels={metric_measure_col: f"Total {metric_measure_col}"})
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=20, r=20, t=30, b=20), xaxis_tickangle=-20)
        st.plotly_chart(fig2, use_container_width=True, config=PLOT_CONFIG)

    row2_c1, row2_c2 = st.columns(2)
    with row2_c1:
        st.subheader(f"⏳ Chart 3: {metric_measure_col} Spread vs. Target")
        fig3 = px.box(analysis_df, x="__Event_Display__", y=metric_measure_col, color="__Event_Display__",
                      color_discrete_map={"Event / Risk": "#ef4444", "Baseline / Normal": "#3b82f6"}, template="plotly_dark")
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=20, r=20, t=30, b=20), showlegend=False)
        st.plotly_chart(fig3, use_container_width=True, config=PLOT_CONFIG)

    with row2_c2:
        secondary_num = num_cols[1] if len(num_cols) > 1 else metric_measure_col
        st.subheader(f"💳 Chart 4: {metric_measure_col} vs. {secondary_num}")
        analysis_df[secondary_num] = pd.to_numeric(analysis_df[secondary_num], errors='coerce').fillna(0)
        fig4 = px.scatter(analysis_df, x=metric_measure_col, y=secondary_num, color="__Event_Display__",
                          color_discrete_map={"Event / Risk": "#ef4444", "Baseline / Normal": "#3b82f6"}, template="plotly_dark")
        fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig4, use_container_width=True, config=PLOT_CONFIG)

elif analysis_mode == "📈 Continuous Metrics & Trends":
    primary_num = st.sidebar.selectbox("Primary Numeric Metric (X)", num_cols, index=0)
    secondary_num = st.sidebar.selectbox("Secondary Numeric Metric (Y)", num_cols, index=1 if len(num_cols)>1 else 0)
    tertiary_num = st.sidebar.selectbox("Color / Gradient Metric (Optional)", num_cols, index=2 if len(num_cols)>2 else 0)
    
    analysis_df = active_df.copy()
    analysis_df[primary_num] = pd.to_numeric(analysis_df[primary_num], errors='coerce').fillna(0)
    analysis_df[secondary_num] = pd.to_numeric(analysis_df[secondary_num], errors='coerce').fillna(0)
    analysis_df[tertiary_num] = pd.to_numeric(analysis_df[tertiary_num], errors='coerce').fillna(0)
    
    summary_metrics_for_report = {
        "Total Observations": f"{len(analysis_df):,}",
        f"Mean {primary_num}": f"{analysis_df[primary_num].mean():,.2f}",
        f"Max {primary_num}": f"{analysis_df[primary_num].max():,.2f}",
        f"Std Dev {primary_num}": f"{analysis_df[primary_num].std():,.2f}"
    }

    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("📋 Total Observations", f"{len(analysis_df):,}")
    with c2:
        st.metric(f"🎯 Mean {primary_num}", f"{analysis_df[primary_num].mean():,.2f}")
    with c3:
        st.metric(f"🏔️ Max {primary_num}", f"{analysis_df[primary_num].max():,.2f}")
    with c4:
        st.metric(f"📊 Std Dev {primary_num}", f"{analysis_df[primary_num].std():,.2f}")
    st.divider()
    
    row1_c1, row1_c2 = st.columns(2)
    with row1_c1:
        st.subheader(f"📊 Chart 1: Distribution of {primary_num}")
        fig1 = px.histogram(
            analysis_df, 
            x=primary_num, 
            nbins=30, 
            marginal="box",
            color_discrete_sequence=["#38bdf8"], 
            template="plotly_dark"
        )
        # Force the marginal box plot to render as a clean standard rectangle (no bow-tie notches)
        fig1.for_each_trace(lambda t: t.update(notched=False) if t.type == 'box' else None)
        fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig1, use_container_width=True, config=PLOT_CONFIG)
        
    with row1_c2:
        st.subheader(f"📈 Chart 2: {primary_num} vs. {secondary_num}")
        enable_trendline = "ols" if (primary_num != secondary_num and len(analysis_df) >= 3) else None
        fig2 = px.scatter(
            analysis_df, 
            x=primary_num, 
            y=secondary_num, 
            color=tertiary_num if (tertiary_num != primary_num and tertiary_num != secondary_num) else None,
            color_continuous_scale="Viridis", 
            trendline=enable_trendline, 
            template="plotly_dark"
        )
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig2, use_container_width=True, config=PLOT_CONFIG)
        
    row2_c1, row2_c2 = st.columns(2)
    with row2_c1:
        st.subheader(f"📦 Chart 3: Spread of {secondary_num}")
        fig3 = px.box(analysis_df, y=secondary_num, template="plotly_dark", color_discrete_sequence=["#06b6d4"])
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig3, use_container_width=True, config=PLOT_CONFIG)
        
    with row2_c2:
        st.subheader(f"🌊 Chart 4: 2D Density ({primary_num} vs. {secondary_num})")
        fig4 = px.density_heatmap(analysis_df, x=primary_num, y=secondary_num, nbinsx=20, nbinsy=20, color_continuous_scale="Plasma", template="plotly_dark")
        fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig4, use_container_width=True, config=PLOT_CONFIG)

else:  # Correlation & Driver Explorer
    num_features_count = len(num_cols)
    corr_matrix = active_df[num_cols].apply(pd.to_numeric, errors='coerce').dropna().corr()
    corr_unstacked = corr_matrix.abs().unstack()
    non_self_corr = corr_unstacked[corr_unstacked < 0.9999]
    max_corr_val = float(non_self_corr.max()) if not non_self_corr.empty else 0.0

    summary_metrics_for_report = {
        "Numerical Features": f"{num_features_count}",
        "Matrix Dimensions": f"{num_features_count} × {num_features_count}",
        "Max Correlation |r|": f"{max_corr_val:.3f}",
        "Analysis Status": "Active"
    }

    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("🔢 Numerical Features", f"{num_features_count}")
    with c2:
        st.metric("📐 Matrix Dimensions", f"{num_features_count} × {num_features_count}")
    with c3:
        st.metric("🔥 Max Correlation |r|", f"{max_corr_val:.3f}")
    with c4:
        st.metric("⚡ Analysis Status", "Active")
    st.divider()

    st.subheader("🔗 Multi-Variable Numeric Correlation Matrix")
    fig_corr = px.imshow(corr_matrix, text_auto=True, aspect="auto", color_continuous_scale="Blues", template="plotly_dark")
    fig_corr.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_corr, use_container_width=True, config=PLOT_CONFIG)

# --- 8. Exports: Cleansed CSV & 1-Click Executive HTML Report ---
st.divider()
st.subheader("📥 Export & Reporting Center")

export_col1, export_col2 = st.columns(2)

with export_col1:
    csv_buffer = io.BytesIO()
    active_df.to_csv(csv_buffer, index=False)
    st.download_button(
        label="📄 Download Cleansed CSV Dataset",
        data=csv_buffer.getvalue(),
        file_name="universal_cleansed_dataset.csv",
        mime="text/csv",
        use_container_width=True
    )

with export_col2:
    table_sample_html = active_df.head(10).to_html(classes='table', index=False)
    html_report_content = generate_executive_html_report(summary_metrics_for_report, table_sample_html)
    
    st.download_button(
        label="📊 Export 1-Click Executive HTML Report",
        data=html_report_content,
        file_name=f"executive_briefing_{datetime.now().strftime('%Y%m%d_%H%M')}.html",
        mime="text/html",
        use_container_width=True
    )

with st.expander("📄 View Active In-Memory Data Table"):
    st.dataframe(active_df, use_container_width=True)