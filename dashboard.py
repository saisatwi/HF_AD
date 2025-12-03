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
    layout="wide"
)

st.title("📊 Health + Finance Analytics Dashboard")
st.markdown("### All analytics generated from your cleaned CSV datasets.")

# --------------------------
# LOAD DATA
# --------------------------
DATA_DIR = Path("data")

health_file = DATA_DIR / "health_data_cleaned.csv"
finance_file = DATA_DIR / "finance_data_cleaned.csv"

try:
    health_df = pd.read_csv(health_file)
    finance_df = pd.read_csv(finance_file)
except FileNotFoundError:
    st.error("❌ CSV files not found. Ensure they exist in the /data folder.")
    st.stop()

# Convert dates
health_df["Date"] = pd.to_datetime(health_df["Date"])
finance_df["Date"] = pd.to_datetime(finance_df["Date"])

# --------------------------
# SIDEBAR FILTERS
# --------------------------
st.sidebar.header("🔎 Filters")

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=[health_df["Date"].min(), health_df["Date"].max()]
)

health_filtered = health_df[
    (health_df["Date"] >= pd.to_datetime(date_range[0])) &
    (health_df["Date"] <= pd.to_datetime(date_range[1]))
]

finance_filtered = finance_df[
    (finance_df["Date"] >= pd.to_datetime(date_range[0])) &
    (finance_df["Date"] <= pd.to_datetime(date_range[1]))
]

st.sidebar.markdown("---")
selected_category = st.sidebar.multiselect(
    "Finance Categories",
    options=finance_df["Category"].unique(),
    default=finance_df["Category"].unique()
)
finance_filtered = finance_filtered[finance_filtered["Category"].isin(selected_category)]

# --------------------------
# HEALTH SECTION
# --------------------------
st.header("💪 Health Analytics")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Steps", f"{health_filtered['Steps'].sum():,}")
col2.metric("Total Calories", f"{health_filtered['Calories'].sum():,}")
col3.metric("Avg Sleep (hrs)", f"{health_filtered['Sleephours'].mean():.2f}")
col4.metric("Avg Heart Rate", f"{health_filtered['Heartrate'].mean():.2f}")

# Line chart – Steps over time
st.subheader("📈 Daily Steps Trend")
fig = px.line(health_filtered, x="Date", y="Steps", title="Steps Over Time")
st.plotly_chart(fig, use_container_width=True)

# Sleep Hours
st.subheader("😴 Sleep Hours Trend")
fig = px.line(health_filtered, x="Date", y="Sleephours", title="Sleep Hours Over Time")
st.plotly_chart(fig, use_container_width=True)

# Heart Rate
st.subheader("❤️ Heart Rate Trend")
fig = px.line(health_filtered, x="Date", y="Heartrate", title="Heart Rate Over Time")
st.plotly_chart(fig, use_container_width=True)

# --------------------------
# FINANCE SECTION
# --------------------------
st.header("💰 Finance Analytics")

col1, col2 = st.columns(2)
col1.metric("Total Transactions", f"{len(finance_filtered)}")
col2.metric("Total Expenses (Amount)", f"₹{finance_filtered['Amount'].sum():,}")

# Expense Trend
st.subheader("📉 Expense Trend by Date")
fig = px.line(finance_filtered, x="Date", y="Amount", title="Expenses Over Time")
st.plotly_chart(fig, use_container_width=True)

# Category Bar Chart
st.subheader("🏷️ Spending by Category")
category_totals = finance_filtered.groupby("Category")["Amount"].sum().reset_index()
fig = px.bar(category_totals, x="Category", y="Amount", title="Category-wise Expense Distribution")
st.plotly_chart(fig, use_container_width=True)

# Pie Chart
st.subheader("🥧 Expense Share by Category")
fig = px.pie(category_totals, names="Category", values="Amount", title="Expense Breakdown")
st.plotly_chart(fig, use_container_width=True)

# Monthly Trend
finance_df["Month"] = finance_df["Date"].dt.to_period("M").astype(str)
monthly_totals = finance_df.groupby("Month")["Amount"].sum().reset_index()

st.subheader("📆 Monthly Total Expenses")
fig = px.bar(monthly_totals, x="Month", y="Amount", title="Monthly Spending Trend")
st.plotly_chart(fig, use_container_width=True)

# --------------------------
# FOOTER
# --------------------------
st.markdown("---")
st.markdown("### ✔ Dashboard generated automatically based on your CSV data.")
