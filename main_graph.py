"""
Main Graph Orchestrator for the AI Services Suite.
This script compiles the stateful LangGraph workflow.

"""

from langgraph.graph import StateGraph # LangGraph ki main library
from models.state import WorkflowState # Memory ka structure import kiya
from nodes.planner import planner_node # Planner agent
from nodes.data_fetch import data_fetch_node # Data khichne wala agent
from nodes.validation import validation_node # Check karne wala agent
from nodes.approval import approval_node # Decision lene wala agent
from nodes.delivery import delivery_node # Report banane wala agent

def build_graph():
    """
    Initializes and compiles the LangGraph state machine.
    Returns:
        Compiled LangGraph workflow.
    """
    # Initialize the graph with the WorkflowState schema
    graph = StateGraph(WorkflowState)  
    
    # Register all processing nodes - Saare stations ko graph mein add kiya
    graph.add_node("planner", planner_node) # Planner station
    graph.add_node("fetch", data_fetch_node) # Fetch station
    graph.add_node("validate", validation_node) # Validate station
    graph.add_node("approve", approval_node) # Approve station
    graph.add_node("deliver", delivery_node) # Deliver station

    # Define the execution flow (Edges) - Kaun kiske baad aayega (Patriya bichayi)
    graph.set_entry_point("planner") # Sabse pehle planner aayega
    graph.add_edge("planner", "fetch") # Planner se Fetch pe jao
    graph.add_edge("fetch", "validate") # Fetch se Validate pe jao
    graph.add_edge("validate", "approve") # Validate se Approve pe jao
    graph.add_edge("approve", "deliver") # Approve se Deliver pe jao

    # Mark the termination point
    graph.set_finish_point("deliver") 
    
    return graph.compile() 