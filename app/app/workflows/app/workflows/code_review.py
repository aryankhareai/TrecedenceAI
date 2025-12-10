from typing import Dict, Any
from app.models.graph import Graph, Node, NodeType, Edge
from app.engine.tool_registry import tool_registry
from app.engine.workflow import workflow_engine

def extract_functions(state) -> Dict[str, Any]:
    """Extract functions from code"""
    code = state.get("code", "")
    # Simple function extraction - in a real system, you'd use AST parsing
    functions = []
    lines = code.split("\n")
    for i, line in enumerate(lines):
        if line.strip().startswith("def "):
            func_name = line.strip().split("(")[0].replace("def ", "")
            functions.append({
                "name": func_name,
                "line": i + 1,
                "code": line
            })
    
    return {"functions": functions}

def check_complexity(state) -> Dict[str, Any]:
    """Check complexity of functions"""
    functions = state.get("functions", [])
    complexity_scores = {}
    
    for func in functions:
        # Simple complexity metric - count of lines
        func_code = func.get("code", "")
        complexity = len(func_code.split("\n"))
        complexity_scores[func["name"]] = complexity
    
    avg_complexity = sum(complexity_scores.values()) / len(complexity_scores) if complexity_scores else 0
    
    return {
        "complexity_scores": complexity_scores,
        "avg_complexity": avg_complexity
    }

def detect_issues(state) -> Dict[str, Any]:
    """Detect basic issues in code"""
    code = state.get("code", "")
    issues = []
    
    # Check for common issues
    if "TODO" in code:
        issues.append("Contains TODO comments")
    
    if "print(" in code:
        issues.append("Contains print statements")
    
    if len(code.split("\n")) > 100:
        issues.append("File is too long (>100 lines)")
    
    # Check for long functions
    complexity_scores = state.get("complexity_scores", {})
    for func_name, complexity in complexity_scores.items():
        if complexity > 20:
            issues.append(f"Function '{func_name}' is too complex ({complexity} lines)")
    
    return {"issues": issues, "issue_count": len(issues)}

def suggest_improvements(state) -> Dict[str, Any]:
    """Suggest improvements based on detected issues"""
    issues = state.get("issues", [])
    suggestions = []
    
    for issue in issues:
        if "TODO" in issue:
            suggestions.append("Complete TODO items")
        elif "print" in issue:
            suggestions.append("Replace print statements with proper logging")
        elif "too long" in issue:
            suggestions.append("Consider splitting the file into smaller modules")
        elif "too complex" in issue:
            suggestions.append("Consider refactoring complex functions into smaller ones")
    
    return {"suggestions": suggestions}

def calculate_quality_score(state) -> Dict[str, Any]:
    """Calculate overall quality score"""
    issues = state.get("issues", [])
    complexity_scores = state.get("complexity_scores", {})
    
    # Base score starts at 100
    score = 100
    
    # Deduct points for issues
    score -= len(issues) * 5
    
    # Deduct points for high complexity
    for complexity in complexity_scores.values():
        if complexity > 20:
            score -= 10
    
    # Ensure score doesn't go below 0
    score = max(0, score)
    
    return {"quality_score": score}

def create_code_review_graph() -> Graph:
    """Create the code review workflow graph"""
    # Define nodes
    nodes = {
        "extract": Node(id="extract", name="Extract Functions", type=NodeType.FUNCTION, function="extract_functions"),
        "complexity": Node(id="complexity", name="Check Complexity", type=NodeType.FUNCTION, function="check_complexity"),
        "detect": Node(id="detect", name="Detect Issues", type=NodeType.FUNCTION, function="detect_issues"),
        "suggest": Node(id="suggest", name="Suggest Improvements", type=NodeType.FUNCTION, function="suggest_improvements"),
        "score": Node(id="score", name="Calculate Quality Score", type=NodeType.FUNCTION, function="calculate_quality_score"),
        "check_quality": Node(id="check_quality", name="Check Quality Threshold", type=NodeType.CONDITION, condition="state.get('quality_score', 0) >= state.get('threshold', 70)"),
    }
    
    # Define edges
    edges = [
        Edge(from_node="extract", to_node="complexity"),
        Edge(from_node="complexity", to_node="detect"),
        Edge(from_node="detect", to_node="suggest"),
        Edge(from_node="suggest", to_node="score"),
        Edge(from_node="score", to_node="check_quality"),
        Edge(from_node="check_quality", to_node="extract", condition="not state.get('quality_score', 0) >= state.get('threshold', 70)"),
    ]
    
    # Create graph
    graph = Graph(
        id="code_review",
        name="Code Review Workflow",
        nodes=nodes,
        edges=edges,
        start_node="extract"
    )
    
    return graph

def register_code_review_tools():
    """Register tools for the code review workflow"""
    tool_registry.register("extract_functions", "Extract functions from code", extract_functions)
    tool_registry.register("check_complexity", "Check complexity of functions", check_complexity)
    tool_registry.register("detect_issues", "Detect basic issues in code", detect_issues)
    tool_registry.register("suggest_improvements", "Suggest improvements based on detected issues", suggest_improvements)
    tool_registry.register("calculate_quality_score", "Calculate overall quality score", calculate_quality_score)

def setup_code_review_workflow():
    """Set up the code review workflow"""
    # Register tools
    register_code_review_tools()
    
    # Create and register the graph
    graph = create_code_review_graph()
    workflow_engine.register_graph(graph)
    
    return graph.i
