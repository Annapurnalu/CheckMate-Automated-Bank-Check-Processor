import os
import pdf2image
import numpy as np
import cv2
from PIL import Image
import streamlit as st

POPPLER_PATH = r"C:\Users\Annapoorna\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"

def convert_pdf_to_image(pdf_file):
    images = pdf2image.convert_from_bytes(pdf_file.read())
    return images[0] if images else None

def process_cheque_image(image):
    img = np.array(image.convert("RGB"))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        x, y, w, h = cv2.boundingRect(max(contours, key=cv2.contourArea))
        cheque_cropped = img[y:y+h, x:x+w]
        cheque_resized = cv2.resize(cheque_cropped, (800, 400))
        return Image.fromarray(cheque_resized)
    return image

def process_uploaded_image(uploaded_file):
    if uploaded_file is not None:
        return {
            "mime_type": uploaded_file.type,
            "data": uploaded_file.getvalue(),
        }
    else:
        st.error("No file uploaded!")
        return None
