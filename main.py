from dotenv import load_dotenv
from fastapi import FastAPI
from routers import router


load_dotenv()

app = FastAPI("MCP Sheets Server")

app.include_router(router.router)