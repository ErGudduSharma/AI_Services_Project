import os # read the system environments variables
import google.generativeai as genai # google gemini library
from dotenv import load_dotenv # load the environment variables

load_dotenv() # load the environment variables

genai.configure(api_key = os.getenv("GEMINI_API_KEY")) # configure the gemini api key

# this function initialize the gemini model
def get_gemini_llm():
    """
    Initialize the Gemini LLM.
    Returns:
        Gemini LLM instance.
    """

    # it return the gemini 2.0 flash model's object 
    return genai.GenerativeModel("gemini-2.0-flash") 