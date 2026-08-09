import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(
    page_title="Nassau Candy Distributor Dashboard",
    page_icon="🍬",
    layout="wide"
)

# Load data
df = pd.read_csv("Nassau Candy Distributor.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Convert numeric columns
for col in ["Sales", "Units", "Gross Profit", "Cost"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# Convert dates
if "Order Date" in df.columns:
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")

# Title
st.title("🍬 Nassau Candy Distributor Dashboard")
st.write("Interactive Sales & Profit Analysis")

# Sidebar filters
st.sidebar.header("🔎 Filters")

filtered_df = df.copy()

if "State/Province" in df.columns:
    states = st.sidebar.multiselect(
        "Select State",
        sorted(df["State/Province"].dropna().unique())
    )
    if states:
        filtered_df = filtered_df[
            filtered_df["State/Province"].isin(states)
        ]

if "Product Name" in df.columns:
    products = st.sidebar.multiselect(
        "Select Product",
        sorted(df["Product Name"].dropna().unique())
    )
    if products:
        filtered_df = filtered_df[
            filtered_df["Product Name"].isin(products)
        ]

# KPIs
total_sales = filtered_df["Sales"].sum() if "Sales" in filtered_df.columns else 0
total_profit = filtered_df["Gross Profit"].sum() if "Gross Profit" in filtered_df.columns else 0
total_orders = filtered_df["Order ID"].nunique() if "Order ID" in filtered_df.columns else len(filtered_df)
total_units = filtered_df["Units"].sum() if "Units" in filtered_df.columns else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Sales", f"${total_sales:,.2f}")
col2.metric("📈 Total Profit", f"${total_profit:,.2f}")
col3.metric("🛒 Total Orders", f"{total_orders:,}")
col4.metric("📦 Total Units", f"{total_units:,.0f}")

st.divider()

# Sales by State
if "State/Province" in filtered_df.columns:
    st.subheader("📍 Sales by State")

    state_sales = (
        filtered_df.groupby("State/Province")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.bar_chart(state_sales)

# Sales by Product
if "Product Name" in filtered_df.columns:
    st.subheader("🍫 Top Products by Sales")

    product_sales = (
        filtered_df.groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.bar_chart(product_sales)

# Sales over time
if "Order Date" in filtered_df.columns:
    st.subheader("📅 Sales Trend")

    sales_trend = (
        filtered_df.dropna(subset=["Order Date"])
        .groupby("Order Date")["Sales"]
        .sum()
    )

    st.line_chart(sales_trend)

# Dataset preview
st.subheader("📊 Dataset Preview")
st.dataframe(filtered_df.head(20), use_container_width=True)

st.caption("Nassau Candy Distributor | Data Analyst Project")