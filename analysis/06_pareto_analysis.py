import pandas as pd
from pathlib import Path

# Load product profitability data
file_path = "eda_outputs/product_profitability_summary.csv"
df = pd.read_csv(file_path)

# Sort by Sales
revenue_df = df.sort_values("Sales", ascending=False).reset_index(drop=True)

revenue_df["Cumulative Revenue %"] = (
    revenue_df["Sales"].cumsum() /
    revenue_df["Sales"].sum()
) * 100

# Sort by Gross Profit
profit_df = df.sort_values("Gross_Profit", ascending=False).reset_index(drop=True)

profit_df["Cumulative Profit %"] = (
    profit_df["Gross_Profit"].cumsum() /
    profit_df["Gross_Profit"].sum()
) * 100

# Products required to generate 80% revenue
revenue_80_count = (
    revenue_df["Cumulative Revenue %"] <= 80
).sum() + 1

# Products required to generate 80% profit
profit_80_count = (
    profit_df["Cumulative Profit %"] <= 80
).sum() + 1

total_products = len(df)

revenue_80_percentage = (revenue_80_count / total_products) * 100
profit_80_percentage = (profit_80_count / total_products) * 100

print("\n===== PROFIT CONCENTRATION ANALYSIS =====")

print("Total products:", total_products)

print("\nProducts contributing approximately 80% of revenue:")
print(revenue_80_count)

print("Percentage of products:", round(revenue_80_percentage, 2), "%")

print("\nProducts contributing approximately 80% of profit:")
print(profit_80_count)

print("Percentage of products:", round(profit_80_percentage, 2), "%")


# Top 20 products
print("\n===== TOP 20 PRODUCTS BY GROSS PROFIT =====")

print(
    profit_df[
        [
            "Product Name",
            "Sales",
            "Gross_Profit",
            "Gross Margin %",
            "Profit Contribution %"
        ]
    ]
    .head(20)
    .to_string(index=False)
)


# Save Pareto data
output_folder = Path("eda_outputs")
output_folder.mkdir(exist_ok=True)

revenue_df.to_csv(
    output_folder / "revenue_pareto_analysis.csv",
    index=False
)

profit_df.to_csv(
    output_folder / "profit_pareto_analysis.csv",
    index=False
)

print("\n===== FILES SAVED =====")
print("revenue_pareto_analysis.csv")
print("profit_pareto_analysis.csv")