import pandas as pd
from pathlib import Path

# Load product-level KPI data
file_path = "eda_outputs/product_profitability_summary.csv"
df = pd.read_csv(file_path)

# Median thresholds
sales_median = df["Sales"].median()
profit_median = df["Gross_Profit"].median()
margin_median = df["Gross Margin %"].median()

# Product categories
df["Product Category"] = "Other"

df.loc[
    (df["Gross_Profit"] >= profit_median) &
    (df["Gross Margin %"] >= margin_median),
    "Product Category"
] = "High Profit / High Margin"

df.loc[
    (df["Sales"] >= sales_median) &
    (df["Gross Margin %"] < margin_median),
    "Product Category"
] = "High Sales / Low Margin"

df.loc[
    (df["Sales"] < sales_median) &
    (df["Gross_Profit"] < profit_median),
    "Product Category"
] = "Low Sales / Low Profit"

# Margin risk
df["Margin Risk"] = "Normal"

df.loc[
    df["Gross Margin %"] < df["Gross Margin %"].quantile(0.25),
    "Margin Risk"
] = "High Risk"

# Display results
print("\n===== HIGH PROFIT / HIGH MARGIN =====")
print(
    df[df["Product Category"] == "High Profit / High Margin"]
    .sort_values("Gross_Profit", ascending=False)
    [["Product Name", "Sales", "Gross_Profit",
      "Gross Margin %", "Profit per Unit"]]
    .head(15)
    .to_string(index=False)
)

print("\n===== HIGH SALES / LOW MARGIN =====")
print(
    df[df["Product Category"] == "High Sales / Low Margin"]
    .sort_values("Sales", ascending=False)
    [["Product Name", "Sales", "Gross_Profit",
      "Gross Margin %", "Profit per Unit"]]
    .head(15)
    .to_string(index=False)
)

print("\n===== LOW SALES / LOW PROFIT =====")
print(
    df[df["Product Category"] == "Low Sales / Low Profit"]
    .sort_values("Gross_Profit")
    [["Product Name", "Sales", "Gross_Profit",
      "Gross Margin %", "Profit per Unit"]]
    .head(15)
    .to_string(index=False)
)

print("\n===== MARGIN RISK PRODUCTS =====")
print(
    df[df["Margin Risk"] == "High Risk"]
    .sort_values("Gross Margin %")
    [["Product Name", "Sales", "Gross_Profit",
      "Gross Margin %", "Profit per Unit"]]
    .head(15)
    .to_string(index=False)
)

# Save
output_file = Path("eda_outputs/product_risk_analysis.csv")
df.to_csv(output_file, index=False)

print("\nSaved:")
print(output_file)