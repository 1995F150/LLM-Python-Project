# LLM Agent with Supabase Memory

This project implements a memory-augmented LLM agent that reads data from a Supabase `ai_memory` table, saves it locally, and uses it to provide context-aware responses via a FastAPI backend.

## Components

- **config.py**: Configuration for Supabase credentials and local paths.
- **memory_loader.py**: Reads memory records from the Supabase `ai_memory` table.
- **memory_exporter.py**: Exports Supabase data to local JSON and text files in the `/data` directory.
- **memory_store.py**: Loads and formats local memory files for use by the agent.
- **agent.py**: The core LLM logic that uses local memory context for inference.
- **app.py**: FastAPI backend with endpoints for querying the agent (`/ask`) and syncing memory (`/sync-memory`).

## Setup

1. Configure your Supabase URL and Key in `config.py`.
2. Run `app.py` to start the backend server.
3. Use the `/sync-memory` endpoint to pull initial data from Supabase.
4. Interact with the agent via the `/ask` endpoint.
