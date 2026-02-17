"""
FastAPI Server: Entry point for the AI Services Suite.
Manages CORS, route handling, and serving the frontend metadata.
"""
from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from main_graph import build_graph 
from models.request import WorkflowRequest 

app = FastAPI(title="AI Services Suite API") 

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Build the LangGraph workflow
workflow = build_graph() 

@app.get("/", response_class=HTMLResponse)
def read_root():
    """Serves the main dashboard user interface."""
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"<h1>Error loading UI</h1><p>{str(e)}</p>"

@app.post("/run-workflow")
def run_workflow(request: WorkflowRequest):
    """
    Main endpoint to trigger the AI workflow.
    Takes client_request and returns the final process state.
    """
    try: 
        # Initialize internal state for the workflow
        input_state = {
            "client_request": request.client_request,
            "plan":[],
            "data":{},
            "validated":False,
            "approved":False,
            "result":"",
            "error": None 
        }
        
        # Execute the compiled graph
        output = workflow.invoke(input_state)
        
        # Log backend errors for developer debugging
        if output.get("error"):
            print(f"Workflow Process Alert: {output['error']}")
            
        return output
    
    except Exception as e: 
        return JSONResponse(
            status_code=500,
            content={"error": "Workflow Engine failure", "details": str(e)}
        )
