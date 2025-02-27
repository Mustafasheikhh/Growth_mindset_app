# Imports
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Setting Up Our App
st.set_page_config(page_title="Data Sweeper", layout="wide")
st.title("Data Sweeper")
st.write("Transform Your Files Between CSV And Excel Formats With Built-In Data Cleaning And Visualization!")

uploaded_files = st.file_uploader("Upload Your Files (CSV Or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()


        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported File Type: {file_ext}")
            continue  # Now properly placed inside the loop

        # Display Info About The File
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size / 1024}")

        # Show Data Preview
        st.write("Preview The Head Of Data Frame:")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("Data Cleaning Options:")
        if st.checkbox(f"Clean Data For {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates From {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")

            with col2:
                if st.button(f"Fill Missing Values For {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values Have Been Filled!")

        # Column Selection
        st.subheader("Select Columns To Convert.")
        columns = st.multiselect(f"Choose Columns For {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Visualization
        st.subheader("Data Visualization")
        if st.checkbox(f"Show Visualization For {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # File Conversion
        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()    
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)  # Ensure buffer is at the beginning

            # Download Button
            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data = buffer,
                file_name=file_name,
                mime =mime_type
            )
st.success("All Files Processed!")