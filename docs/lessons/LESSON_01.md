# Lesson 1: Understanding Multi-Agent Systems & CrewAI

**Duration:** 1-2 hours
**Prerequisites:** Basic Python knowledge

---

## The Problem

Here's how you currently solve CTF steganography challenges:

```
Run exiftool → nothing
Try steghide → password protected
Run binwalk → found ZIP!
Extract ZIP → encoded text
Decode Base64 → FLAG!
```

This works, but it's manual, tedious, and you'll forget tools. You need a systematic approach.

That's what we're building: a team of AI agents that automatically run through this process.

---

## What is an AI Agent?

An AI agent is a program that can:
1. Perceive its environment (read inputs)
2. Reason about what to do (think)
3. Act using tools (execute commands)
4. Learn from results (adapt)

**Traditional script:**
```python
def analyze_file(filename):
    if filename.endswith('.png'):
        run_tool('zsteg')
    elif filename.endswith('.jpg'):
        run_tool('steghide')
    else:
        print("Unknown file type")
```

**AI agent:**
```python
agent = Agent(
    role="Steganography Expert",
    goal="Find hidden data in files",
    backstory="CTF veteran who knows all stego techniques"
)

# Agent thinks: "PNG file, high entropy... try LSB first,
#                then zsteg, then check for polyglots..."
```

The agent can think and adapt, not just follow fixed rules.

---

## Why Multiple Agents?

**One agent doing everything:**
- Too many responsibilities
- Jack of all trades, master of none
- Hard to debug

**Specialized team:**
- Each agent has one focus
- Agents work in sequence
- Clear handoffs
- Easy to debug and improve

Real-world analogy: medical diagnosis team (triage → specialist → lab → doctor → coordinator). Each person has expertise and passes information to the next.

---

## How CrewAI Works

CrewAI has four core components:

**1. Agents** - Team members

Each agent needs:
- Role: Job title ("File Analysis Specialist")
- Goal: What they're trying to achieve
- Backstory: Context that shapes behavior
- Tools: What they can use
- LLM: Their "brain" (Claude, GPT-4, etc.)

Example:
```python
from crewai import Agent

recon_agent = Agent(
    role="File Analysis Specialist",
    goal="Analyze file structure and metadata",
    backstory="Digital forensics expert with 10 years of CTF experience",
    tools=[metadata_tool, entropy_tool],
    llm=llm,
    verbose=True
)
```

**2. Tools** - Capabilities

Tools are functions agents can call:

```python
from crewai_tools import tool

@tool
def extract_metadata(file_path: str) -> str:
    """Extract metadata from an image file using exiftool."""
    import subprocess
    result = subprocess.run(
        ['exiftool', file_path],
        capture_output=True,
        text=True
    )
    return result.stdout
```

The docstring is critical - it tells the agent what the tool does.

**3. Tasks** - Work items

Tasks define what needs to be done:

```python
from crewai import Task

analyze_file_task = Task(
    description="""
        Analyze the file at {file_path}.

        Include:
        1. File type verification
        2. Metadata extraction
        3. Entropy calculation
        4. Structural anomalies
    """,
    agent=recon_agent,
    expected_output="Analysis report"
)
```

**4. Crew** - The team

Brings it all together:

```python
from crewai import Crew, Process

stego_crew = Crew(
    agents=[recon_agent, stego_agent, decoder_agent],
    tasks=[analyze_task, stego_task, decode_task],
    process=Process.sequential,
    verbose=True
)

result = stego_crew.kickoff(inputs={"file_path": "suspicious.png"})
```

Process types:
- `Process.sequential` - Tasks run in order
- `Process.hierarchical` - Manager assigns tasks
- `Process.parallel` - Tasks run simultaneously

---

## Our 5-Agent System

**1. Reconnaissance Agent**
- Examines file structure and metadata
- Tools: exiftool, file checker, entropy analyzer
- Output example:
  ```
  File: suspicious.png
  Type: PNG (verified)
  Size: 2.4 MB (larger than typical)
  Entropy: 7.8/8.0 (HIGH - suggests hidden data)
  Metadata: Created by Photoshop but missing Photoshop markers (SUSPICIOUS)
  ```

**2. Steganography Expert**
- Runs specialized extraction tools
- Tools: steghide, binwalk, zsteg
- Output example:
  ```
  zsteg: No LSB data
  steghide: Password-protected
  binwalk: FOUND! Embedded ZIP at offset 0x45A2B
  Extracted: secret.zip
  ```

**3. Pattern Hunter**
- Detects encodings and patterns
- Tools: string extractor, encoding detector
- Output example:
  ```
  Content: "Q1RGe2gxZGQzbl8xbl9wbDQxbl9zMWdodH0="
  Pattern: Base64 (ends with '=', valid charset)
  Recommendation: Decode as Base64
  ```

**4. Decoder Agent**
- Decodes/decrypts data
- Tools: multi-cipher decoder, hash identifier
- Output example:
  ```
  Base64 decode: "CTF{h1dd3n_1n_pl41n_s1ght}"
  Format: Matches CTF flag pattern
  FLAG FOUND
  ```

**5. Orchestrator**
- Coordinates team and compiles report
- Tools: result aggregator, report generator
- Output example:
  ```
  === Solution Report ===
  1. Recon identified high entropy
  2. Stego Expert found embedded ZIP
  3. Pattern Hunter detected Base64
  4. Decoder revealed flag

  FLAG: CTF{h1dd3n_1n_pl41n_s1ght}
  Time: 47 seconds
  ```

---

## Workflow

```
suspicious.png
    ↓
[Recon] → "High entropy, likely contains data"
    ↓
[Stego] → "Found embedded ZIP, extracted encoded.txt"
    ↓
[Pattern] → "Detected Base64 encoding"
    ↓
[Decoder] → "Decoded! FLAG FOUND!"
    ↓
[Orchestrator] → "Solution report ready"
    ↓
Output: Report + FLAG
```

---

## Context Sharing Between Agents

Agents share information through task context:

```python
task_1 = Task(
    description="Analyze the file",
    agent=recon_agent
)

task_2 = Task(
    description="Extract hidden data based on analysis",
    agent=stego_agent,
    context=[task_1]  # Links to previous task
)
```

When stego_agent runs, it sees:
```
Previous findings from Recon Agent:
---
File: suspicious.png
Entropy: 7.8/8.0 (HIGH)
Metadata anomalies detected
---

Your task: Extract hidden data based on these findings.
```

---

## Why This Approach Works

| Feature | Script | Agents |
|---------|--------|--------|
| Adaptability | Fixed logic | Reasons and adapts |
| Tool selection | Predefined | Intelligent choice |
| Error handling | Crashes/skips | Tries alternatives |
| Explainability | Silent | Shows reasoning |
| Maintenance | Hard to modify | Easy to extend |

**Example:** File with no extension

Script fails:
```python
if filename.endswith('.png'):
    analyze_png()
else:
    print("Unknown")  # FAILS
```

Agent adapts:
```
"No extension... checking file signature"
"Signature shows PNG despite no extension"
"Proceeding with PNG analysis"
```

---

## Key Concepts

**Agent:** AI program that perceives, reasons, acts, and learns

**Multi-Agent System:** Specialized agents working as a team

**CrewAI:** Framework for creating agent teams

**Four Components:**
1. Agents - Team members
2. Tools - Capabilities
3. Tasks - Work items
4. Crew - Coordination

---

## Knowledge Check

**Q1: Why use multiple specialized agents instead of one?**

<details>
<summary>Answer</summary>
Specialized agents are experts in their domain, make clearer decisions, easier to debug, and can be improved independently.
</details>

**Q2: What are CrewAI's four core components?**

<details>
<summary>Answer</summary>
1. Agents (who), 2. Tools (capabilities), 3. Tasks (what), 4. Crew (coordination)
</details>

**Q3: How do agents share information?**

<details>
<summary>Answer</summary>
Through task context - later tasks access earlier task outputs via the `context` parameter.
</details>

---

## Next Steps

You now understand multi-agent systems and CrewAI architecture.

Next lesson: Setting up your development environment.

[Continue to Lesson 2 →](./LESSON_02.md)

---

*Confused? Check the [GLOSSARY](../GLOSSARY.md) or re-read sections. This is foundational material worth understanding well.*
