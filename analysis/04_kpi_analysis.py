import pandas as pd
from pathlib import Path

# ==============================
# 1. LOAD CLEANED DATA
# ==============================

file_path = Path("eda_outputs/cleaned_data.csv")

df = pd.read_csv(file_path)

df["Order Date"] = pd.to_datetime(df["Order Date"])


# ==============================
# 2. PRODUCT-LEVEL AGGREGATION
# ==============================

product_summary = (
    df.groupby(["Product ID", "Product Name"], as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Units=("Units", "sum"),
        Gross_Profit=("Gross Profit", "sum"),
        Cost=("Cost", "sum")
    )
)

# Required KPIs
product_summary["Gross Margin %"] = (
    product_summary["Gross_Profit"]
    / product_summary["Sales"]
) * 100

product_summary["Profit per Unit"] = (
    product_summary["Gross_Profit"]
    / product_summary["Units"]
)

total_sales = product_summary["Sales"].sum()
total_profit = product_summary["Gross_Profit"].sum()

product_summary["Revenue Contribution %"] = (
    product_summary["Sales"] / total_sales
) * 100

product_summary["Profit Contribution %"] = (
    product_summary["Gross_Profit"] / total_profit
) * 100


# ==============================
# 3. PRODUCT PROFITABILITY
# ==============================

print("\n===== TOP 10 PRODUCTS BY GROSS PROFIT =====")

print(
    product_summary
    .sort_values("Gross_Profit", ascending=False)
    [["Product Name", "Sales", "Gross_Profit",
      "Gross Margin %", "Profit per Unit"]]
    .head(10)
    .to_string(index=False)
)


print("\n===== TOP 10 PRODUCTS BY GROSS MARGIN =====")

print(
    product_summary
    .sort_values("Gross Margin %", ascending=False)
    [["Product Name", "Sales", "Gross_Profit",
      "Gross Margin %", "Profit per Unit"]]
    .head(10)
    .to_string(index=False)
)


print("\n===== TOP 10 PRODUCTS BY PROFIT PER UNIT =====")

print(
    product_summary
    .sort_values("Profit per Unit", ascending=False)
    [["Product Name", "Sales", "Gross_Profit",
      "Gross Margin %", "Profit per Unit"]]
    .head(10)
    .to_string(index=False)
)


# ==============================
# 4. DIVISION ANALYSIS
# ==============================

division_summary = (
    df.groupby("Division", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Units=("Units", "sum"),
        Gross_Profit=("Gross Profit", "sum"),
        Cost=("Cost", "sum")
    )
)

division_summary["Gross Margin %"] = (
    division_summary["Gross_Profit"]
    / division_summary["Sales"]
) * 100

division_summary["Profit per Unit"] = (
    division_summary["Gross_Profit"]
    / division_summary["Units"]
)

division_summary["Revenue Contribution %"] = (
    division_summary["Sales"] / division_summary["Sales"].sum()
) * 100

division_summary["Profit Contribution %"] = (
    division_summary["Gross_Profit"]
    / division_summary["Gross_Profit"].sum()
) * 100


print("\n===== DIVISION PERFORMANCE =====")

print(
    division_summary.to_string(index=False)
)


# ==============================
# 5. MARGIN VOLATILITY
# ==============================

monthly_margin = (
    df.groupby(
        [df["Order Date"].dt.to_period("M"), "Division"]
    )
    .agg(
        Sales=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum")
    )
    .reset_index()
)

monthly_margin["Gross Margin %"] = (
    monthly_margin["Gross_Profit"]
    / monthly_margin["Sales"]
) * 100

margin_volatility = (
    monthly_margin
    .groupby("Division")["Gross Margin %"]
    .agg(["mean", "std", "min", "max"])
    .reset_index()
)

margin_volatility.columns = [
    "Division",
    "Average Margin %",
    "Margin Volatility",
    "Minimum Margin %",
    "Maximum Margin %"
]

print("\n===== MARGIN VOLATILITY BY DIVISION =====")

print(
    margin_volatility.to_string(index=False)
)


# ==============================
# 6. SAVE KPI OUTPUTS
# ==============================

output_folder = Path("eda_outputs")
output_folder.mkdir(exist_ok=True)

product_summary.to_csv(
    output_folder / "product_profitability_summary.csv",
    index=False
)

division_summary.to_csv(
    output_folder / "division_performance_summary.csv",
    index=False
)

margin_volatility.to_csv(
    output_folder / "margin_volatility_summary.csv",
    index=False
)


print("\n===== FILES SAVED =====")
print("product_profitability_summary.csv")
print("division_performance_summary.csv")
print("margin_volatility_summary.csv")