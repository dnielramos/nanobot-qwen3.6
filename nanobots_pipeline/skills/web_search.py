from pydantic import BaseModel, Field

class WebSearchInput(BaseModel):
    query: str = Field(description="The search query to look up on the internet.")
    num_results: int = Field(default=3, description="The number of search results to return.")

def web_search(query: str, num_results: int = 3) -> str:
    """
    Simulated web search tool.
    In a production environment, integrate with SerpAPI, Google Custom Search, or Tavily.
    """
    # Mocking external API call
    results = [
        f"Result 1 for {query}: Mocked web snippet detailing the latest info.",
        f"Result 2 for {query}: Another source confirming the data.",
        f"Result 3 for {query}: A forum post with additional context."
    ]
    return "\\n".join(results[:num_results])

# Schema definition for LLM tool calling
web_search_schema = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "Searches the web for information based on a query.",
        "parameters": WebSearchInput.model_json_schema()
    }
}
