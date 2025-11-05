# Lesson 7: Building the Complete StegoCrew MVP 🚀

**Duration:** 4-6 hours
**Prerequisite:** Lessons 1-6 completed
**Goal:** Build the complete 5-agent StegoCrew system with modular, production-ready code

---

## 📚 What You'll Build

By the end of this lesson, you will have:

1. ✅ A complete 5-agent CTF steganography solver
2. ✅ Modular codebase with proper structure (src/ directory)
3. ✅ Reusable tool library
4. ✅ Production-ready main application
5. ✅ Comprehensive reporting system
6. ✅ Working CTF challenge solver you can showcase

---

## Part 1: System Architecture Overview

### The Complete StegoCrew Team

```
┌─────────────────────────────────────────────────────────┐
│                   STEGOCREW SYSTEM                      │
└─────────────────────────────────────────────────────────┘
                           │
                    [Input: File]
                           │
                           ▼
        ┌──────────────────────────────────────┐
        │  🔍 AGENT 1: Reconnaissance Specialist│
        │  Tools: file, exiftool, entropy       │
        └──────────────────┬───────────────────┘
                           │
                    [File Analysis]
                           │
                           ▼
        ┌──────────────────────────────────────┐
        │  🛠️ AGENT 2: Steganography Expert     │
        │  Tools: steghide, binwalk, zsteg     │
        └──────────────────┬───────────────────┘
                           │
                  [Hidden Data Found]
                           │
                           ▼
        ┌──────────────────────────────────────┐
        │  🧩 AGENT 3: Pattern Hunter          │
        │  Tools: strings, regex, encoding ID  │
        └──────────────────┬───────────────────┘
                           │
                  [Patterns Detected]
                           │
                           ▼
        ┌──────────────────────────────────────┐
        │  🔐 AGENT 4: Decoder Specialist      │
        │  Tools: base64, hex, rot13, crypto   │
        └──────────────────┬───────────────────┘
                           │
                    [Data Decoded]
                           │
                           ▼
        ┌──────────────────────────────────────┐
        │  📊 AGENT 5: Orchestrator            │
        │  Compiles final report & flags       │
        └──────────────────┬───────────────────┘
                           │
                           ▼
                    [Output: Report]
                    [Found Flags: 🚩]
```

### Agent Responsibilities

| Agent | Role | Tools | Output |
|-------|------|-------|--------|
| **Reconnaissance** | Initial file analysis | file, exiftool, entropy | File characteristics, anomalies |
| **Stego Expert** | Extract hidden data | steghide, binwalk, zsteg | Extracted data, embedded files |
| **Pattern Hunter** | Detect patterns | strings, regex | Encoded data, suspicious patterns |
| **Decoder** | Decode/decrypt | base64, hex, crypto | Decoded messages, flags |
| **Orchestrator** | Coordinate & report | No tools | Comprehensive final report |

### Why 5 Agents?

**Specialization Benefits:**
1. Each agent masters specific techniques
2. Clear separation of concerns
3. Easy to debug and improve
4. Can run in parallel (future enhancement)
5. Mirrors real CTF team structure

**Sequential Workflow:**
- Each agent builds on previous findings
- Context flows through the pipeline
- No duplicate work
- Comprehensive coverage

---

## Part 2: Project Structure

### Directory Organization

```
StegoCrew/
├── src/
│   ├── __init__.py
│   ├── main.py                    # Main entry point
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── reconnaissance.py      # Agent 1
│   │   ├── stego_expert.py        # Agent 2
│   │   ├── pattern_hunter.py      # Agent 3
│   │   ├── decoder.py             # Agent 4
│   │   └── orchestrator.py        # Agent 5
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── file_analysis.py       # File type, metadata
│   │   ├── stego_tools.py         # Steghide, binwalk
│   │   ├── pattern_tools.py       # Strings, regex
│   │   └── decoder_tools.py       # Base64, hex, crypto
│   │
│   ├── tasks/
│   │   ├── __init__.py
│   │   └── task_definitions.py    # All task definitions
│   │
│   └── utils/
│       ├── __init__.py
│       ├── config.py              # Configuration
│       └── logger.py              # Logging setup
│
├── examples/
│   └── 06_complete_stegocrew.py   # Single-file demo
│
├── tests/
│   └── test_stegocrew.py
│
├── .env
├── requirements.txt
└── README.md
```

### Why This Structure?

**Modular Design:**
- Easy to find and modify code
- Each file has single responsibility
- Reusable components
- Testable units

**Scalability:**
- Add new agents easily
- Extend tool libraries
- Add new task types
- Support different workflows

---

## Part 3: Building the Tool Library

### Creating Reusable Tools

**File: src/tools/stego_tools.py**

```python
"""
Steganography tools for StegoCrew
Wraps common stego utilities with consistent interface
"""

import subprocess
import os
from crewai_tools import tool

def check_tool_installed(tool_name: str) -> bool:
    """Check if a system tool is installed."""
    try:
        subprocess.run(
            [tool_name, '--version'],
            capture_output=True,
            timeout=5,
            stderr=subprocess.DEVNULL
        )
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False

@tool
def extract_with_steghide(file_path: str, password: str = "") -> str:
    """Extract hidden data using steghide."""
    if not check_tool_installed('steghide'):
        return "❌ steghide not installed"

    # Implementation here...
    pass

@tool
def analyze_with_binwalk(file_path: str) -> str:
    """Analyze file for embedded data using binwalk."""
    if not check_tool_installed('binwalk'):
        return "❌ binwalk not installed"

    # Implementation here...
    pass

# Export all tools
__all__ = [
    'extract_with_steghide',
    'analyze_with_binwalk',
    # ... more tools
]
```

### Tool Categories

**1. File Analysis Tools** (`file_analysis.py`)
- get_file_type()
- extract_metadata()
- calculate_entropy()
- detect_anomalies()

**2. Steganography Tools** (`stego_tools.py`)
- extract_with_steghide()
- analyze_with_binwalk()
- analyze_lsb()
- extract_embedded_files()

**3. Pattern Tools** (`pattern_tools.py`)
- extract_strings()
- find_encoded_patterns()
- detect_encoding_type()
- search_for_flags()

**4. Decoder Tools** (`decoder_tools.py`)
- decode_base64()
- decode_hex()
- decode_rot13()
- try_all_decodings()

---

## Part 4: Creating the Agents

### Agent 1: Reconnaissance Specialist

**File: src/agents/reconnaissance.py**

```python
"""
Reconnaissance Agent - Initial file analysis
"""

from crewai import Agent
from ..tools.file_analysis import (
    get_file_type,
    extract_metadata,
    calculate_entropy
)

def create_recon_agent(llm):
    """Create the reconnaissance agent."""

    return Agent(
        role="File Reconnaissance Specialist",

        goal="Perform thorough initial file analysis to identify characteristics and anomalies",

        backstory="""You are a digital forensics expert with years of experience
        analyzing suspicious files. You start every investigation by carefully
        examining file properties, metadata, and structure. Your findings guide
        the entire team.""",

        tools=[
            get_file_type,
            extract_metadata,
            calculate_entropy
        ],

        llm=llm,
        verbose=True
    )
```

### Agent 2: Steganography Expert

**File: src/agents/stego_expert.py**

```python
"""
Steganography Expert Agent - Extract hidden data
"""

from crewai import Agent
from ..tools.stego_tools import (
    extract_with_steghide,
    analyze_with_binwalk,
    analyze_lsb
)

def create_stego_agent(llm):
    """Create the steganography expert agent."""

    return Agent(
        role="Steganography Extraction Expert",

        goal="Extract hidden data using specialized steganography tools and techniques",

        backstory="""You are a CTF veteran who has solved hundreds of steganography
        challenges. You know every technique: LSB, file embedding, steghide, and more.
        You systematically apply your tools to uncover hidden data.""",

        tools=[
            extract_with_steghide,
            analyze_with_binwalk,
            analyze_lsb
        ],

        llm=llm,
        verbose=True
    )
```

### Agent 3: Pattern Hunter

```python
"""
Pattern Hunter Agent - Detect encoding patterns
"""

from crewai import Agent
from ..tools.pattern_tools import (
    extract_strings,
    find_encoded_patterns,
    detect_encoding_type
)

def create_pattern_agent(llm):
    """Create the pattern hunter agent."""

    return Agent(
        role="Pattern Detection Specialist",

        goal="Identify encoded data, suspicious patterns, and potential flags",

        backstory="""You have a keen eye for patterns. You can spot base64,
        hex encoding, binary data, and other encodings instantly. You find
        what others miss.""",

        tools=[
            extract_strings,
            find_encoded_patterns,
            detect_encoding_type
        ],

        llm=llm,
        verbose=True
    )
```

### Agent 4: Decoder Specialist

```python
"""
Decoder Agent - Decode and decrypt data
"""

from crewai import Agent
from ..tools.decoder_tools import (
    decode_base64,
    decode_hex,
    try_all_decodings
)

def create_decoder_agent(llm):
    """Create the decoder specialist agent."""

    return Agent(
        role="Decoding and Decryption Specialist",

        goal="Decode encoded messages and decrypt data to reveal flags",

        backstory="""You are a cryptography expert who can decode any encoding.
        Base64, hex, ROT13, XOR - you've cracked them all. You work methodically
        through encodings until you find the flag.""",

        tools=[
            decode_base64,
            decode_hex,
            try_all_decodings
        ],

        llm=llm,
        verbose=True
    )
```

### Agent 5: Orchestrator

```python
"""
Orchestrator Agent - Coordinate and compile results
"""

from crewai import Agent

def create_orchestrator_agent(llm):
    """Create the orchestrator agent."""

    return Agent(
        role="Analysis Coordinator and Report Generator",

        goal="Synthesize all findings into comprehensive report and identify all flags",

        backstory="""You are an experienced CTF team leader who excels at
        coordinating complex investigations. You review all findings, identify
        the most important discoveries, and create clear, actionable reports
        highlighting all flags found.""",

        tools=[],  # No tools - synthesizes information

        llm=llm,
        verbose=True
    )
```

---

## Part 5: Defining Tasks

### Task Structure with Context

**File: src/tasks/task_definitions.py**

```python
"""
Task definitions for StegoCrew workflow
"""

from crewai import Task

def create_recon_task(file_path: str, agent):
    """Create reconnaissance task."""

    return Task(
        description=f"""
        Perform initial reconnaissance on: {file_path}

        Use your tools to:
        1. Identify file type and size
        2. Extract all metadata
        3. Calculate entropy
        4. Note any anomalies

        Provide a clear summary of file characteristics.
        """,

        expected_output="Initial reconnaissance report with file characteristics and anomalies",

        agent=agent
    )


def create_stego_task(agent, context_tasks):
    """Create steganography extraction task."""

    return Task(
        description="""
        Based on the reconnaissance findings, extract hidden data.

        Use your tools to:
        1. Try steghide extraction (empty password first)
        2. Scan with binwalk for embedded files
        3. Analyze LSB channels (if PNG/BMP)

        Report all extracted data and findings.
        """,

        expected_output="Steganography analysis with all extracted data",

        agent=agent,
        context=context_tasks  # ← Sees previous agent's work
    )


def create_pattern_task(agent, context_tasks):
    """Create pattern detection task."""

    return Task(
        description="""
        Analyze all data found so far for patterns and encodings.

        Use your tools to:
        1. Extract and examine strings
        2. Identify encoding patterns (base64, hex, binary)
        3. Search for flag formats (CTF{...}, FLAG{...})

        Report all suspicious patterns and potential encoded data.
        """,

        expected_output="Pattern analysis with encoding detection",

        agent=agent,
        context=context_tasks
    )


def create_decoder_task(agent, context_tasks):
    """Create decoding task."""

    return Task(
        description="""
        Decode all encoded data identified by the pattern hunter.

        Use your tools to:
        1. Decode base64 strings
        2. Decode hex data
        3. Try other common encodings
        4. Look for flags in decoded data

        Report all successfully decoded messages and flags found.
        """,

        expected_output="Decoded messages and identified flags",

        agent=agent,
        context=context_tasks
    )


def create_orchestrator_task(agent, context_tasks):
    """Create final reporting task."""

    return Task(
        description="""
        Create comprehensive final report of the analysis.

        Your report should:
        1. Summarize findings from all agents
        2. Highlight the most important discoveries
        3. Clearly list all flags found (if any)
        4. Provide the solution path taken
        5. Suggest any further investigation needed

        Format professionally with clear sections.
        """,

        expected_output="Comprehensive final analysis report with all flags",

        agent=agent,
        context=context_tasks  # ← Sees ALL previous work
    )
```

### Context Flow

```
Task 1 (Recon) →
    Task 2 (Stego) [sees Task 1] →
        Task 3 (Pattern) [sees Task 1, 2] →
            Task 4 (Decoder) [sees Task 1, 2, 3] →
                Task 5 (Orchestrator) [sees Task 1, 2, 3, 4]
```

---

## Part 6: Building the Main Application

### Main Entry Point

**File: src/main.py**

```python
#!/usr/bin/env python3
"""
StegoCrew - Multi-Agent CTF Steganography Solver
Main application entry point
"""

import os
import sys
from dotenv import load_dotenv
from crewai import Crew, Process
from langchain_anthropic import ChatAnthropic

from agents.reconnaissance import create_recon_agent
from agents.stego_expert import create_stego_agent
from agents.pattern_hunter import create_pattern_agent
from agents.decoder import create_decoder_agent
from agents.orchestrator import create_orchestrator_agent

from tasks.task_definitions import (
    create_recon_task,
    create_stego_task,
    create_pattern_task,
    create_decoder_task,
    create_orchestrator_task
)

load_dotenv()


def analyze_file(file_path: str) -> str:
    """
    Analyze a file using the complete StegoCrew team.

    Args:
        file_path: Path to file to analyze

    Returns:
        Complete analysis report
    """

    # Validate file
    if not os.path.exists(file_path):
        return f"❌ ERROR: File not found - {file_path}"

    print("="*70)
    print("🔍 STEGOCREW: MULTI-AGENT CTF SOLVER")
    print("="*70)
    print(f"\n📁 Target: {file_path}\n")
    print("👥 Assembling Agent Team:")
    print("   1. 🔍 Reconnaissance Specialist")
    print("   2. 🛠️  Steganography Expert")
    print("   3. 🧩 Pattern Hunter")
    print("   4. 🔐 Decoder Specialist")
    print("   5. 📊 Orchestrator")
    print("\n" + "="*70 + "\n")

    # Initialize LLM
    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        temperature=0
    )

    # Create agents
    recon_agent = create_recon_agent(llm)
    stego_agent = create_stego_agent(llm)
    pattern_agent = create_pattern_agent(llm)
    decoder_agent = create_decoder_agent(llm)
    orchestrator_agent = create_orchestrator_agent(llm)

    # Create tasks with context chain
    recon_task = create_recon_task(file_path, recon_agent)
    stego_task = create_stego_task(stego_agent, [recon_task])
    pattern_task = create_pattern_task(pattern_agent, [recon_task, stego_task])
    decoder_task = create_decoder_task(decoder_agent, [stego_task, pattern_task])
    orchestrator_task = create_orchestrator_task(
        orchestrator_agent,
        [recon_task, stego_task, pattern_task, decoder_task]
    )

    # Create crew
    crew = Crew(
        agents=[
            recon_agent,
            stego_agent,
            pattern_agent,
            decoder_agent,
            orchestrator_agent
        ],
        tasks=[
            recon_task,
            stego_task,
            pattern_task,
            decoder_task,
            orchestrator_task
        ],
        process=Process.sequential,
        verbose=True
    )

    # Execute analysis
    print("🚀 Starting analysis...\n")
    result = crew.kickoff()

    # Display results
    print("\n" + "="*70)
    print("✅ ANALYSIS COMPLETE - FINAL REPORT")
    print("="*70)
    print(result)
    print("="*70)

    return result


def main():
    """Main CLI entry point."""

    if len(sys.argv) < 2:
        print("Usage: python -m src.main <file_path>")
        print("\nExample:")
        print("  python -m src.main test_files/challenge.jpg")
        sys.exit(1)

    file_path = sys.argv[1]
    analyze_file(file_path)


if __name__ == "__main__":
    main()
```

---

## Part 7: Putting It All Together

### Step-by-Step Build Process

**Step 1: Create Directory Structure**

```bash
mkdir -p src/{agents,tools,tasks,utils}
touch src/__init__.py
touch src/{agents,tools,tasks,utils}/__init__.py
```

**Step 2: Build Tool Libraries**

1. Copy and organize tools from Lesson 6
2. Create `src/tools/` modules
3. Export tools properly

**Step 3: Create Agent Modules**

1. Build each agent in `src/agents/`
2. Import necessary tools
3. Define clear roles and goals

**Step 4: Define Tasks**

1. Create task definitions in `src/tasks/`
2. Set up context chains
3. Write clear task descriptions

**Step 5: Build Main Application**

1. Create `src/main.py`
2. Import all components
3. Wire everything together

**Step 6: Test the System**

```bash
# Test with simple file
python -m src.main test_files/sample_with_metadata.txt

# Test with CTF challenge
python -m src.main test_files/challenge_steghide.jpg
```

---

## Part 8: Example Usage

### Running StegoCrew

```bash
# Activate environment
source venv/bin/activate

# Run on CTF challenge
python -m src.main test_files/challenge_metadata.jpg
```

### Expected Output

```
======================================================================
🔍 STEGOCREW: MULTI-AGENT CTF SOLVER
======================================================================

📁 Target: test_files/challenge_metadata.jpg

👥 Assembling Agent Team:
   1. 🔍 Reconnaissance Specialist
   2. 🛠️  Steganography Expert
   3. 🧩 Pattern Hunter
   4. 🔐 Decoder Specialist
   5. 📊 Orchestrator

======================================================================

🚀 Starting analysis...

[Agent 1: Reconnaissance]
Analyzing file characteristics...
✅ File type: JPEG image
✅ Size: 125 KB
✅ Entropy: 7.2/8.0 (normal)
✅ Metadata: 15 fields found

[Agent 2: Steganography Expert]
Checking for hidden data...
✅ Binwalk: No embedded files
✅ Steghide: Attempting extraction...
🚩 Flag found in metadata!

[Agent 3: Pattern Hunter]
Analyzing patterns...
✅ Found flag format: CTF{...}

[Agent 4: Decoder]
Decoding data...
✅ Flag already in plaintext

[Agent 5: Orchestrator]
Compiling final report...

======================================================================
✅ ANALYSIS COMPLETE - FINAL REPORT
======================================================================

STEGOCREW ANALYSIS REPORT

File: test_files/challenge_metadata.jpg
Analysis Date: 2025-11-05

FINDINGS SUMMARY:
1. File Type: JPEG image (125 KB)
2. Steganography: Flag found in EXIF metadata
3. No additional encoding detected

FLAGS FOUND:
🚩 CTF{check_the_exif_data}

SOLUTION PATH:
1. Initial reconnaissance identified JPEG with metadata
2. Metadata extraction revealed flag in Comment field
3. No decoding required - plaintext flag

RECOMMENDATION:
Challenge solved! Flag retrieved successfully.

======================================================================
```

---

## Part 9: Testing Your MVP

### Test Cases

**Test 1: Simple Metadata Challenge**
```bash
python -m src.main test_files/challenge_metadata.jpg
# Expected: Find flag in metadata
```

**Test 2: Steghide Challenge**
```bash
python -m src.main test_files/challenge_steghide.jpg
# Expected: Extract hidden data with steghide
```

**Test 3: Embedded Archive**
```bash
python -m src.main test_files/challenge_embedded_archive.jpg
# Expected: Detect ZIP with binwalk
```

**Test 4: Multi-Layer Challenge**
```bash
# Create challenge with metadata → password → steghide → flag
# Test the complete pipeline
```

### Validation Checklist

- ✅ All agents execute in order
- ✅ Context flows between tasks
- ✅ Tools work correctly
- ✅ Flags are detected
- ✅ Final report is comprehensive
- ✅ Error handling works
- ✅ Can handle various file types

---

## Part 10: What's Next

### Completed MVP Features

You now have:
- ✅ 5-agent team working together
- ✅ 15+ steganography tools
- ✅ Sequential workflow with context
- ✅ Comprehensive reporting
- ✅ Modular, maintainable code

### Future Enhancements (Lesson 8+)

1. **Logging & Debugging**
   - Detailed logs for each step
   - Progress tracking
   - Error diagnostics

2. **Performance Optimization**
   - Parallel tool execution
   - Caching results
   - Faster processing

3. **Additional Features**
   - GUI interface
   - Batch processing
   - Custom tool plugins
   - Machine learning integration

4. **Extended Capabilities**
   - More encoding types
   - Audio/video steganography
   - Advanced cryptography
   - Network steganography

---

## 📊 Progress Check

You should now have:

- ✅ Complete understanding of multi-agent architecture
- ✅ Working 5-agent StegoCrew system
- ✅ Modular codebase structure
- ✅ Production-ready CTF solver
- ✅ Portfolio-worthy project

---

## 🎯 Next Steps

1. **Build the MVP** - Follow the steps in this lesson
2. **Test thoroughly** - Use the provided test cases
3. **Extend functionality** - Add your own tools and agents
4. **Move to Lesson 8** - Testing, debugging, and polish

---

## 📚 Additional Resources

- **CrewAI Documentation:** https://docs.crewai.com/
- **CTF Challenge Sources:** https://ctftime.org/
- **Steganography Guide:** https://github.com/DominicBreuker/stego-toolkit

---

**You're building something amazing!** 🚀

The complete StegoCrew system brings together everything you've learned into a real-world application that can solve actual CTF challenges!
