import os
import pandas as pd
import numpy as np

# Create 'data' folder if it doesn't exist
os.makedirs('data', exist_ok=True)

# Health dataset
dates = pd.date_range(start='2025-12-01', periods=30)
health_df = pd.DataFrame({
    'Date': dates,
    'Steps': np.random.randint(3000, 12000, size=30),
    'Calories': np.random.randint(1500, 3000, size=30),
    'SleepHours': np.round(np.random.uniform(5, 9, size=30), 1),
    'HeartRate': np.random.randint(60, 100, size=30)
})
health_df.to_csv('data/health_data.csv', index=False)

# Finance dataset
categories = ['Income', 'Expense']
finance_df = pd.DataFrame({
    'Date': np.random.choice(dates, 50),
    'Category': np.random.choice(categories, 50, p=[0.3, 0.7]),
    'Amount': np.random.randint(50, 5000, size=50),
    'Notes': np.random.choice(['Salary', 'Groceries', 'Bills', 'Investments', 'Rent'], 50)
})
finance_df.to_csv('data/finance_data.csv', index=False)

print("Health and Finance CSVs saved in 'data/' folder!")
