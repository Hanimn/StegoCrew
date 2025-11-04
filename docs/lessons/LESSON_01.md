# Lesson 1: Understanding Multi-Agent Systems & CrewAI

**Duration:** 1-2 hours
**Prerequisites:** Basic Python knowledge
**Goal:** Understand what we're building and why agents are powerful

---

## 🎯 What You'll Learn

By the end of this lesson, you'll understand:
1. What multi-agent systems are and why they're powerful
2. How CrewAI works at a high level
3. The architecture of our CTF solver
4. The roles of each agent in our system

---

## 📚 Part 1: The Problem We're Solving

### Traditional Approach to CTF Stego Challenges

Imagine solving a steganography challenge manually:

```
Step 1: Run exiftool to check metadata
        ↓ (nothing found)
Step 2: Try steghide with common passwords
        ↓ (password protected)
Step 3: Run binwalk to find embedded files
        ↓ (found a ZIP file!)
Step 4: Extract and analyze the ZIP
        ↓ (contains encoded text)
Step 5: Decode Base64
        ↓ (FLAG FOUND!)
```

**Problems with this approach:**
- ❌ Must remember all tools
- ❌ Trial and error is tedious
- ❌ Easy to miss techniques
- ❌ No systematic process
- ❌ Doesn't learn from experience

### The AI Agent Approach

Now imagine having a **team of experts** who:
- ✅ Know all the tools
- ✅ Work systematically
- ✅ Share findings with each other
- ✅ Make intelligent decisions
- ✅ Explain their reasoning

**This is what we're building!**

---

## 🧠 Part 2: What is an AI Agent?

### Definition

An **AI agent** is a program that can:
1. **Perceive** its environment (read inputs)
2. **Reason** about what to do (use LLM brain)
3. **Act** using tools (execute commands)
4. **Learn** from results (adapt approach)

### Simple Example

Let's see the difference:

**Traditional Script:**
```python
# Fixed logic - no intelligence
def analyze_file(filename):
    if filename.endswith('.png'):
        run_tool('zsteg')
    elif filename.endswith('.jpg'):
        run_tool('steghide')
    else:
        print("Unknown file type")
```

**AI Agent:**
```python
# Agent can reason and adapt
agent = Agent(
    role="Steganography Expert",
    goal="Find hidden data in files",
    backstory="You're a CTF veteran who knows all stego techniques..."
)

# Agent receives: suspicious.png
# Agent thinks: "PNG file... entropy looks high...
#                let me check LSB first, then try zsteg,
#                and if nothing works, check for polyglots..."
```

**Key difference:** The agent can **think** and **adapt**, not just follow rigid rules.

---

## 🏗️ Part 3: Multi-Agent Systems

### Why Multiple Agents?

**One agent doing everything:**
```
[Super Agent]
- Analyzes files
- Runs stego tools
- Finds patterns
- Decodes data
- Generates report

Problem: Too many responsibilities!
         Jack of all trades, master of none.
```

**Specialized agent team:**
```
[Recon Agent]        → Expert in file analysis
[Stego Expert]       → Master of stego tools
[Pattern Hunter]     → Specialist in finding patterns
[Decoder]            → Cryptography expert
[Orchestrator]       → Coordinates the team
```

**Benefits:**
- ✅ Each agent is focused and expert
- ✅ Agents work in sequence (pipeline)
- ✅ Clear handoffs between agents
- ✅ Easier to debug and improve
- ✅ Mimics how real teams work

### Real-World Analogy

Think of a **medical diagnosis team:**

```
Patient arrives with symptoms
         ↓
[Triage Nurse] → Initial assessment
         ↓
[Specialist] → Runs diagnostic tests
         ↓
[Lab Technician] → Analyzes test results
         ↓
[Doctor] → Interprets findings
         ↓
[Coordinator] → Compiles medical report
```

Each person has **expertise**, and they **pass information** to the next person.

Our CTF solver works the same way!

---

## 🔧 Part 4: How CrewAI Works

### The Four Core Components

CrewAI is built around 4 main concepts:

```
1. AGENTS  → Who does the work
2. TOOLS   → What they can use
3. TASKS   → What needs to be done
4. CREW    → How they work together
```

### 1. Agents (Team Members)

Each agent has:
- **Role:** Their job title (e.g., "File Analysis Specialist")
- **Goal:** What they're trying to achieve
- **Backstory:** Context that shapes their behavior
- **Tools:** What they can use
- **LLM:** Their "brain" (Claude, GPT-4, etc.)

**Example Agent Definition:**
```python
from crewai import Agent

recon_agent = Agent(
    role="File Analysis Specialist",
    goal="Thoroughly analyze file structure and metadata",
    backstory="""You're a digital forensics expert with 10 years
                 of CTF experience. You know how to spot anomalies
                 in file signatures, headers, and metadata.""",
    tools=[metadata_tool, entropy_tool],
    llm=llm,  # The AI brain
    verbose=True  # Show thinking process
)
```

**What happens when this agent runs:**
1. Receives a task
2. Reads the task description
3. Thinks about what to do (using LLM)
4. Decides which tool to use
5. Executes the tool
6. Interprets results
7. Decides next action or finishes

### 2. Tools (Capabilities)

Tools are functions that agents can call. Example:

```python
from crewai_tools import tool

@tool
def extract_metadata(file_path: str) -> str:
    """
    Extract metadata from an image file using exiftool.

    Args:
        file_path: Path to the image file

    Returns:
        Metadata information as formatted string
    """
    import subprocess
    result = subprocess.run(
        ['exiftool', file_path],
        capture_output=True,
        text=True
    )
    return result.stdout
```

**Important:** The docstring tells the agent what the tool does!

### 3. Tasks (Work Items)

Tasks define **what** needs to be done:

```python
from crewai import Task

analyze_file_task = Task(
    description="""
        Analyze the file at {file_path}.

        Your analysis should include:
        1. File type and format verification
        2. Metadata extraction
        3. Entropy calculation
        4. Any anomalies in file structure

        Provide a detailed report of your findings.
    """,
    agent=recon_agent,  # Who does this task
    expected_output="A comprehensive analysis report",
    output_file="recon_report.txt"  # Optional: save results
)
```

### 4. Crew (The Team)

The Crew brings it all together:

```python
from crewai import Crew, Process

stego_crew = Crew(
    agents=[recon_agent, stego_agent, decoder_agent],
    tasks=[analyze_task, stego_task, decode_task],
    process=Process.sequential,  # One task at a time
    verbose=True
)

# Run the crew!
result = stego_crew.kickoff(inputs={"file_path": "suspicious.png"})
```

**Process types:**
- `Process.sequential` - Tasks run in order (A → B → C)
- `Process.hierarchical` - Manager agent assigns tasks
- `Process.parallel` - Tasks run simultaneously (advanced)

---

## 🎯 Part 5: Our CTF Solver Architecture

### The 5-Agent Team

Let's meet our team members:

#### 1. 🔍 Reconnaissance Agent
**Role:** File Analysis Specialist
**Personality:** Methodical, detail-oriented
**Tools:** exiftool, file signature checker, entropy analyzer
**Job:** "I examine files to understand their structure and find anything unusual."

**Example output:**
```
File: suspicious.png
Type: PNG image (verified)
Size: 2.4 MB (larger than typical for this resolution)
Entropy: 7.8/8.0 (HIGH - suggests compressed or encrypted data)
Metadata: Created by "Adobe Photoshop" - but no Photoshop-specific markers found (SUSPICIOUS!)
Conclusion: High probability of hidden data.
```

#### 2. 🛠️ Steganography Expert Agent
**Role:** Steganography Specialist
**Personality:** Experienced, tool-savvy
**Tools:** steghide, binwalk, zsteg, LSB extractor
**Job:** "I use specialized tools to extract hidden data."

**Example output:**
```
Ran zsteg: No LSB data found
Ran steghide: Password-protected (trying common passwords...)
Ran binwalk: FOUND! Embedded ZIP file at offset 0x45A2B
Extracted: secret.zip (contains encoded_message.txt)
```

#### 3. 🧩 Pattern Hunter Agent
**Role:** Pattern Recognition Specialist
**Personality:** Observant, analytical
**Tools:** String extractor, encoding detector, pattern matcher
**Job:** "I find patterns and recognize encoding schemes."

**Example output:**
```
Analyzing: encoded_message.txt
Content: "Q1RGe2gxZGQzbl8xbl9wbDQxbl9zMWdodH0="
Pattern detected: Base64 encoding (ends with '=', valid Base64 charset)
Length: 44 characters
Recommendation: Decode as Base64
```

#### 4. 🔐 Decoder Agent
**Role:** Cryptanalysis Expert
**Personality:** Persistent, knowledgeable
**Tools:** Multi-cipher decoder, hash identifier, encoding chain solver
**Job:** "I decode and decrypt discovered data."

**Example output:**
```
Input: "Q1RGe2gxZGQzbl8xbl9wbDQxbl9zMWdodH0="
Attempting Base64 decode...
Result: "CTF{h1dd3n_1n_pl41n_s1ght}"
Format check: Matches CTF flag format!
FLAG FOUND: CTF{h1dd3n_1n_pl41n_s1ght}
```

#### 5. 📊 Orchestrator Agent
**Role:** Mission Coordinator
**Personality:** Strategic, organized
**Tools:** Result aggregator, report generator
**Job:** "I coordinate the team and compile the final report."

**Example output:**
```
=== CTF Challenge Solution Report ===
Challenge: suspicious.png

Solution Path:
1. Recon Agent identified high entropy and suspicious metadata
2. Stego Expert found embedded ZIP file using binwalk
3. Pattern Hunter detected Base64 encoding in extracted file
4. Decoder successfully decoded to reveal flag

FLAG: CTF{h1dd3n_1n_pl41n_s1ght}

Time taken: 47 seconds
Techniques used: File carving, Base64 decoding
```

### How They Work Together

```
INPUT: suspicious.png

    ↓

┌───────────────────────────────────────────┐
│ Orchestrator: "Team, analyze this file"  │
└───────────────────────────────────────────┘

    ↓

┌───────────────────────────────────────────┐
│ Recon: "High entropy detected,           │
│         likely contains hidden data"      │
└───────────────────────────────────────────┘

    ↓ (passes findings)

┌───────────────────────────────────────────┐
│ Stego Expert: "Found embedded ZIP file   │
│                Extracted: encoded.txt"    │
└───────────────────────────────────────────┘

    ↓ (passes extracted file)

┌───────────────────────────────────────────┐
│ Pattern Hunter: "Detected Base64 encoding"│
└───────────────────────────────────────────┘

    ↓ (passes encoded data)

┌───────────────────────────────────────────┐
│ Decoder: "Decoded! FLAG FOUND!"          │
└───────────────────────────────────────────┘

    ↓ (passes flag)

┌───────────────────────────────────────────┐
│ Orchestrator: "Mission complete! Here's  │
│                the comprehensive report"  │
└───────────────────────────────────────────┘

    ↓

OUTPUT: Solution report + FLAG
```

---

## 💡 Part 6: Why This Approach is Powerful

### Traditional Script vs. Agent System

| Feature | Traditional Script | Agent System |
|---------|-------------------|--------------|
| **Adaptability** | Fixed logic | Can reason and adapt |
| **Tool selection** | Predefined | Intelligent choice |
| **Error handling** | Crashes or skips | Can try alternatives |
| **Explainability** | Silent execution | Shows reasoning |
| **Maintenance** | Hard to modify | Easy to add new agents/tools |
| **Learning** | None | Can improve with feedback |

### Real Example: Unexpected Challenge

**Scenario:** File has no extension

**Traditional script:**
```python
if filename.endswith('.png'):
    analyze_png()
else:
    print("Unknown file type")  # FAILS!
```

**Agent system:**
```
Agent: "No extension... let me check the file signature"
Agent: [uses file_signature_tool]
Agent: "File signature shows this is a PNG despite no extension"
Agent: "I'll proceed with PNG analysis tools"
```

**The agent can reason through unexpected situations!**

---

## 🧪 Part 7: How Information Flows Between Agents

### Context Sharing

Agents share information through **context**:

```python
# Task 1 output becomes available to Task 2
task_1 = Task(
    description="Analyze the file",
    agent=recon_agent,
    expected_output="Analysis report"
)

task_2 = Task(
    description="""
        Based on the analysis from the previous task,
        extract any hidden data you find.
    """,  # ← Can reference previous task!
    agent=stego_agent,
    context=[task_1]  # ← Explicitly link tasks
)
```

### What the Second Agent Sees

When `stego_agent` runs, they can see:
- The task description
- The output from `recon_agent`
- The original input file path

**Example context:**
```
You are the Steganography Expert Agent.

Previous findings from Recon Agent:
---
File: suspicious.png
Entropy: 7.8/8.0 (HIGH)
Metadata anomalies detected
---

Your task: Extract any hidden data based on these findings.
```

---

## 🎓 Part 8: Key Concepts Summary

### What is an Agent?
An AI-powered program that can **perceive, reason, act, and learn**.

### What is a Multi-Agent System?
Multiple specialized agents working together as a team.

### What is CrewAI?
A framework that makes it easy to create and coordinate agent teams.

### The Four Components:
1. **Agents** - Team members with roles
2. **Tools** - Capabilities they can use
3. **Tasks** - Work to be done
4. **Crew** - Coordination system

### Our Architecture:
5 specialized agents working sequentially to solve CTF stego challenges.

---

## ✅ Knowledge Check

Test your understanding:

**Question 1:** What's the main advantage of using multiple specialized agents instead of one super-agent?

<details>
<summary>Click to see answer</summary>

**Answer:** Specialized agents are experts in their domain, make clearer decisions, are easier to debug, and can be improved independently. Like having a team of specialists rather than one generalist.
</details>

**Question 2:** What are the four core components of CrewAI?

<details>
<summary>Click to see answer</summary>

**Answer:**
1. Agents (who does the work)
2. Tools (what they can use)
3. Tasks (what needs to be done)
4. Crew (how they work together)
</details>

**Question 3:** How do agents share information in CrewAI?

<details>
<summary>Click to see answer</summary>

**Answer:** Through task context - later tasks can access the outputs of earlier tasks by linking them with the `context` parameter.
</details>

---

## 🚀 What's Next?

Now that you understand the concepts, we'll:

1. ✅ You now understand multi-agent systems (this lesson)
2. ⏭️ **Next:** Set up your development environment
3. ⏭️ **Then:** Build your first simple agent (Hello World!)

---

## 📝 Homework (Optional but Recommended)

Before the next lesson, think about:

1. **What other domains could use multi-agent systems?**
   - Medical diagnosis?
   - Financial analysis?
   - Content creation?

2. **What would a 6th agent do in our system?**
   - Report formatter?
   - Password guesser?
   - Image manipulator?

3. **What tools would be most useful?**
   - Think about what stego challenges require

Write down your ideas - we'll reference them later!

---

**🎉 Congratulations!** You've completed Lesson 1!

You now understand:
- ✅ What multi-agent systems are
- ✅ How CrewAI works
- ✅ Our project architecture
- ✅ Why agents are powerful

**Next lesson:** [Setting Up Your Development Environment](./LESSON_02.md)

---

*Questions or confused about something? That's completely normal! Review the [GLOSSARY](../GLOSSARY.md) and take your time.*
