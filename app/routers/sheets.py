from fastapi import APIRouter
from app.models.model import MCPRequest, MCPResponse
from app.services.sheets_services import SheetService

router = APIRouter()

@router.post("/execute", response_model=MCPResponse)
async def execute_sheet_operation(request: MCPRequest):
    return SheetService.execute(request)
