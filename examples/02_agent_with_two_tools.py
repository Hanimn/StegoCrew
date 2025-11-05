#!/usr/bin/env python3
"""
Lesson 3 Advanced: Agent with Multiple Tools
Demonstrates how an agent chooses between different tools.
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import tool
from langchain_anthropic import ChatAnthropic

load_dotenv()

# ============================================
# TOOLS
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
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        return f"""
File exists: YES
Path: {file_path}
Size: {size} bytes
Type: {'Directory' if os.path.isdir(file_path) else 'File'}
"""
    else:
        return f"File does not exist: {file_path}"


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


# ============================================
# AGENT WITH MULTIPLE TOOLS
# ============================================

llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0
)

file_inspector = Agent(
    role="File System Analyst",
    goal="Check files and analyze their contents thoroughly",
    backstory="""You are a thorough system administrator who not only
    checks if files exist but also analyzes their contents. You provide
    comprehensive reports about files.""",
    tools=[check_file_exists, count_lines_in_file],  # TWO TOOLS!
    llm=llm,
    verbose=True
)


# ============================================
# TASK REQUIRING MULTIPLE TOOLS
# ============================================

analysis_task = Task(
    description="""
    Perform a complete analysis of the file 'README.md'.

    First, verify the file exists and get its basic information.
    Then, count how many lines it contains.

    Provide a comprehensive report with all findings.
    """,
    agent=file_inspector,
    expected_output="Complete analysis including existence, size, and line count"
)


# ============================================
# RUN
# ============================================

def main():
    print("=" * 60)
    print("🤖 LESSON 3: Agent with Multiple Tools")
    print("=" * 60)
    print("\nWatch how the agent decides which tools to use!\n")

    crew = Crew(
        agents=[file_inspector],
        tasks=[analysis_task],
        verbose=True
    )

    result = crew.kickoff()

    print("\n" + "=" * 60)
    print("✅ ANALYSIS COMPLETE!")
    print("=" * 60)
    print("\n📋 Final Report:")
    print(result)
    print()


if __name__ == "__main__":
    main()
