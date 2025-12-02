import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from io import BytesIO

st.set_page_config(
    page_title="HF_AD Health & Finance Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# LOAD DATA
# -----------------------------
health = pd.read_csv("data/health_data.csv")
finance = pd.read_csv("data/finance_data.csv")

health['Date'] = pd.to_datetime(health['Date'])
finance['Date'] = pd.to_datetime(finance['Date'])

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")

# Health filters
st.sidebar.subheader("Health Filters")
selected_health_dates = st.sidebar.date_input(
    "Select Health Date Range:",
    [health['Date'].min(), health['Date'].max()]
)

# Finance filters
st.sidebar.subheader("Finance Filters")
selected_category = st.sidebar.multiselect(
    "Select Finance Categories:",
    options=finance['Category'].unique(),
    default=finance['Category'].unique()
)

# Apply filters
health_filtered = health[
    (health['Date'] >= pd.to_datetime(selected_health_dates[0])) &
    (health['Date'] <= pd.to_datetime(selected_health_dates[1]))
]

finance_filtered = finance[finance['Category'].isin(selected_category)]

# -----------------------------
# DASHBOARD TITLE
# -----------------------------
st.title("📊 HF_AD Health & Finance Interactive Dashboard")

# -----------------------------
# KPI CARDS
# -----------------------------
st.header("🏆 Key Metrics")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Steps", int(health_filtered['Steps'].sum()))
with col2:
    st.metric("Average Sleep Hours", round(health_filtered['SleepHours'].mean(), 2))
with col3:
    st.metric("Average Heart Rate", round(health_filtered['HeartRate'].mean(), 1))

col4, col5 = st.columns(2)
with col4:
    total_income = finance_filtered[finance_filtered['Category']=='Income']['Amount'].sum()
    st.metric("Total Income", f"${total_income}")
with col5:
    total_expense = finance_filtered[finance_filtered['Category']=='Expense']['Amount'].sum()
    st.metric("Total Expense", f"${total_expense}")

# -----------------------------
# HEALTH ANALYTICS
# -----------------------------
st.header("🏥 Health Insights")

# Steps Trend
st.subheader("Daily Steps Trend")
fig1, ax1 = plt.subplots()
ax1.plot(health_filtered['Date'], health_filtered['Steps'], marker='o', color='green')
ax1.set_xlabel("Date")
ax1.set_ylabel("Steps")
plt.xticks(rotation=45)
st.pyplot(fig1)

# Sleep Distribution
st.subheader("Sleep Hours Distribution")
fig2, ax2 = plt.subplots()
sns.histplot(health_filtered['SleepHours'], bins=10, kde=True, ax=ax2)
ax2.set_xlabel("Sleep Hours")
ax2.set_ylabel("Frequency")
st.pyplot(fig2)

# Heart Rate Trend
st.subheader("Heart Rate Trend")
fig3, ax3 = plt.subplots()
ax3.plot(health_filtered['Date'], health_filtered['HeartRate'], marker='o', color='red')
ax3.set_xlabel("Date")
ax3.set_ylabel("Heart Rate")
plt.xticks(rotation=45)
st.pyplot(fig3)

# -----------------------------
# ML Prediction for Steps
# -----------------------------
st.subheader("📈 Steps Prediction (Next Day)")

try:
    X = np.arange(len(health_filtered)).reshape(-1, 1)
    y = health_filtered['Steps'].values
    model = LinearRegression()
    model.fit(X, y)
    next_day_index = np.array([[len(X)]])
    predicted_steps = int(model.predict(next_day_index)[0])
    st.success(f"Predicted Steps for next day: {predicted_steps}")
except:
    st.warning("Not enough data for prediction")

# -----------------------------
# FINANCE ANALYTICS
# -----------------------------
st.header("💰 Finance Insights")

# Income vs Expense Pie
st.subheader("Income vs Expense Share")
fig4, ax4 = plt.subplots()
finance_filtered.groupby("Category")["Amount"].sum().plot(
    kind="pie",
    autopct="%1.1f%%",
    ax=ax4
)
ax4.set_ylabel("")
st.pyplot(fig4)

# Expense Trend
st.subheader("Expense Trend Over Time")
expenses = finance_filtered[finance_filtered["Category"] == "Expense"]
fig5, ax5 = plt.subplots()
ax5.plot(expenses["Date"], expenses["Amount"], marker='o', color='orange')
ax5.set_xlabel("Date")
ax5.set_ylabel("Expense Amount")
plt.xticks(rotation=45)
st.pyplot(fig5)

# Income Trend
st.subheader("Income Trend Over Time")
income = finance_filtered[finance_filtered["Category"] == "Income"]
fig6, ax6 = plt.subplots()
ax6.plot(income["Date"], income["Amount"], marker='o', color='blue')
ax6.set_xlabel("Date")
ax6.set_ylabel("Income Amount")
plt.xticks(rotation=45)
st.pyplot(fig6)

# -----------------------------
# DOWNLOAD BUTTONS
# -----------------------------
st.header("💾 Download Reports")

def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download Health Data CSV",
    data=convert_df(health_filtered),
    file_name='health_filtered.csv',
    mime='text/csv'
)

st.download_button(
    label="Download Finance Data CSV",
    data=convert_df(finance_filtered),
    file_name='finance_filtered.csv',
    mime='text/csv'
)

st.success("Dashboard Loaded Successfully!")
