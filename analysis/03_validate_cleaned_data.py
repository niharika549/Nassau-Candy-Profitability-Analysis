import pandas as pd

# Load cleaned dataset
file_path = "eda_outputs/cleaned_data.csv"

df = pd.read_csv(file_path)

print("===== CLEANED DATASET VALIDATION =====")

print("\nDataset shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nSales range:")
print(df["Sales"].min(), "to", df["Sales"].max())

print("\nGross Profit range:")
print(df["Gross Profit"].min(), "to", df["Gross Profit"].max())

print("\nCost range:")
print(df["Cost"].min(), "to", df["Cost"].max())

print("\nUnits range:")
print(df["Units"].min(), "to", df["Units"].max())

print("\nGross Margin % summary:")
print(df["Gross Margin %"].describe())

print("\nProfit per Unit summary:")
print(df["Profit per Unit"].describe())

print("\nDivisions:")
print(df["Division"].value_counts())

print("\nDate range:")
print(df["Order Date"].min(), "to", df["Order Date"].max())