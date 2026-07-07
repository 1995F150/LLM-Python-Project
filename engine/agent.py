from engine.inference import generate

def get_agent_response(user_input, user_id="guest", conversation_id=None):
    """
    Main entry point for getting an agent response.
    Returns a tuple: (response_text, memories_used_count)
    """
    # Call the inference engine
    response, memories_used = generate(
        user_input, 
        user_id=user_id, 
        conversation_id=conversation_id
    )
    
    return response, memories_used
