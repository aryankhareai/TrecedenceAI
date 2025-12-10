from pydantic import BaseModel, Field
from typing import Dict, Callable, Any, Optional, List, Union
from enum import Enum

class NodeType(str, Enum):
    FUNCTION = "function"
    CONDITION = "condition"
    LOOP = "loop"

class Node(BaseModel):
    """Represents a node in the workflow graph"""
    id: str
    name: str
    type: NodeType = NodeType.FUNCTION
    function: Optional[str] = None  # Function name to call
    condition: Optional[str] = None  # Condition for branching
    loop_condition: Optional[str] = None  # Condition for looping
    max_iterations: int = 10  # Max iterations for loop nodes
    
class Edge(BaseModel):
    """Represents an edge between nodes"""
    from_node: str
    to_node: str
    condition: Optional[str] = None  # Optional condition for conditional edges

class Graph(BaseModel):
    """Represents a workflow graph"""
    id: str
    name: str
    nodes: Dict[str, Node]
    edges: List[Edge]
    start_node: str
    
    def get_next_nodes(self, current_node: str, state: "State") -> List[str]:
        """Get the next nodes based on current node and state"""
        next_nodes = []
        for edge in self.edges:
            if edge.from_node == current_node:
                if edge.condition is None:
                    next_nodes.append(edge.to_node)
                else:
                    # Evaluate condition
                    try:
                        # Simple condition evaluation - in a real system, you might want a safer approach
                        if eval(edge.condition, {}, {"state": state}):
                            next_nodes.append(edge.to_node)
                    except Exception as e:
                        # Log error but continue
                        pass
        return next_nodes
    
    def get_node(self, node_id: str) -> Optional[Node]:
        """Get a node by ID"""
        return self.nodes.get(node_id)
