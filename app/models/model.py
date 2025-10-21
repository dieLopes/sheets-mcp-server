from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel


class MCPRequest(BaseModel):
    action: str
    tab: str
    data: Optional[list[dict[str, Any]]] = None


class MCPResponse(BaseModel):
    status: str
    message: Optional[str] = None
    data: Optional[list[dict[str, Any]]] = None


class ActionType(Enum):
    READ = "read"
    WRITE = "write"
    UPDATE = "update"
    DELETE = "delete"