# Lesson 3: Your First CrewAI Agent (Hello World)

**Duration:** 2-3 hours
**Prerequisites:** Lessons 1 & 2 completed, environment set up
**Goal:** Build and run your first AI agent, understand how agents work

---

## 🎯 What You'll Learn

By the end of this lesson, you'll have:
1. ✅ Created your first AI agent
2. ✅ Given it a simple tool to use
3. ✅ Run a task with the agent
4. ✅ Understood how agents think and act
5. ✅ Debugged and seen agent reasoning

---

## 📚 Lesson Overview

We'll build this step-by-step:

```
Step 1: Understand the basic structure
Step 2: Create a simple tool
Step 3: Define an agent
Step 4: Create a task
Step 5: Run the agent
Step 6: See it work!
```

**By the end, you'll have a working agent that can analyze files!**

---

## Part 1: Understanding Agent Anatomy

Before we code, let's understand what we're building.

### What Makes an Agent?

An agent needs 4 things:

```python
Agent = {
    "role": "What job does this agent do?",
    "goal": "What is it trying to achieve?",
    "backstory": "Context that shapes behavior",
    "tools": ["What can it use?"]
}
```

### Real Example

Let's say we want an agent that checks if files exist:

```
Role: "File System Inspector"
Goal: "Verify that files exist and report their details"
Backstory: "You are a meticulous system administrator who ensures
            all files are properly organized and accessible."
Tools: [file_checker_tool]
```

---

## Part 2: Creating Your First Tool

Tools are **functions that agents can call**. Let's create a simple one!

### Create the Project File

First, let's create a simple example file:

```bash
# Navigate to your project
cd ~/ctf-stego-solver  # or wherever you created it

# Create examples directory if it doesn't exist
mkdir -p examples

# Create our first example
touch examples/01_first_agent.py
```

### Write Your First Tool

Open `examples/01_first_agent.py` and add this code:

```python
#!/usr/bin/env python3
"""
Lesson 3: Your First CrewAI Agent
A simple file checker agent to learn the basics.
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import tool
from langchain_anthropic import ChatAnthropic

# Load environment variables (API keys)
load_dotenv()

# ============================================
# PART 1: CREATE A TOOL
# ============================================

@tool
def check_file_exists(file_path: str) -> str:
    """
    Check if a file exists and return information about it.

    Args:
        file_path: The path to the file to check

    Returns:
        Information about the file (exists, size, etc.)
    """
    # Check if file exists
    if os.path.exists(file_path):
        # Get file size
        size = os.path.getsize(file_path)

        # Return information
        return f"""
File exists: YES
Path: {file_path}
Size: {size} bytes
Type: {'Directory' if os.path.isdir(file_path) else 'File'}
"""
    else:
        return f"File does not exist: {file_path}"


# ============================================
# PART 2: INITIALIZE THE LLM (Agent's Brain)
# ============================================

llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0  # 0 = deterministic, 1 = creative
)


# ============================================
# PART 3: CREATE AN AGENT
# ============================================

file_inspector = Agent(
    role="File System Inspector",

    goal="Check if files exist and provide detailed information about them",

    backstory="""You are a meticulous system administrator with years of
    experience managing file systems. You always verify files exist before
    working with them and provide clear, detailed reports.""",

    tools=[check_file_exists],  # Give the agent our tool

    llm=llm,  # Give the agent a brain (Claude)

    verbose=True  # Show us what the agent is thinking!
)


# ============================================
# PART 4: CREATE A TASK
# ============================================

inspection_task = Task(
    description="""
    Check if the file '/etc/hosts' exists on the system.

    Use your file checking tool to verify the file exists and
    provide all available information about it.

    Your report should be clear and concise.
    """,

    agent=file_inspector,  # Assign to our agent

    expected_output="A clear report stating whether the file exists and its details"
)


# ============================================
# PART 5: CREATE A CREW AND RUN!
# ============================================

def main():
    """Run the file inspection agent."""

    print("=" * 60)
    print("🤖 LESSON 3: Your First CrewAI Agent")
    print("=" * 60)
    print()

    # Create a crew with just one agent and one task
    crew = Crew(
        agents=[file_inspector],
        tasks=[inspection_task],
        verbose=True
    )

    # Run the crew!
    print("🚀 Starting agent...\n")
    result = crew.kickoff()

    # Show the result
    print("\n" + "=" * 60)
    print("✅ AGENT COMPLETED!")
    print("=" * 60)
    print("\n📋 Final Report:")
    print(result)
    print()


if __name__ == "__main__":
    main()
```

---

## Part 3: Understanding the Code

Let's break down what each part does:

### 1. The Tool Decorator

```python
@tool
def check_file_exists(file_path: str) -> str:
    """Check if a file exists..."""
```

**What happens:**
- `@tool` tells CrewAI this is a tool agents can use
- The **docstring** is crucial - the agent reads it to understand what the tool does!
- The agent decides when to call this function

### 2. The LLM (Brain)

```python
llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0
)
```

**What this means:**
- `ChatAnthropic` = Using Claude as the brain
- `temperature=0` = Deterministic (same input → same output)
- This is what makes the agent "intelligent"

### 3. The Agent Definition

```python
file_inspector = Agent(
    role="File System Inspector",
    goal="Check if files exist...",
    backstory="You are a meticulous...",
    tools=[check_file_exists],
    llm=llm,
    verbose=True
)
```

**What each part does:**
- `role` = Job title, shapes how agent thinks
- `goal` = What agent is trying to achieve
- `backstory` = Context that influences decisions
- `tools` = Array of tools agent can use
- `verbose=True` = Show agent's thinking process

### 4. The Task

```python
inspection_task = Task(
    description="Check if the file '/etc/hosts' exists...",
    agent=file_inspector,
    expected_output="A clear report..."
)
```

**What this does:**
- Gives the agent instructions
- Assigns the task to specific agent
- Defines what good output looks like

### 5. The Crew

```python
crew = Crew(
    agents=[file_inspector],
    tasks=[inspection_task],
    verbose=True
)

result = crew.kickoff()
```

**What happens:**
- `Crew` orchestrates agents and tasks
- `kickoff()` starts the execution
- Returns the final result

---

## Part 4: Run Your First Agent!

Time to see it in action!

### Step 1: Make the File Executable

```bash
chmod +x examples/01_first_agent.py
```

### Step 2: Run It!

```bash
python examples/01_first_agent.py
```

### What You'll See

You should see output like this:

```
============================================================
🤖 LESSON 3: Your First CrewAI Agent
============================================================

🚀 Starting agent...

# Agent File System Inspector
## Task: Check if the file '/etc/hosts' exists...

# Agent File System Inspector
## Thought: I need to use my file checking tool to verify
   if /etc/hosts exists.
## Using tool: check_file_exists
## Tool Input: {"file_path": "/etc/hosts"}
## Tool Output:
File exists: YES
Path: /etc/hosts
Size: 220 bytes
Type: File

## Final Answer:
The file /etc/hosts exists on the system. It is a regular file
(not a directory) with a size of 220 bytes. This is the standard
hosts file used for mapping hostnames to IP addresses.

============================================================
✅ AGENT COMPLETED!
============================================================

📋 Final Report:
[Agent's final answer displayed here]
```

---

## Part 5: What Just Happened?

Let's trace the execution:

```
1. Crew starts → gives task to file_inspector agent
2. Agent reads task: "Check if /etc/hosts exists"
3. Agent thinks: "I have a tool called check_file_exists"
4. Agent decides: "I should use this tool"
5. Agent calls: check_file_exists("/etc/hosts")
6. Tool executes and returns result
7. Agent interprets result
8. Agent writes final report
9. Task completes!
```

**The magic:** The agent *decided* to use the tool. You didn't tell it explicitly "call check_file_exists." It reasoned about the task and chose the right tool!

---

## Part 6: Experiment Time!

Now let's modify the code to understand how agents work.

### Experiment 1: Change the File Path

Modify the task description:

```python
inspection_task = Task(
    description="""
    Check if the file 'README.md' exists in the current directory.

    Use your file checking tool to verify the file exists and
    provide all available information about it.
    """,
    agent=file_inspector,
    expected_output="A clear report about README.md"
)
```

**Run it again!**

**What changed?** The agent now checks a different file!

### Experiment 2: Make the Task More Complex

```python
inspection_task = Task(
    description="""
    Check if BOTH of these files exist:
    1. README.md
    2. .env

    For each file, use your tool to check if it exists and
    report the findings. Compare their sizes if both exist.
    """,
    agent=file_inspector,
    expected_output="A comparison report of both files"
)
```

**Run it again!**

**What happens?** The agent will call the tool TWICE - once for each file! It figured out it needed to check both files.

### Experiment 3: Change the Agent's Personality

Modify the backstory:

```python
file_inspector = Agent(
    role="File System Inspector",
    goal="Check if files exist and provide detailed information about them",
    backstory="""You are a paranoid security officer who is extremely
    cautious. You always double-check everything and warn about potential
    security risks. You never trust that files are what they claim to be.""",
    tools=[check_file_exists],
    llm=llm,
    verbose=True
)
```

**Run it again!**

**What changes?** The agent's *tone* and *focus* changes! It might mention security concerns or be more cautious in its report.

---

## Part 7: Understanding Agent Decision-Making

### How Does the Agent Know What to Do?

When you give an agent a task, here's what happens internally:

```
1. Agent receives task description
2. LLM reads: role, goal, backstory, available tools
3. LLM thinks: "What should I do to accomplish this?"
4. LLM decides: "I should use tool X with parameter Y"
5. CrewAI executes the tool
6. LLM receives tool result
7. LLM thinks: "Is this enough or do I need more?"
8. LLM either:
   - Uses another tool
   - Provides final answer
```

**This is called "Agent Loop" or "ReAct Pattern":**
- **Re**asoning
- **Act**ion
- (Repeat until task complete)

---

## Part 8: Adding a Second Tool

Let's give our agent more capabilities!

Add this tool to your code:

```python
@tool
def count_lines_in_file(file_path: str) -> str:
    """
    Count the number of lines in a text file.

    Args:
        file_path: The path to the text file

    Returns:
        The number of lines in the file, or error message
    """
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            return f"File has {len(lines)} lines"
    except Exception as e:
        return f"Error reading file: {str(e)}"
```

**Update the agent to include both tools:**

```python
file_inspector = Agent(
    role="File System Inspector",
    goal="Check files and analyze their contents",
    backstory="""You are a thorough system administrator...""",
    tools=[check_file_exists, count_lines_in_file],  # Two tools now!
    llm=llm,
    verbose=True
)
```

**Give it a task that needs both tools:**

```python
inspection_task = Task(
    description="""
    Analyze the file '/etc/hosts'.

    First, verify it exists and get its size.
    Then, count how many lines it contains.

    Provide a complete report with all findings.
    """,
    agent=file_inspector,
    expected_output="Complete analysis including size and line count"
)
```

**Run it!**

**What happens?** The agent will:
1. Use `check_file_exists` first
2. Then use `count_lines_in_file`
3. Combine both results into a final report

**You didn't tell it the order!** The agent figured it out!

---

## Part 9: Common Issues & Debugging

### Issue 1: "API key not found"

**Error:**
```
anthropic.AnthropicError: API key not found
```

**Solution:**
- Check `.env` file has `ANTHROPIC_API_KEY=your_key_here`
- Make sure you're running from project root directory
- Verify: `python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('ANTHROPIC_API_KEY')[:10])"`

### Issue 2: Agent Doesn't Use the Tool

**Problem:** Agent gives answer without calling tool

**Reasons:**
1. Tool docstring is unclear - make it very descriptive
2. Task description doesn't indicate a tool is needed
3. Agent thinks it already knows the answer

**Solution:** Make task explicit:
```python
description="Use your check_file_exists tool to verify if /etc/hosts exists."
```

### Issue 3: Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'crewai'
```

**Solution:**
- Make sure venv is activated: `source venv/bin/activate`
- Reinstall: `pip install crewai crewai-tools`

---

## Part 10: Key Concepts Review

### What is a Tool?

```python
@tool
def my_tool(param: str) -> str:
    """Clear description of what this does"""
    # Do something
    return result
```

**Key points:**
- Decorated with `@tool`
- Has clear docstring (agent reads this!)
- Takes typed parameters
- Returns string or serializable data

### What is an Agent?

```python
Agent(
    role="Job title",
    goal="What to achieve",
    backstory="Context",
    tools=[list of tools],
    llm=brain
)
```

**Key points:**
- Has personality (role + backstory)
- Has objective (goal)
- Has capabilities (tools)
- Has intelligence (LLM)

### What is a Task?

```python
Task(
    description="Clear instructions",
    agent=which_agent,
    expected_output="What good looks like"
)
```

**Key points:**
- Instructions for the agent
- Assigned to specific agent
- Defines success criteria

### What is a Crew?

```python
Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    verbose=True
)
```

**Key points:**
- Orchestrates multiple agents
- Manages task execution
- Returns final results

---

## ✅ Practice Exercises

### Exercise 1: File Counter Agent

**Goal:** Create an agent that counts how many Python files are in a directory.

**Steps:**
1. Create a tool `count_python_files(directory: str)`
2. Create an agent with role "Python File Counter"
3. Give it a task to count Python files in current directory
4. Run and verify

<details>
<summary>Click for solution</summary>

```python
import os
import glob

@tool
def count_python_files(directory: str) -> str:
    """Count all Python files (.py) in a directory."""
    py_files = glob.glob(os.path.join(directory, "*.py"))
    return f"Found {len(py_files)} Python files in {directory}"

counter_agent = Agent(
    role="Python File Counter",
    goal="Count Python files in directories",
    backstory="You love Python and keep track of all .py files",
    tools=[count_python_files],
    llm=llm,
    verbose=True
)

count_task = Task(
    description="Count how many Python files are in the current directory (.)",
    agent=counter_agent,
    expected_output="Number of Python files found"
)
```
</details>

### Exercise 2: File Size Comparator

**Goal:** Agent that compares sizes of two files.

**Requirements:**
- Tool that gets file size
- Agent that compares and reports which is larger
- Task to compare README.md and .env

**Try it yourself before looking at the solution!**

---

## 🎓 What You've Learned

Congratulations! You now understand:

✅ **How to create tools** - Functions agents can use
✅ **How to define agents** - Role, goal, backstory, tools
✅ **How to create tasks** - Instructions for agents
✅ **How to run crews** - Orchestrating everything
✅ **How agents think** - Decision-making process
✅ **How to debug** - Common issues and solutions

---

## 🚀 What's Next?

Now that you understand the basics, we'll build on this:

**Next lesson: [Lesson 4 - Custom Tools Deep Dive](./LESSON_04.md)**

We'll learn:
- Creating complex tools with multiple parameters
- Error handling in tools
- Tools that return structured data
- Wrapping system commands (like binwalk, steghide)

---

## 📝 Homework

Before moving to Lesson 4:

1. **Modify the example** - Add a third tool of your choice
2. **Change personalities** - Try different backstories and see how output changes
3. **Break it intentionally** - Remove the tool docstring, see what happens
4. **Experiment with temperature** - Try `temperature=1` vs `temperature=0`

**Keep notes** - You'll reference this later!

---

## 💡 Key Takeaways

1. **Agents are intelligent** - They decide which tools to use
2. **Docstrings matter** - Agents read them to understand tools
3. **Backstory shapes behavior** - Personality influences output
4. **Tasks should be clear** - Explicit instructions work best
5. **Verbose=True is your friend** - See what agents are thinking

---

**🎉 Congratulations on creating your first AI agent!**

You're now ready to build more complex systems!

*Questions? Review the [GLOSSARY](../GLOSSARY.md) for any unfamiliar terms.*

*Previous: [Lesson 2 - Environment Setup](./LESSON_02.md)*
*Next: [Lesson 4 - Custom Tools Deep Dive](./LESSON_04.md)*
