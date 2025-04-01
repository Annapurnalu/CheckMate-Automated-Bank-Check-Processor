import os
import streamlit as st
from PIL import Image
import mysql.connector
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
from config.settings import DB_CONFIG
from utils.image_processing import process_cheque_image,process_uploaded_image
from utils.db_operations import insert_cheque_details
from utils.api_client import get_api_response
from utils.text_processing import format_extracted_text
from utils.image_processing import convert_pdf_to_image
st.set_page_config(page_title="CheckMate - Automated Cheque Processor", layout="wide")
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 20px;
    }
    .sub-title {
        text-align: center;
        font-size: 24px;
        color: #16a085;
        margin-bottom: 30px;
    }
    .stButton>button {
        background-color: #3498db !important;
        color: white !important;
        font-size: 18px !important;
        padding: 10px 20px !important;
        border-radius: 10px !important;
    }
    .stButton>button:hover {
        background-color: #2980b9 !important;
    }
    .stDataFrame {
        background-color: #ecf0f1;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Navigation Bar
st.sidebar.title("🚀 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "📤 Upload & Process", "📄 Cheque Details", "📊 Analytics", "📥 Export Data"])

os.makedirs("uploads", exist_ok=True)
os.makedirs("processed", exist_ok=True)

if page == "🏠 Home":
    st.markdown("<h1 class='main-title'>🏦 Welcome to CheckMate: Automated Bank Cheque Processor</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-title'>Automated Bank Cheque Processing</h2>", unsafe_allow_html=True)
    st.image(r"C:\Users\Annapoorna\Downloads\DALL·E 2025-03-06 20.12.33 - A modern and sleek digital interface concept for 'CheckMate_ Automated Bank Cheque Processor'. The image should include a futuristic AI-driven banking.webp", use_column_width=True)
    st.markdown("""
    **Welcome to CheckMate!**
                
    - 📌 **Upload** cheque images or PDFs.
    - 🤖 **Automated Processing** using AI.
    - 📊 **Detailed Analytics** and tracking.
    - 📥 **Export Data** to CSV, JSON, or Excel.
                
    **CheckMate** is an AI-powered tool designed to automate the processing of bank cheques. It offers:
    - 📄 **Cheque Image Processing** for extracting details
    - 🤖 **AI-powered Data Extraction** using Google Gemini API
    - 🏦 **Database Integration** for storing cheque details
    - 📊 **Analytics & Visualization** of processed cheques
    - 📥 **Data Export** in multiple formats (CSV, JSON, Excel)
    
    **Use the sidebar to navigate and get started!**
    """)

elif page == "📤 Upload & Process":
    st.title("🔹 Automated Cheque Uploading & Processing")
    uploaded_file = st.file_uploader("Upload Cheque Image or PDF", type=["jpg", "png", "jpeg", "pdf"])

    if uploaded_file:
        file_path = os.path.join("uploads", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        image = convert_pdf_to_image(uploaded_file) if uploaded_file.type == "application/pdf" else Image.open(uploaded_file)
        processed_image = process_cheque_image(image)
        processed_path = file_path.replace("uploads", "processed")
        processed_image.save(processed_path)
        col1, col2 = st.columns(2)
        with col1:
            st.image(image, caption="Original Cheque", use_column_width=True)
        with col2:
            st.image(processed_image, caption="Processed Cheque", use_column_width=True)
        if image:
            image_content = process_uploaded_image(uploaded_file)
            if image_content:
                st.write("🔍 Extracting cheque details...")
                response = get_api_response(image_content)

                if response:
                    extracted_data = format_extracted_text(response)
                    if extracted_data:
                        st.subheader("Extracted Information")
                        for key, value in extracted_data.items():
                            st.write(f"**{key.replace('_', ' ').title()}:** {value}")
                        
                        if insert_cheque_details(extracted_data):
                            st.success("✅ Cheque details saved successfully!")
                        else:
                            st.error("❌ Failed to save cheque details.")
                    else:
                        st.error("No cheque details extracted. Please check the uploaded image.")
                else:
                    st.error("Failed to get a response from the AI model.")

    

elif page == "📄 Cheque Details":
    st.title("📄 Cheque Details")
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        df = pd.read_sql("SELECT * FROM cheques ORDER BY id DESC", conn)
        conn.close()
        if not df.empty:
            if "cheque_date" in df.columns:
                df["cheque_date"] = pd.to_datetime(df["cheque_date"], errors="coerce", dayfirst=True).dt.strftime("%d-%m-%Y")
            st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Database Error: {e}")

elif page == "📊 Analytics":
    st.title("📊 Cheque Analytics")
    try:
        def get_data():
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="chequedb")
            query = "SELECT cheque_date, bank, cheque_number FROM cheques;"
            df = pd.read_sql(query, conn)
            conn.close()
            return df
        data = get_data()
        data['cheque_date'] = pd.to_datetime(data['cheque_date'])
        total_cheques = len(data)
        todays_cheques = len(data[data['cheque_date'] == pd.to_datetime('today')])
        st.header("Cheque Processing Analytics")
        st.metric(label="Total Cheques Processed", value=total_cheques)
        st.metric(label="Today's Cheques Processed", value=todays_cheques)
        st.subheader("Cheques Processed Over Time")
        fig, ax = plt.subplots()
        data.groupby('cheque_date').count()['cheque_number'].plot(ax=ax, marker='o', linestyle='-')
        ax.set_xlabel("Date")
        ax.set_ylabel("Cheques Processed")
        st.pyplot(fig)
        st.subheader("Cheques by Bank")
        fig, ax = plt.subplots()
        data.groupby('bank').count()['cheque_number'].plot(kind='bar', ax=ax)
        ax.set_ylabel("Cheques Processed")
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Database Error: {e}")

elif page == "📥 Export Data":
    st.title("📥 Export Cheque Data")
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        df = pd.read_sql("SELECT * FROM cheques ORDER BY id DESC", conn)
        conn.close()
        if not df.empty:
            csv_data = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Export to CSV", csv_data, "cheque_data.csv", "text/csv")
            
            json_data = df.to_json(orient="records", indent=4).encode("utf-8")
            st.download_button("📥 Export to JSON", json_data, "cheque_data.json", "application/json")
            
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
                df.to_excel(writer, sheet_name="Cheques", index=False)
            excel_data = excel_buffer.getvalue()
            st.download_button("📥 Export to Excel", excel_data, "cheque_data.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        st.dataframe(df)
    except Exception as e:
        st.error(f"Database Error: {e}")
