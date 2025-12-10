from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class State(BaseModel):
    """Base state model for workflows"""
    data: Dict[str, Any] = Field(default_factory=dict)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the state"""
        return self.data.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a value in the state"""
        self.data[key] = value
    
    def update(self, updates: Dict[str, Any]) -> None:
        """Update the state with multiple values"""
        self.data.update(updates)

class WorkflowState(State):
    """State for workflow execution"""
    workflow_id: Optional[str] = None
    run_id: Optional[str] = None
    current_node: Optional[str] = None
    execution_log: list = Field(default_factory=list)
    is_complete: bool = False
    error: Optional[str] = None
