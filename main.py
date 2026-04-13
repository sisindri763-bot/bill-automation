# from fastapi import FastAPI
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# import os
# import json
# from datetime import datetime

# app = FastAPI()

# # ✅ Load credentials (works for both local + deploy)
# if os.getenv("GOOGLE_CREDENTIALS"):
#     creds_dict = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
#     creds = service_account.Credentials.from_service_account_info(creds_dict)
# else:
#     creds = service_account.Credentials.from_service_account_file("credentials.json")

# service = build("sheets", "v4", credentials=creds)

# SPREADSHEET_ID = "1Wt5QuN46nce3dbPKMRCp2HdpZFMfqAnBvGioKHh3gnU"

# # ✅ Ensure headers
# def ensure_headers():
#     result = service.spreadsheets().values().get(
#         spreadsheetId=SPREADSHEET_ID,
#         range="Sheet1!A1:G1"
#     ).execute()

#     if "values" not in result:
#         headers = [[
#             "Date", "Vendor", "Amount", "Category",
#             "GST", "Invoice No", "Notes"
#         ]]

#         service.spreadsheets().values().update(
#             spreadsheetId=SPREADSHEET_ID,
#             range="Sheet1!A1:G1",
#             valueInputOption="RAW",
#             body={"values": headers}
#         ).execute()

# # ✅ Root check
# @app.get("/")
# def home():
#     return {"message": "API is running 🚀"}

# # ✅ Add bill API
# @app.post("/add-bill")
# def add_bill(data: dict):
#     try:
#         ensure_headers()

#         row = [[
#             data.get("date", datetime.now().strftime("%Y-%m-%d")),
#             data.get("vendor"),
#             data.get("amount"),
#             data.get("category"),
#             data.get("gst"),
#             data.get("invoice"),
#             data.get("notes", "Auto")
#         ]]

#         service.spreadsheets().values().append(
#             spreadsheetId=SPREADSHEET_ID,
#             range="Sheet1!A:G",
#             valueInputOption="USER_ENTERED",
#             body={"values": row}
#         ).execute()

#         return {"success": True}

#     except Exception as e:
#         return {"error": str(e)}


# from fastapi import FastAPI
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# import os
# import json
# from datetime import datetime

# app = FastAPI()

# # ✅ Load credentials
# if os.getenv("GOOGLE_CREDENTIALS"):
#     creds_dict = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
#     creds = service_account.Credentials.from_service_account_info(creds_dict)
# else:
#     creds = service_account.Credentials.from_service_account_file("credentials.json")

# service = build("sheets", "v4", credentials=creds)

# SPREADSHEET_ID = "1Wt5QuN46nce3dbPKMRCp2HdpZFMfqAnBvGioKHh3gnU"

# # ✅ All headers from your CSV
# HEADERS = [
#     "Bill Date","Bill Number","PurchaseOrder","Bill Status","Source of Supply","Destination of Supply",
#     "GST Treatment","GST Identification Number (GSTIN)","Is Inclusive Tax","TDS Percentage","TDS Amount",
#     "TDS Section Code","TDS Name","Vendor Name","Due Date","Currency Code","Exchange Rate","Attachment ID",
#     "Attachment Preview ID","Attachment Name","Attachment Type","Attachment Size","Item Name","SKU",
#     "Item Description","Account","Usage unit","Quantity","Rate","Adjustment","Item Type","Tax Name",
#     "Tax Percentage","Tax Amount","Tax Type","Item Exemption Code","Reverse Charge Tax Name",
#     "Reverse Charge Tax Rate","Reverse Charge Tax Type","Item Total","SubTotal","Total","Balance",
#     "Vendor Notes","Terms & Conditions","Payment Terms","Payment Terms Label","Is Billable","Customer Name",
#     "Project Name","Purchase Order Number","Is Discount Before Tax","Entity Discount Amount","Discount Account",
#     "Is Landed Cost","Warehouse Name","Branch Name","CF.Transporte_Name","TCS Tax Name","TCS Percentage",
#     "Nature Of Collection","TCS Amount","HSN/SAC","Supply Type","ITC Eligibility"
# ]

# # ✅ Helper to convert column number to Sheets column name
# def colnum_to_colname(n: int) -> str:
#     """Convert column number (1-based) to Excel/Sheets column name."""
#     name = ""
#     while n > 0:
#         n, remainder = divmod(n - 1, 26)
#         name = chr(65 + remainder) + name
#     return name

# # ✅ Ensure headers
# def ensure_headers():
#     last_col = colnum_to_colname(len(HEADERS))  # e.g. 63 → "BK"
#     service.spreadsheets().values().update(
#         spreadsheetId=SPREADSHEET_ID,
#         range=f"Sheet1!A1:{last_col}1",
#         valueInputOption="RAW",
#         body={"values": [HEADERS]}
#     ).execute()

# # ✅ Root check
# @app.get("/")
# def home():
#     return {"message": "API is running 🚀"}

# # ✅ Add bill API
# @app.post("/add-bill")
# def add_bill(data: dict):
#     try:
#         ensure_headers()

#         # Build row in the same order as HEADERS
#         row = [[data.get(h.lower().replace(" ", "_"), "") for h in HEADERS]]

#         last_col = colnum_to_colname(len(HEADERS))
#         service.spreadsheets().values().append(
#             spreadsheetId=SPREADSHEET_ID,
#             range=f"Sheet1!A:{last_col}",
#             valueInputOption="USER_ENTERED",
#             body={"values": row}
#         ).execute()

#         return {"success": True}

#     except Exception as e:
#         return {"error": str(e)}

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import json

app = FastAPI()

# ✅ Load credentials
try:
    if os.getenv("GOOGLE_CREDENTIALS"):
        creds_dict = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
        creds = service_account.Credentials.from_service_account_info(creds_dict)
    else:
        creds = service_account.Credentials.from_service_account_file("credentials.json")

    service = build("sheets", "v4", credentials=creds)

except Exception as e:
    print("❌ Google Auth Error:", str(e))
    service = None

SPREADSHEET_ID = "1Wt5QuN46nce3dbPKMRCp2HdpZFMfqAnBvGioKHh3gnU"

HEADERS = [
    "Bill Date","Bill Number","PurchaseOrder","Bill Status","Source of Supply","Destination of Supply",
    "GST Treatment","GST Identification Number (GSTIN)","Is Inclusive Tax","TDS Percentage","TDS Amount",
    "TDS Section Code","TDS Name","Vendor Name","Due Date","Currency Code","Exchange Rate","Attachment ID",
    "Attachment Preview ID","Attachment Name","Attachment Type","Attachment Size","Item Name","SKU",
    "Item Description","Account","Usage unit","Quantity","Rate","Adjustment","Item Type","Tax Name",
    "Tax Percentage","Tax Amount","Tax Type","Item Exemption Code","Reverse Charge Tax Name",
    "Reverse Charge Tax Rate","Reverse Charge Tax Type","Item Total","SubTotal","Total","Balance",
    "Vendor Notes","Terms & Conditions","Payment Terms","Payment Terms Label","Is Billable","Customer Name",
    "Project Name","Purchase Order Number","Is Discount Before Tax","Entity Discount Amount","Discount Account",
    "Is Landed Cost","Warehouse Name","Branch Name","CF.Transporte_Name","TCS Tax Name","TCS Percentage",
    "Nature Of Collection","TCS Amount","HSN/SAC","Supply Type","ITC Eligibility"
]

# ✅ Convert column number → column name (A, B, C... AA, AB...)
def colnum_to_colname(n: int) -> str:
    name = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        name = chr(65 + remainder) + name
    return name

# ✅ Ensure headers exist
def ensure_headers():
    if not service:
        raise Exception("Google Sheets service not initialized")

    last_col = colnum_to_colname(len(HEADERS))
    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f"Sheet1!A1:{last_col}1",
        valueInputOption="RAW",
        body={"values": [HEADERS]}
    ).execute()

# ✅ Root route
@app.get("/")
def home():
    return {"success": True, "message": "API is running 🚀"}

# ✅ Health check (useful for Render)
@app.get("/health")
def health():
    return {"status": "ok"}

# ✅ Main API
@app.post("/add-bill")
def add_bill(data: dict):
    try:
        print("📥 Incoming data:", data)

        if not service:
            return JSONResponse(
                status_code=500,
                content={"success": False, "error": "Google Sheets not initialized"}
            )

        ensure_headers()

        # ✅ Normalize keys
        normalized_data = {k.lower(): v for k, v in data.items()}

        # ✅ Build row safely
        row = [
            [
                normalized_data.get(h.lower().replace(" ", "_"), "")
                for h in HEADERS
            ]
        ]

        print("📤 Row to insert:", row)

        last_col = colnum_to_colname(len(HEADERS))

        service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=f"Sheet1!A:{last_col}",
            valueInputOption="USER_ENTERED",
            body={"values": row}
        ).execute()

        return JSONResponse(content={"success": True})

    except Exception as e:
        print("❌ ERROR:", str(e))
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )