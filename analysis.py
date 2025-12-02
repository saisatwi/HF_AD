"""
HF_AD Robust analysis.py
- Put this file at HF_AD/analysis.py
- Make sure your data files are in HF_AD/data/
  Prefer: data/health_data_cleaned.csv and data/finance_data_cleaned.csv
  Fallback: data/health_data.csv and data/finance_data.csv
- Activate venv and run: python analysis.py
"""

import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# create output folders
os.makedirs("output/charts", exist_ok=True)
os.makedirs("output/reports", exist_ok=True)

DATA_DIR = Path("data")
# fallback file names
HEALTH_FILES = [
    DATA_DIR / "health_data_cleaned.csv",
    DATA_DIR / "health_data.csv",
    Path("health_data_cleaned.csv"),
    Path("health_data.csv"),
]
FINANCE_FILES = [
    DATA_DIR / "finance_data_cleaned.csv",
    DATA_DIR / "finance_data.csv",
    Path("finance_data_cleaned.csv"),
    Path("finance_data.csv"),
]


def find_first_existing(paths):
    for p in paths:
        if p.exists():
            return p
    return None


health_path = find_first_existing(HEALTH_FILES)
finance_path = find_first_existing(FINANCE_FILES)

if health_path is None:
    print("ERROR: No health CSV found. Looked for:", [str(p) for p in HEALTH_FILES])
    sys.exit(1)

if finance_path is None:
    print("WARNING: No finance CSV found. Finance charts will be skipped.")
    finance_exists = False
else:
    finance_exists = True

print(f"Using health file: {health_path}")
if finance_exists:
    print(f"Using finance file: {finance_path}")

# helper to safely load CSV
def safe_read_csv(path):
    try:
        return pd.read_csv(path)
    except Exception as e:
        print(f"Failed to read {path}: {e}")
        return pd.DataFrame()


health_df = safe_read_csv(health_path)
finance_df = safe_read_csv(finance_path) if finance_exists else pd.DataFrame()

# -------------------------
# Normalize column names
# -------------------------
def normalize_cols(df):
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
        .str.replace(" ", "_")
        .str.replace("-", "_")
        .str.lower()
    )
    return df


health_df = normalize_cols(health_df)
finance_df = normalize_cols(finance_df)

# helper to get best column name from candidates
def choose_col(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None

# map expected columns (health)
steps_col = choose_col(health_df, ["steps", "step", "daily_steps"])
calories_col = choose_col(health_df, ["calories", "calorie"])
sleep_col = choose_col(health_df, ["sleephours", "sleep_hours", "sleep", "hours_slept"])
hr_col = choose_col(health_df, ["heartrate", "heart_rate", "hr"])

date_col_h = choose_col(health_df, ["date", "day", "datetime"])

# map expected columns (finance)
amount_col = choose_col(finance_df, ["amount", "amt", "value"])
category_col = choose_col(finance_df, ["category", "cat", "type"])
notes_col = choose_col(finance_df, ["notes", "note", "description"])
date_col_f = choose_col(finance_df, ["date", "datetime"])

# ensure date columns
if date_col_h:
    try:
        health_df[date_col_h] = pd.to_datetime(health_df[date_col_h])
    except Exception:
        health_df[date_col_h] = pd.to_datetime(health_df[date_col_h], errors="coerce")
        print("Warning: some health date rows could not be parsed and may be NaT.")
else:
    # create synthetic index date if missing
    health_df["date"] = pd.date_range("2025-01-01", periods=len(health_df))
    date_col_h = "date"
    print("Notice: health data had no date column. Created synthetic 'date' column.")

if finance_exists:
    if date_col_f:
        try:
            finance_df[date_col_f] = pd.to_datetime(finance_df[date_col_f])
        except Exception:
            finance_df[date_col_f] = pd.to_datetime(finance_df[date_col_f], errors="coerce")
            print("Warning: some finance date rows could not be parsed.")
    else:
        finance_df["date"] = pd.date_range("2025-01-01", periods=len(finance_df))
        date_col_f = "date"
        print("Notice: finance data had no date column. Created synthetic 'date' column.")

# convert numeric columns to numeric type safely
def to_numeric_if_exists(df, col):
    if col and col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        return True
    return False

to_numeric_if_exists(health_df, steps_col)
to_numeric_if_exists(health_df, calories_col)
to_numeric_if_exists(health_df, sleep_col)
to_numeric_if_exists(health_df, hr_col)

if finance_exists:
    to_numeric_if_exists(finance_df, amount_col)

# drop rows where steps is missing (for health analysis)
if steps_col:
    before = len(health_df)
    health_df = health_df.dropna(subset=[steps_col])
    after = len(health_df)
    if before != after:
        print(f"Dropped {before-after} health rows with missing steps.")

# Add derived columns
if date_col_h:
    health_df = health_df.sort_values(date_col_h)
    health_df["day_name"] = health_df[date_col_h].dt.day_name()

if finance_exists:
    finance_df = finance_df.sort_values(date_col_f)

# ---------- PLOTTING ----------
sns.set(style="whitegrid")
# helper to safe save figure
def save_fig(fig_name):
    out = Path("output/charts") / fig_name
    plt.tight_layout()
    plt.savefig(out)
    plt.close()

from pathlib import Path

print("\n--- Generating charts ---")

# Health charts
if steps_col:
    try:
        plt.figure(figsize=(10, 5))
        plt.plot(health_df[date_col_h], health_df[steps_col], marker="o")
        plt.title("Daily Steps Trend")
        plt.xlabel("Date")
        plt.ylabel("Steps")
        plt.xticks(rotation=45)
        save_fig("daily_steps_trend.png")
        print("Saved: output/charts/daily_steps_trend.png")
    except Exception as e:
        print("Could not plot steps trend:", e)
else:
    print("Skipping steps trend - 'steps' column not found.")

if sleep_col:
    try:
        plt.figure(figsize=(8, 5))
        sns.histplot(health_df[sleep_col].dropna(), bins=10, kde=True)
        plt.title("Sleep Hours Distribution")
        plt.xlabel("Sleep Hours")
        save_fig("sleep_distribution.png")
        print("Saved: output/charts/sleep_distribution.png")
    except Exception as e:
        print("Could not plot sleep distribution:", e)
else:
    print("Skipping sleep distribution - no suitable column found.")

# steps vs sleep scatter (only if both exist)
if steps_col and sleep_col:
    try:
        plt.figure(figsize=(8, 5))
        sns.scatterplot(x=health_df[sleep_col], y=health_df[steps_col])
        plt.title("Steps vs Sleep Hours")
        plt.xlabel("Sleep Hours")
        plt.ylabel("Steps")
        save_fig("daily_steps_vs_sleep.png")
        print("Saved: output/charts/daily_steps_vs_sleep.png")
    except Exception as e:
        print("Could not plot steps vs sleep:", e)

# correlation heatmap for numeric health columns
try:
    numeric_health = health_df.select_dtypes(include=[np.number])
    if not numeric_health.empty:
        plt.figure(figsize=(8, 6))
        sns.heatmap(numeric_health.corr(), annot=True, cmap="coolwarm")
        plt.title("Health Data Correlation Heatmap")
        save_fig("steps_correlation_heatmap.png")
        print("Saved: output/charts/steps_correlation_heatmap.png")
except Exception as e:
    print("Could not plot correlation heatmap:", e)

# Finance charts
if finance_exists and amount_col and category_col in finance_df.columns:
    try:
        monthly = (
            finance_df[finance_df[category_col].str.lower() == "expense"]
            .groupby(finance_df[date_col_f].dt.month)[amount_col]
            .sum()
        )
        if not monthly.empty:
            plt.figure(figsize=(8, 5))
            monthly.plot(kind="bar")
            plt.title("Monthly Expenses (sum)")
            plt.xlabel("Month")
            plt.ylabel("Amount")
            save_fig("expense_trend.png")
            print("Saved: output/charts/expense_trend.png")
    except Exception as e:
        print("Could not create finance expense trend:", e)
else:
    print("Skipping finance expense trend - finance data or required columns missing.")

# ---------- SIMPLE ML (optional, safe) ----------
print("\n--- Attempting ML prediction (if sklearn available and columns exist) ---")
ml_model_info = {"ran": False, "note": ""}

# we will try to use sklearn.LinearRegression if available
try:
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split
    SKLEARN_OK = True
except Exception:
    SKLEARN_OK = False

if SKLEARN_OK and steps_col:
    # choose features available: prefer sleep, hr, calories
    feature_cols = [c for c in [sleep_col, hr_col, calories_col] if c in health_df.columns]
    if feature_cols:
        X = health_df[feature_cols].fillna(health_df[feature_cols].mean())
        y = health_df[steps_col].fillna(health_df[steps_col].mean())
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            model = LinearRegression()
            model.fit(X_train, y_train)
            pred_next = None
            # create a sample next-day input using column means (you can change)
            sample = np.array(X.mean()).reshape(1, -1)
            pred_next = model.predict(sample)[0]
            # save report
            with open("output/reports/prediction_report.txt", "w") as f:
                f.write(f"ML model used features: {feature_cols}\n")
                f.write(f"Predicted next-day steps (sample input = feature means): {int(pred_next)}\n")
            ml_model_info["ran"] = True
            ml_model_info["note"] = f"Model predicted {int(pred_next)} using features {feature_cols}"
            print("ML prediction completed and saved to output/reports/prediction_report.txt")
            # plot predicted point on steps vs first feature if makes sense
            try:
                plt.figure(figsize=(8,5))
                sns.scatterplot(x=health_df[feature_cols[0]], y=health_df[steps_col], label="history")
                # plot sample point (first feature vs predicted)
                plt.scatter(sample[0,0], pred_next, color="red", s=100, label="predicted")
                plt.xlabel(feature_cols[0])
                plt.ylabel(steps_col)
                plt.title("Prediction (red) vs History")
                plt.legend()
                save_fig("predicted_steps_plot.png")
                print("Saved: output/charts/predicted_steps_plot.png")
            except Exception:
                pass
        except Exception as e:
            ml_model_info["note"] = f"ML failed: {e}"
            print("ML training/prediction failed:", e)
    else:
        ml_model_info["note"] = "No required features found for ML (need sleep/hr/calories)."
        print("Skipping ML: no usable feature columns found.")
else:
    print("scikit-learn not available or steps column missing — ML skipped.")
    ml_model_info["note"] = "sklearn not available or steps column missing."

print("\n--- Done ---")
print("ML info:", ml_model_info)
print("Charts: output/charts/")
print("Reports: output/reports/")
