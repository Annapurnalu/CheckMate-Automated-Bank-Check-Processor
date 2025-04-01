import re
from dateutil import parser
import pandas as pd

def clean_text(text):
    if isinstance(text, str):
        return re.sub(r'[:*"()]+', '', text).strip()
    return text


def format_extracted_text(response):
    formatted_data = {}
    pattern = re.compile(r"\*?\s*(\w[\w\s]+)\s*(.+)")
    matches = pattern.findall(response)

    for key, value in matches:
        formatted_data[key.strip().lower().replace(" ", "_")] = clean_text(value)

    required_fields = ["payee_name", "amount", "bank_name", "branch_name", "cheque_number", "ifsc_code", "micr_code", "cheque_date", "account_number", "signature_verified"]

    for field in required_fields:
        if field not in formatted_data:
            formatted_data[field] = "Unknown" if field != "amount" else "0.00"

    formatted_data["amount"] = re.sub(r'[^0-9.]', '', formatted_data["amount"])

    # ✅ Cheque Date Parsing
    if formatted_data["cheque_date"] and formatted_data["cheque_date"].lower() != "unknown":
        try:
            parsed_date = parser.parse(formatted_data["cheque_date"], dayfirst=True)  # Ensure day-first parsing
            formatted_data["cheque_date"] = parsed_date.strftime("%Y-%m-%d")  # Standardized format
        except (ValueError, TypeError) as e:
            print(f"Error parsing cheque date: {formatted_data['cheque_date']} - {e}")  # Debugging log
            formatted_data["cheque_date"] = "0000-00-00"


    # ✅ Signature Verification Logic
    if "signature_verification" in formatted_data:
        signature_text = formatted_data.get("signature_verification", "").strip().lower()
        print("Signature Text Extracted:", signature_text)
        # ✅ Ensure "No" when manual verification is required
        if signature_text in [
        "not possible, as the signature area is empty","Not possible from the image","not possible","not found""missing","unknown","not specified","not available""none","","n/a",
        "requires manual verification indicated by authorised signatories please sign above"]:
            formatted_data["signature_verified"] = "No"
        elif signature_text in ["verified", "Yes", "signature present", "authenticated", "signed by", "authorised signatory", "Present"]:
            formatted_data["signature_verified"] = "Yes"
        elif re.match(r"^[A-Z][a-zA-Z\s.]+$", signature_text) and len(signature_text) > 3:
            formatted_data["signature_verified"] = "Yes"
            print("✅ Signature verified as name")
        elif re.search(r"signature.*present", signature_text, re.IGNORECASE):
            formatted_data["signature_verified"] = "Yes"
        else:
            formatted_data["signature_verified"] = "No"  # Default to No if key is missing
  # Default to No if key is missing

    if "branch" in formatted_data:
        branch_text = formatted_data["branch"].strip()
        print("Extracted Branch:", branch_text)
        if branch_text.lower() in ["unknown", "", "not found"]:
            formatted_data["branch_name"] = "Unknown"
        else:
            branch_names = branch_text.split(" and ")  # Adjust if needed
            formatted_data["branch_name"] = branch_names[0].strip()
    else:
        formatted_data["branch_name"] = "Unknown"  # Default if missing


    if formatted_data["cheque_number"] in ["Unknown", "N/A", "", None]:
        formatted_data["cheque_number"] = f"CHK-{int(pd.Timestamp.now().timestamp())}"  # Unique timestamp-based ID

    return formatted_data

