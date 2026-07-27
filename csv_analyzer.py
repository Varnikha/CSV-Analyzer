"""
Simple CSV Data Analyzer
-------------------------
This script loads a CSV file and shows:
1. Basic info (rows, columns, column names, data types)
2. Summary statistics (average, min, max, etc. for number columns)
"""

import pandas as pd

# ---- Step A: Load the CSV file ----
# Change 'data.csv' to the path of your own CSV file
file_path = "data.csv"
df = pd.read_csv(file_path)

# ---- Step B: Basic info ----
print("=" * 50)
print("BASIC INFO")
print("=" * 50)

print(f"Number of rows: {df.shape[0]}")
print(f"Number of columns: {df.shape[1]}")
print(f"Column names: {list(df.columns)}")
print("\nData types of each column:")
print(df.dtypes)

print("\nFirst 5 rows of the data:")
print(df.head())

# ---- Step C: Summary statistics ----
print("\n" + "=" * 50)
print("SUMMARY STATISTICS (numeric columns)")
print("=" * 50)

# .describe() automatically calculates count, mean, min, max, std, etc.
print(df.describe())

# ---- Step D: Check for missing values (bonus, good to know) ----
print("\n" + "=" * 50)
print("MISSING VALUES PER COLUMN")
print("=" * 50)
print(df.isnull().sum())