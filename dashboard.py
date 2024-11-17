import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Load data
st.title("Tap Water Quality Analysis")

try:
    data = pd.read_csv("water_quality_data.csv")
    st.success("Data loaded successfully!")
except FileNotFoundError:
    st.error("The file 'water_quality_data.csv' was not found. Please make sure it exists.")
    data = None

# Display the data if available
if data is not None:
    st.subheader("Water Quality Data")
    st.dataframe(data)

# Filter by parameter
selected_parameter = st.selectbox("Select a parameter to view:", data["Mineral"].unique())
filtered_data = data[data["Mineral"] == selected_parameter]
st.dataframe(filtered_data)