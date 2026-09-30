import pandas as pd
from pathlib import Path

# Load cleaned data
df = pd.read_csv("eda_outputs/cleaned_data.csv")

# Product-level analysis
product = (
    df.groupby(["Product ID", "Product Name"], as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Cost=("Cost", "sum"),
        Gross_Profit=("Gross Profit", "sum"),
        Units=("Units", "sum")
    )
)

# KPIs
product["Gross Margin %"] = (
    product["Gross_Profit"] / product["Sales"]
) * 100

product["Cost % of Sales"] = (
    product["Cost"] / product["Sales"]
) * 100

product["Profit per Unit"] = (
    product["Gross_Profit"] / product["Units"]
)

# Risk thresholds
margin_threshold = product["Gross Margin %"].quantile(0.25)
cost_threshold = product["Cost % of Sales"].quantile(0.75)

product["Risk Flag"] = "Normal"

product.loc[
    (product["Gross Margin %"] <= margin_threshold) &
    (product["Cost % of Sales"] >= cost_threshold),
    "Risk Flag"
] = "High Cost / Low Margin"

product.loc[
    (product["Gross Margin %"] <= margin_threshold) &
    (product["Cost % of Sales"] < cost_threshold),
    "Risk Flag"
] = "Low Margin"

product.loc[
    (product["Gross Margin %"] > margin_threshold) &
    (product["Cost % of Sales"] >= cost_threshold),
    "Risk Flag"
] = "Cost Heavy"

# Display
print("\n===== COST VS MARGIN DIAGNOSTICS =====")

print("Margin risk threshold:",
      round(margin_threshold, 2), "%")

print("Cost threshold:",
      round(cost_threshold, 2), "%")

print("\n===== HIGH COST / LOW MARGIN PRODUCTS =====")

print(
    product[product["Risk Flag"] == "High Cost / Low Margin"]
    .sort_values("Gross Margin %")
    [["Product Name", "Sales", "Cost",
      "Gross_Profit", "Gross Margin %",
      "Cost % of Sales", "Profit per Unit"]]
    .head(20)
    .to_string(index=False)
)

print("\n===== LOW MARGIN PRODUCTS =====")

print(
    product[product["Risk Flag"] == "Low Margin"]
    .sort_values("Gross Margin %")
    [["Product Name", "Sales", "Cost",
      "Gross_Profit", "Gross Margin %",
      "Cost % of Sales"]]
    .head(20)
    .to_string(index=False)
)

print("\n===== COST HEAVY PRODUCTS =====")

print(
    product[product["Risk Flag"] == "Cost Heavy"]
    .sort_values("Cost % of Sales", ascending=False)
    [["Product Name", "Sales", "Cost",
      "Gross_Profit", "Gross Margin %",
      "Cost % of Sales"]]
    .head(20)
    .to_string(index=False)
)

# Save
output_file = Path(
    "eda_outputs/cost_margin_diagnostics.csv"
)

product.to_csv(output_file, index=False)

print("\nSaved:")
print(output_file)