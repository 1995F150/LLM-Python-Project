from supabase import create_client, Client
from .config import SUPABASE_URL, SUPABASE_KEY

def load_memory_from_supabase():
    """Reads all rows from Supabase ai_memory table."""
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Read all records from the existing ai_memory table.
    # As per instructions: Do not write, only read.
    response = supabase.table("ai_memory").select("*").execute()
    
    return response.data

if __name__ == "__main__":
    memories = load_memory_from_supabase()
    print(f"Loaded {len(memories)} memory records from Supabase.")
