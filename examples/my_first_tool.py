#!/usr/bin/env python3
"""
Your First Custom Tool - Practice from Lesson 4

Create a tool that counts specific types of lines in a file.
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import tool
from langchain_anthropic import ChatAnthropic

load_dotenv()

# ==================== YOUR CUSTOM TOOL ====================

@tool
def count_lines_by_type(file_path: str, line_type: str = "all") -> str:
    """
    Count different types of lines in a file.

    Args:
        file_path: Path to the file to analyze
        line_type: Type to count - "all", "empty", "comments", "code"

    Returns:
        Count of lines matching the specified type
    """
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            return f"ERROR: File not found - {file_path}"

        # Read the file
        with open(file_path, 'r') as f:
            lines = f.readlines()

        # Count based on type
        if line_type == "all":
            count = len(lines)
            return f"Total lines: {count}"

        elif line_type == "empty":
            count = sum(1 for line in lines if line.strip() == "")
            return f"Empty lines: {count}"

        elif line_type == "comments":
            # Count lines starting with # (Python comments)
            count = sum(1 for line in lines if line.strip().startswith("#"))
            return f"Comment lines: {count}"

        elif line_type == "code":
            # Non-empty, non-comment lines
            code_lines = [
                line for line in lines
                if line.strip() and not line.strip().startswith("#")
            ]
            count = len(code_lines)
            return f"Code lines: {count}"

        else:
            return f"ERROR: Unknown line_type '{line_type}'. Use: all, empty, comments, code"

    except PermissionError:
        return f"ERROR: Permission denied - {file_path}"
    except Exception as e:
        return f"ERROR: {type(e).__name__}: {str(e)}"


# ==================== TEST YOUR TOOL ====================

def test_tool():
    """Test the tool without an agent first."""
    print("="*60)
    print("Testing count_lines_by_type tool")
    print("="*60)

    # Test 1: Count all lines
    print("\nTest 1: All lines in README.md")
    result = count_lines_by_type("../README.md", "all")
    print(result)

    # Test 2: Count empty lines
    print("\nTest 2: Empty lines")
    result = count_lines_by_type("../README.md", "empty")
    print(result)

    # Test 3: Count comments
    print("\nTest 3: Comment lines")
    result = count_lines_by_type("../README.md", "comments")
    print(result)

    # Test 4: Error case - invalid type
    print("\nTest 4: Invalid line type")
    result = count_lines_by_type("../README.md", "invalid")
    print(result)

    # Test 5: Error case - file not found
    print("\nTest 5: File not found")
    result = count_lines_by_type("nonexistent.txt", "all")
    print(result)

    print("\n" + "="*60)
    print("All tests complete!")
    print("="*60)


# ==================== USE WITH AN AGENT ====================

def use_with_agent():
    """Now use the tool with an agent."""
    print("\n" + "="*60)
    print("Using tool with an AI agent")
    print("="*60 + "\n")

    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)

    # Create an agent
    code_analyst = Agent(
        role="Code Analysis Specialist",
        goal="Analyze code files and provide statistics",
        backstory="""You are a code quality expert who analyzes
        source code files. You provide detailed statistics about
        code structure and composition.""",
        tools=[count_lines_by_type],
        llm=llm,
        verbose=True
    )

    # Create a task
    analysis_task = Task(
        description="""
        Analyze the file: ../README.md

        Use your line counting tool to:
        1. Count total lines
        2. Count empty lines
        3. Count comment lines
        4. Count code lines

        Provide a summary report with all these statistics.
        Calculate the percentage of comments vs code.
        """,
        agent=code_analyst,
        expected_output="Detailed code statistics report"
    )

    # Run it
    crew = Crew(
        agents=[code_analyst],
        tasks=[analysis_task],
        verbose=True
    )

    result = crew.kickoff()

    print("\n" + "="*60)
    print("AGENT ANALYSIS COMPLETE")
    print("="*60)
    print(result)


# ==================== MAIN ====================

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--agent":
        # Run with agent
        use_with_agent()
    else:
        # Run tests first
        test_tool()
        print("\n💡 Tip: Run with --agent to see it work with an AI agent!")
        print("   python my_first_tool.py --agent\n")
