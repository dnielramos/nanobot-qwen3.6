import os
from pydantic import BaseModel, Field

class FileReaderInput(BaseModel):
    file_path: str = Field(description="The absolute or relative path of the file to read.")

def file_reader(file_path: str) -> str:
    """
    Reads the content of a local file safely.
    Restricts access to specific directories to prevent path traversal vulnerabilities.
    """
    safe_dir = os.path.abspath(os.getcwd())
    target_path = os.path.abspath(file_path)

    if not target_path.startswith(safe_dir):
        return "Error: Access to directories outside the working directory is restricted."

    if not os.path.exists(target_path):
        return f"Error: File '{target_path}' does not exist."
    try:
        with open(target_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        return f"Error reading file '{target_path}': {str(e)}"

# Schema definition for LLM tool calling
file_reader_schema = {
    "type": "function",
    "function": {
        "name": "file_reader",
        "description": "Reads the content of a file given its path.",
        "parameters": FileReaderInput.model_json_schema()
    }
}
