import pandas as pd

print("\nHealth Data Columns:")
df1 = pd.read_csv("data/health_data_cleaned.csv")
print(df1.columns.tolist())

print("\nFinance Data Columns:")
df2 = pd.read_csv("data/finance_data_cleaned.csv")
print(df2.columns.tolist())
