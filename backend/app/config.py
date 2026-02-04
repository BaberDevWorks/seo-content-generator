from dotenv import load_dotenv
import os

load_dotenv()  

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment")
SERP_API_KEY = os.getenv("Serp_API_key") or os.getenv("SERP_API_KEY")
if not SERP_API_KEY:
    raise ValueError("SERP_API_KEY not found in environment")