"""
Main Graph Orchestrator for the AI Services Suite.
This script compiles the stateful LangGraph workflow.
"""

from langgraph.graph import StateGraph 
from models.state import WorkflowState
from nodes.planner import planner_node 
from nodes.data_fetch import data_fetch_node 
from nodes.validation import validation_node 
from nodes.approval import approval_node
from nodes.delivery import delivery_node 

def build_graph():
    """
    Initializes and compiles the LangGraph state machine.
    Returns:
        Compiled LangGraph workflow.
    """
    # Initialize the graph with the WorkflowState schema
    graph = StateGraph(WorkflowState)  
    
    # Register all processing nodes
    graph.add_node("planner", planner_node)
    graph.add_node("fetch", data_fetch_node)
    graph.add_node("validate", validation_node) 
    graph.add_node("approve", approval_node) 
    graph.add_node("deliver", delivery_node) 

    # Define the execution flow (Edges)
    graph.set_entry_point("planner") 
    graph.add_edge("planner", "fetch")
    graph.add_edge("fetch", "validate")
    graph.add_edge("validate", "approve")
    graph.add_edge("approve", "deliver") 

    # Mark the termination point
    graph.set_finish_point("deliver") 
    
    return graph.compile() 