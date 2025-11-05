# StegoCrew Source Code

This directory contains the modular, production-ready implementation of StegoCrew.

## 📁 Directory Structure

```
src/
├── __init__.py
├── main.py                    # Main entry point
│
├── agents/                    # Agent definitions
│   ├── __init__.py
│   ├── reconnaissance.py      # Agent 1: File analysis
│   ├── stego_expert.py        # Agent 2: Steganography extraction
│   ├── pattern_hunter.py      # Agent 3: Pattern detection
│   ├── decoder.py             # Agent 4: Decoding/decryption
│   └── orchestrator.py        # Agent 5: Report coordination
│
├── tools/                     # Tool libraries
│   ├── __init__.py
│   ├── file_analysis.py       # File type, metadata, entropy
│   ├── stego_tools.py         # Steghide, binwalk, zsteg
│   ├── pattern_tools.py       # Strings, regex, encoding detection
│   └── decoder_tools.py       # Base64, hex, crypto
│
├── tasks/                     # Task definitions
│   ├── __init__.py
│   └── task_definitions.py    # All task definitions with context
│
└── utils/                     # Utilities
    ├── __init__.py
    └── helpers.py             # Helper functions
```

## 🚀 Quick Start

### Running the Complete System

```bash
# From project root
python -m src.main test_files/challenge_metadata.jpg
```

### Usage

```python
from src.main import analyze_file

# Analyze a file
result = analyze_file("path/to/file.jpg")
print(result)
```

## 🛠️ Building the Modular Structure

Follow **Lesson 7** to build each component step-by-step.

### Step 1: Tool Libraries

Create tool modules in `src/tools/`:

- **file_analysis.py** - File type, metadata, entropy tools
- **stego_tools.py** - Steganography extraction tools
- **pattern_tools.py** - Pattern detection and string tools
- **decoder_tools.py** - Encoding/decoding tools

Each tool follows this pattern:

```python
from crewai_tools import tool
from ..utils.helpers import check_tool_installed

@tool
def my_tool(param: str) -> str:
    """Tool description."""
    if not check_tool_installed('tool_name'):
        return "❌ tool_name not installed"

    # Implementation
    return "result"
```

### Step 2: Agent Modules

Create agent modules in `src/agents/`:

Each agent module exports a `create_*_agent(llm)` function:

```python
from crewai import Agent
from ..tools.stego_tools import extract_with_steghide

def create_stego_agent(llm):
    """Create the steganography expert agent."""
    return Agent(
        role="Steganography Expert",
        goal="Extract hidden data",
        backstory="...",
        tools=[extract_with_steghide],
        llm=llm,
        verbose=True
    )
```

### Step 3: Task Definitions

Create `src/tasks/task_definitions.py`:

```python
from crewai import Task

def create_stego_task(agent, context_tasks):
    """Create steganography task."""
    return Task(
        description="...",
        expected_output="...",
        agent=agent,
        context=context_tasks  # ← Context chain
    )
```

### Step 4: Main Application

Create `src/main.py`:

```python
from .agents.reconnaissance import create_recon_agent
from .agents.stego_expert import create_stego_agent
# ... import all agents

from .tasks.task_definitions import (
    create_recon_task,
    create_stego_task,
    # ... import all tasks
)

def analyze_file(file_path: str):
    """Main analysis function."""
    # Create agents
    # Create tasks
    # Create crew
    # Execute and return results
    pass
```

## 📝 Development Notes

### Adding New Tools

1. Create tool function with `@tool` decorator
2. Add to appropriate tool module
3. Export in `__init__.py`
4. Import in agent module
5. Add to agent's tools list

### Adding New Agents

1. Create agent module in `src/agents/`
2. Define `create_*_agent(llm)` function
3. Import tools from tool modules
4. Create corresponding task in `task_definitions.py`
5. Wire into main.py

### Testing

```bash
# Test individual components
python -c "from src.tools.stego_tools import extract_with_steghide; print(extract_with_steghide('test.jpg'))"

# Test complete system
python -m src.main test_files/sample_with_metadata.txt
```

## 🎯 vs. Single-File Example

**Single-File (`06_complete_stegocrew.py`)**
- ✅ Easy to understand
- ✅ Quick to run
- ❌ Hard to maintain
- ❌ Not scalable

**Modular (`src/`)**
- ✅ Easy to maintain
- ✅ Reusable components
- ✅ Scalable
- ✅ Professional structure
- ✅ Testable

## 📚 Resources

- **Lesson 7** - Complete build guide
- **examples/06_complete_stegocrew.py** - Working single-file version
- **docs/lessons/LESSON_07.md** - Detailed documentation

---

**Build the future of CTF solving!** 🚀
