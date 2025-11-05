# Lesson 5: Multi-Agent Coordination

**Duration:** 3-4 hours
**Prerequisites:** Lessons 3 & 4 completed
**Goal:** Build teams of agents that work together to solve complex problems

---

## 🎯 What You'll Learn

By the end of this lesson, you'll have:
1. ✅ Created multiple specialized agents
2. ✅ Coordinated agents to work sequentially
3. ✅ Shared context between agents
4. ✅ Built task dependencies and handoffs
5. ✅ Understood crew processes (sequential, hierarchical)
6. ✅ Created your first multi-agent CTF solver prototype

---

## 📚 Lesson Overview

```
Part 1: Why Multiple Agents?
Part 2: Agent Specialization
Part 3: Sequential Workflows
Part 4: Context Sharing & Memory
Part 5: Task Dependencies
Part 6: Building Our CTF Crew
Part 7: Debugging Multi-Agent Systems
```

---

## Part 1: Why Multiple Agents?

### The Problem: One Agent Doing Everything

Imagine one agent trying to solve a CTF challenge:

```python
# ❌ BAD: One agent with ALL responsibilities
super_agent = Agent(
    role="CTF Solver",
    goal="Analyze files, extract data, decode messages, find flags",
    tools=[
        exiftool, binwalk, steghide, strings,
        base64_decode, rot13, caesar_cipher,
        entropy_calc, file_check, ...  # 20+ tools!
    ]
)
```

**Problems:**
- ❌ Overwhelming choice of tools (agent gets confused)
- ❌ Unfocused decision-making
- ❌ Tries to do everything at once
- ❌ Poor at specialization
- ❌ Hard to debug

### The Solution: Specialized Agent Team

```python
# ✅ GOOD: Multiple specialized agents
recon_agent = Agent(
    role="File Analyst",
    goal="Analyze file structure and metadata",
    tools=[exiftool, file_check, entropy_calc]  # Only 3 focused tools
)

stego_agent = Agent(
    role="Steganography Expert",
    goal="Extract hidden data",
    tools=[binwalk, steghide, strings]  # Only stego tools
)

decoder_agent = Agent(
    role="Decoder Specialist",
    goal="Decode encoded messages",
    tools=[base64_decode, rot13, caesar]  # Only decoding tools
)
```

**Benefits:**
- ✅ Each agent is focused and expert
- ✅ Clear responsibilities
- ✅ Easier tool selection
- ✅ Better decision quality
- ✅ Easy to debug

---

## Part 2: Agent Specialization

Let's create our first specialized agent team!

### Agent 1: The Reconnaissance Agent

```python
from crewai import Agent
from crewai_tools import tool
from langchain_anthropic import ChatAnthropic
import os

# Initialize LLM
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)

# Tools for reconnaissance
@tool
def check_file_type(file_path: str) -> str:
    """Identify file type using magic bytes and extension."""
    import subprocess
    result = subprocess.run(['file', file_path], capture_output=True, text=True)
    return result.stdout

@tool
def get_file_size(file_path: str) -> str:
    """Get file size in human-readable format."""
    size = os.path.getsize(file_path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

@tool
def calculate_file_entropy(file_path: str) -> str:
    """Calculate Shannon entropy (randomness) of file."""
    import math
    from collections import Counter

    with open(file_path, 'rb') as f:
        data = f.read()

    byte_counts = Counter(data)
    entropy = 0
    for count in byte_counts.values():
        p = count / len(data)
        entropy -= p * math.log2(p)

    if entropy > 7.5:
        assessment = "VERY HIGH - likely encrypted or compressed"
    elif entropy > 6:
        assessment = "HIGH - possible hidden data"
    elif entropy > 4:
        assessment = "MEDIUM - normal file"
    else:
        assessment = "LOW - simple data"

    return f"Entropy: {entropy:.4f}/8.0 - {assessment}"

# Create the Reconnaissance Agent
recon_agent = Agent(
    role="File Reconnaissance Specialist",

    goal="Perform thorough initial analysis of files to identify characteristics and anomalies",

    backstory="""You are a meticulous digital forensics expert with 10 years
    of experience. You always start investigations by thoroughly examining
    file properties, structure, and metadata. You have a keen eye for spotting
    anomalies that others miss.""",

    tools=[check_file_type, get_file_size, calculate_file_entropy],

    llm=llm,
    verbose=True
)
```

### Agent 2: The Steganography Expert

```python
@tool
def run_binwalk_analysis(file_path: str) -> str:
    """Analyze file for embedded files and data."""
    import subprocess
    result = subprocess.run(
        ['binwalk', file_path],
        capture_output=True,
        text=True,
        timeout=30
    )
    return result.stdout if result.returncode == 0 else "Binwalk found nothing"

@tool
def extract_strings_from_file(file_path: str) -> str:
    """Extract printable strings from file."""
    import subprocess
    result = subprocess.run(
        ['strings', file_path],
        capture_output=True,
        text=True
    )
    strings = result.stdout.split('\n')
    # Look for interesting strings
    interesting = [s for s in strings if 'flag' in s.lower() or 'CTF{' in s or len(s) > 30]
    return "\n".join(interesting[:20]) if interesting else "No interesting strings found"

stego_expert = Agent(
    role="Steganography Extraction Expert",

    goal="Extract and identify hidden data using specialized steganography tools",

    backstory="""You are a CTF veteran who has solved hundreds of steganography
    challenges. You know every trick in the book for hiding data in files. You
    systematically use your tools to uncover hidden information.""",

    tools=[run_binwalk_analysis, extract_strings_from_file],

    llm=llm,
    verbose=True
)
```

### Agent 3: The Pattern Decoder

```python
@tool
def detect_encoding(text: str) -> str:
    """Detect if text is Base64, hex, or other encoding."""
    import re

    # Check Base64
    if re.match(r'^[A-Za-z0-9+/]*={0,2}$', text) and len(text) % 4 == 0:
        return "Likely BASE64 encoded"

    # Check Hex
    if re.match(r'^[0-9A-Fa-f]+$', text):
        return "Likely HEX encoded"

    # Check Binary
    if re.match(r'^[01]+$', text):
        return "Likely BINARY encoded"

    return "Plain text or unknown encoding"

@tool
def decode_base64(encoded_text: str) -> str:
    """Decode Base64 encoded text."""
    import base64
    try:
        decoded = base64.b64decode(encoded_text).decode('utf-8')
        return f"Decoded: {decoded}"
    except:
        return "Failed to decode as Base64"

decoder_agent = Agent(
    role="Pattern Recognition and Decoding Specialist",

    goal="Identify encoding patterns and decode encrypted or encoded messages",

    backstory="""You are a cryptography expert who can spot encoded data
    instantly. You recognize patterns like Base64, hexadecimal, ROT13, and
    more. You systematically decode messages layer by layer.""",

    tools=[detect_encoding, decode_base64],

    llm=llm,
    verbose=True
)
```

---

## Part 3: Sequential Workflows

Now let's make these agents work together!

### Basic Sequential Workflow

```python
from crewai import Task, Crew, Process

# Task 1: Reconnaissance
recon_task = Task(
    description="""
    Perform initial analysis of the file: {file_path}

    Your analysis should include:
    1. File type identification
    2. File size
    3. Entropy calculation

    Provide a comprehensive report of your findings.
    """,

    expected_output="A detailed reconnaissance report",

    agent=recon_agent
)

# Task 2: Steganography Analysis
stego_task = Task(
    description="""
    Based on the reconnaissance findings, analyze the file for hidden data.

    Use your steganography tools to:
    1. Run binwalk to find embedded files
    2. Extract strings looking for flags or clues

    Report what you find.
    """,

    expected_output="Steganography analysis results",

    agent=stego_expert,

    context=[recon_task]  # ← This is key! Stego agent sees recon results
)

# Task 3: Decode Findings
decode_task = Task(
    description="""
    Analyze the data found by the steganography expert.

    If any encoded strings were found:
    1. Identify the encoding type
    2. Decode the data
    3. Look for CTF flags in the format CTF{...}

    Report your findings.
    """,

    expected_output="Decoded messages and potential flags",

    agent=decoder_agent,

    context=[stego_task]  # Decoder sees stego results
)

# Create the crew
ctf_crew = Crew(
    agents=[recon_agent, stego_expert, decoder_agent],

    tasks=[recon_task, stego_task, decode_task],

    process=Process.sequential,  # One agent at a time, in order

    verbose=True
)

# Run it!
result = ctf_crew.kickoff(inputs={"file_path": "challenge.png"})

print("\n" + "="*60)
print("FINAL RESULT:")
print("="*60)
print(result)
```

**What happens:**
1. Recon agent analyzes file → produces report
2. Stego expert reads recon report → extracts hidden data
3. Decoder reads stego findings → decodes messages
4. Final result combines all insights

---

## Part 4: Context Sharing & Memory

### How Agents Share Information

```python
# Task A produces output
task_a = Task(
    description="Find the file size",
    agent=agent_a,
    expected_output="File size in bytes"
)

# Task B can reference Task A's output
task_b = Task(
    description="""
    Based on the file size found in the previous analysis,
    determine if the file is suspiciously large or small.
    """,

    agent=agent_b,

    context=[task_a]  # ← Agent B sees Agent A's output!
)
```

**Under the hood:**
- CrewAI passes task_a's output to task_b
- Agent B's LLM sees both the description AND task_a's result
- Agent B can reference findings from Agent A

### Example: Context in Action

```python
# Agent 1 finds something
task_find = Task(
    description="Look for encoded strings in the file",
    agent=finder_agent,
    expected_output="List of suspicious strings"
)

# Agent 2 uses Agent 1's findings
task_decode = Task(
    description="""
    The previous agent found some suspicious strings.

    Examine each string they found and:
    1. Identify the encoding type
    2. Decode it
    3. Check if it's a flag

    Focus on the strings that look most promising.
    """,

    agent=decoder_agent,

    context=[task_find]  # Decoder sees finder's results
)
```

---

## Part 5: Task Dependencies

### Simple Chain

```
Task 1 (Recon) → Task 2 (Stego) → Task 3 (Decode)
```

```python
recon = Task(..., agent=recon_agent)
stego = Task(..., agent=stego_agent, context=[recon])
decode = Task(..., agent=decode_agent, context=[stego])
```

### Multiple Dependencies

```
       Task 1 (Recon)
       ↓             ↓
Task 2 (Stego)   Task 3 (Strings)
       ↓             ↓
       Task 4 (Decode) ← Uses both
```

```python
recon = Task(..., agent=recon_agent)

stego = Task(..., agent=stego_agent, context=[recon])
strings = Task(..., agent=string_agent, context=[recon])

# Decode sees BOTH stego and strings results
decode = Task(..., agent=decode_agent, context=[stego, strings])
```

---

## Part 6: Building Our CTF Crew

Let's put it all together into a real CTF solver!

### Complete Example

```python
#!/usr/bin/env python3
"""
Multi-Agent CTF Steganography Solver
"""

from crewai import Agent, Task, Crew, Process
from crewai_tools import tool
from langchain_anthropic import ChatAnthropic
import os
from dotenv import load_dotenv

load_dotenv()
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)

# ==================== TOOLS ====================

@tool
def analyze_file_properties(file_path: str) -> str:
    """Get basic file properties."""
    import subprocess
    size = os.path.getsize(file_path)
    file_type = subprocess.run(['file', file_path], capture_output=True, text=True)
    return f"Size: {size} bytes\nType: {file_type.stdout}"

@tool
def run_binwalk(file_path: str) -> str:
    """Check for embedded files."""
    import subprocess
    result = subprocess.run(['binwalk', file_path], capture_output=True, text=True)
    return result.stdout if "DECIMAL" in result.stdout else "No embedded files found"

@tool
def extract_strings(file_path: str) -> str:
    """Extract readable strings."""
    import subprocess
    result = subprocess.run(['strings', file_path], capture_output=True, text=True)
    lines = result.stdout.split('\n')
    interesting = [l for l in lines if 'flag' in l.lower() or 'CTF{' in l or len(l) > 30]
    return "\n".join(interesting[:10]) if interesting else "No interesting strings"

@tool
def decode_base64_string(encoded: str) -> str:
    """Decode Base64."""
    import base64
    try:
        return base64.b64decode(encoded).decode('utf-8')
    except:
        return "Not valid Base64"

# ==================== AGENTS ====================

recon_agent = Agent(
    role="Reconnaissance Specialist",
    goal="Analyze file properties and identify anomalies",
    backstory="Expert in digital forensics with keen eye for details",
    tools=[analyze_file_properties],
    llm=llm,
    verbose=True
)

stego_agent = Agent(
    role="Steganography Expert",
    goal="Extract hidden data using stego techniques",
    backstory="CTF veteran who knows all steganography tricks",
    tools=[run_binwalk, extract_strings],
    llm=llm,
    verbose=True
)

decoder_agent = Agent(
    role="Decoder Specialist",
    goal="Decode encoded messages and find flags",
    backstory="Cryptography expert skilled in pattern recognition",
    tools=[decode_base64_string],
    llm=llm,
    verbose=True
)

# ==================== TASKS ====================

recon_task = Task(
    description="Analyze the file {file_path} and report its properties",
    expected_output="File analysis report",
    agent=recon_agent
)

stego_task = Task(
    description="""
    Based on the reconnaissance, extract any hidden data from {file_path}.
    Use binwalk to check for embedded files and strings to find text.
    """,
    expected_output="Extracted data and findings",
    agent=stego_agent,
    context=[recon_task]
)

decode_task = Task(
    description="""
    Examine the data found by the steganography expert.
    If you find encoded strings, decode them.
    Look for flags in format: CTF{{...}} or FLAG{{...}}
    """,
    expected_output="Decoded messages and any flags found",
    agent=decoder_agent,
    context=[stego_task]
)

# ==================== CREW ====================

def solve_ctf_challenge(file_path: str):
    """Solve a CTF steganography challenge."""

    crew = Crew(
        agents=[recon_agent, stego_agent, decoder_agent],
        tasks=[recon_task, stego_task, decode_task],
        process=Process.sequential,
        verbose=True
    )

    print("="*60)
    print("🔍 STARTING CTF CHALLENGE ANALYSIS")
    print("="*60)
    print(f"File: {file_path}\n")

    result = crew.kickoff(inputs={"file_path": file_path})

    print("\n" + "="*60)
    print("✅ ANALYSIS COMPLETE")
    print("="*60)
    print(result)

    return result

# ==================== MAIN ====================

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = "README.md"  # Default test file

    solve_ctf_challenge(file_path)
```

**Usage:**
```bash
python ctf_solver.py challenge.png
```

---

## Part 7: Debugging Multi-Agent Systems

### Common Issues

**Issue 1: Agents Don't See Previous Results**

```python
# ❌ WRONG - missing context
task_2 = Task(
    description="Decode the data",
    agent=decoder_agent
    # Missing: context=[task_1]
)

# ✅ CORRECT
task_2 = Task(
    description="Decode the data from previous analysis",
    agent=decoder_agent,
    context=[task_1]  # ← This is crucial!
)
```

**Issue 2: Agents Repeat Work**

Make task descriptions clear about what NOT to do:

```python
task_2 = Task(
    description="""
    The previous agent already analyzed the file structure.
    DO NOT re-analyze.

    Your job is to decode the strings they found.
    """,
    agent=decoder_agent,
    context=[task_1]
)
```

**Issue 3: Too Much Context**

Don't overload agents with irrelevant information:

```python
# ❌ BAD - too much context
task_5 = Task(
    description="Final report",
    agent=reporter,
    context=[task_1, task_2, task_3, task_4]  # Overwhelming!
)

# ✅ BETTER - only relevant context
task_5 = Task(
    description="Create final report from decoder findings",
    agent=reporter,
    context=[task_4]  # Just the last task
)
```

### Debugging Tips

**1. Use verbose=True**
```python
agent = Agent(..., verbose=True)
crew = Crew(..., verbose=True)
```

**2. Check Task Outputs Individually**
```python
# Run crew step by step in debug mode
print("Task 1 output:", recon_task.output)
print("Task 2 output:", stego_task.output)
```

**3. Simplify First**
Start with 2 agents, then add more:
```python
# Start simple
crew = Crew(agents=[agent_1, agent_2], tasks=[task_1, task_2])

# Then expand
crew = Crew(agents=[agent_1, agent_2, agent_3], tasks=[task_1, task_2, task_3])
```

---

## 🧪 Practice Exercises

### Exercise 1: Add a Reporter Agent

Create a 4th agent that takes all findings and creates a formatted report.

**Requirements:**
- Agent role: "Report Generator"
- Takes context from all previous tasks
- Generates markdown-formatted report
- Highlights the flag if found

### Exercise 2: Parallel Analysis

Create two agents that work on the same file in parallel:
- Agent A: Analyzes metadata
- Agent B: Extracts strings

Then a third agent combines their findings.

**Hint:** Use `context=[task_a, task_b]` for the combiner.

---

## 🎓 Summary

You now understand:

✅ **Why multiple agents** are better than one super-agent
✅ **Agent specialization** and role definition
✅ **Sequential workflows** with task dependencies
✅ **Context sharing** between agents
✅ **Building multi-agent crews** for complex tasks
✅ **Debugging** multi-agent systems

---

## 🚀 What's Next?

**Next lesson: [Lesson 6 - Steganography Tool Integration](./LESSON_06.md)**

We'll learn:
- Integrating all real stego tools (steghide, binwalk, exiftool, zsteg)
- Building a complete tool library
- Creating specialized stego agents
- Handling edge cases and errors

---

## 📝 Homework

Before Lesson 6:

1. **Create a 4-agent crew** for analyzing text files
2. **Experiment with context** - try different combinations
3. **Break something intentionally** - remove context and see what happens
4. **Time your crews** - how long do different workflows take?

---

**🎉 Congratulations! You can now orchestrate teams of AI agents!**

*Previous: [Lesson 4 - Custom Tools Deep Dive](./LESSON_04.md)*
*Next: [Lesson 6 - Steganography Tool Integration](./LESSON_06.md)*
