from pydantic import BaseModel 

# Ye ek simple "Container" hai jo user se input lega.
class WorkflowRequest(BaseModel):
    client_request: str # User ka original question