# Ye define karta hai ki machine ke dimaag (State) mein kya-kya save hoga.
# Python ko batane ke liye ki hum custom data types (Dictionary/List) use kar rahe hain.
from typing import TypedDict, List , Optional 

#Ek "Blueprint" banaya hai jisme workflow ki saari details save hongi.
class WorkflowState(TypedDict):
    client_request: str  # User ka original question.
    plan: List[str] # AI ka step-by-step plan.
    data: dict # Data jo humne database/API se nikala.
    validated: bool # Kya data sahi hai? (True/False)
    approved: bool # Kya user ne approve kiya? (True/False)
    result: str # Final answer.
    error: Optional[str] # Agar koi error aaye toh yahan save hoga.