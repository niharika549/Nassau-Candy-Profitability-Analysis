
import matplotlib
matplotlib.use("Agg")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


# ==================================================
# 1. LOAD DATA
# ==================================================

df = pd.read_csv("eda_outputs/cleaned_data.csv")


# ==================================================
# 2. CREATE OUTPUT FOLDER
# ==================================================

output_folder = Path("eda_outputs/charts")
output_folder.mkdir(parents=True, exist_ok=True)


# ==================================================
# 3. PRODUCT SUMMARY
# ==================================================

product = (
    df.groupby(["Product ID", "Product Name"], as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Cost=("Cost", "sum"),
        Gross_Profit=("Gross Profit", "sum"),
        Units=("Units", "sum")
    )
)

product["Gross Margin %"] = (
    product["Gross_Profit"] / product["Sales"]
) * 100


# ==================================================
# CHART 1 — TOP 10 PRODUCTS BY PROFIT
# ==================================================

top_profit = product.nlargest(10, "Gross_Profit")

plt.figure(figsize=(10, 6))

plt.barh(
    top_profit["Product Name"],
    top_profit["Gross_Profit"]
)

plt.xlabel("Gross Profit")
plt.ylabel("Product")
plt.title("Top 10 Products by Gross Profit")

plt.gca().invert_yaxis()

plt.tight_layout()

plt.savefig(
    output_folder / "top_10_profit.png"
)

plt.close()


# ==================================================
# CHART 2 — TOP 10 PRODUCTS BY GROSS MARGIN
# ==================================================

top_margin = product.nlargest(10, "Gross Margin %")

plt.figure(figsize=(10, 6))

plt.barh(
    top_margin["Product Name"],
    top_margin["Gross Margin %"]
)

plt.xlabel("Gross Margin (%)")
plt.ylabel("Product")
plt.title("Top 10 Products by Gross Margin")

plt.gca().invert_yaxis()

plt.tight_layout()

plt.savefig(
    output_folder / "top_10_margin.png"
)

plt.close()


# ==================================================
# CHART 3 — DIVISION REVENUE VS PROFIT
# ==================================================

division = (
    df.groupby("Division", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum")
    )
)

division_plot = division.set_index("Division")

division_plot[
    ["Sales", "Gross_Profit"]
].plot(
    kind="bar",
    figsize=(9, 6)
)

plt.xlabel("Division")
plt.ylabel("Amount")
plt.title("Division Revenue vs Gross Profit")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    output_folder / "division_revenue_profit.png"
)

plt.close()


# ==================================================
# CHART 4 — MARGIN DISTRIBUTION
# ==================================================

plt.figure(figsize=(9, 6))

sns.histplot(
    product["Gross Margin %"],
    bins=20,
    kde=True
)

plt.xlabel("Gross Margin (%)")
plt.ylabel("Number of Products")
plt.title("Gross Margin Distribution")

plt.tight_layout()

plt.savefig(
    output_folder / "margin_distribution.png"
)

plt.close()


# ==================================================
# CHART 5 — COST VS SALES
# ==================================================

plt.figure(figsize=(9, 6))

plt.scatter(
    product["Sales"],
    product["Cost"],
    alpha=0.6
)

plt.xlabel("Sales")
plt.ylabel("Cost")
plt.title("Cost vs Sales")

plt.tight_layout()

plt.savefig(
    output_folder / "cost_vs_sales.png"
)

plt.close()


# ==================================================
# CHART 6 — SALES VS GROSS PROFIT
# ==================================================

plt.figure(figsize=(9, 6))

plt.scatter(
    product["Sales"],
    product["Gross_Profit"],
    alpha=0.6
)

plt.xlabel("Sales")
plt.ylabel("Gross Profit")
plt.title("Sales vs Gross Profit")

plt.tight_layout()

plt.savefig(
    output_folder / "sales_vs_profit.png"
)

plt.close()


# ==================================================
# 7. DISPLAY CREATED FILES
# ==================================================

print("\n===== CHARTS CREATED =====")

for file in sorted(output_folder.iterdir()):
    print(file.name)

