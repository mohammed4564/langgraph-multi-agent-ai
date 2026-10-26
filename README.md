# Extensible Data Engineering Multi-Agent System

Modular LangGraph project with local Ollama (`qwen2.5:3b`), auto-discovered agents, shared graph state, and deterministic supervisor routing. Runs locally without a cloud API key.

## Architecture

```text
User request -> Supervisor (keyword-based routing)
                      |-> SQL Agent -> END
                      |-> Quality Agent -> END
                      |-> Reporting Agent -> END
```

Each request selects **one** specialist. This is a modular multi-agent router, not yet a multi-step collaborative orchestration engine. SQL is generated but **not executed**. CSV quality metrics are computed with pandas.

## Project layout

```text
main.py                 CLI entrypoint
config.py               Ollama settings
agents/base.py          Agent interface
agents/registry.py      Auto-discovery and registration
agents/sql_agent.py     SQL generation
agents/quality_agent.py CSV validation
agents/reporting_agent.py Reporting
core/state.py           Shared LangGraph state
core/llm.py             Shared local model client
core/workflow.py        Dynamic LangGraph routing
data/customers.csv      Sample data
tests/test_registry.py  Registry smoke tests
```

## Setup (Windows PowerShell)

Install Python 3.11 or 3.12 and [Ollama](https://ollama.com/). From the project directory:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
ollama pull qwen2.5:3b
python main.py
```

Ensure Ollama is running (`ollama serve` if not already started). If Python 3.12 is unavailable, use a supported installed Python version.

Example questions:
- `Write a SQL query to find duplicate CustomerID values`
- `Check missing values and duplicate rows in the CSV`
- `Write a data engineering report outline`

Run tests:

```powershell
python -m pytest -q
```

## Add an agent without editing the graph

Create `agents/pyspark_agent.py`:

```python
from agents.base import BaseAgent
from agents.registry import register
from core.llm import get_llm

@register
class PySparkAgent(BaseAgent):
    name = 'pyspark'
    description = 'Explain PySpark transformations'
    keywords = ('pyspark', 'spark', 'dataframe')

    def run(self, request: str) -> str:
        return str(get_llm().invoke('Explain using PySpark: ' + request).content)
```

Restart `python main.py`. The registry discovers the module automatically and the graph adds the node and route. Note: this example **explains PySpark**, it does not run Spark jobs.

## Configuration

Environment variables:
- `OLLAMA_MODEL` (default `qwen2.5:3b`)
- `OLLAMA_BASE_URL` (default `http://localhost:11434`)

## Roadmap

- Add structured LLM-based routing and fallback handling.
- Add multi-step plans and agent-to-agent handoffs.
- Integrate SQL Server with read-only credentials, query validation, and execution limits.
- Add PySpark execution in a controlled environment.
- Add checkpoints, tracing, human approval, and integration tests.

## Security

Never commit secrets or database credentials. SQL generation is not execution; validate and approve any generated SQL before connecting an executor. Do not run untrusted model-generated Python or shell commands automatically.
