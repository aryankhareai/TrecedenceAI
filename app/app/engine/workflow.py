import uuid
from typing import Dict, Any, Optional, List
from app.models.graph import Graph, Node, NodeType
from app.models.state import WorkflowState
from app.engine.tool_registry import tool_registry

class WorkflowEngine:
    """Engine for executing workflow graphs"""
    
    def __init__(self):
        self.graphs: Dict[str, Graph] = {}
        self.runs: Dict[str, WorkflowState] = {}
    
    def register_graph(self, graph: Graph) -> None:
        """Register a new graph"""
        self.graphs[graph.id] = graph
    
    def get_graph(self, graph_id: str) -> Optional[Graph]:
        """Get a graph by ID"""
        return self.graphs.get(graph_id)
    
    def start_run(self, graph_id: str, initial_state: Dict[str, Any]) -> str:
        """Start a new run of a graph"""
        graph = self.get_graph(graph_id)
        if not graph:
            raise ValueError(f"Graph '{graph_id}' not found")
        
        run_id = str(uuid.uuid4())
        state = WorkflowState(
            workflow_id=graph_id,
            run_id=run_id,
            data=initial_state,
            current_node=graph.start_node
        )
        
        self.runs[run_id] = state
        return run_id
    
    def get_run_state(self, run_id: str) -> Optional[WorkflowState]:
        """Get the state of a run"""
        return self.runs.get(run_id)
    
    def execute_step(self, run_id: str) -> bool:
        """Execute a single step of a workflow"""
        state = self.get_run_state(run_id)
        if not state or state.is_complete:
            return False
        
        graph = self.get_graph(state.workflow_id)
        if not graph:
            state.error = f"Graph '{state.workflow_id}' not found"
            state.is_complete = True
            return False
        
        current_node_id = state.current_node
        current_node = graph.get_node(current_node_id)
        
        if not current_node:
            state.error = f"Node '{current_node_id}' not found"
            state.is_complete = True
            return False
        
        try:
            # Execute the node
            if current_node.type == NodeType.FUNCTION:
                self._execute_function_node(current_node, state)
            elif current_node.type == NodeType.CONDITION:
                self._execute_condition_node(current_node, state)
            elif current_node.type == NodeType.LOOP:
                self._execute_loop_node(current_node, state)
            
            # Find next node
            next_nodes = graph.get_next_nodes(current_node_id, state)
            
            if not next_nodes:
                # No next nodes, workflow is complete
                state.is_complete = True
                state.execution_log.append(f"Completed at node '{current_node_id}'")
            else:
                # Move to the first next node
                state.current_node = next_nodes[0]
                state.execution_log.append(f"Moved from '{current_node_id}' to '{state.current_node}'")
            
            return True
        except Exception as e:
            state.error = str(e)
            state.is_complete = True
            return False
    
    def run_to_completion(self, run_id: str) -> WorkflowState:
        """Run a workflow to completion"""
        while self.execute_step(run_id):
            pass
        return self.get_run_state(run_id)
    
    def _execute_function_node(self, node: Node, state: WorkflowState) -> None:
        """Execute a function node"""
        if not node.function:
            raise ValueError(f"Function node '{node.id}' has no function specified")
        
        # Call the function
        result = tool_registry.call_tool(node.function, state)
        
        # Update state with result
        if isinstance(result, dict):
            state.update(result)
        else:
            state.set(f"{node.id}_result", result)
        
        state.execution_log.append(f"Executed function '{node.function}' at node '{node.id}'")
    
    def _execute_condition_node(self, node: Node, state: WorkflowState) -> None:
        """Execute a condition node"""
        if not node.condition:
            raise ValueError(f"Condition node '{node.id}' has no condition specified")
        
        # Evaluate condition
        try:
            result = eval(node.condition, {}, {"state": state})
            state.set(f"{node.id}_result", result)
            state.execution_log.append(f"Evaluated condition '{node.condition}' at node '{node.id}': {result}")
        except Exception as e:
            raise ValueError(f"Error evaluating condition '{node.condition}': {str(e)}")
    
    def _execute_loop_node(self, node: Node, state: WorkflowState) -> None:
        """Execute a loop node"""
        if not node.loop_condition:
            raise ValueError(f"Loop node '{node.id}' has no loop condition specified")
        
        # Get current iteration count
        iteration_key = f"{node.id}_iteration"
        iteration = state.get(iteration_key, 0)
        
        # Check if we've exceeded max iterations
        if iteration >= node.max_iterations:
            state.execution_log.append(f"Loop node '{node.id}' reached max iterations ({node.max_iterations})")
            return
        
        # Evaluate loop condition
        try:
            should_continue = eval(node.loop_condition, {}, {"state": state})
            
            if should_continue:
                # Execute the loop body function
                if node.function:
                    result = tool_registry.call_tool(node.function, state)
                    if isinstance(result, dict):
                        state.update(result)
                    else:
                        state.set(f"{node.id}_result", result)
                
                # Increment iteration count
                iteration += 1
                state.set(iteration_key, iteration)
                state.execution_log.append(f"Loop node '{node.id}' iteration {iteration}")
                
                # Stay at this node for the next iteration
                state.current_node = node.id
            else:
                state.execution_log.append(f"Loop node '{node.id}' condition false, exiting loop")
        except Exception as e:
            raise ValueError(f"Error evaluating loop condition '{node.loop_condition}': {str(e)}")

# Global workflow engine instance
workflow_engine = WorkflowEngine()
