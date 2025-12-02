HF_AD — Health & Finance Analytics Dashboard
Project Overview

HF_AD is a comprehensive Health and Finance Analytics Dashboard developed using Python.
This project demonstrates end-to-end data analysis skills, dashboard creation, and ML-based prediction, making it suitable for Data Analyst, Data Engineering, and AI/ML roles.

Key objectives:

Explore, clean, and analyze health & finance datasets.

Visualize key metrics and trends using interactive charts.

Provide actionable insights via KPIs and predictions.

Allow report downloads for further use.

Features
Health Analytics

Daily Steps Trend

Sleep Hours Distribution

Heart Rate Trend

Predicted Steps for Next Day using Linear Regression

Finance Analytics

Income vs Expense Pie Chart

Expense Trend Over Time

Income Trend Over Time

Interactive Dashboard Features

Sidebar filters: select date ranges, categories

KPI cards: Total Steps, Avg Sleep, Avg Heart Rate, Total Income, Total Expense

Download filtered data as CSV reports

Fully interactive charts for insights

Tech Stack & Libraries

Languages: Python 3.10+

Data Analysis: pandas, numpy

Visualization: matplotlib, seaborn

Machine Learning: scikit-learn (Linear Regression)

Dashboard & UI: Streamlit

Optional DB/ETL: SQLite, PostgreSQL, Snowflake (future extension)

Folder Structure
HF_AD/
├── dashboard.py          # Streamlit dashboard
├── analysis.py           # Data cleaning & analysis
├── data/
│   ├── health_data.csv
│   └── finance_data.csv
├── venv/                 # Python virtual environment
├── requirements.txt
└── README.md

Installation & Setup

Clone the repository:

git clone https://github.com/<yourusername>/HF_AD.git
cd HF_AD


Create and activate virtual environment:

python -m venv venv
venv\Scripts\activate    # Windows
# source venv/bin/activate   # macOS/Linux


Install required libraries:

pip install -r requirements.txt


Run the dashboard:

streamlit run dashboard.py


The dashboard will open in your default browser at:

http://localhost:8502

Usage

Use sidebar filters to select specific date ranges and finance categories.

Explore KPIs and trends in health and finance.

Download CSV reports of filtered data.

View predicted steps for the next day to showcase ML capability.

Screenshots

(Add screenshots of your dashboard here for professional touch)

Skills Showcased

Data Cleaning & Analysis

Data Visualization & Reporting

Machine Learning (Prediction)

Dashboard Development (Streamlit)

Optional: SQL / ETL Integration

Future Enhancements

Deploy dashboard online (Streamlit Cloud, AWS, Heroku)

Include more advanced ML predictions (e.g., expense forecasting)

Integrate multiple datasets and build relational database dashboards

Add PDF / Excel export of charts and reports