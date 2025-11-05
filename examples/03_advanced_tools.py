#!/usr/bin/env python3
"""
Lesson 4: Advanced Tools Example
Demonstrates multi-parameter tools, error handling, and system command wrapping.
"""

import os
import subprocess
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import tool
from langchain_anthropic import ChatAnthropic

load_dotenv()

# ==================== ADVANCED TOOLS ====================

@tool
def search_in_file(file_path: str, search_term: str, case_sensitive: bool = False) -> str:
    """
    Search for a term in a file with configurable case sensitivity.

    Args:
        file_path: Path to the file
        search_term: Term to search for
        case_sensitive: Whether search should be case-sensitive (default: False)

    Returns:
        Matching lines with line numbers
    """
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()

        results = []
        for i, line in enumerate(lines, 1):
            line_to_check = line if case_sensitive else line.lower()
            term_to_check = search_term if case_sensitive else search_term.lower()

            if term_to_check in line_to_check:
                results.append(f"Line {i}: {line.strip()}")

        if results:
            return f"Found {len(results)} matches:\n" + "\n".join(results[:10])
        else:
            return f"No matches found for '{search_term}'"

    except FileNotFoundError:
        return f"ERROR: File not found - {file_path}"
    except Exception as e:
        return f"ERROR: {type(e).__name__}: {str(e)}"


@tool
def run_command_safely(command: str, file_path: str) -> str:
    """
    Run a safe system command on a file with timeout and error handling.

    Args:
        command: Command to run (file, strings, exiftool)
        file_path: Path to file

    Returns:
        Command output or error message
    """
    # Whitelist of allowed commands
    allowed_commands = ['file', 'strings', 'wc', 'head', 'tail']

    if command not in allowed_commands:
        return f"ERROR: Command '{command}' not allowed. Allowed: {', '.join(allowed_commands)}"

    try:
        result = subprocess.run(
            [command, file_path],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            return f"Output from '{command}':\n{result.stdout}"
        else:
            return f"Command failed: {result.stderr}"

    except subprocess.TimeoutExpired:
        return f"ERROR: Command '{command}' timed out (30 seconds)"
    except FileNotFoundError:
        return f"ERROR: Command '{command}' not found. Install it first."
    except Exception as e:
        return f"ERROR: {str(e)}"


@tool
def analyze_file_advanced(file_path: str, check_size: bool = True, check_type: bool = True) -> str:
    """
    Advanced file analysis with configurable checks.

    Args:
        file_path: Path to file
        check_size: Include file size analysis (default: True)
        check_type: Include file type detection (default: True)

    Returns:
        Comprehensive file analysis
    """
    import json

    try:
        analysis = {
            "file_path": file_path,
            "exists": os.path.exists(file_path)
        }

        if not analysis["exists"]:
            return json.dumps({"error": "File does not exist"}, indent=2)

        if check_size:
            size = os.path.getsize(file_path)
            analysis["size_bytes"] = size
            analysis["size_readable"] = f"{size / 1024:.2f} KB" if size > 1024 else f"{size} bytes"

        if check_type:
            result = subprocess.run(['file', file_path], capture_output=True, text=True)
            analysis["file_type"] = result.stdout.strip()

        analysis["is_readable"] = os.access(file_path, os.R_OK)
        analysis["is_writable"] = os.access(file_path, os.W_OK)

        return json.dumps(analysis, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e), "error_type": type(e).__name__}, indent=2)


# ==================== AGENT WITH ADVANCED TOOLS ====================

llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)

advanced_analyst = Agent(
    role="Advanced File Analyst",
    goal="Perform sophisticated file analysis using multiple tools",
    backstory="""You are an expert system analyst who uses advanced tools
    to thoroughly investigate files. You combine multiple data points to
    draw intelligent conclusions.""",
    tools=[search_in_file, run_command_safely, analyze_file_advanced],
    llm=llm,
    verbose=True
)

# ==================== TASK ====================

analysis_task = Task(
    description="""
    Perform a comprehensive analysis of the file: README.md

    Use your tools to:
    1. Get advanced file information
    2. Search for the word "StegoCrew" (case-insensitive)
    3. Run the 'wc' command to count lines

    Provide a complete report of your findings.
    """,
    agent=advanced_analyst,
    expected_output="Comprehensive analysis report with all findings"
)

# ==================== MAIN ====================

def main():
    print("="*60)
    print("🔧 Lesson 4: Advanced Tools Demonstration")
    print("="*60)
    print()

    crew = Crew(
        agents=[advanced_analyst],
        tasks=[analysis_task],
        verbose=True
    )

    result = crew.kickoff()

    print("\n" + "="*60)
    print("✅ ANALYSIS COMPLETE")
    print("="*60)
    print(result)


if __name__ == "__main__":
    main()
