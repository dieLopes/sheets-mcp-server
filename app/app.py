from fastapi import FastAPI
from app.routers import mcp, sheets
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(
    servers=[
        {'url': 'http://localhost:8000', 'description': 'Local Server'}
    ]
)

app.include_router(sheets.router)
app.include_router(mcp.router)