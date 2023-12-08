# Import library
import streamlit as st
import pandas as pd
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
    Selamat datang di Web Data Processing!

    **Kami adalah tim yang berdedikasi untuk membantu Anda memproses dan menganalisis data dengan mudah. Tim ini terdiri dari:**

    - Rhena Tabella - 064002200004
    - Andri Martin - 064002200010
    - Muhammad Ziddan Fadillah - 064002200025
    - Muhammad Fahmi - 064002200036

    Cara Penggunaan:

    - **Upload File CSV:**
      Silakan unggah file CSV Anda dengan menggunakan tombol di bawah.
      
    - **Pilih Metode:**
      Pilih metode pemrosesan data dari menu drop-down, seperti "Shape", "Information", "Boxplot", dan lainnya.
      
    - **Analisis Data:**
      Lakukan analisis data dengan menekan tombol yang sesuai. Misalnya, tekan "Generate Boxplot" untuk membuat boxplot.
      
    - **Hasil dan Informasi:**
      Hasil analisis dan informasi akan ditampilkan secara interaktif di bawahnya.
      
    Semoga alat ini membantu Anda menjelajahi dan memahami data Anda dengan lebih baik. Jangan ragu untuk menghubungi kami jika Anda memiliki pertanyaan atau masukan!
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
    selected_method = st.selectbox("Select Data Processing Method:", ["Shape",
                                                                      "Information",
                                                                      "Describe",
                                                                      "Unique",
                                                                      "Check Missing Values",
                                                                      "Boxplot",
                                                                      "One-Hot Encoding",
                                                                      "Histogram Countplot"])

    # Check if "Boxplot" is selected
    if selected_method == "Boxplot":
        # Allow user to select a column for the boxplot
        selected_column = st.selectbox("Select a column for the Boxplot:", df.columns)

        # Check if the selected column is numeric
        if pd.api.types.is_numeric_dtype(df[selected_column]):
            # Display the Boxplot
            st.write(f"Boxplot for {selected_column}:")
            # Button to generate Boxplot
            generate_boxplot = st.button("Generate Boxplot")
            if generate_boxplot:
                fig, ax = plt.subplots()
                sns.boxplot(x=selected_column, data=df, ax=ax)
                st.pyplot(fig)
        else:
            st.warning(f"Selected column '{selected_column}' is not numeric and cannot be used for Boxplot.")

    # Check if "One-Hot Encoding" is selected
    elif selected_method == "One-Hot Encoding":
        # Allow user to select a column for one-hot encoding
        selected_column = st.selectbox("Select a column for One-Hot Encoding:", df.columns)

        # Button to perform One-Hot Encoding
        onehot_encode_button = st.button("Perform One-Hot Encoding")
        if onehot_encode_button:
            # Perform one-hot encoding if the column is object type
            df = onehot_encode_column(df, selected_column)
            # Display the updated DataFrame
            st.write(f"One-Hot Encoding for {selected_column}:")
            st.write(df)

    # Check if "Histogram Countplot" is selected
    elif selected_method == "Histogram Countplot":
        # Allow user to select a column for histogram
        selected_column_a = st.selectbox("Select a column for histogram:", df.columns)

        # Allow user to select a column for 'hue' (optional)
        hue_column = st.selectbox("Select a column for 'hue' (optional):", [None] + list(df.columns))

        # Button to generate Histogram Countplot
        generate_histogram_countplot = st.button("Generate Histogram Countplot")
        if generate_histogram_countplot:
            # Display the histogram countplot
            st.write(f"Histogram Countplot for {selected_column_a} with 'hue' by {hue_column if hue_column else 'None'}:")
            fig, ax = plt.subplots(figsize=(10, 8))

            if hue_column:
                plot = sns.countplot(x=selected_column_a, data=df, hue=hue_column)
            else:
                plot = sns.countplot(x=selected_column_a, data=df)

            # Add count labels on top of each bar
            for p in plot.patches:
                count_label = p.get_height()
                x_position = p.get_x() + p.get_width() / 2
                y_position = p.get_height() + 0.05  # Adjust the vertical position of the count label
                ax.annotate(count_label, (x_position, y_position), ha='center', va='center')

            ax.legend()
            st.pyplot(fig)
    
    # Check if "Check Missing Values" is selected
    elif selected_method == "Check Missing Values":
        # Display missing values for each column
        st.write("Missing Values:")
        missing_values = df.isnull().sum()
        st.write(missing_values)
        # Check if there are missing values
        if missing_values.sum() == 0:
            st.info("No missing values found. No need to drop rows.")
        else:
            # Button to drop rows with missing values and proceed to "Cleaned Data"
            drop_missing_values_button = st.button("Drop Rows with Missing Values and Proceed to Cleaned Data")
            if drop_missing_values_button:
                # Drop rows with missing values
                df_cleaned = df.dropna()
                # Display the cleaned DataFrame
                st.write("Data after dropping rows with missing values:")
                st.write(df_cleaned)

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
                # Create a string with information
                info_str = f"Shape of DataFrame: {df.shape}\n"
                info_str += f"Data types:\n{df.dtypes}\n"
                info_str += f"Non-null counts:\n{df.count()}\n"
                # Display the information string
                st.text(info_str)
            elif selected_method == "Describe":
                # Display DataFrame information directly
                st.write("DataFrame Information:")
                st.write(df.describe())
            elif selected_method == "Unique":
                # Display DataFrame information directly
                st.write("DataFrame Information:")
                st.write(df.nunique())
