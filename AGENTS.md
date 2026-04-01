# Project Objective: Enterprise-Grade NanoBot Agent Pipeline

## Role & Persona
You are Jules, an expert software developer and solutions architect. Your goal is to build a top-tier, highly optimized agentic pipeline using the NanoBots framework. The solution must adhere to Clean Architecture principles, ensure maximum efficiency, and be ready to interface with a flawless UI/UX.

## Core Stack & LLM Configuration
- **Framework:** NanoBots
- **Language:** Python / Node.js (Select based on the existing repository ecosystem).
- **LLM Provider:** OpenRouter
- **Model ID:** `qwen/qwen3.6-plus-preview:free`
- **Base URL:** `https://openrouter.ai/api/v1`

## Architectural Requirements

### 1. Model & Provider Wiring
- Implement a dedicated LLM service interface to handle OpenRouter API calls.
- Ensure the `Authorization: Bearer <OPENROUTER_API_KEY>` header is securely managed via `.env`.
- Implement robust error handling for OpenRouter's rate limits (HTTP 429) with exponential backoff, considering we are using a free-tier model.

### 2. Memory Management (Context Optimization)
- Implement a dual-layer memory system:
  - **Short-term Memory:** Session-based, keeping track of the current conversational thread.
  - **Long-term Memory:** Vector database integration (e.g., ChromaDB, Qdrant, or SQLite with pgvector if using Postgres) to store and retrieve past interactions and subagent outputs.

### 3. Tool Wiring & Custom Skills
- Create a `skills/` directory containing modular, single-responsibility functions.
- Every tool must have a strongly typed schema (Pydantic/JSON Schema) so Qwen 3.6 can accurately use tool-calling capabilities.
- Implement at least two baseline skills: `web_search` and `file_reader`.

### 4. Subagent Orchestration
- Design a hierarchical agent structure:
  - **Orchestrator Agent:** Receives the main user prompt, breaks it down, and delegates tasks.
  - **Worker Subagents:** Specialized agents that execute specific skills (e.g., Data Processor, Code Reviewer).
- Use Qwen's 1M token context window to allow the Orchestrator to maintain the full state of the workers' outputs without losing detail.

### 5. Cron Scheduling & Automation
- Integrate a scheduling mechanism (e.g., `APScheduler` for Python or `node-cron` for Node.js).
- Create a `cron_jobs.py` (or equivalent) to trigger specific subagents at defined intervals.
- Ensure background jobs log their outputs to the long-term memory for the Orchestrator to review later.

## Output Standards
- Code must be fully modular, adhering to SOLID principles.
- Include comprehensive docstrings and type hints.
- Do not write monolithic files. Separate concerns: config, memory, agents, tools, and scheduler.
- Go one step further: Implement a clean API layer (FastAPI or NestJS) to expose this pipeline to a modern frontend, ensuring the backend supports a perfect UI/UX.
