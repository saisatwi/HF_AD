HF_AD — Health & Finance Analytics Dashboard
Project Overview

HF_AD is a comprehensive Health and Finance Analytics Dashboard developed using Python. This project demonstrates end-to-end data analysis skills, interactive dashboard creation, and ML-based prediction, making it suitable for Data Analyst, Data Engineering, and AI/ML roles.

Key Objectives

Explore, clean, and analyze health & finance datasets.

Visualize key metrics and trends using interactive charts.

Provide actionable insights via KPIs and predictions.

Enable report downloads for further use.

Features
Health Analytics

Daily Steps Trend

Sleep Hours Trend & Distribution

Heart Rate Trend

Predicted Steps for Next Day using Linear Regression

Finance Analytics

Income vs Expense Pie Chart

Expense Trend Over Time

Income Trend Over Time

Interactive Dashboard Features

Sidebar filters: select date ranges and finance categories.

KPI cards: Total Steps, Avg Sleep, Avg Heart Rate, Total Income, Total Expense.

Download filtered data as CSV reports.

Fully interactive charts for insights.

Light/Dark theme toggle for user-friendly visualization.

Tech Stack & Libraries

Languages: Python 3.10+

Data Analysis: pandas, numpy

Visualization: plotly, seaborn

Machine Learning: scikit-learn (Linear Regression)

Dashboard & UI: Streamlit

Optional DB/ETL: SQLite, PostgreSQL, Snowflake (future extension)

Folder Structure
HF_AD/
├── app.py                   # Streamlit dashboard
├── analysis.py              # Data cleaning & analysis
├── data/
│   ├── health_data_cleaned.csv
│   └── finance_data_cleaned.csv
├── venv/                    # Python virtual environment
├── requirements.txt
└── README.md

Installation & Setup
1. Clone the repository
git clone https://github.com/saisatwi/HF_AD.git
cd HF_AD

2. Create and activate virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
# source venv/bin/activate

3. Install required libraries
pip install -r requirements.txt

4. Run the Streamlit dashboard
streamlit run app.py


The dashboard will open in your default browser at:
http://localhost:8501

Usage

Use sidebar filters to select date ranges and finance categories.

Explore KPIs and trends in health and finance.

Download CSV reports of filtered data.

View predicted steps for the next day to showcase ML capability.

Switch between Light/Dark mode for better visualization.

Screenshots

(Add screenshots of your dashboard here for professional presentation)

Skills Showcased

Data Cleaning & Analysis

Data Visualization & Reporting

Machine Learning (Prediction)

Dashboard Development (Streamlit)

Optional: SQL / ETL Integration

Future Enhancements

Deploy dashboard online (Streamlit Cloud, AWS, Heroku).

Include more advanced ML predictions (e.g., expense forecasting).

Integrate multiple datasets and build relational database dashboards.

Add PDF / Excel export of charts and reports.
