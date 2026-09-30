import pandas as pd
from pathlib import Path

# ==============================
# 1. LOAD ORIGINAL DATA
# ==============================

input_file = Path("data/Nassau Candy Distributor.csv")

df = pd.read_csv(input_file)

print("Original dataset shape:", df.shape)


# ==============================
# 2. CLEAN COLUMN NAMES
# ==============================

df.columns = df.columns.str.strip()


# ==============================
# 3. CONVERT DATE COLUMNS
# ==============================

df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")


# ==============================
# 4. CONVERT NUMERIC COLUMNS
# ==============================

numeric_columns = [
    "Sales",
    "Units",
    "Gross Profit",
    "Cost"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")


# ==============================
# 5. REMOVE INVALID RECORDS
# ==============================

before_cleaning = len(df)

df = df.dropna(
    subset=[
        "Order Date",
        "Ship Date",
        "Sales",
        "Units",
        "Gross Profit",
        "Cost"
    ]
)

# Remove zero or negative sales
df = df[df["Sales"] > 0]

# Remove zero or negative units
df = df[df["Units"] > 0]


# ==============================
# 6. CREATE REQUIRED METRICS
# ==============================

df["Gross Margin %"] = (
    df["Gross Profit"] / df["Sales"]
) * 100

df["Profit per Unit"] = (
    df["Gross Profit"] / df["Units"]
)


# ==============================
# 7. CREATE TIME FEATURES
# ==============================

df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.month
df["Month Name"] = df["Order Date"].dt.strftime("%B")


# ==============================
# 8. CHECK FOR INVALID MARGINS
# ==============================

invalid_margin = df[
    (df["Gross Margin %"] < 0)
]

print("Negative-margin records:", len(invalid_margin))


# ==============================
# 9. SAVE CLEANED DATA
# ==============================

output_folder = Path("eda_outputs")
output_folder.mkdir(exist_ok=True)

output_file = output_folder / "cleaned_data.csv"

df.to_csv(output_file, index=False)


# ==============================
# 10. CLEANING SUMMARY
# ==============================

print("\n===== CLEANING SUMMARY =====")

print("Original rows:", before_cleaning)
print("Final rows:", len(df))
print("Rows removed:", before_cleaning - len(df))

print("\nFinal columns:")
print(df.columns.tolist())

print("\nMissing values after cleaning:")
print(df.isnull().sum())

print("\nCleaned dataset shape:")
print(df.shape)

print("\nCleaned data saved to:")
print(output_file)