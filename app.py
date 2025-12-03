import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# --------------------------
# PAGE CONFIG
# --------------------------
st.set_page_config(
    page_title="HF_AD Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------
# DATA FILE PATHS
# --------------------------
DATA_DIR = Path("data")
health_file = DATA_DIR / "health_data_cleaned.csv"
finance_file = DATA_DIR / "finance_data_cleaned.csv"

# --------------------------
# LOAD DATA
# --------------------------
try:
    health_df = pd.read_csv(health_file)
    finance_df = pd.read_csv(finance_file)
except FileNotFoundError:
    st.error("❌ CSV files not found in 'data' folder. Make sure health_data_cleaned.csv and finance_data_cleaned.csv exist.")
    st.stop()

# Standardize column names (avoid errors)
health_df.columns = [c.strip() for c in health_df.columns]
finance_df.columns = [c.strip() for c in finance_df.columns]

# Convert Date columns
health_df["Date"] = pd.to_datetime(health_df["Date"])
finance_df["Date"] = pd.to_datetime(finance_df["Date"])

# --------------------------
# SIDEBAR
# --------------------------
st.sidebar.title("Filters & Theme")

# Theme selection
theme_option = st.sidebar.radio("Select Theme", ["Light", "Dark"])
if theme_option == "Dark":
    st.markdown("""
    <style>
    .reportview-container {background-color: #0E1117; color: white;}
    .sidebar .sidebar-content {background-color: #111827; color:white;}
    h1, h2, h3, h4, h5, h6 {color: white;}
    .stMetric-label {color: white;}
    </style>
    """, unsafe_allow_html=True)
    plot_template = "plotly_dark"
else:
    plot_template = "plotly_white"

# Date filter
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=[health_df["Date"].min(), health_df["Date"].max()]
)

# Finance category filter
selected_categories = st.sidebar.multiselect(
    "Finance Categories",
    options=finance_df["Category"].unique(),
    default=finance_df["Category"].unique()
)

# --------------------------
# FILTER DATA
# --------------------------
health_filtered = health_df[
    (health_df["Date"] >= pd.to_datetime(date_range[0])) &
    (health_df["Date"] <= pd.to_datetime(date_range[1]))
]

finance_filtered = finance_df[
    (finance_df["Date"] >= pd.to_datetime(date_range[0])) &
    (finance_df["Date"] <= pd.to_datetime(date_range[1])) &
    (finance_df["Category"].isin(selected_categories))
]

# --------------------------
# TABS
# --------------------------
tab1, tab2 = st.tabs(["💪 Health Dashboard", "💰 Finance Dashboard"])

# --------------------------
# HEALTH DASHBOARD
# --------------------------
with tab1:
    st.header("Health Analytics")
    
    # KPI cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Steps", f"{health_filtered['Steps'].sum():,}")
    col2.metric("Total Calories", f"{health_filtered['Calories'].sum():,}")
    col3.metric("Avg Sleep (hrs)", f"{health_filtered['Sleephours'].mean():.2f}")
    col4.metric("Avg Heart Rate", f"{health_filtered['Heartrate'].mean():.2f}")
    
    # Charts
    st.subheader("Steps Over Time")
    fig = px.line(health_filtered, x="Date", y="Steps", title="Steps Trend", template=plot_template)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Sleep Hours Over Time")
    fig = px.line(health_filtered, x="Date", y="Sleephours", title="Sleep Trend", template=plot_template)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Heart Rate Over Time")
    fig = px.line(health_filtered, x="Date", y="Heartrate", title="Heart Rate Trend", template=plot_template)
    st.plotly_chart(fig, use_container_width=True)

# --------------------------
# FINANCE DASHBOARD
# --------------------------
with tab2:
    st.header("Finance Analytics")
    
    # KPI cards
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Transactions", len(finance_filtered))
    col2.metric("Total Amount (₹)", f"{finance_filtered['Amount'].sum():,}")
    col3.metric("Average Transaction (₹)", f"{finance_filtered['Amount'].mean():,.2f}")
    
    # Expense/Income trend
    st.subheader("Transactions Over Time")
    fig = px.line(finance_filtered, x="Date", y="Amount", color="Category",
                  title="Finance Trend", template=plot_template)
    st.plotly_chart(fig, use_container_width=True)
    
    # Category-wise bar chart
    st.subheader("Category-wise Spending")
    cat_totals = finance_filtered.groupby("Category")["Amount"].sum().reset_index()
    fig = px.bar(cat_totals, x="Category", y="Amount", color="Category", title="Category-wise Amount", template=plot_template)
    st.plotly_chart(fig, use_container_width=True)

    # Pie chart
    st.subheader("Expense Share by Category")
    fig = px.pie(cat_totals, names="Category", values="Amount", title="Category Distribution")
    st.plotly_chart(fig, use_container_width=True)

    # Monthly trend
    finance_filtered["Month"] = finance_filtered["Date"].dt.to_period("M").astype(str)
    month_totals = finance_filtered.groupby("Month")["Amount"].sum().reset_index()
    st.subheader("Monthly Total Amount")
    fig = px.bar(month_totals, x="Month", y="Amount", title="Monthly Trend", template=plot_template)
    st.plotly_chart(fig, use_container_width=True)

# --------------------------
# FOOTER
# --------------------------
st.markdown("---")
st.markdown("Made with ❤️ by HF_AD | Health & Finance Dashboard")
