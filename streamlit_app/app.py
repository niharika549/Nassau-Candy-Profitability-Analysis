
import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Nassau Candy Profitability Dashboard",
    page_icon="🍫",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv(
        "eda_outputs/cleaned_data.csv"
    )

    df["Order Date"] = pd.to_datetime(
        df["Order Date"]
    )

    return df


df = load_data()


# ============================================================
# HEADER
# ============================================================

st.title("🍫 Nassau Candy Distributor")

st.subheader(
    "Product Line Profitability & Margin Performance Analysis"
)

st.write(
    "Interactive dashboard for analysing sales, profitability, "
    "margins, product performance, cost efficiency and "
    "profit concentration."
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🎛️ Dashboard Filters")


# DATE FILTER
min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()

date_range = st.sidebar.date_input(
    "📅 Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


# DIVISION FILTER
divisions = sorted(
    df["Division"].dropna().unique()
)

selected_divisions = st.sidebar.multiselect(
    "🏢 Division",
    divisions,
    default=divisions
)


# MARGIN FILTER
margin_threshold = st.sidebar.slider(
    "📊 Minimum Gross Margin (%)",
    min_value=0.0,
    max_value=100.0,
    value=50.0,
    step=1.0
)


# PRODUCT SEARCH
product_search = st.sidebar.text_input(
    "🔎 Search Product"
)


# ============================================================
# FILTER DATA
# ============================================================

filtered_df = df.copy()


# DATE
if len(date_range) == 2:

    start_date = pd.Timestamp(
        date_range[0]
    )

    end_date = (
        pd.Timestamp(date_range[1])
        + pd.Timedelta(days=1)
    )

    filtered_df = filtered_df[
        (filtered_df["Order Date"] >= start_date)
        &
        (filtered_df["Order Date"] < end_date)
    ]


# DIVISION
if selected_divisions:

    filtered_df = filtered_df[
        filtered_df["Division"].isin(
            selected_divisions
        )
    ]


# PRODUCT SEARCH
if product_search:

    filtered_df = filtered_df[
        filtered_df["Product Name"]
        .str.contains(
            product_search,
            case=False,
            na=False
        )
    ]


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_sales = filtered_df["Sales"].sum()

total_profit = filtered_df["Gross Profit"].sum()

total_units = filtered_df["Units"].sum()

gross_margin = (
    total_profit / total_sales * 100
    if total_sales > 0
    else 0
)


# ============================================================
# KPI CARDS
# ============================================================

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "💵 Total Sales",
    f"${total_sales:,.2f}"
)

k2.metric(
    "💰 Gross Profit",
    f"${total_profit:,.2f}"
)

k3.metric(
    "📦 Units Sold",
    f"{total_units:,}"
)

k4.metric(
    "📊 Gross Margin",
    f"{gross_margin:.2f}%"
)


st.divider()


# ============================================================
# PRODUCT SUMMARY
# ============================================================

product_summary = (
    filtered_df
    .groupby(
        ["Product ID", "Product Name"],
        as_index=False
    )
    .agg(
        Sales=("Sales", "sum"),
        Units=("Units", "sum"),
        Gross_Profit=("Gross Profit", "sum"),
        Cost=("Cost", "sum")
    )
)

product_summary["Gross Margin %"] = (
    product_summary["Gross_Profit"]
    / product_summary["Sales"]
) * 100

product_summary["Profit per Unit"] = (
    product_summary["Gross_Profit"]
    / product_summary["Units"]
)

product_summary["Cost % of Sales"] = (
    product_summary["Cost"]
    / product_summary["Sales"]
) * 100


# ============================================================
# PRODUCT SEGMENTS
# ============================================================

sales_median = product_summary["Sales"].median()

profit_median = product_summary["Gross_Profit"].median()

margin_median = product_summary["Gross Margin %"].median()


product_summary["Product Segment"] = "Other"


product_summary.loc[
    (
        product_summary["Gross_Profit"]
        >= profit_median
    )
    &
    (
        product_summary["Gross Margin %"]
        >= margin_median
    ),
    "Product Segment"
] = "High Profit / High Margin"


product_summary.loc[
    (
        product_summary["Sales"]
        >= sales_median
    )
    &
    (
        product_summary["Gross Margin %"]
        < margin_median
    ),
    "Product Segment"
] = "High Sales / Low Margin"


product_summary.loc[
    (
        product_summary["Sales"]
        < sales_median
    )
    &
    (
        product_summary["Gross_Profit"]
        < profit_median
    ),
    "Product Segment"
] = "Low Sales / Low Profit"


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📊 Product Profitability",
        "🏢 Division Performance",
        "💰 Cost & Margin",
        "📈 Profit Concentration",
        "📋 Product Details"
    ]
)


# ============================================================
# TAB 1 — PRODUCT PROFITABILITY
# ============================================================

with tab1:

    st.header(
        "📊 Product Profitability Overview"
    )

    st.write(
        "Products ranked by gross profit, gross margin "
        "and profitability segments."
    )


    # TOP PROFIT PRODUCTS

    top_profit = (
        product_summary
        .nlargest(
            10,
            "Gross_Profit"
        )
    )


    fig_profit = px.bar(
        top_profit,
        x="Gross_Profit",
        y="Product Name",
        orientation="h",
        title="Top 10 Products by Gross Profit"
    )

    fig_profit.update_layout(
        yaxis={
            "categoryorder": "total ascending"
        }
    )

    st.plotly_chart(
        fig_profit,
        use_container_width=True
    )


    # TOP MARGIN PRODUCTS

    top_margin = (
        product_summary
        .nlargest(
            10,
            "Gross Margin %"
        )
    )


    fig_margin = px.bar(
        top_margin,
        x="Gross Margin %",
        y="Product Name",
        orientation="h",
        title="Top 10 Products by Gross Margin"
    )

    fig_margin.update_layout(
        yaxis={
            "categoryorder": "total ascending"
        }
    )

    st.plotly_chart(
        fig_margin,
        use_container_width=True
    )


    # PRODUCT SEGMENTS

    st.subheader(
        "🎯 Product Profitability Segments"
    )


    segment_counts = (
        product_summary[
            "Product Segment"
        ]
        .value_counts()
        .reset_index()
    )

    segment_counts.columns = [
        "Product Segment",
        "Number of Products"
    ]


    fig_segments = px.bar(
        segment_counts,
        x="Product Segment",
        y="Number of Products",
        title="Product Segmentation"
    )

    st.plotly_chart(
        fig_segments,
        use_container_width=True
    )


# ============================================================
# TAB 2 — DIVISION PERFORMANCE
# ============================================================

with tab2:

    st.header(
        "🏢 Division Performance Dashboard"
    )


    division_summary = (
        filtered_df
        .groupby(
            "Division",
            as_index=False
        )
        .agg(
            Sales=("Sales", "sum"),
            Gross_Profit=("Gross Profit", "sum"),
            Units=("Units", "sum")
        )
    )


    division_summary["Gross Margin %"] = (
        division_summary["Gross_Profit"]
        / division_summary["Sales"]
    ) * 100


    # REVENUE VS PROFIT

    fig_division = px.bar(
        division_summary,
        x="Division",
        y=[
            "Sales",
            "Gross_Profit"
        ],
        barmode="group",
        title="Revenue vs Gross Profit by Division"
    )

    st.plotly_chart(
        fig_division,
        use_container_width=True
    )


    # MARGIN BY DIVISION

    fig_div_margin = px.bar(
        division_summary,
        x="Division",
        y="Gross Margin %",
        title="Gross Margin by Division"
    )

    st.plotly_chart(
        fig_div_margin,
        use_container_width=True
    )


    # DIVISION TABLE

    st.subheader(
        "Division Financial Summary"
    )

    st.dataframe(
        division_summary,
        use_container_width=True
    )


# ============================================================
# TAB 3 — COST & MARGIN
# ============================================================

with tab3:

    st.header(
        "💰 Cost vs Margin Diagnostics"
    )


    # COST VS SALES

    fig_cost = px.scatter(
        product_summary,
        x="Sales",
        y="Cost",
        size="Gross_Profit",
        color="Gross Margin %",
        hover_name="Product Name",
        title="Cost vs Sales by Product"
    )

    st.plotly_chart(
        fig_cost,
        use_container_width=True
    )


    # SALES VS PROFIT

    fig_sales_profit = px.scatter(
        product_summary,
        x="Sales",
        y="Gross_Profit",
        size="Units",
        color="Gross Margin %",
        hover_name="Product Name",
        title="Sales vs Gross Profit"
    )

    st.plotly_chart(
        fig_sales_profit,
        use_container_width=True
    )


    # MARGIN DISTRIBUTION

    fig_distribution = px.histogram(
        product_summary,
        x="Gross Margin %",
        nbins=20,
        title="Gross Margin Distribution"
    )

    st.plotly_chart(
        fig_distribution,
        use_container_width=True
    )


    # MARGIN RISK

    st.subheader(
        "⚠️ Margin Risk Products"
    )


    risk_products = (
        product_summary
        .nsmallest(
            15,
            "Gross Margin %"
        )
    )


    st.dataframe(
        risk_products[
            [
                "Product Name",
                "Sales",
                "Cost",
                "Gross_Profit",
                "Gross Margin %",
                "Cost % of Sales",
                "Profit per Unit"
            ]
        ],
        use_container_width=True
    )


# ============================================================
# TAB 4 — PROFIT CONCENTRATION
# ============================================================

with tab4:

    st.header(
        "📈 Profit Concentration Analysis"
    )


    # PROFIT PARETO

    profit_pareto = (
        product_summary
        .sort_values(
            "Gross_Profit",
            ascending=False
        )
        .reset_index(drop=True)
    )


    profit_pareto["Cumulative Profit %"] = (
        profit_pareto["Gross_Profit"]
        .cumsum()
        /
        profit_pareto["Gross_Profit"].sum()
    ) * 100


    profit_pareto["Product Rank"] = (
        profit_pareto.index + 1
    )


    fig_profit_pareto = px.line(
        profit_pareto,
        x="Product Rank",
        y="Cumulative Profit %",
        title="Cumulative Profit Contribution"
    )


    fig_profit_pareto.add_hline(
        y=80,
        line_dash="dash",
        annotation_text="80% Profit"
    )


    st.plotly_chart(
        fig_profit_pareto,
        use_container_width=True
    )


    # REVENUE PARETO

    revenue_pareto = (
        product_summary
        .sort_values(
            "Sales",
            ascending=False
        )
        .reset_index(drop=True)
    )


    revenue_pareto["Cumulative Revenue %"] = (
        revenue_pareto["Sales"]
        .cumsum()
        /
        revenue_pareto["Sales"].sum()
    ) * 100


    revenue_pareto["Product Rank"] = (
        revenue_pareto.index + 1
    )


    fig_revenue_pareto = px.line(
        revenue_pareto,
        x="Product Rank",
        y="Cumulative Revenue %",
        title="Cumulative Revenue Contribution"
    )


    fig_revenue_pareto.add_hline(
        y=80,
        line_dash="dash",
        annotation_text="80% Revenue"
    )


    st.plotly_chart(
        fig_revenue_pareto,
        use_container_width=True
    )


    # CONCENTRATION TABLE

    st.subheader(
        "Top Profit-Contributing Products"
    )


    st.dataframe(
        profit_pareto[
            [
                "Product Name",
                "Sales",
                "Gross_Profit",
                "Gross Margin %",
                "Cumulative Profit %"
            ]
        ].head(20),
        use_container_width=True
    )


# ============================================================
# TAB 5 — PRODUCT DETAILS
# ============================================================

with tab5:

    st.header(
        "📋 Product Profitability Details"
    )


    display_df = (
        product_summary[
            product_summary["Gross Margin %"]
            >= margin_threshold
        ]
        .sort_values(
            "Gross_Profit",
            ascending=False
        )
    )


    st.write(
        f"Showing products with gross margin "
        f"≥ {margin_threshold:.0f}%"
    )


    st.dataframe(
        display_df[
            [
                "Product ID",
                "Product Name",
                "Sales",
                "Units",
                "Cost",
                "Gross_Profit",
                "Gross Margin %",
                "Profit per Unit",
                "Cost % of Sales",
                "Product Segment"
            ]
        ],
        use_container_width=True
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Nassau Candy Distributor | "
    "Data Science Internship Project | "
    "Product Line Profitability & Margin Performance Analysis"
)
