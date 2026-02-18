"""
Delivery Node: Synthesizes the final output and solution description for the user.

"""
from llm.gemini_client import get_gemini_llm # AI model import kiya

def delivery_node(state):
    """
    Generates a comprehensive solution description including an explanation 
    of the workflow executed by the agents.

    """
    
    # Static template for offline/fallback mode - Bina AI ke report banane wala function
    def get_fallback_message(state):
        status = "✅ APPROVED" if state.get('approved') else "❌ REJECTED"
        workflow_steps = "\n".join([f"- {step}" for step in state.get('plan', [])])
        
        return f"""
## Service Execution Report

### 📋 Request Overview
**Client Request:** {state['client_request']}

### ⚙️ Workflow Executed
The system followed these logical steps to process your request:
{workflow_steps}

### 🔍 Data Analysis
- **Customer Identity:** {state['data'].get('customer_id', 'N/A')}
- **Transaction Value:** ₹{state['data'].get('amount', 0)}
- **Processing Status:** {state['data'].get('status', 'PENDING')}

### 🎯 Final Outcome
**Status:** {status}

**Reason:** {"The request meets all security and limit policy requirements." if state.get('approved') else "The request was declined during the risk validation phase (Check amount or ID)."}

---
*Note: AI Generation is currently in Lite Mode. Standard system summary provided above.*
"""

    try:
        # Agar request approve ho gayi hai, toh ek sundar AI powered response banayenge
        if state.get('approved'):
            llm = get_gemini_llm() # AI chalu kiya
            # AI ko instructions: Analyst ki tarah behave karo aur puri summary do

            prompt = f"""
            Act as an AI Business Analyst. Provide a detailed solution for the following request:
            
            USER REQUEST: {state['client_request']}
            
            WORKFLOW FOLLOWED:
            {state['plan']}
            
            EXTRACTED DATA:
            {state['data']}
            
            STRICT GUIDELINES:
            1. Start with a friendly AI greeting.
            2. Add a section '## Workflow Summary' explaining the steps taken.
            3. Add a section '## Solution Details' explaining the final result.
            4. Use clear Markdown headers and bullet points.

            """

            response = llm.generate_content(prompt)
            
            if response and hasattr(response, 'text') and response.text:
                state['result'] = response.text # AI ki likhi report save ki
            else:
                state['result'] = get_fallback_message(state) # AI reply nahi diya toh manual template
        else:
            # Agar reject hua hai, toh manual structured format mein explain karo kyun reject hua
            state['result'] = get_fallback_message(state)
            
    except Exception as e:
        # Connection ya quota errors mein bhi manual template dikhao taaki user ko output mile
        state['result'] = get_fallback_message(state)
        state['error'] = f"Synthesis Module: Using Static Template ({str(e)})"
        
    return state # Final report state mein daal kar finish
