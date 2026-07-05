import os
from supabase import create_client, Client
from transformers import pipeline

# Supabase configuration
# Please replace these with your project's API URL and Key
SUPABASE_URL = os.environ.get("SUPABASE_URL", "YOUR_PROJECT_API_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "YOUR_PROJECT_API_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def init_agent_memory(agent_id):
    """Augment LLM workflow using the 'ai_memory' table."""
    # Fetch memory context from Supabase
    res = supabase.table('ai_memory').select('content').eq('agent_id', agent_id).execute()
    return " ".join([m['content'] for m in res.data]) if res.data else ""

def run_agent_workflow(agent_id, prompt):
    # Initialize a simple LLM pipeline
    gen = pipeline("text-generation", model="gpt2")
    
    # Retrieve memory context
    context = init_agent_memory(agent_id)
    
    # Process prompt with contextimport os
from dotenv import load_dotenv

load_dotenv()
import os
from dotenv import load_dotenv

load_dotenv()

# Supabase configuration for project: udpldrrpebdyuiqdtqnq
SUPABASE_URL = os.environ.get("SUPABASE_URL", "REPLACE_WITH_YOUR_SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "REPLACE_WITH_YOUR_SUPABASE_KEY")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt2")
DATA_DIR = "llm-agent/data"

# Supabase configuration for project: udpldrrpebdyuiqdtqnq
SUPABASE_URL = os.environ.get("SUPABASE_URL", "YOUR_SUPABASE_API_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "YOUR_SUPABASE_API_KEY")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt2")
DATA_DIR = "llm-agent/data"

    full_prompt = f"Context: {context}\nUser: {prompt}\nAgent:"
    output = gen(full_prompt, max_length=100)[0]['generated_text']
    
    # Update memory in Supabase
    supabase.table('ai_memory').insert({"agent_id": agent_id, "content": f"Prompt: {prompt} | Response: {output}"}).execute()
    
    return output

if __name__ == "__main__":
    print(run_agent_workflow("agent_1", "Hello!"))
