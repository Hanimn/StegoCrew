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
