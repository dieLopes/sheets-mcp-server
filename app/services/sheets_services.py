import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from app.models.model import MCPRequest, MCPResponse, ActionType

SHEET_NAME = os.getenv("SHEET_NAME")
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH")

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIALS_PATH, scope)
client = gspread.authorize(creds)


class SheetService:

    @staticmethod
    def execute(request: MCPRequest) -> MCPResponse:
        try:
            sheet = client.open(SHEET_NAME).worksheet(request.tab)
        except Exception as e:
            return MCPResponse(status="error", message=f"Error accessing sheet/tab: {str(e)}")

        if request.action == ActionType.READ.value:
            rows = sheet.get_all_records()
            return MCPResponse(status="ok", data=rows)

        elif request.action == ActionType.WRITE.value:
            if not request.data:
                return MCPResponse(status="error", message="No data provided for WRITE action")
            sheet.append_row(list(request.data[0].values()))
            return MCPResponse(status="ok", message="Row added successfully")

        elif request.action == ActionType.UPDATE.value:
            if not request.data:
                return MCPResponse(status="error", message="No data provided for UPDATE action")
            payload = request.data[0]
            sheet.update_cell(payload["row"], payload["col"], payload["value"])
            return MCPResponse(status="ok", message="Cell updated successfully")

        elif request.action == ActionType.DELETE.value:
            if not request.data:
                return MCPResponse(status="error", message="No data provided for DELETE action")
            payload = request.data[0]
            sheet.delete_row(payload["row"])
            return MCPResponse(status="ok", message="Row deleted successfully")

        return MCPResponse(status="error", message="Invalid action specified")
