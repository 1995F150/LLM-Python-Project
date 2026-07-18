"""Legacy compatibility exports."""

from config import settings

SUPABASE_URL = settings.supabase_url
SUPABASE_KEY = settings.supabase_service_role_key
MODEL_NAME = settings.ollama_model
DATA_DIR = "data"
