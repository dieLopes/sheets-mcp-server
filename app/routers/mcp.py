import json
from pathlib import Path
from fastapi import APIRouter
from fastapi.responses import JSONResponse


router = APIRouter()

@router.get("/mcp.json")
def manifest():
    path = Path(__file__).parent.parent / "mcp.json"
    with open(path) as f:
        data = json.load(f)
    return JSONResponse(content=data)