import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
DATABASE_URL = os.getenv("DATABASE_URL", "leads.db")

# Fail fast at startup if critical config is missing
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set. Add it to your .env file.")