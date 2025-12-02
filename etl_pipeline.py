import os
import pandas as pd
from sqlalchemy import create_engine

# ----------------------------
# Step 0: Ensure 'data' folder exists
# ----------------------------
os.makedirs('data', exist_ok=True)

# ----------------------------
# Step 1: Load CSVs
# ----------------------------
health_df = pd.read_csv('data/health_data.csv')
finance_df = pd.read_csv('data/finance_data.csv')

# ----------------------------
# Step 2: Inspect Data
# ----------------------------
print("Health data preview:")
print(health_df.head())

print("\nFinance data preview:")
print(finance_df.head())

# ----------------------------
# Step 3: Clean Health Data
# ----------------------------
# Remove missing values
health_df.dropna(inplace=True)

# Remove duplicates
health_df.drop_duplicates(inplace=True)

# Normalize column names
health_df.columns = [col.strip().title() for col in health_df.columns]

# Add additional features
health_df['Day'] = pd.to_datetime(health_df['Date']).dt.day_name()

# ----------------------------
# Step 4: Clean Finance Data
# ----------------------------
finance_df.dropna(inplace=True)
finance_df.drop_duplicates(inplace=True)
finance_df['Category'] = finance_df['Category'].str.capitalize()
finance_df['Month'] = pd.to_datetime(finance_df['Date']).dt.month

# ----------------------------
# Step 5: Save Cleaned Data
# ----------------------------
health_df.to_csv('data/health_data_cleaned.csv', index=False)
finance_df.to_csv('data/finance_data_cleaned.csv', index=False)
print("\nCleaned CSVs saved in 'data/' folder!")

# ----------------------------
# Step 6: Load Data into SQL
# ----------------------------
# Using SQLite for simplicity; replace with Snowflake connection if needed
engine = create_engine('sqlite:///data/analytics.db')

health_df.to_sql('health_data', engine, if_exists='replace', index=False)
finance_df.to_sql('finance_data', engine, if_exists='replace', index=False)

print("\nData loaded into SQLite database 'analytics.db' successfully!")
