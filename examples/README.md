# 🧪 CrewAI Examples - Learn by Doing

This directory contains hands-on examples to accompany the lessons.

---

## 📚 Examples by Lesson

### Lesson 3: Your First CrewAI Agent

**01_first_agent.py** - Basic single agent with one tool
- ✅ Learn agent structure
- ✅ Create your first tool
- ✅ Run a simple task
- ✅ See agent reasoning

**Run it:**
```bash
cd examples
python 01_first_agent.py
```

**02_agent_with_two_tools.py** - Agent with multiple tools
- ✅ Multiple tools in one agent
- ✅ Watch agent choose which tool to use
- ✅ More complex task

**Run it:**
```bash
python 02_agent_with_two_tools.py
```

---

## 🚀 How to Use These Examples

### Step 1: Make sure your environment is activated

```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Step 2: Ensure your .env file has your API key

```bash
# Should contain:
ANTHROPIC_API_KEY=your_key_here
```

### Step 3: Run any example

```bash
cd examples
python 01_first_agent.py
```

---

## 💡 Learning Tips

1. **Run First** - See it work before modifying
2. **Read the Code** - Each section is commented
3. **Experiment** - Change values and see what happens
4. **Break It** - Remove things to understand what they do
5. **Add Features** - Try adding your own tools

---

## 🎯 Suggested Learning Path

1. Run `01_first_agent.py` without changes
2. Modify the file path in the task
3. Change the agent's backstory
4. Add your own tool
5. Move to `02_agent_with_two_tools.py`
6. Create your own example combining concepts

---

## 🐛 Troubleshooting

**Error: "No module named 'crewai'"**
- Solution: Activate your venv and run `pip install -r requirements.txt`

**Error: "API key not found"**
- Solution: Check your .env file has `ANTHROPIC_API_KEY=...`

**Agent doesn't use the tool**
- Solution: Make the task description more explicit about using tools

---

## 📝 Your Own Examples

Create your own examples here!

**Template:**
```python
#!/usr/bin/env python3
"""Your example description"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import tool
from langchain_anthropic import ChatAnthropic

load_dotenv()

# Your tool here
@tool
def my_tool(param: str) -> str:
    """Tool description"""
    return "result"

# Your agent
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
my_agent = Agent(...)

# Your task
my_task = Task(...)

# Run it
crew = Crew(agents=[my_agent], tasks=[my_task])
result = crew.kickoff()
print(result)
```

---

**Happy coding! 🚀**

*Back to: [Lesson 3](../docs/lessons/LESSON_03.md)*
