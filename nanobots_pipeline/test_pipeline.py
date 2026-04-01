import asyncio
from agents.orchestrator import orchestrator
from memory.short_term import short_term_memory

async def run_test():
    session_id = short_term_memory.create_session()
    print(f"Created Session: {session_id}")

    # Simple direct query
    response = await orchestrator.process_request(session_id, "What is the capital of France?")
    print(f"Orchestrator Response: {response}")

    # Delegated Code task
    response2 = await orchestrator.process_request(session_id, "Can you review the code in skills/file_reader.py?")
    print(f"Orchestrator Code Review Output: {response2}")

    # Delegated Data task
    response3 = await orchestrator.process_request(session_id, "Can you search the web for the latest Python version?")
    print(f"Orchestrator Data Search Output: {response3}")

if __name__ == "__main__":
    # We won't actually run this as it hits real API endpoints,
    # but having it available is useful for testing locally.
    print("Test file created.")
