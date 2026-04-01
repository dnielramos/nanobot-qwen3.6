from agents.workers import data_processor, code_reviewer
from memory.short_term import short_term_memory
from memory.long_term import long_term_memory
from services.llm_provider import LLMProvider
import logging

logger = logging.getLogger(__name__)

class OrchestratorAgent:
    """Main agent responsible for breaking down user prompts and delegating to workers."""
    def __init__(self):
        self.llm = LLMProvider()

    async def process_request(self, session_id: str, prompt: str) -> str:
        short_term_memory.add_message(session_id, "user", prompt)

        # Retrieve relevant context from long-term memory
        past_context = long_term_memory.retrieve_memory(prompt)
        context_str = "\n".join(past_context) if past_context else "No prior context found."

        system_prompt = (
            "You are an Orchestrator Agent with a 1M token context window. "
            "Your job is to analyze the user's request, delegate tasks to specialized subagents "
            "if necessary, or directly answer the question using the context. "
            f"Relevant Past Context:\n{context_str}"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            *short_term_memory.get_context(session_id)
        ]

        # Step 1: Ask LLM for the orchestration plan
        orchestration_response = await self.llm.generate_response(messages=messages)
        content = orchestration_response["choices"][0]["message"]["content"]

        # Basic heuristic to delegate tasks (can be advanced with structured JSON outputs later)
        if "data" in prompt.lower() or "summarize" in prompt.lower():
            logger.info("Delegating to Data Processor")
            worker_output = await data_processor.execute_task(prompt)
            content = f"Data Processor Output:\n{worker_output}"
        elif "code" in prompt.lower() or "review" in prompt.lower():
            logger.info("Delegating to Code Reviewer")
            worker_output = await code_reviewer.execute_task(prompt)
            content = f"Code Reviewer Output:\n{worker_output}"

        short_term_memory.add_message(session_id, "assistant", content)

        # Store interaction in long-term memory for future retrieval
        long_term_memory.store_memory(session_id, f"User: {prompt}\nOrchestrator: {content}")

        return content

orchestrator = OrchestratorAgent()
