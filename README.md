# College Football Agent

An agentic program that uses AI agents to answer questions about college football.

## Setup

1. **Create a virtual environment:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file:**

   Create a `.env` file in the project root with your API keys:

   ```bash
   OPENAI_API_KEY=your_api_key_here
   ```

## Running the Application

```bash
python main.py
```

## Running Tests

Run all tests:

```bash
pytest tests/ -v
```

Run a specific test file:

```bash
pytest tests/test_scores_fetcher.py -v
```

## Directory Structure

```bash
cfb-agent/
├── main.py                               # Application entry point
├── requirements.txt                      # Python dependencies
├── pytest.ini                            # Pytest configuration
├── README.md                             # This file
├── src/
│   ├── agents/                           # AI agents
│   │   ├── base.py                       # Base agent class
│   │   ├── cfb_agent.py                  # Main College Football Agent interface
│   │   ├── router_agent.py               # Router agent for workflow selection
│   │   └── scores/                       # Scores feature (agents + workflow)
│   │       ├── scores_agent.py           # Score fetching agent
│   │       ├── scores_analyzer_agent.py  # Analysis enhancement agent
│   │       ├── scores_qa_agent.py        # Quality assurance agent
│   │       └── scores_workflow.py        # Scores workflow orchestrator
│   └── tools/                            # Tools agents can use
│       └── fetchers/                     # Data fetching tools
│           ├── scores_fetcher.py         # Score fetching with filtering
│           └── scores_data.json          # Score data file
└── tests/                                # Unit tests
    └── test_scores_fetcher.py
```

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
