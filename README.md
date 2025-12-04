# HF_AD — Health & Finance Analytics Dashboard

## Project Overview
HF_AD is a **comprehensive Health and Finance Analytics Dashboard** developed using Python.  
This project demonstrates **end-to-end data analysis, visualization, and ML-based prediction**, making it ideal for **Data Analyst, Data Engineering, and AI/ML roles**.

With this project, you can:
- Explore, clean, and analyze health and finance datasets.
- Visualize key metrics and trends using interactive charts.
- Provide actionable insights via KPIs and basic ML predictions.
- Download reports for further analysis.

---

## Live Dashboard
Access the fully interactive dashboard here:  
[**HF_AD Streamlit Dashboard**](https://hfad-wa5yumpcftkn2bdbnnfxov.streamlit.app)

---

## Features

### Health Analytics
- Daily Steps Trend
- Sleep Hours Distribution
- Heart Rate Trend
- Predicted Steps for Next Day (Linear Regression)

### Finance Analytics
- Income vs Expense Pie Chart
- Expense Trend Over Time
- Income Trend Over Time

### Interactive Dashboard
- Sidebar filters: select date ranges, categories
- KPI cards: Total Steps, Avg Sleep, Avg Heart Rate, Total Income, Total Expense
- Download filtered data as CSV reports
- Light/Dark theme toggle
- Fully interactive charts for insights

---

## Tech Stack & Libraries
- **Languages:** Python 3.10+  
- **Data Analysis:** pandas, numpy  
- **Visualization:** matplotlib, seaborn, plotly  
- **Machine Learning:** scikit-learn (Linear Regression)  
- **Dashboard & UI:** Streamlit  
- **Optional DB/ETL:** SQLite, PostgreSQL, Snowflake  

---

## Folder Structure
HF_AD/
├── app.py # Streamlit dashboard (updated version)
├── dashboard.py # Optional older version
├── analysis.py # Data cleaning & analysis scripts
├── data/
│ ├── health_data_cleaned.csv
│ └── finance_data_cleaned.csv
├── output/ # Optional images & charts saved
├── venv/ # Python virtual environment
├── requirements.txt
└── README.md


---

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/saisatwi/HF_AD.git
cd HF_AD

2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate    # Windows
# source venv/bin/activate   # macOS/Linux

3. Install dependencies
pip install -r requirements.txt

4. Run the dashboard locally
streamlit run app.py

The dashboard will open in your browser at: http://localhost:8501

Usage

Use sidebar filters to select date ranges and finance categories.

Explore KPIs, charts, and trends for health and finance.

Download CSV reports of filtered data.

Toggle Light/Dark theme for better visualization.

View predicted steps for next day using ML model.

Skills Showcased

Data Cleaning & Analysis (pandas, numpy)

Data Visualization & Reporting (matplotlib, seaborn, plotly)

Machine Learning Prediction (Linear Regression with scikit-learn)

Interactive Dashboard Development (Streamlit)

Optional: SQL/ETL Integration


GitHub: https://github.com/saisatwi/HF_AD
Streamlit Dashboard: https://hfad-wa5yumpcftkn2bdbnnfxov.streamlit.app
