import os
from urllib import response
from dotenv import load_dotenv
from fastapi import APIRouter
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from models.model import ActionType, MCPRequest, MCPResponse


load_dotenv()

SHEET_NAME= os.getenv("SHEET_NAME")
GOOGLE_CREDENTIALS_PATH= os.getenv("GOOGLE_CREDENTIALS_PATH")

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIALS_PATH, scope)
client = gspread.authorize(creds)

router = APIRouter()

@router.post("/execute", response_model=MCPResponse)
async def execute_sheet_operation(request: MCPRequest):

    try:
        sheet = client.open(SHEET_NAME).worksheet(request.tab)
    except Exception as e:
        return MCPResponse(
            status = "error", 
            message = f"Error accessing sheet/tab: {str(e)}"
        )

    if request.action == ActionType.READ.value:
        rows = sheet.get_all_records()
        return MCPResponse(
            status = "ok", 
            data = rows
        )
    
    elif request.action == ActionType.WRITE.value:
        sheet.append_row(list(request.data.values()))
        return MCPResponse(
            status = "ok", 
            message = "Row added successfully"
        )
    
    elif request.action == ActionType.UPDATE.value:
        sheet.update_cell(request.data["row"], request.data["col"], request.data["value"])
        return MCPResponse(
            status = "ok", 
            message = "Cell updated successfully"
        )
    
    elif request.action == ActionType.DELETE.value:
        sheet.delete_row(request.data["row"])
        return MCPResponse(
            status = "ok", 
            message = "Row deleted successfully"
        )
    
    else:
        return MCPResponse(
            status = "error", 
            message = "Invalid action specified"
        )