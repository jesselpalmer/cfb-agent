# College Football Agent

An agentic program that uses AI agents to answer questions about college football.

## Setup

This project uses [uv](https://docs.astral.sh/uv/) to manage Python and dependencies. It requires Python 3.11 or newer.

1. **Install uv** (if you don't have it):

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install dependencies:**

   ```bash
   uv sync
   ```

   This creates a `.venv` and installs the locked dependencies from `uv.lock`, including the dev tools (pytest and Ruff).

3. **Create a `.env` file:**

   Create a `.env` file in the project root with your API keys:

   ```bash
   OPENAI_API_KEY=your_api_key_here
   ```

## Configuring the Model

Every agent uses the model set in `src/config.py`, which defaults to
`openai:gpt-5-nano`. Models use LangChain's `provider:model` format. To use a
different model without editing code, set `CFB_AGENT_MODEL` in your `.env`:

```bash
CFB_AGENT_MODEL=openai:gpt-5-mini
```

## Running the Application

```bash
uv run python main.py
```

## Running Tests

Tests run offline. They use a dummy API key and LangChain's fake chat model,
so no OpenAI key or network access is needed.

Run all tests:

```bash
uv run pytest -v
```

Run a specific test file:

```bash
uv run pytest tests/test_scores_fetcher.py -v
```

## Linting and Formatting

[Ruff](https://docs.astral.sh/ruff/) handles both linting and formatting:

```bash
uv run ruff check .          # lint
uv run ruff check --fix .    # lint and apply safe fixes
uv run ruff format .         # format
```

## Managing Dependencies

```bash
uv add <package>             # add a runtime dependency
uv add --dev <package>       # add a dev dependency
uv lock --upgrade            # upgrade locked versions
```

## Project Layout

- `src/agents/` holds the agents. Each feature, such as `scores/`, keeps its agents and workflow together in its own folder.
- `src/tools/` holds the tools agents can call, such as the data fetchers and their JSON data.
- `tests/` holds the unit tests, which run offline.

## Architecture

The system uses a multi-agent architecture to process user queries:

- **CfbAgent**: Main interface for the application. Handles user queries and coordinates the agent system.
- **RouterAgent**: Analyzes user queries and routes them to the appropriate workflow (used internally by CfbAgent).
- **ScoresAgent**: Handles score-related queries and uses tools to fetch game data.
- **ScoresAnalyzerAgent**: Enhances responses with analysis and context.
- **ScoresQAAgent**: Reviews and improves responses for quality assurance.
- **Scores Workflow**: Orchestrates the multi-agent pipeline (Scores → Analyzer → QA).

The system is organized using a feature-based structure where each feature (e.g., scores) contains its agents and workflow together. Score data is stored separately in JSON format for easy maintenance.

The system supports filtering game scores by team, date, status, and location.
