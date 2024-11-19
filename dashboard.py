import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import base64

# Styling the dashboard 

# Load the background image
# encoded_image = base64.b64encode(open('water_background2.jpg', 'rb').read()).decode()

# # Set the background
# st.markdown(
#     f"""
#     <style>
#     .stApp {{
#         background-image: url(data:image/jpg;base64,{encoded_image});
#         background-size: cover;
#         background-position: center;
#         background-repeat: no-repeat;
#     }}
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# Set the font
st.markdown("""
    <style>
    .stApp {
        font-family: 'Comic Sans MS', 'Comic Sans', cursive !important;
    }
    h1, h2, h3, p, span {
        font-family: 'Comic Sans MS', 'Comic Sans', cursive !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data
st.title("Charlotte Tap Water Quality Analysis")

# Add a brief introduction
st.write(
    "Welcome to our interactive dashboard on Charlotte's tap water!"
    " We're here to help you explore the quality of your local water supply "
    "and understand how it affects your health. "
    "Dive into key water quality parameters and see what they mean for you and your family."
)

try:
    data = pd.read_csv("water_analysis.csv")
    st.success("Data loaded successfully!")
except FileNotFoundError:
    st.error("Data was not found. Sorry for the inconvienience, try again later. ")
    data = None

try: 
    data2 = pd.read_csv("water_quality_data.csv")
except FileNotFoundError:
    st.error("Meta Data was not found. Sorry for the inconvienience. ")
# Display the data if available
if data2 is not None:
    st.subheader("Water Quality Data")
    metadata_row = data2[data2["Mineral"] == "Metadata"]
    if not metadata_row.empty:
        metadata_text = metadata_row.iloc[0]["Value"]  # Get the Metadata value
        # Display metadata at the top
        st.markdown(f"{metadata_text}")
    st.dataframe(data[["Mineral", "Value", "Safe Range", "Health Impacts Above Safe Range"]])
