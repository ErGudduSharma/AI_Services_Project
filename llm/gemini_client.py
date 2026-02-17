import os 
import google.generativeai as genai 
from dotenv import load_dotenv 

load_dotenv() 

genai.configure(api_key=os.getenv("GEMINI_API_KEY")) 

def get_gemini_llm():
    # Using gemini-2.0-flash based on list_models check
    return genai.GenerativeModel("gemini-2.0-flash") 