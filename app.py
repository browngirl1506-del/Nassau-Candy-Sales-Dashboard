import streamlit as st
import pandas as pd

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="Nassau Candy Sales Dashboard",
    page_icon="🍬",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
df = pd.read_csv("Nassau Candy Distributor.csv")
df.columns = df.columns.str.strip()

# Numeric columns
for col in ["Sales", "Units", "Gross Profit", "Cost"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# Date columns
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")

# Shipping Lead Time
df["Shipping Lead Time"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

# ---------------- TITLE ----------------
st.title("🍬 NASSAU CANDY SALES DASHBOARD")
st.caption("Interactive Sales & Shipping Analysis")

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔎 Dashboard Filters")

filtered_df = df.copy()

# Date filter
min_date = df["Order Date"].min()
max_date = df["Order Date"].max()

date_range = st.sidebar.date_input(
    "Order Date",
    value=(min_date.date(), max_date.date())
)

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df["Order Date"].dt.date >= start_date)
        & (filtered_df["Order Date"].dt.date <= end_date)
    ]

# Ship Mode filter
if "Ship Mode" in df.columns:
    ship_modes = st.sidebar.multiselect(
        "Ship Mode",
        sorted(df["Ship Mode"].dropna().unique())
    )
    if ship_modes:
        filtered_df = filtered_df[
            filtered_df["Ship Mode"].isin(ship_modes)
        ]

# State filter
if "State/Province" in df.columns:
    states = st.sidebar.multiselect(
        "State / Province",
        sorted(df["State/Province"].dropna().unique())
    )
    if states:
        filtered_df = filtered_df[
            filtered_df["State/Province"].isin(states)
        ]

# Division filter
if "Division" in df.columns:
    divisions = st.sidebar.multiselect(
        "Division",
        sorted(df["Division"].dropna().unique())
    )
    if divisions:
        filtered_df = filtered_df[
            filtered_df["Division"].isin(divisions)
        ]

# ---------------- KPI CARDS ----------------
total_profit = filtered_df["Gross Profit"].sum()
shipping_lead = filtered_df["Shipping Lead Time"].mean()
total_orders = filtered_df["Order ID"].nunique()
total_sales = filtered_df["Sales"].sum()
total_units = filtered_df["Units"].sum()

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("💰 Total Profit", f"${total_profit:,.2f}")
c2.metric("🚚 Avg Shipping Lead Time", f"{shipping_lead:.1f} Days")
c3.metric("📦 Total Orders", f"{total_orders:,}")
c4.metric("💵 Total Sales", f"${total_sales:,.2f}")
c5.metric("🍫 Total Units", f"{total_units:,.0f}")

st.divider()

# =========================================================
# PAGE 1 - SALES OVERVIEW
# =========================================================

st.header("📊 Sales Overview")

# Sales by Division
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales by Division")
    division_sales = (
        filtered_df.groupby("Division")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )
    st.bar_chart(division_sales)

with col2:
    st.subheader("Sales by Ship Mode")
    ship_sales = (
        filtered_df.groupby("Ship Mode")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )
    st.bar_chart(ship_sales)

# Sales by State
st.subheader("🏆 Top 10 Sales by State")

state_sales = (
    filtered_df.groupby("State/Province")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(state_sales)

# Monthly sales
st.subheader("📅 Total Sales by Month")

monthly_sales = (
    filtered_df.dropna(subset=["Order Date"])
    .assign(Month=lambda x: x["Order Date"].dt.to_period("M").astype(str))
    .groupby("Month")["Sales"]
    .sum()
)

st.line_chart(monthly_sales)

# Top products
st.subheader("🍫 Top 5 Products by Sales")

product_sales = (
    filtered_df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

st.bar_chart(product_sales)

# Sales by City
st.subheader("🏙️ Top 10 Sales by City")

city_sales = (
    filtered_df.groupby("City")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(city_sales)

# =========================================================
# PAGE 2 - PRODUCT & SHIPPING ANALYSIS
# =========================================================

st.divider()
st.header("🚚 Product & Shipping Analysis")

# Average shipping lead time by Division
col1, col2 = st.columns(2)

with col1:
    st.subheader("Average Shipping Lead Time by Division")

    division_ship = (
        filtered_df.groupby("Division")["Shipping Lead Time"]
        .mean()
        .sort_values(ascending=False)
    )

    st.bar_chart(division_ship)

with col2:
    st.subheader("Average Shipping Lead Time by State")

    state_ship = (
        filtered_df.groupby("State/Province")["Shipping Lead Time"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )

    st.bar_chart(state_ship)

# Gross Profit by Product
st.subheader("💰 Gross Profit by Product")

profit_product = (
    filtered_df.groupby("Product Name")["Gross Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(profit_product)

# Total orders by ship mode
st.subheader("📦 Total Orders by Ship Mode")

orders_ship = (
    filtered_df.groupby("Ship Mode")["Order ID"]
    .nunique()
    .sort_values(ascending=False)
)

st.bar_chart(orders_ship)

# Gross Profit by Division
st.subheader("💵 Gross Profit by Division")

profit_division = (
    filtered_df.groupby("Division")["Gross Profit"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(profit_division)

# Average shipping by Ship Mode
st.subheader("🚚 Average Shipping Lead Time by Ship Mode")

ship_lead_mode = (
    filtered_df.groupby("Ship Mode")["Shipping Lead Time"]
    .mean()
    .sort_values(ascending=False)
)

st.bar_chart(ship_lead_mode)

# Average shipping by Region
if "Region" in filtered_df.columns:
    st.subheader("🌎 Average Shipping Lead Time by Region")

    region_ship = (
        filtered_df.groupby("Region")["Shipping Lead Time"]
        .mean()
        .sort_values(ascending=False)
    )

    st.bar_chart(region_ship)

# ---------------- DATA PREVIEW ----------------
st.divider()
st.subheader("📋 Dataset Preview")

st.dataframe(
    filtered_df.head(20),
    use_container_width=True
)

st.caption("Nassau Candy Distributor | Data Analyst Internship Project")