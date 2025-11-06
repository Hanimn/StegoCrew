# Lesson 5: Multi-Agent Coordination

**Duration:** 3-4 hours
**Prerequisites:** Lessons 3-4 completed

---

## Why Multiple Agents?

**One agent doing everything:**
```python
super_agent = Agent(
    role="Do all the things",
    tools=[tool1, tool2, ..., tool20]  # Too many!
)
```

Problems:
- Overwhelmed by tool choices
- Unfocused decisions
- Hard to debug

**Specialized team:**
```python
agent1 = Agent(role="File Analysis", tools=[metadata_tool])
agent2 = Agent(role="Stego Expert", tools=[steghide, binwalk])
agent3 = Agent(role="Decoder", tools=[base64, hex])
```

Benefits:
- Clear responsibilities
- Focused tool use
- Easy to debug
- Sequential workflow

---

## Context Sharing

Agents share findings through task context:

```python
task1 = Task(
    description="Analyze file and report suspicious indicators",
    agent=agent1
)

task2 = Task(
    description="Based on previous analysis, extract hidden data",
    agent=agent2,
    context=[task1]  # Gets task1's output!
)
```

When agent2 runs, it sees:
```
Previous task output:
"File entropy: 7.9/8.0 (HIGH)
Metadata shows creation tool: Adobe but no Adobe markers
Recommendation: Check for steganography"

Your task: Based on previous analysis, extract hidden data
```

---

## Sequential Workflow

Tasks run in order, each building on previous results:

```python
from crewai import Crew, Process

crew = Crew(
    agents=[recon_agent, stego_agent, decoder_agent],
    tasks=[recon_task, stego_task, decoder_task],
    process=Process.sequential  # One at a time, in order
)

result = crew.kickoff(inputs={"file_path": "challenge.png"})
```

Flow:
```
recon_agent → finds high entropy
              ↓
stego_agent → extracts base64 string
              ↓
decoder_agent → decodes to flag
```

---

## Complete Example

Create `examples/04_multi_agent_crew.py`:

```python
#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import tool
from langchain_anthropic import ChatAnthropic

load_dotenv()

# Tools
@tool
def get_file_info(file_path: str) -> str:
    """Get basic file information."""
    if not os.path.exists(file_path):
        return f"File not found: {file_path}"
    size = os.path.getsize(file_path)
    return f"File: {file_path}\nSize: {size} bytes"

@tool
def extract_strings(file_path: str) -> str:
    """Extract readable strings from file."""
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        # Simple string extraction
        strings = []
        current = []
        for byte in data:
            if 32 <= byte <= 126:  # Printable ASCII
                current.append(chr(byte))
            elif current:
                if len(current) >= 4:
                    strings.append(''.join(current))
                current = []
        return "\n".join(strings[:20])  # First 20 strings
    except Exception as e:
        return f"Error: {str(e)}"

# LLM
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)

# Agents
analyst = Agent(
    role="File Analyst",
    goal="Analyze file and identify characteristics",
    backstory="You examine files methodically",
    tools=[get_file_info],
    llm=llm,
    verbose=True
)

extractor = Agent(
    role="Data Extractor",
    goal="Extract readable data from file",
    backstory="You pull out hidden text and patterns",
    tools=[extract_strings],
    llm=llm,
    verbose=True
)

reporter = Agent(
    role="Report Writer",
    goal="Summarize all findings",
    backstory="You compile results clearly",
    tools=[],
    llm=llm,
    verbose=True
)

# Tasks
analyze_task = Task(
    description="Analyze the file at {file_path} and report basic info",
    agent=analyst,
    expected_output="File analysis summary"
)

extract_task = Task(
    description="Extract strings from {file_path} based on analysis",
    agent=extractor,
    context=[analyze_task],  # Sees analyst's output
    expected_output="Extracted strings"
)

report_task = Task(
    description="Compile findings into final report",
    agent=reporter,
    context=[analyze_task, extract_task],  # Sees both outputs
    expected_output="Summary report"
)

# Crew
crew = Crew(
    agents=[analyst, extractor, reporter],
    tasks=[analyze_task, extract_task, report_task],
    process=Process.sequential,
    verbose=True
)

if __name__ == '__main__':
    result = crew.kickoff(inputs={"file_path": "/etc/hosts"})
    print("\n" + "="*60)
    print("FINAL RESULT:")
    print("="*60)
    print(result)
```

Run it:
```bash
python examples/04_multi_agent_crew.py
```

---

## How Context Works

**Task definitions:**
```python
task1 = Task(..., agent=agent1)
task2 = Task(..., agent=agent2, context=[task1])
task3 = Task(..., agent=agent3, context=[task1, task2])
```

**What each agent sees:**
- agent1: Only the task description
- agent2: task description + task1's output
- agent3: task description + task1's output + task2's output

**Task inputs:**

Use `{variable}` in descriptions:
```python
crew.kickoff(inputs={"file_path": "test.jpg", "target": "flag"})

task = Task(
    description="Analyze {file_path} looking for {target}",
    ...
)
```

---

## Common Patterns

**Pattern 1: Analysis Pipeline**
```
Reconnaissance → Extraction → Decoding → Reporting
```

**Pattern 2: Parallel then Merge**
```
Agent1 ─┐
Agent2 ─┼─→ Coordinator → Report
Agent3 ─┘
```
(Requires Process.hierarchical)

**Pattern 3: Iterative Refinement**
```
Analyzer → Validator → (if fail) → Analyzer again
```

---

## Debugging Multi-Agent Systems

**Problem: Agents don't share context properly**

Check context links:
```python
task2 = Task(..., context=[task1])  # Correct
task2 = Task(..., context=task1)     # Wrong! Must be list
```

**Problem: Task order wrong**

Agents run in the order listed in tasks array:
```python
tasks=[task1, task2, task3]  # Runs in this order
```

**Problem: Agent ignores previous findings**

Make task description reference previous work:
```python
description="Based on the previous agent's findings, extract..."
```

**Problem: Too much context**

If previous outputs are huge, agents get overwhelmed. Summarize:
```python
expected_output="Brief 2-3 sentence summary"  # Not paragraphs
```

---

## Best Practices

1. **3-5 agents ideal** - More than 5 gets complex
2. **One job per agent** - Keep roles focused
3. **Chain context carefully** - Not every task needs all previous outputs
4. **Clear handoffs** - Explicitly state what next agent should do
5. **Test individually** - Make sure each agent works alone first
6. **Limit output length** - Keep context manageable
7. **Use verbose mode** - See what agents are thinking

---

## Key Takeaways

**Sequential process:**
```python
Process.sequential  # Tasks run one at a time, in order
```

**Context sharing:**
```python
Task(..., context=[previous_task1, previous_task2])
```

**Task inputs:**
```python
crew.kickoff(inputs={"var": "value"})
# Use {var} in task descriptions
```

---

## Next Steps

You can now coordinate multiple agents. Next: integrating real steganography tools.

[Continue to Lesson 6: Steganography Tools →](./LESSON_06.md)

---

*Practice: Create a 3-agent crew that analyzes a text file: one counts words, one finds longest word, one summarizes.*
