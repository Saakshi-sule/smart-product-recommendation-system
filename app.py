# app.py
import streamlit as st
import pandas as pd
from collections import Counter

# App title
st.title("Smart Product Recommendation System")

# Load data (cached for performance)
@st.cache_data
def load_data():
    df = pd.read_csv("notebooks/cleaned_ecommerce.csv")
    df = df[df['CustomerID'].notnull()]  # Remove rows with missing CustomerID
    return df

df = load_data()

# -------------------------------
# Sidebar Controls
# -------------------------------
st.sidebar.title("Options")

# Show raw data
show_data = st.sidebar.checkbox("Show raw data")
if show_data:
    st.subheader("Raw Dataset")
    st.write(df)

# Product selection
selected_product = st.sidebar.selectbox("Select a product", df['Description'].unique())

# -------------------------------
# Recommendation Logic
# -------------------------------
if selected_product:
    # Find customers who bought the selected product
    customers = df[df['Description'] == selected_product]['CustomerID'].unique()
    
    # Get all other products bought by these customers
    co_purchased = df[df['CustomerID'].isin(customers) & (df['Description'] != selected_product)]
    
    # Count frequency of each product
    recommendations = Counter(co_purchased['Description']).most_common(5)
    
    # -------------------------------
    # Display Recommendations in Columns
    # -------------------------------
    st.subheader(f"Products frequently bought with '{selected_product}':")
    
    if recommendations:
        cols = st.columns(len(recommendations))
        for i, (product, count) in enumerate(recommendations):
            with cols[i]:
                st.markdown(f"**{product}**")
                st.write(f"{count} purchases")
    else:
        st.write("No recommendations found for this product.")
