# Import library
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Function for one-hot encoding
def onehot_encode_column(df, column_name):
    if pd.api.types.is_object_dtype(df[column_name]):
        unique_values = df[column_name].unique()
        mapping = {value: index for index, value in enumerate(unique_values)}
        df[column_name] = df[column_name].map(mapping)
        onehot_encoded = pd.get_dummies(df[column_name], prefix=column_name)
        df = pd.concat([df, onehot_encoded], axis=1)
    else:
        st.warning(f"Selected column '{column_name}' is not an object type and cannot be one-hot encoded.")
    return df

# Set page title and tab title
st.set_page_config(page_title="Data Processing Project", page_icon=":chart_with_upwards_trend:")

# Page title
st.title("Data Processing Project")

# Penjelasan proyek
st.markdown("""
    Perkenalkan ini adalah web yang menampilkan data processing yang kami buat.
    
    **Kelompok ini beranggotakan:**
    - Rhena Tabella - 064002200004
    - Andri Martin - 064002200010
    - Muhammad Ziddan Fadillah - 064002200025
    - Muhammad Fahmi - 064002200036
""")

# Upload CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

# Check if a file is uploaded
if uploaded_file is not None:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)

    # Display the DataFrame
    st.write("Data Preview:")
    st.write(df)

    # Menu for data processing methods
    selected_method = st.selectbox("Select Data Processing Method:", ["Shape", "Information", "Describe", "Unique", "Boxplot", "One-Hot Encoding"])

    # Check if "Boxplot" is selected
    if selected_method == "Boxplot":
        # Allow user to select a column for the boxplot
        selected_column = st.selectbox("Select a column for the Boxplot:", df.columns)

        # Check if the selected column is numeric
        if pd.api.types.is_numeric_dtype(df[selected_column]):
            # Display the Boxplot
            st.write(f"Boxplot for {selected_column}:")
            fig, ax = plt.subplots()
            sns.boxplot(x=selected_column, data=df, ax=ax)
            st.pyplot(fig)
        else:
            st.warning(f"Selected column '{selected_column}' is not numeric and cannot be used for Boxplot.")

    # Check if "One-Hot Encoding" is selected
    elif selected_method == "One-Hot Encoding":
        # Allow user to select a column for one-hot encoding
        selected_column = st.selectbox("Select a column for One-Hot Encoding:", df.columns)

        # Perform one-hot encoding if the column is object type
        df = onehot_encode_column(df, selected_column)

        # Display the updated DataFrame
        st.write(f"One-Hot Encoding for {selected_column}:")
        st.write(df)

    else:
        # Button to trigger data processing
        process_data_button = st.button("Process Data")

        if process_data_button:
            # Perform data processing based on the selected method
            if selected_method == "Shape":
                # Display DataFrame information directly
                st.write("DataFrame Information:")
                st.write(df.shape)
            elif selected_method == "Information":
                # Display DataFrame information directly
                st.write("DataFrame Information:")
                st.write(df.info())
            elif selected_method == "Describe":
                # Display DataFrame information directly
                st.write("DataFrame Information:")
                st.write(df.describe())
            elif selected_method == "Unique":
                # Display DataFrame information directly
                st.write("DataFrame Information:")
                st.write(df.nunique())