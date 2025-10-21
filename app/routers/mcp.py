from fastapi import APIRouter
from app.services.mcp_services import McpService

router = APIRouter()


@router.get("/mcp.json")
def manifest():
    return McpService.manifest()