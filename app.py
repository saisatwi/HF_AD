import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# Load Data
# ----------------------------
health_df = pd.read_csv("data/health_data_cleaned.csv")
finance_df = pd.read_csv("data/finance_data_cleaned.csv")

# Convert 'Date' columns to datetime
health_df['Date'] = pd.to_datetime(health_df['Date'])
finance_df['Date'] = pd.to_datetime(finance_df['Date'])

# ----------------------------
# Sidebar Theme Toggle
# ----------------------------
theme_option = st.sidebar.radio("Select Theme", ("Light", "Dark"))

if theme_option == "Light":
    bg_color = "#f0f2f6"
    text_color = "#262730"
    secondary_bg = "#e6e6e6"
    plotly_template = "plotly_white"
else:
    bg_color = "#262730"
    text_color = "#f0f2f6"
    secondary_bg = "#333333"
    plotly_template = "plotly_dark"

st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: {bg_color};
            color: {text_color};
        }}
        .css-1d391kg {{
            background-color: {secondary_bg};
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.header("Filters")

# Health filters
health_start_date = st.sidebar.date_input("Health: Start Date", health_df['Date'].min())
health_end_date = st.sidebar.date_input("Health: End Date", health_df['Date'].max())
health_filtered = health_df[(health_df['Date'] >= pd.to_datetime(health_start_date)) &
                            (health_df['Date'] <= pd.to_datetime(health_end_date))]

# Finance filters
finance_category = st.sidebar.multiselect("Finance: Select Category", finance_df['Category'].unique(), default=finance_df['Category'].unique())
finance_filtered = finance_df[finance_df['Category'].isin(finance_category)]

# ----------------------------
# KPIs
# ----------------------------
st.title("Health & Finance Analytics Dashboard")

# Health KPIs
st.subheader("Health Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Steps", f"{health_filtered['Steps'].sum():,}")
col2.metric("Avg Sleep (hrs)", f"{health_filtered['Sleephours'].mean():.1f}")
col3.metric("Avg Heart Rate", f"{health_filtered['Heartrate'].mean():.0f}")

# Finance KPIs
st.subheader("Finance Metrics")
col4, col5 = st.columns(2)
col4.metric("Total Income", f"₹{finance_filtered[finance_filtered['Category']=='Income']['Amount'].sum():,}")
col5.metric("Total Expense", f"₹{finance_filtered[finance_filtered['Category']=='Expense']['Amount'].sum():,}")

# ----------------------------
# Health Charts
# ----------------------------
st.subheader("Health Analytics")

# Steps Trend
fig_steps = px.line(health_filtered, x="Date", y="Steps", template=plotly_template, title="Daily Steps Trend")
st.plotly_chart(fig_steps, use_container_width=True)

# Sleep Hours Distribution
fig_sleep = px.histogram(health_filtered, x="Sleephours", nbins=10, template=plotly_template, title="Sleep Hours Distribution")
st.plotly_chart(fig_sleep, use_container_width=True)

# Heart Rate Trend
fig_hr = px.line(health_filtered, x="Date", y="Heartrate", template=plotly_template, title="Heart Rate Trend")
st.plotly_chart(fig_hr, use_container_width=True)

# ----------------------------
# Finance Charts
# ----------------------------
st.subheader("Finance Analytics")

# Income vs Expense Pie
finance_summary = finance_filtered.groupby("Category")['Amount'].sum().reset_index()
fig_pie = px.pie(finance_summary, names="Category", values="Amount", template=plotly_template, title="Income vs Expense Share")
st.plotly_chart(fig_pie, use_container_width=True)

# Expense Trend
expense_df = finance_filtered[finance_filtered['Category']=="Expense"]
fig_expense = px.bar(expense_df, x="Date", y="Amount", template=plotly_template, title="Expense Trend Over Time")
st.plotly_chart(fig_expense, use_container_width=True)

# Income Trend
income_df = finance_filtered[finance_filtered['Category']=="Income"]
fig_income = px.bar(income_df, x="Date", y="Amount", template=plotly_template, title="Income Trend Over Time")
st.plotly_chart(fig_income, use_container_width=True)

# ----------------------------
# Download filtered data
# ----------------------------
st.subheader("Download Data")
st.download_button("Download Health Data", health_filtered.to_csv(index=False).encode('utf-8'), "health_data_filtered.csv", "text/csv")
st.download_button("Download Finance Data", finance_filtered.to_csv(index=False).encode('utf-8'), "finance_data_filtered.csv", "text/csv")
