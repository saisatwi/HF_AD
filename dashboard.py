import streamlit as st
import pandas as pd
import plotly.express as px
import os

# -------------------------------------------------------
# CONFIG
# -------------------------------------------------------
st.set_page_config(
    page_title="Health & Finance Dashboard",
    layout="wide",
    page_icon="📊"
)

st.title("📊 My Personal Health & Finance Dashboard")
st.markdown("Interactive analytics built from cleaned datasets.")

DATA_PATH = "data"
OUTPUT_PATH = "output"

# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------
@st.cache_data
def load_data():
    health = pd.read_csv(f"{DATA_PATH}/health_data_cleaned.csv")
    finance = pd.read_csv(f"{DATA_PATH}/finance_data_cleaned.csv")

    # Cleanup
    health.columns = [c.strip().title().replace(" ", "") for c in health.columns]
    finance.columns = [c.strip().title().replace(" ", "") for c in finance.columns]

    if "Date" in health.columns:
        health["Date"] = pd.to_datetime(health["Date"])
    if "Date" in finance.columns:
        finance["Date"] = pd.to_datetime(finance["Date"])

    return health, finance

health_df, finance_df = load_data()

# -------------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------------
st.sidebar.header("🔍 Filters")

# Health date filter
if "Date" in health_df.columns:
    start_date = st.sidebar.date_input("Health Start Date", health_df["Date"].min())
    end_date = st.sidebar.date_input("Health End Date", health_df["Date"].max())

    health_filtered = health_df[
        (health_df["Date"] >= pd.to_datetime(start_date)) &
        (health_df["Date"] <= pd.to_datetime(end_date))
    ]
else:
    health_filtered = health_df

# Finance Category filter
category_filter = st.sidebar.multiselect(
    "Finance Categories",
    options=finance_df["Category"].unique(),
    default=finance_df["Category"].unique()
)
finance_filtered = finance_df[finance_df["Category"].isin(category_filter)]

# -------------------------------------------------------
# KPI CALCULATIONS
# -------------------------------------------------------

# HEALTH KPIs
steps_avg = int(health_filtered["Steps"].mean()) if "Steps" in health_filtered else 0
sleep_avg = round(health_filtered["Sleephours"].mean(), 2) if "Sleephours" in health_filtered else 0
calories_avg = int(health_filtered["Calories"].mean()) if "Calories" in health_filtered else 0

# FINANCE KPIs
total_income = int(finance_filtered[finance_filtered["Category"] == "Income"]["Amount"].sum())
total_expenses = int(finance_filtered[finance_filtered["Category"] == "Expense"]["Amount"].sum())
total_savings = total_income - total_expenses

# -------------------------------------------------------
# KPI DISPLAY
# -------------------------------------------------------
st.subheader("📌 Key Performance Indicators")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("🦶 Avg Steps", steps_avg)
c2.metric("🔥 Avg Calories Burned", calories_avg)
c3.metric("😴 Avg Sleep Hours", sleep_avg)
c4.metric("💰 Total Income", f"₹{total_income}")
c5.metric("💸 Total Expenses", f"₹{total_expenses}")

st.metric("💵 Net Savings", f"₹{total_savings}")

# -------------------------------------------------------
# HEALTH CHARTS
# -------------------------------------------------------
st.header("🏃 Health Analytics")

if "Steps" in health_filtered:
    fig = px.line(health_filtered, x="Date", y="Steps", title="Daily Steps Trend", markers=True)
    st.plotly_chart(fig, use_container_width=True)

if "Calories" in health_filtered:
    fig = px.area(health_filtered, x="Date", y="Calories", title="Daily Calories Burned")
    st.plotly_chart(fig, use_container_width=True)

if "Sleephours" in health_filtered:
    fig = px.histogram(health_filtered, x="Sleephours", nbins=15, title="Sleep Hours Distribution")
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------------
# FINANCE CHARTS (FIXED)
# -------------------------------------------------------
st.header("💵 Finance Analytics")

# 1. Income vs Expenses Bar Chart
finance_summary = finance_filtered.groupby("Category")["Amount"].sum().reset_index()

fig = px.bar(
    finance_summary,
    x="Category",
    y="Amount",
    title="Income vs Expenses",
    text_auto=True
)
st.plotly_chart(fig, use_container_width=True)

# 2. Monthly Trend
if "Month" in finance_filtered:
    monthly = finance_filtered.groupby(["Month", "Category"])["Amount"].sum().reset_index()
    fig = px.bar(
        monthly,
        x="Month",
        y="Amount",
        color="Category",
        barmode="group",
        title="Monthly Income & Expense Trend"
    )
    st.plotly_chart(fig, use_container_width=True)

# 3. Expense Share Pie Chart (Expense Only)
expense_only = finance_filtered[finance_filtered["Category"] == "Expense"]

if not expense_only.empty:
    fig = px.pie(
        expense_only,
        names="Notes",
        values="Amount",
        title="Expense Breakdown by Notes"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No expense data available for pie chart.")

# -------------------------------------------------------
# IMAGES FROM OUTPUT/
# -------------------------------------------------------
st.header("🖼️ Generated Images")

if os.path.exists("output/"):
    files = [f for f in os.listdir("output") if f.endswith(".png")]
    if files:
        for img in files:
            st.image(f"output/{img}", caption=img)
    else:
        st.info("No images found.")
else:
    st.error("Output folder missing!")

# -------------------------------------------------------
# RAW DATA VIEW
# -------------------------------------------------------
st.header("📄 Raw Data Preview")

with st.expander("Show Health Data"):
    st.dataframe(health_df)

with st.expander("Show Finance Data"):
    st.dataframe(finance_df)

st.success("Dashboard Loaded Successfully!")
