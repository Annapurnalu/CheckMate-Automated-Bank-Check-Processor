import mysql.connector
import pandas as pd
import streamlit as st
from config.settings import DB_CONFIG
def insert_cheque_details(data):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if not conn.is_connected():
            st.error("Database connection failed.")
            return False

        cursor = conn.cursor()

        query = """
        INSERT INTO cheques (payee_name, amount, bank, branch_name, cheque_number, ifsc_code, micr_code, cheque_date, account_number, signature_verified)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        values = (
            data.get("payee_name", "Unknown"),
            data.get("amount", "0.00"),
            data.get("bank_name", "Unknown"),
            data.get("branch_name"),
            data.get("cheque_number", f"CHK-{int(pd.Timestamp.now().timestamp())}"),
            data.get("ifsc_code", "Unknown"),
            data.get("micr_code", "Unknown"),
            data.get("cheque_date", "0000-00-00"),
            data.get("account_number", "Unknown"),
            data.get("signature_verified"),
        )

        cursor.execute(query, values)
        conn.commit()

        cursor.close()
        conn.close()
        return True

    except mysql.connector.Error as e:
        st.error(f"Database Error: {e}")
        return False

    #except mysql.connector.IntegrityError as e:
        #st.error(f"Duplicate entry error: {e}")
        #conn.rollback()

    #except Exception as e:
        #st.error(f"Database Error: {e}")
        #return False
    #finally:
        #if conn.is_connected():
         #   conn.close()
    #return False

def get_all_cheques():
    """
    Fetch all stored cheque records.
    """
    conn = mysql.connector.connect(**DB_CONFIG)
    if conn is None:
        print("❌ Cannot fetch data, no database connection.")
        return []

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cheques ORDER BY id DESC LIMIT 10")
    cheques = cursor.fetchall()
    cursor.close()
    conn.close()
    return cheques

# ✅ New functions for dashboard statistics
def get_total_checks():
    """
    Get the total number of cheques.
    """
    conn = mysql.connector.connect(**DB_CONFIG)
    if conn is None:
        return 0

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM cheques")
    total = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return total

def get_recent_checks(limit=3):
    """
    Fetch the most recent cheque processing records.
    """
    conn = mysql.connector.connect(**DB_CONFIG)
    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, status, timestamp FROM cheques ORDER BY timestamp DESC LIMIT %s", (limit,))
    recent_checks = cursor.fetchall()
    cursor.close()
    conn.close()
    return recent_checks