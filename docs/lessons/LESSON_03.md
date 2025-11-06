# Lesson 3: Your First Agent

**Duration:** 2-3 hours
**Prerequisites:** Environment set up from Lesson 2

---

## Building a Simple File Inspector Agent

We'll create an agent that checks if files exist. Simple but demonstrates all core concepts.

**What you're building:**
```
Tool → Agent → Task → Crew → Result
```

---

## The Code

Create `examples/01_first_agent.py`:

```python
#!/usr/bin/env python3
"""Simple file checking agent - Hello World for CrewAI"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import tool
from langchain_anthropic import ChatAnthropic

load_dotenv()

# 1. CREATE A TOOL
@tool
def check_file_exists(file_path: str) -> str:
    """
    Check if a file exists and return information about it.

    Args:
        file_path: Path to the file to check

    Returns:
        File information or error message
    """
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        file_type = 'Directory' if os.path.isdir(file_path) else 'File'
        return f"Exists: YES\nPath: {file_path}\nSize: {size} bytes\nType: {file_type}"
    else:
        return f"File does not exist: {file_path}"


# 2. INITIALIZE LLM (the "brain")
llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0  # 0 = consistent, 1 = creative
)


# 3. CREATE AGENT
file_inspector = Agent(
    role="File System Inspector",
    goal="Check if files exist and provide details",
    backstory="You verify files exist before operations. Always thorough.",
    tools=[check_file_exists],
    llm=llm,
    verbose=True  # Shows agent's thinking process
)


# 4. CREATE TASK
inspection_task = Task(
    description="""
    Check if the file '/etc/hosts' exists.
    Use your file checking tool and report the results.
    """,
    agent=file_inspector,
    expected_output="Report on file existence and details"
)


# 5. CREATE CREW AND RUN
def main():
    print("Running file inspection agent...\n")

    crew = Crew(
        agents=[file_inspector],
        tasks=[inspection_task],
        verbose=True
    )

    result = crew.kickoff()

    print("\n" + "="*60)
    print("RESULT:")
    print("="*60)
    print(result)

if __name__ == '__main__':
    main()
```

---

## Run It

```bash
cd examples
python 01_first_agent.py
```

**What happens:**

1. Agent receives task: "Check if /etc/hosts exists"
2. Agent thinks: "I need to use my file checking tool"
3. Agent calls: `check_file_exists("/etc/hosts")`
4. Tool returns: File information
5. Agent reports: Results to user

**Output you'll see:**

```
> Entering new CrewAgentExecutor chain...
I need to check if the file exists using my tool.

Action: check_file_exists
Action Input: {"/etc/hosts"}

Exists: YES
Path: /etc/hosts
Size: 220 bytes
Type: File

Final Answer: The file /etc/hosts exists...
```

---

## How It Works

**The @tool decorator:**

Makes any function available to agents. The docstring is critical - agents read it to understand what the tool does.

```python
@tool
def my_tool(param: str) -> str:
    """Clear description of what this does."""  # Agent reads this!
    return result
```

**Agent structure:**

```python
Agent(
    role="Job title",           # What they do
    goal="What to achieve",     # Their objective
    backstory="Context",        # Shapes behavior
    tools=[list_of_tools],      # What they can use
    llm=llm,                    # Their "brain"
    verbose=True                # Show thinking
)
```

**Task structure:**

```python
Task(
    description="What to do",   # Instructions
    agent=which_agent,          # Who does it
    expected_output="Format"    # What you want back
)
```

**Crew orchestration:**

```python
Crew(
    agents=[agent1, agent2],    # The team
    tasks=[task1, task2],       # The work
    verbose=True                # Show process
)

result = crew.kickoff()         # Execute
```

---

## Agent Reasoning Process

When you run with `verbose=True`, you see the agent's thought process:

```
Thought: I need to check if this file exists
Action: check_file_exists
Action Input: "/etc/hosts"
Observation: Exists: YES, Size: 220 bytes
Thought: Now I have the information
Final Answer: The file exists at /etc/hosts...
```

This is the **ReAct pattern** (Reasoning + Acting):
- Agent reasons about what to do
- Agent acts using tools
- Agent observes results
- Agent reasons about next step
- Repeats until task complete

---

## Common Issues

**"Tool not found" error:**

Make sure tool is in the agent's tools list:
```python
agent = Agent(
    tools=[check_file_exists],  # Include your tool!
    ...
)
```

**Agent doesn't use the tool:**

Check the docstring is clear. Agent decides based on description:
```python
@tool
def vague_name(x: str) -> str:
    """Does stuff."""  # Too vague!
```

Better:
```python
@tool
def check_file_exists(file_path: str) -> str:
    """Check if a file exists and return size/type info."""  # Clear!
```

**Infinite loop:**

Agent keeps trying the same thing. Usually means:
- Tool is returning unclear results
- Expected output doesn't match what tool provides
- Agent can't determine if task is complete

Fix: Make tool return formats match task expectations.

**API errors:**

Check your `.env` file has valid `ANTHROPIC_API_KEY`.

---

## Experiments to Try

**1. Check different files:**

Modify the task description to check different paths:
```python
description="Check if the file '/var/log/syslog' exists."
```

**2. Add another tool:**

```python
@tool
def count_lines(file_path: str) -> str:
    """Count lines in a text file."""
    if not os.path.exists(file_path):
        return "File not found"
    with open(file_path) as f:
        return f"Lines: {len(f.readlines())}"

# Add to agent's tools
file_inspector = Agent(
    tools=[check_file_exists, count_lines],  # Two tools now!
    ...
)
```

Agent will choose which tool based on the task.

**3. Change temperature:**

```python
llm = ChatAnthropic(temperature=0.7)  # More creative responses
```

**4. Try multiple files:**

```python
description="""
Check if these files exist:
1. /etc/hosts
2. /etc/passwd
3. /etc/shadow

Report on each.
"""
```

---

## Key Takeaways

**Tool = Function + @tool decorator + docstring**
- Agents read docstrings to understand tools
- Return strings, not exceptions
- Handle errors inside the tool

**Agent = Role + Goal + Backstory + Tools + LLM**
- Role/goal/backstory shape behavior
- Tools define capabilities
- LLM provides reasoning

**Task = Description + Agent + Expected output**
- Description is the instruction
- Agent executes it
- Expected output guides format

**Crew = Agents + Tasks + Process**
- Orchestrates execution
- `kickoff()` starts the work
- Returns result

---

## Next Steps

You now have a working agent. Next lesson: building custom tools for steganography analysis.

[Continue to Lesson 4: Custom Tools →](./LESSON_04.md)

---

*Tip: Read the verbose output carefully. Understanding how agents think helps you write better tool descriptions and task instructions.*
