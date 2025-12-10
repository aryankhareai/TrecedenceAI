# TrecedenceAI
A simplified LangGraph-like workflow engine built with FastAPI
Workflow Engine API
A simple workflow engine API that allows you to define, execute, and monitor workflows.

Features
Define workflows with nodes and edges
Support for different node types (function, condition, loop)
Tool registry for reusable functions
RESTful API for creating and running workflows
WebSocket support for real-time execution updatess
Code review workflow example
Getting Started
Prerequisites
Python 3.8+
FastAPI
Uvicorn (for running the server)
SQLAlchemy (optional, for database persistence)
Installation
Clone the repository
Install dependencies:
pip install fastapi uvicorn sqlalchemy
Workflow Engine
A minimal workflow/graph engine similar to LangGraph, built with Python and FastAPI for an AI Engineering internship.

Overview
This project implements a small agent workflow engine that allows defining a sequence of steps (nodes), connecting them, maintaining a shared state, and running the workflow end-to-end via APIs. The system supports branching, looping, and tool integration.

Features
Node-based workflow execution with state management
Support for different node types (function, condition, loop)
Tool registry for reusable functions
REST API for creating and running workflows
Code review workflow example
Clean, modular architecture
Quick Start
Clone this repository:
bash

Line Wrapping

Collapse
Copy
1
2
git clone https://github.com/yourusername/workflow-engine.git
cd workflow-engine
Install dependencies:
bash

Line Wrapping

Collapse
Copy
1
pip install -r requirements.txt
Run the application:
bash

Line Wrapping

Collapse
Copy
1
uvicorn app.main:app --reload
Access the API at http://localhost:8000
View API documentation at http://localhost:8000/docs
Architecture
The application is structured into the following components:

Core Engine (app/engine/)
workflow.py: The main engine that executes workflows step by step
tool_registry.py: A registry of functions that can be called by nodes
Data Models (app/models/)
graph.py: Defines the structure of workflows (nodes and edges)
state.py: Manages the state that flows between nodes
tool.py: Represents tools that can be used in workflows
API Layer (app/api/)
endpoints.py: FastAPI endpoints that allow external systems to create and run workflows
Example Workflow (app/workflows/)
code_review.py: A concrete example of a code review workflow
API Endpoints
POST /api/graph/run - Run a workflow with initial state
GET /api/graph/state/{run_id} - Get the current state of a running workflow
Example Workflow: Code Review
The included example is a Code Review Mini-Agent that:

Extract Functions: Finds all function definitions in the code
Check Complexity: Calculates a complexity score for each function
Detect Issues: Looks for common code issues (TODOs, print statements, etc.)
Suggest Improvements: Based on detected issues
Calculate Quality Score: Computes an overall quality score
Loop: Repeats the process until the quality score meets a threshold
Running the Code Review Workflow
To run the code review workflow, send a POST request to /api/graph/run with the following body:

json

Line Wrapping

Collapse
Copy
1
2
3
4
5
6
7
⌄
⌄
{
  "graph_id": "code_review",
  "initial_state": {
    "code": "def example_function():\n    print('Hello, world!')\n    # TODO: Implement this function\n    return True",
    "threshold": 70
  }
}
The API will return the final state and execution log, showing:

Detected issues
Quality score
Suggestions for improvement
How many iterations were needed to reach the threshold
How It Works
Graph Definition: Workflows are defined as graphs with nodes and edges
State Management: A shared state object flows between nodes
Node Execution: Each node processes the state and potentially modifies it
Transition Logic: Edges determine which node runs next, with support for conditional routing
Looping: Special loop nodes can repeat execution until a condition is met
What This Demonstrates
This project showcases:

Clean Python code structure and organization
API design with FastAPI
State machine implementation
Workflow and state transition thinking
Modular, extensible architecture
What Would Be Improved With More Time
With additional time, I would enhance the project with:

More Sophisticated Condition Evaluation: Replace the current eval() approach with a safer, more powerful expression parser
Workflow Visualization: Add a web interface to visualize workflow graphs and execution
Additional Node Types: Implement parallel execution, sub-workflows, and other advanced node types
Persistent Storage: Replace in-memory storage with PostgreSQL for better durability
Authentication and Authorization: Add user management and access controls
More Comprehensive Test Coverage: Implement unit and integration tests for all components
WebSocket Support: Add real-time workflow execution updates via WebSockets
Error Handling and Recovery: Implement more robust error handling and recovery mechanisms
Performance Optimization: Add caching and other optimizations for large workflows
Documentation: Add more detailed documentation and examples for building custom workflows
