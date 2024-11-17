import pandas as pd
import streamlit as st

# Load data
data = pd.read_csv("water_quality_data.csv")

# Display the data
st.dataframe(data)