"""
FastAPI Server: Entry point for the AI Services Suite.
Manages CORS, route handling, and serving the frontend metadata.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from main_graph import build_graph 
from models.request import WorkflowRequest 

app = FastAPI(title="AI Services Suite API") # ye fast api ka object hai...ek web application server bnaya 

# Configure CORS for frontend communication - ye browser security settings allow karta hai
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # saari websites ko allow karta hai
    allow_credentials=True,
    allow_methods=["*"], # saare methods (GET, POST) allow karta hai
    allow_headers=["*"], # saari headers allow karta hai
)

# Build the LangGraph workflow - ye AI ki poori machine (graph) taiyaar karta hai
workflow = build_graph() 

@app.get("/", response_class=HTMLResponse) # ye homepage ka address hai
def read_root():
    """Serves the main dashboard user interface."""
    try:
        # index.html file ko read karke browser pe dikhata hai
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"<h1>Error loading UI</h1><p>{str(e)}</p>"

@app.post("/run-workflow") # ye wahi address hai jaha frontend user ka message bhejta hai
def run_workflow(request: WorkflowRequest):
    """
    Main endpoint to trigger the AI workflow.
    Takes client_request and returns the final process state.
    """
    try: 
        # Initialize internal state for the workflow - ye khaali memory setup karna hai
        input_state = {
            "client_request": request.client_request, # user ka sawal
            "plan":[], # shuruat mein plan khaali hai
            "data":{}, # data bhi khaali hai
            "validated":False, # abhi check nahi hua
            "approved":False, # abhi approve nahi hua
            "result":"", # final answer abhi nahi aaya
            "error": None # koi error nahi hai abhi
        }
        
        # Execute the compiled graph - ye AI machine ko chalu kar deta hai
        output = workflow.invoke(input_state)
        
        # Log backend errors for developer debugging
        if output.get("error"):
            print(f"Workflow Process Alert: {output['error']}")
            
        return output # final poora result frontend ko wapas bhej deta hai
    
    except Exception as e: 
        # agar kuch phat gaya toh 500 error dikhayega
        return JSONResponse(
            status_code=500,
            content={"error": "Workflow Engine failure", "details": str(e)}
        )
