from typing import Dict, Callable, Any
from app.models.tool import Tool

class ToolRegistry:
    """Registry for managing tools"""
    
    def __init__(self):
        self._tools: Dict[str, Tool] = {}
    
    def register(self, name: str, description: str, function: Callable) -> None:
        """Register a new tool"""
        self._tools[name] = Tool(name=name, description=description, function=function)
    
    def get_tool(self, name: str) -> Tool:
        """Get a tool by name"""
        if name not in self._tools:
            raise ValueError(f"Tool '{name}' not found")
        return self._tools[name]
    
    def list_tools(self) -> Dict[str, Tool]:
        """List all registered tools"""
        return self._tools.copy()
    
    def call_tool(self, name: str, *args, **kwargs) -> Any:
        """Call a tool by name"""
        tool = self.get_tool(name)
        return tool.function(*args, **kwargs)

# Global tool registry instance
tool_registry = ToolRegistry()
