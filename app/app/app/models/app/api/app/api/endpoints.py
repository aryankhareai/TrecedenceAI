from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List

from app.engine.workflow import workflow_engine
from app.workflows.code_review import setup_code_review_workflow

router = APIRouter()

# Set up the code review workflow when the API starts
setup_code_review_workflow()

class GraphRunRequest(BaseModel):
    """Request model for running a graph"""
    graph_id: str
    initial_state: Dict[str, Any]

class GraphRunResponse(BaseModel):
    """Response model for running a graph"""
    run_id: str
    final_state: Dict[str, Any]
    execution_log: List[str]

class GraphStateResponse(BaseModel):
    """Response model for getting graph state"""
    run_id: str
    state: Dict[str, Any]
    is_complete: bool
    error: Optional[str] = None

@router.post("/graph/run", response_model=GraphRunResponse)
async def run_graph(request: GraphRunRequest):
    """Run a graph with initial state"""
    try:
        # Start the run
        run_id = workflow_engine.start_run(request.graph_id, request.initial_state)
        
        # Run to completion
        final_state = workflow_engine.run_to_completion(run_id)
        
        return GraphRunResponse(
            run_id=run_id,
            final_state=final_state.data,
            execution_log=final_state.execution_log
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/graph/state/{run_id}", response_model=GraphStateResponse)
async def get_graph_state(run_id: str):
    """Get the current state of a running workflow"""
    state = workflow_engine.get_run_state(run_id)
    if not state:
        raise HTTPException(status_code=404, detail="Run not found")
    
    return GraphStateResponse(
        run_id=run_id,
        state=state.data,
        is_complete=state.is_complete,
        error=state.error
    )
