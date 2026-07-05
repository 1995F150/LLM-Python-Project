import json
import os
from .memory_loader import load_memory_from_supabase
try:
    from config import DATA_DIR
except ImportError:
    DATA_DIR = "data"

def export_memory():
    """Fetches memory from Supabase and saves it to ai_memory.json."""
    print("Fetching memory from Supabase...")
    data = load_memory_from_supabase()

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    file_path = os.path.join(DATA_DIR, "ai_memory.json")
    
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
    
    print(f"Memory exported successfully to {file_path}")

if __name__ == "__main__":
    export_memory()
