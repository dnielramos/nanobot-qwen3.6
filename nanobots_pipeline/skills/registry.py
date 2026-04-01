from skills.web_search import web_search, web_search_schema
from skills.file_reader import file_reader, file_reader_schema

# Tool implementations map
AVAILABLE_TOOLS = {
    "web_search": web_search,
    "file_reader": file_reader
}

# Tool schemas for OpenRouter/Qwen API
TOOL_SCHEMAS = [
    web_search_schema,
    file_reader_schema
]
