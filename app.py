from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from main_graph import build_graph 
from models.request import WorkflowRequest 
import os

app = FastAPI() 

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

workflow = build_graph() 

@app.get("/", response_class=HTMLResponse)
def read_root():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"<h1>Error loading index.html</h1><p>{str(e)}</p>"

@app.post("/run-workflow")
def run_workflow(request: WorkflowRequest):
    try: 
        input_state = {
            "client_request": request.client_request,
            "plan":[],
            "data":{},
            "validated":False,
            "approved":False,
            "result":"",
            "error": None 
        }
        # Run the compiled graph
        output = workflow.invoke(input_state)
        
        # Ensure we return a structured response even if internal error field is set
        return output
    
    except Exception as e : 
        return JSONResponse(
            status_code=500,
            content={
                "error": "Workflow execution failed",
                "details": str(e) 
            }
        )
