import requests
import json
import os
from engine.prompts import SYSTEM_PROMPT
from config import OLLAMA_BASE_URL, OLLAMA_MODEL
from memory.memory_loader import (
    get_writing_samples,
    get_training_corpus,
    get_ai_memory,
    get_conversation_history
)
from memory.memory_store import supabase

def build_prompt(user_input, context=""):
    """Constructs the full prompt for the LLM."""
    full_prompt = f"{SYSTEM_PROMPT}\n\n"
    
    # 1. Writing Samples
    writing_samples = get_writing_samples()
    if writing_samples:
        full_prompt += "### WRITING STYLE ANCHORS\n"
        for sample in writing_samples[:3]:
            full_prompt += f"- {sample.get('content', '')}\n"
        full_prompt += "\n"

    # 2. Training Corpus Hits
    training_hits = get_training_corpus()
    if training_hits:
        full_prompt += "### TRAINING CORPUS HITS\n"
        for hit in training_hits[:2]:
            full_prompt += f"- {hit.get('content', '')}\n"
        full_prompt += "\n"

    # 3. Memory Context
    user_memory = get_ai_memory()
    if user_memory:
        full_prompt += "### USER MEMORY\n"
        full_prompt += user_memory + "\n\n"

    # 4. Conversation History
    history = get_conversation_history()
    if history:
        full_prompt += "### RECENT CONVERSATION\n"
        full_prompt += history + "\n\n"

    full_prompt += f"User: {user_input}\nAssistant:"
    return full_prompt

def persona_guard(response):
    """Ensures the response adheres to the CriderGPT persona."""
    # Basic cleanup: remove raw JSON if returned
    if response.startswith("{") and "response" in response:
        try:
            data = json.loads(response)
            response = data.get("response", response)
        except:
            pass
    
    # Remove any unwanted prefixes/suffixes
    response = response.replace("Assistant:", "").replace("User:", "").strip()
    
    # DO NOT add debug text here
    return response

def generate(user_input, user_id="guest", conversation_id=None):
    """Calls Ollama and handles response pipeline."""
    prompt = build_prompt(user_input)
    
    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        response.raise_for_status()
        result = response.json().get("response", "")
    except Exception as e:
        print(f"Ollama Error: {e}")
        result = ""

    # Persona Guard & Cleanup
    final_response = persona_guard(result)

    # Safety Fallback
    if not final_response or final_response.strip() == "":
        final_response = "I am having trouble generating a response right now."

    # Memory Save (Final Assistant Response)
    try:
        if conversation_id:
            supabase.table("ai_memory").insert({
                "user_id": user_id,
                "conversation_id": conversation_id,
                "content": final_response,
                "type": "assistant"
            }).execute()
    except Exception as e:
        print(f"Memory Save Error: {e}")

    return final_response
