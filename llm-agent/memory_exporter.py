import json
import os
from .memory_loader import load_memory_from_supabase
from .config import DATA_DIR

def export_memory():
    """Saves memory from Supabase into local files inside /data."""
    memories = load_memory_from_supabase()
    
    # Create data directory if it doesn't exist
    os.makedirs(DATA_DIR, exist_ok=True)
        
    # Save as JSON
    json_path = os.path.join(DATA_DIR, "ai_memory.json")
    with open(json_path, "w") as f:
        json.dump(memories, f, indent=4)
        
    # Save as TXT
    txt_path = os.path.join(DATA_DIR, "ai_memory.txt")
    with open(txt_path, "w") as f:
        for m in memories:
            content = m.get('content', '')
            f.write(f"{content}\n")
            
    # Save as Index JSON
    index_path = os.path.join(DATA_DIR, "ai_memory_index.json")
    index_data = {str(m.get('id', i)): m.get('content', '') for i, m in enumerate(memories)}
    with open(index_path, "w") as f:
        json.dump(index_data, f, indent=4)

if __name__ == "__main__":
    export_memory()
    print("Memory export complete.")
