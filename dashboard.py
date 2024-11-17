import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import base64

# Styling the dashboard 

encoded_image = base64.b64encode(open('water_background.jpg', 'rb').read()).decode()

# Set the background
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/jpg;base64,{encoded_image});
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <style>
    * {
        font-family: 'Comic Sans MS', 'Comic Sans', cursive;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data
st.title("Tap Water Quality Analysis")

# Add a brief introduction
st.write(
    "Welcome to our interactive dashboard on Charlotte's tap water!"
    " We're here to help you explore the quality of your local water supply "
    "and understand how it affects your health. "
    "Dive into key water quality parameters and see what they mean for you and your family."
)

try:
    data = pd.read_csv("water_quality_data.csv")
    st.success("Data loaded successfully!")
except FileNotFoundError:
    st.error("Data was not found. Sorry for the inconvienience, try again later. ")
    data = None

if data is not None:
    # Extract metadata row
    metadata_row = data[data["Mineral"] == "Metadata"]
    if not metadata_row.empty:
        metadata_text = metadata_row.iloc[0]["Value"]  # Get the Metadata value
        # Display metadata at the top
        st.markdown(f"{metadata_text}")

# Display the data if available
if data is not None:
    st.subheader("Water Quality Data")
    st.dataframe(data[["Mineral", "Value"]])
