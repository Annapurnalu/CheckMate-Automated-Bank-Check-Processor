import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "chequedb"),
}

genai.configure(api_key="AIzaSyCJweqKO1Yv8mMqbfIMlb0Ykqnub7sYT88")
model = genai.GenerativeModel("gemini-2.0-flash")
