from fastapi import FastAPI
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import json
from datetime import datetime

app = FastAPI()

# ✅ Load credentials (works for both local + deploy)
if os.getenv("GOOGLE_CREDENTIALS"):
    creds_dict = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
    creds = service_account.Credentials.from_service_account_info(creds_dict)
else:
    creds = service_account.Credentials.from_service_account_file("credentials.json")

service = build("sheets", "v4", credentials=creds)

SPREADSHEET_ID = "1Wt5QuN46nce3dbPKMRCp2HdpZFMfqAnBvGioKHh3gnU"

# ✅ Ensure headers
def ensure_headers():
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range="Sheet1!A1:G1"
    ).execute()

    if "values" not in result:
        headers = [[
            "Date", "Vendor", "Amount", "Category",
            "GST", "Invoice No", "Notes"
        ]]

        service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range="Sheet1!A1:G1",
            valueInputOption="RAW",
            body={"values": headers}
        ).execute()

# ✅ Root check
@app.get("/")
def home():
    return {"message": "API is running 🚀"}

# ✅ Add bill API
@app.post("/add-bill")
def add_bill(data: dict):
    try:
        ensure_headers()

        row = [[
            data.get("date", datetime.now().strftime("%Y-%m-%d")),
            data.get("vendor"),
            data.get("amount"),
            data.get("category"),
            data.get("gst"),
            data.get("invoice"),
            data.get("notes", "Auto")
        ]]

        service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range="Sheet1!A:G",
            valueInputOption="USER_ENTERED",
            body={"values": row}
        ).execute()

        return {"success": True}

    except Exception as e:
        return {"error": str(e)}