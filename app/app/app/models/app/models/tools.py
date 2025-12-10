from pydantic import BaseModel
from typing import Callable, Any

class Tool(BaseModel):
    """Represents a tool that can be called by nodes"""
    name: str
    description: str
    function: Callable

    class Config:
        arbitrary_types_allowed = True
