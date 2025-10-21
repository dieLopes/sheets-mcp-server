import json
from pathlib import Path

from fastapi.responses import JSONResponse


class McpService:

    @staticmethod
    def manifest() -> JSONResponse:
        path = Path(__file__).parent.parent.parent / "mcp.json"
        with open(path) as f:
            data = json.load(f)
        return JSONResponse(content=data)