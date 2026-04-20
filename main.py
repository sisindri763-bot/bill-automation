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

# from fastapi import FastAPI
# from fastapi.responses import JSONResponse
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# import os
# import json

# app = FastAPI()

# # ✅ Load credentials
# try:
#     if os.getenv("GOOGLE_CREDENTIALS"):
#         creds_dict = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
#         creds = service_account.Credentials.from_service_account_info(creds_dict)
#     else:
#         creds = service_account.Credentials.from_service_account_file("credentials.json")

#     service = build("sheets", "v4", credentials=creds)

# except Exception as e:
#     print("❌ Google Auth Error:", str(e))
#     service = None

# SPREADSHEET_ID = "1Wt5QuN46nce3dbPKMRCp2HdpZFMfqAnBvGioKHh3gnU"

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

# # ✅ Convert column number → column name (A, B, C... AA, AB...)
# def colnum_to_colname(n: int) -> str:
#     name = ""
#     while n > 0:
#         n, remainder = divmod(n - 1, 26)
#         name = chr(65 + remainder) + name
#     return name

# # ✅ Ensure headers exist
# def ensure_headers():
#     if not service:
#         raise Exception("Google Sheets service not initialized")

#     last_col = colnum_to_colname(len(HEADERS))
#     service.spreadsheets().values().update(
#         spreadsheetId=SPREADSHEET_ID,
#         range=f"Sheet1!A1:{last_col}1",
#         valueInputOption="RAW",
#         body={"values": [HEADERS]}
#     ).execute()

# # ✅ Root route
# @app.get("/")
# def home():
#     return {"success": True, "message": "API is running 🚀"}

# # ✅ Health check (useful for Render)
# @app.get("/health")
# def health():
#     return {"status": "ok"}

# # ✅ Main API
# @app.post("/add-bill")
# def add_bill(data: dict):
#     try:
#         print("📥 Incoming data:", data)

#         if not service:
#             return JSONResponse(
#                 status_code=500,
#                 content={"success": False, "error": "Google Sheets not initialized"}
#             )

#         ensure_headers()

#         # ✅ Normalize keys
#         normalized_data = {k.lower(): v for k, v in data.items()}

#         # ✅ Build row safely
#         row = [
#             [
#                 normalized_data.get(h.lower().replace(" ", "_"), "")
#                 for h in HEADERS
#             ]
#         ]

#         print("📤 Row to insert:", row)

#         last_col = colnum_to_colname(len(HEADERS))

#         service.spreadsheets().values().append(
#             spreadsheetId=SPREADSHEET_ID,
#             range=f"Sheet1!A:{last_col}",
#             valueInputOption="USER_ENTERED",
#             body={"values": row}
#         ).execute()

#         return JSONResponse(content={"success": True})

#     except Exception as e:
#         print("❌ ERROR:", str(e))
#         return JSONResponse(
#             status_code=500,
#             content={"success": False, "error": str(e)}
#         )


# from fastapi import FastAPI
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# import os
# import json

# app = FastAPI()

# # ✅ Load credentials
# if os.getenv("GOOGLE_CREDENTIALS"):
#     creds_dict = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
#     creds = service_account.Credentials.from_service_account_info(creds_dict)
# else:
#     creds = service_account.Credentials.from_service_account_file("credentials.json")

# service = build("sheets", "v4", credentials=creds)

# SPREADSHEET_ID = "1Wt5QuN46nce3dbPKMRCp2HdpZFMfqAnBvGioKHh3gnU"

# # ✅ All 63 headers
# HEADERS = [
#     "Bill Date", "Bill Number", "PurchaseOrder", "Bill Status", "Source of Supply", "Destination of Supply",
#     "GST Treatment", "GST Identification Number (GSTIN)", "Is Inclusive Tax", "TDS Percentage", "TDS Amount",
#     "TDS Section Code", "TDS Name", "Vendor Name", "Due Date", "Currency Code", "Exchange Rate", "Attachment ID",
#     "Attachment Preview ID", "Attachment Name", "Attachment Type", "Attachment Size", "Item Name", "SKU",
#     "Item Description", "Account", "Usage unit", "Quantity", "Rate", "Adjustment", "Item Type", "Tax Name",
#     "Tax Percentage", "Tax Amount", "Tax Type", "Item Exemption Code", "Reverse Charge Tax Name",
#     "Reverse Charge Tax Rate", "Reverse Charge Tax Type", "Item Total", "SubTotal", "Total", "Balance",
#     "Vendor Notes", "Terms & Conditions", "Payment Terms", "Payment Terms Label", "Is Billable", "Customer Name",
#     "Project Name", "Purchase Order Number", "Is Discount Before Tax", "Entity Discount Amount", "Discount Account",
#     "Is Landed Cost", "Warehouse Name", "Branch Name", "CF.Transporte_Name", "TCS Tax Name", "TCS Percentage",
#     "Nature Of Collection", "TCS Amount", "HSN/SAC", "Supply Type", "ITC Eligibility"
# ]


# def normalize_key(header: str) -> str:
#     """
#     Normalize a header string to a consistent snake_case key.
#     Strips all non-alphanumeric characters (except underscore), lowercases, collapses spaces to _.
#     Matches the normalization used in the vgen script.
#     """
#     import re
#     return re.sub(r'[^a-z0-9]+', '_', header.lower()).strip('_')


# # Pre-build a mapping: normalized_key -> header display name
# HEADER_KEY_MAP = {normalize_key(h): h for h in HEADERS}


# def colnum_to_colname(n: int) -> str:
#     """Convert 1-based column number to Sheets column letter(s)."""
#     name = ""
#     while n > 0:
#         n, remainder = divmod(n - 1, 26)
#         name = chr(65 + remainder) + name
#     return name


# def ensure_headers():
#     last_col = colnum_to_colname(len(HEADERS))
#     service.spreadsheets().values().update(
#         spreadsheetId=SPREADSHEET_ID,
#         range=f"Sheet1!A1:{last_col}1",
#         valueInputOption="RAW",
#         body={"values": [HEADERS]}
#     ).execute()


# @app.get("/")
# def home():
#     return {"message": "API is running 🚀"}


# @app.post("/add-bill")
# def add_bill(data: dict):
#     try:
#         ensure_headers()

#         # Build row using normalized key lookup — same normalization as vgen
#         row = [[data.get(normalize_key(h), "") for h in HEADERS]]

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



# import re
# import os
# import json

# from fastapi import FastAPI
# from fastapi.responses import JSONResponse
# from google.oauth2 import service_account
# from googleapiclient.discovery import build

# app = FastAPI()

# # ── Credentials ──────────────────────────────────────────────────────────────
# if os.getenv("GOOGLE_CREDENTIALS"):
#     creds = service_account.Credentials.from_service_account_info(
#         json.loads(os.getenv("GOOGLE_CREDENTIALS"))
#     )
# else:
#     creds = service_account.Credentials.from_service_account_file("credentials.json")

# service = build("sheets", "v4", credentials=creds)

# SPREADSHEET_ID = "1Wt5QuN46nce3dbPKMRCp2HdpZFMfqAnBvGioKHh3gnU"

# HEADERS = [
#     "Bill Date", "Bill Number", "PurchaseOrder", "Bill Status", "Source of Supply", "Destination of Supply",
#     "GST Treatment", "GST Identification Number (GSTIN)", "Is Inclusive Tax", "TDS Percentage", "TDS Amount",
#     "TDS Section Code", "TDS Name", "Vendor Name", "Due Date", "Currency Code", "Exchange Rate", "Attachment ID",
#     "Attachment Preview ID", "Attachment Name", "Attachment Type", "Attachment Size", "Item Name", "SKU",
#     "Item Description", "Account", "Usage unit", "Quantity", "Rate", "Adjustment", "Item Type", "Tax Name",
#     "Tax Percentage", "Tax Amount", "Tax Type", "Item Exemption Code", "Reverse Charge Tax Name",
#     "Reverse Charge Tax Rate", "Reverse Charge Tax Type", "Item Total", "SubTotal", "Total", "Balance",
#     "Vendor Notes", "Terms & Conditions", "Payment Terms", "Payment Terms Label", "Is Billable", "Customer Name",
#     "Project Name", "Purchase Order Number", "Is Discount Before Tax", "Entity Discount Amount", "Discount Account",
#     "Is Landed Cost", "Warehouse Name", "Branch Name", "CF.Transporte_Name", "TCS Tax Name", "TCS Percentage",
#     "Nature Of Collection", "TCS Amount", "HSN/SAC", "Supply Type", "ITC Eligibility"
# ]

# # FIX 3: normalize_key no longer imports re on every call — re is imported at top level
# def normalize_key(h: str) -> str:
#     return re.sub(r'[^a-z0-9]+', '_', h.lower()).strip('_')

# # FIX 5: pre-compute normalized keys and last column once at startup — not on every request
# NORMALIZED_KEYS = [normalize_key(h) for h in HEADERS]

# def colnum_to_colname(n: int) -> str:
#     name = ""
#     while n > 0:
#         n, remainder = divmod(n - 1, 26)
#         name = chr(65 + remainder) + name
#     return name

# LAST_COL = colnum_to_colname(len(HEADERS))  # computed once at startup

# # FIX 1: headers_initialized flag — ensure_headers() runs only once per server lifetime,
# # not on every POST request (saves 1 Google Sheets API call per bill upload)
# headers_initialized = False

# def ensure_headers():
#     global headers_initialized
#     if headers_initialized:
#         return
#     service.spreadsheets().values().update(
#         spreadsheetId=SPREADSHEET_ID,
#         range=f"Sheet1!A1:{LAST_COL}1",
#         valueInputOption="RAW",
#         body={"values": [HEADERS]}
#     ).execute()
#     headers_initialized = True


# @app.get("/")
# def home():
#     return {"message": "API is running 🚀"}


# @app.post("/add-bill")
# def add_bill(data: dict):
#     try:
#         ensure_headers()

#         row = [[data.get(k, "") for k in NORMALIZED_KEYS]]

#         service.spreadsheets().values().append(
#             spreadsheetId=SPREADSHEET_ID,
#             range=f"Sheet1!A:{LAST_COL}",
#             valueInputOption="USER_ENTERED",
#             body={"values": row}
#         ).execute()

#         return {"success": True}

#     except Exception as e:
#         # FIX 2: return HTTP 500 so the vgen client can detect failure by status code
#         return JSONResponse(status_code=500, content={"success": False, "error": str(e)})




# import re
# import os
# import json
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# from typing import List, Union
# from google.oauth2 import service_account
# from googleapiclient.discovery import build

# app = FastAPI()

# # ── CORS ─────────────────────────────────────
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ── Google Credentials ───────────────────────
# google_creds_env = os.getenv("GOOGLE_CREDENTIALS")

# if google_creds_env:
#     creds = service_account.Credentials.from_service_account_info(
#         json.loads(google_creds_env)
#     )
# else:
#     creds = service_account.Credentials.from_service_account_file("credentials.json")

# service = build("sheets", "v4", credentials=creds)

# SPREADSHEET_ID = "1Wt5QuN46nce3dbPKMRCp2HdpZFMfqAnBvGioKHh3gnU"

# # ── HEADERS ──────────────────────────────────
# HEADERS = [
#     "Bill Date", "Bill Number", "PurchaseOrder", "Bill Status", "Source of Supply", "Destination of Supply",
#     "GST Treatment", "GST Identification Number (GSTIN)", "Is Inclusive Tax", "TDS Percentage", "TDS Amount",
#     "TDS Section Code", "TDS Name", "Vendor Name", "Due Date", "Currency Code", "Exchange Rate",
#     "Attachment Type", "Item Name", "SKU", "Item Description", "Account",
#     "Quantity", "Rate", "Adjustment", "Item Type", "Tax Name", "Tax Percentage",
#     "Tax Amount", "Tax Type", "Item Exemption Code", "Item Total",
#     "SubTotal", "Total", "Balance", "Vendor Notes", "Terms & Conditions", "Payment Terms Label"
# ]

# # ── Normalize Keys ───────────────────────────
# def normalize_key(h: str) -> str:
#     return re.sub(r'[^a-z0-9]+', '_', h.lower()).strip('_')

# NORMALIZED_KEYS = [normalize_key(h) for h in HEADERS]

# # ── Column Name Generator ────────────────────
# def colnum_to_colname(n: int) -> str:
#     name = ""
#     while n > 0:
#         n, remainder = divmod(n - 1, 26)
#         name = chr(65 + remainder) + name
#     return name

# LAST_COL = colnum_to_colname(len(HEADERS))

# # ── Header Init ──────────────────────────────
# _headers_initialized = False

# def ensure_headers():
#     global _headers_initialized
#     if _headers_initialized:
#         return
#     service.spreadsheets().values().update(
#         spreadsheetId=SPREADSHEET_ID,
#         range=f"Sheet1!A1:{LAST_COL}1",
#         valueInputOption="RAW",
#         body={"values": [HEADERS]}
#     ).execute()
#     _headers_initialized = True

# # ── Build Row ────────────────────────────────
# def build_row(data: dict) -> list:
#     return [data.get(k, "") for k in NORMALIZED_KEYS]

# # ── Normalize Input Keys ─────────────────────
# def normalize_input(data: dict) -> dict:
#     normalized = {}
#     for k, v in data.items():
#         nk = normalize_key(k)
#         normalized[nk] = v
#     return normalized

# # ── Routes ───────────────────────────────────

# @app.get("/")
# def home():
#     return {"message": "Invoice API running 🚀"}


# # ✅ SINGLE + MULTIPLE (SMART ENDPOINT)
# @app.post("/add-bills")
# def add_bills(payload: Union[List[dict]]):

#     if not payload:
#         return JSONResponse(status_code=400, content={"success": False, "error": "Empty payload"})

#     try:
#         ensure_headers()

#         # 🔥 Accept BOTH single and list
#         if isinstance(payload, dict):
#             bills = [payload]
#         else:
#             bills = payload

#         rows = [build_row(normalize_input(b)) for b in bills]

#         service.spreadsheets().values().append(
#             spreadsheetId=SPREADSHEET_ID,
#             range=f"Sheet1!A:{LAST_COL}",
#             valueInputOption="USER_ENTERED",
#             body={"values": rows}
#         ).execute()

#         return {"success": True, "inserted": len(rows)}

#     except Exception as e:
#         return JSONResponse(status_code=500, content={"success": False, "error": str(e)})



import re
import os
import json
from typing import List, Dict, Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from google.oauth2 import service_account
from googleapiclient.discovery import build


app = FastAPI()

# ── CORS ─────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Google Credentials ───────────────────────
google_creds_env = os.getenv("GOOGLE_CREDENTIALS")

if google_creds_env:
    creds = service_account.Credentials.from_service_account_info(
        json.loads(google_creds_env)
    )
else:
    creds = service_account.Credentials.from_service_account_file("credentials.json")

service = build("sheets", "v4", credentials=creds)

SPREADSHEET_ID = "1Wt5QuN46nce3dbPKMRCp2HdpZFMfqAnBvGioKHh3gnU"

# ── HEADERS ──────────────────────────────────
HEADERS = [
    "Bill Date", "Bill Number", "PurchaseOrder", "Bill Status", "Source of Supply",
    "Destination of Supply", "GST Treatment", "GST Identification Number (GSTIN)",
    "Is Inclusive Tax", "TDS Percentage", "TDS Amount", "TDS Section Code",
    "TDS Name", "Vendor Name", "Due Date", "Currency Code", "Exchange Rate",
    "Attachment Type", "Item Name", "SKU", "Item Description", "Account",
    "Quantity", "Rate", "Adjustment", "Item Type", "Tax Name", "Tax Percentage",
    "Tax Amount", "Tax Type", "Item Exemption Code", "Item Total",
    "SubTotal", "Total", "Balance", "Vendor Notes", "Terms & Conditions",
    "Payment Terms Label"
]

# ── Normalize Keys ───────────────────────────
def normalize_key(h: str) -> str:
    return re.sub(r'[^a-z0-9]+', '_', h.lower()).strip('_')

NORMALIZED_KEYS = [normalize_key(h) for h in HEADERS]

# ── Column Generator ─────────────────────────
def colnum_to_colname(n: int) -> str:
    name = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        name = chr(65 + remainder) + name
    return name

LAST_COL = colnum_to_colname(len(HEADERS))

# ── Ensure Headers Exist ─────────────────────
_headers_initialized = False

def ensure_headers():
    global _headers_initialized
    if _headers_initialized:
        return

    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f"Sheet1!A1:{LAST_COL}1",
        valueInputOption="RAW",
        body={"values": [HEADERS]}
    ).execute()

    _headers_initialized = True

# ── Normalize Input ──────────────────────────
def normalize_input(data: Dict[str, Any]) -> Dict[str, Any]:
    return {normalize_key(k): v for k, v in data.items()}

# ── Build Row ────────────────────────────────
def build_row(data: Dict[str, Any]) -> List[Any]:
    data = normalize_input(data)
    return [data.get(k, "") for k in NORMALIZED_KEYS]

# ── Check if row is empty ────────────────────
def is_empty_row(row: List[Any]) -> bool:
    return all(v in ("", None) for v in row)

# ── Routes ───────────────────────────────────

@app.get("/")
def home():
    return {"message": "Invoice API running 🚀"}

# ── MAIN ENDPOINT ────────────────────────────
@app.post("/add-bills")
def add_bills(payload: List[Dict[str, Any]]):

    if not payload:
        return JSONResponse(
            status_code=400,
            content={"success": False, "error": "Empty payload"}
        )

    try:
        ensure_headers()

        # ✅ Build rows and skip empty ones
        rows = []
        for item in payload:
            row = build_row(item)
            if not is_empty_row(row):
                rows.append(row)

        if not rows:
            return {
                "success": False,
                "error": "No valid data to insert"
            }

        service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=f"Sheet1!A:{LAST_COL}",
            valueInputOption="USER_ENTERED",
            body={"values": rows}
        ).execute()

        return {
            "success": True,
            "inserted": len(rows)
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )