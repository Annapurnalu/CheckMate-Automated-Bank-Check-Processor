import streamlit as st
import google.generativeai as genai

genai.configure(api_key="AIzaSyCJweqKO1Yv8mMqbfIMlb0Ykqnub7sYT88")
model = genai.GenerativeModel("gemini-2.0-flash")

def get_api_response(image_content):
    try:
        response = model.generate_content([
            "Extract cheque details including Payee Name, Amount, Bank Name, MICR Code, Branch, IFSC Code, Account Number, Cheque Number, Cheque Date, and Signature Verification.",
            image_content,
        ])
        return response.text if response else None
    except Exception as e:
        st.error(f"API Error: {e}")
        return None