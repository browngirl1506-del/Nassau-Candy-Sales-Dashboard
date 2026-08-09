import streamlit as st 
import pandas as pd

st.set_page_config(page_title="Nassau Candy Distributor", layout="wide")
st.title("Nassau Candy Distributor Dashboard")
df = pd.read_csv("Nassau Candy Distributor.csv")
Total_Sales = df["Sales"].sum()
st.metric("Total Sales",Total_Sales)
st.subheader("Dataset Preview")
st.dataframe(df) 
st.subheader("Dataset Information")
st.write("Rows:",df.shape[0]) 

st.write("Columns:", df.shape[1])
st.subheader("Column Names")
st.write(df.columns.tolist())