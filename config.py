OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3"
API_KEYS = ["crider-key-1", "crider-key-2"]
import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
API_KEYS = ["crider-key-1", "crider-key-2"]

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
