import requests
from engine.prompts import SYSTEM_PROMPT
from config import OLLAMA_BASE_URL, OLLAMA_MODEL

def build_prompt(user_input, context=""):
    """Constructs the full prompt for the LLM."""
    return f"{SYSTEM_PROMPT}\n\nContext: {context}\n\nUser: {user_input}"

def persona_guard(response):import requests
import os
from engine.prompts import SYSTEM_PROMPT
from config import OLLAMA_BASE_URL, OLLAMA_MODEL
from memory.memory_loader import (
    get_ai_memory, get_writing_samples, get_training_corpus, 
    get_profiles, get_chat_history
)
from memory.memory_store import supabase

def build_prompt(user_input, conversation_id=None, memory_enabled=True):
    """Constructs the full prompt for the LLM based on persona anchors and history."""
    
    # 1. System Prompt
    full_prompt = SYSTEM_PROMPT + "\n\n"
    
    if memory_enabled:
        # 2. Writing Style Anchors
        writing_samples = get_writing_samples()
        if writing_samples:
            full_prompt += "### WRITING STYLE ANCHORS\n"
            for sample in writing_samples[:3]:
                full_prompt += f"- {sample.get('content', '')}\n"
            full_prompt += "\n"
        
        # 3. Training Corpus Hits
        training_hits = get_training_corpus()
        if training_hits:
            full_prompt += "### TRAINING CORPUS HITS\n"
            for hit in training_hits[:2]:
                full_prompt += f"- {hit.get('content', '')}\n"
            full_prompt += "\n"
            
        # 4. User Memory Context
        user_memory = get_ai_memory()
        if user_memory:
            full_prompt += "### USER MEMORY CONTEXT\n"
            for mem in user_memory[-5:]:
                full_prompt += f"- {mem.get('content', '')}\n"
            full_prompt += "\n"

    # 5. Conversation History
    if conversation_id:
        history = get_chat_history(conversation_id)
        if history:
            full_prompt += "### CONVERSATION HISTORY\n"
            for msg in history[-10:]:
                role = msg.get('role', 'user')
                content = msg.get('content', '')
                full_prompt += f"{role.capitalize()}: {content}\n"
            full_prompt += "\n"

    # 6. User Message
    full_prompt += f"User: {user_input}\nAssistant:"
    
    return full_prompt

def persona_guard(response):
    """Ensures the response maintains the CriderGPT persona."""
    if "CriderGPT" not in response:
        return response + "\n\n(Response verified by CriderGPT persona guard)"
    return response

def generate(user_input, conversation_id=None, memory_enabled=True):
    """Generates a response and implements write-back logic."""
    prompt = build_prompt(user_input, conversation_id, memory_enabled)
    
    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=30
        )
        result = response.json().get("response", "")
    except Exception as e:
        result = f"Error generating response: {e}"
        
    final_response = persona_guard(result)
    
    if memory_enabled and supabase:
        try:
            supabase.table("ai_memory").insert({
                "content": user_input,
                "metadata": {"type": "user_input"}
            }).execute()
            
            if conversation_id:
                supabase.table("chat_messages").insert([
                    {"conversation_id": conversation_id, "role": "user", "content": user_input},
                    {"conversation_id": conversation_id, "role": "assistant", "content": final_response}
                ]).execute()
        except Exception as e:
            print(f"Write-back failed: {e}")
            
    return final_response

    """Ensures the response maintains the CriderGPT persona."""
    if "CriderGPT" not in response:
        return response + "\n\n(Response verified by CriderGPT persona guard)"
    return response

def generate(user_input, context=""):
    """Generates a response using Ollama and applies the persona guard."""
    prompt = build_prompt(user_input, context)
    
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload)
        response.raise_for_status()
        data = response.json()
        raw_response = data.get("response", "")
        return persona_guard(raw_response)
    except Exception as e:
        return f"Error during inference: {str(e)}"
