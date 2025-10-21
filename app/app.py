from fastapi import FastAPI
from app.routers import mcp, sheets

app = FastAPI(
    servers=[
        {'url': 'http://localhost:8080', 'description': 'Local Server'}
    ]
)

app.include_router(sheets.router)
app.include_router(mcp.router)