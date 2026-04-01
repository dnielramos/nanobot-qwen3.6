from services.llm_provider import LLMProvider
from skills.registry import TOOL_SCHEMAS, AVAILABLE_TOOLS
import logging

logger = logging.getLogger(__name__)

class WorkerAgent:
    """Specialized agent that executes tasks utilizing available skills."""
    def __init__(self, role: str, instruction: str):
        self.role = role
        self.instruction = instruction
        self.llm = LLMProvider()

    async def execute_task(self, task: str) -> str:
        messages = [
            {"role": "system", "content": f"You are a specialized worker acting as a {self.role}. {self.instruction}"},
            {"role": "user", "content": f"Execute the following task: {task}"}
        ]

        # Call LLM with tools
        response = await self.llm.generate_response(messages=messages, tools=TOOL_SCHEMAS)
        message = response["choices"][0]["message"]

        # Check for tool calls
        if "tool_calls" in message:
            for tool_call in message["tool_calls"]:
                function_name = tool_call["function"]["name"]
                import json
                arguments = json.loads(tool_call["function"]["arguments"])

                if function_name in AVAILABLE_TOOLS:
                    logger.info(f"Worker {self.role} is executing tool {function_name} with args {arguments}")
                    tool_result = AVAILABLE_TOOLS[function_name](**arguments)

                    # Append tool response
                    messages.append(message)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "name": function_name,
                        "content": str(tool_result)
                    })

            # Generate final response after tool execution
            final_response = await self.llm.generate_response(messages=messages)
            return final_response["choices"][0]["message"]["content"]

        return message["content"]

data_processor = WorkerAgent(
    role="Data Processor",
    instruction="Extract key insights from text, clean formatting, and structure it clearly. Use your tools if you need to fetch data."
)

code_reviewer = WorkerAgent(
    role="Code Reviewer",
    instruction="Review code for best practices, SOLID principles, and security vulnerabilities. Suggest improvements."
)
