#!/usr/bin/env python3
"""
Lesson 5: Multi-Agent Coordination Example
Demonstrates multiple specialized agents working together.
"""

import os
import subprocess
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import tool
from langchain_anthropic import ChatAnthropic

load_dotenv()
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)

# ==================== TOOLS FOR EACH AGENT ====================

# Reconnaissance Tools
@tool
def get_file_info(file_path: str) -> str:
    """Get basic file information."""
    try:
        size = os.path.getsize(file_path)
        result = subprocess.run(['file', file_path], capture_output=True, text=True)
        return f"Size: {size} bytes\nType: {result.stdout.strip()}"
    except Exception as e:
        return f"ERROR: {str(e)}"


@tool
def calculate_entropy(file_path: str) -> str:
    """Calculate file entropy (measure of randomness)."""
    import math
    from collections import Counter

    try:
        with open(file_path, 'rb') as f:
            data = f.read()

        if len(data) == 0:
            return "ERROR: Empty file"

        byte_counts = Counter(data)
        entropy = 0
        for count in byte_counts.values():
            p = count / len(data)
            entropy -= p * math.log2(p)

        assessment = "HIGH - possible encryption/compression" if entropy > 7 else "NORMAL"

        return f"Entropy: {entropy:.4f}/8.0 - {assessment}"
    except Exception as e:
        return f"ERROR: {str(e)}"


# Steganography Tools
@tool
def extract_strings(file_path: str) -> str:
    """Extract printable strings from file."""
    try:
        result = subprocess.run(
            ['strings', file_path],
            capture_output=True,
            text=True,
            timeout=30
        )

        lines = result.stdout.split('\n')
        # Look for interesting strings
        interesting = []

        for line in lines:
            if 'flag' in line.lower() or 'CTF{' in line or 'password' in line.lower():
                interesting.append(f"⭐ {line}")
            elif len(line) > 40:  # Long strings might be encoded data
                interesting.append(f"📝 {line}")

        if interesting:
            return "Interesting strings found:\n" + "\n".join(interesting[:15])
        else:
            return f"Found {len(lines)} strings, but none particularly interesting"

    except Exception as e:
        return f"ERROR: {str(e)}"


@tool
def check_for_embedded_files(file_path: str) -> str:
    """Check for files embedded within the file."""
    try:
        result = subprocess.run(
            ['binwalk', file_path],
            capture_output=True,
            text=True,
            timeout=60
        )

        if "DECIMAL" in result.stdout:
            return f"Embedded files detected!\n{result.stdout}"
        else:
            return "No embedded files detected"

    except FileNotFoundError:
        return "Note: binwalk not installed (optional for this demo)"
    except Exception as e:
        return f"ERROR: {str(e)}"


# Decoding Tools
@tool
def decode_base64(text: str) -> str:
    """Attempt to decode Base64 encoded text."""
    import base64

    try:
        decoded = base64.b64decode(text).decode('utf-8')
        return f"Successfully decoded:\n{decoded}"
    except Exception as e:
        return f"Not valid Base64 or decoding failed: {str(e)}"


@tool
def identify_encoding(text: str) -> str:
    """Identify the encoding type of text."""
    import re

    if re.match(r'^[A-Za-z0-9+/]*={0,2}$', text) and len(text) % 4 == 0:
        return "LIKELY BASE64: Contains Base64 character set and proper padding"

    if re.match(r'^[0-9A-Fa-f]+$', text) and len(text) % 2 == 0:
        return "LIKELY HEXADECIMAL: Contains only hex characters"

    if re.match(r'^[01]+$', text):
        return "LIKELY BINARY: Contains only 0s and 1s"

    if all(32 <= ord(c) <= 126 for c in text):
        return "PLAIN TEXT: All printable ASCII characters"

    return "UNKNOWN ENCODING: Unable to identify pattern"


# ==================== SPECIALIZED AGENTS ====================

# Agent 1: Reconnaissance Specialist
recon_agent = Agent(
    role="File Reconnaissance Specialist",
    goal="Perform initial file analysis to identify key characteristics",
    backstory="""You are a digital forensics expert with a keen eye for detail.
    You always start by thoroughly examining file properties and structure.
    Your analysis guides the rest of the team.""",
    tools=[get_file_info, calculate_entropy],
    llm=llm,
    verbose=True
)

# Agent 2: Steganography Expert
stego_agent = Agent(
    role="Steganography Extraction Expert",
    goal="Extract and identify hidden data using steganography techniques",
    backstory="""You are a CTF veteran who has solved hundreds of steganography
    challenges. You know how to find data hidden in plain sight. You systematically
    apply your tools to uncover secrets.""",
    tools=[extract_strings, check_for_embedded_files],
    llm=llm,
    verbose=True
)

# Agent 3: Decoder Specialist
decoder_agent = Agent(
    role="Encoding Detection and Decoding Specialist",
    goal="Identify and decode encoded messages to find flags",
    backstory="""You are a cryptography expert who can recognize encoding patterns
    instantly. You decode messages layer by layer, always on the hunt for CTF flags
    in formats like CTF{...} or FLAG{...}""",
    tools=[identify_encoding, decode_base64],
    llm=llm,
    verbose=True
)

# Agent 4: Report Coordinator
coordinator_agent = Agent(
    role="Analysis Coordinator and Report Generator",
    goal="Coordinate findings from all agents and create comprehensive report",
    backstory="""You are an experienced project manager who excels at synthesizing
    information from multiple sources. You create clear, actionable reports that
    highlight the most important findings.""",
    tools=[],  # No tools - just synthesizes information
    llm=llm,
    verbose=True
)

# ==================== SEQUENTIAL TASKS ====================

# Task 1: Initial Reconnaissance
recon_task = Task(
    description="""
    Analyze the file {file_path} and provide initial reconnaissance.

    Your analysis should include:
    1. File type and size
    2. Entropy calculation to detect anomalies

    Provide a clear summary of your findings.
    """,
    expected_output="Initial reconnaissance report with file characteristics",
    agent=recon_agent
)

# Task 2: Steganography Analysis
stego_task = Task(
    description="""
    Based on the reconnaissance findings, analyze {file_path} for hidden data.

    Use your tools to:
    1. Extract strings and look for interesting text
    2. Check for embedded files

    Report all findings, especially anything that looks like encoded data.
    """,
    expected_output="Steganography analysis with extracted data",
    agent=stego_agent,
    context=[recon_task]  # ← Sees recon agent's findings
)

# Task 3: Decode Findings
decode_task = Task(
    description="""
    Analyze the data found by the steganography expert.

    For any suspicious strings or encoded text:
    1. Identify the encoding type
    2. Attempt to decode it
    3. Look for CTF flags in format: CTF{{...}} or FLAG{{...}}

    Report what you decode and highlight any flags found.
    """,
    expected_output="Decoded messages and flag candidates",
    agent=decoder_agent,
    context=[stego_task]  # ← Sees stego agent's findings
)

# Task 4: Final Report
report_task = Task(
    description="""
    Create a comprehensive final report of the analysis.

    Your report should:
    1. Summarize findings from all agents
    2. Highlight the most important discoveries
    3. Clearly identify any flags found
    4. Provide recommendations for further investigation if needed

    Format the report in a clear, professional manner.
    """,
    expected_output="Comprehensive final analysis report",
    agent=coordinator_agent,
    context=[recon_task, stego_task, decode_task]  # ← Sees ALL previous work
)

# ==================== MULTI-AGENT CREW ====================

def analyze_file(file_path: str):
    """Analyze a file using the multi-agent crew."""

    print("="*70)
    print("🔍 STEGOCREW: MULTI-AGENT FILE ANALYSIS")
    print("="*70)
    print(f"\n📁 Analyzing file: {file_path}\n")
    print("👥 Agent Team:")
    print("   1. 🔍 Reconnaissance Specialist")
    print("   2. 🛠️  Steganography Expert")
    print("   3. 🔐 Decoder Specialist")
    print("   4. 📊 Report Coordinator")
    print("\n" + "="*70 + "\n")

    # Create the crew
    crew = Crew(
        agents=[recon_agent, stego_agent, decoder_agent, coordinator_agent],
        tasks=[recon_task, stego_task, decode_task, report_task],
        process=Process.sequential,  # One agent at a time
        verbose=True
    )

    # Execute the analysis
    result = crew.kickoff(inputs={"file_path": file_path})

    # Display final result
    print("\n" + "="*70)
    print("✅ ANALYSIS COMPLETE - FINAL REPORT")
    print("="*70)
    print(result)
    print("="*70)

    return result


# ==================== MAIN ====================

def main():
    import sys

    # Get file path from command line or use default
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        # Use README.md as default test file
        file_path = "README.md"
        print(f"No file specified, using default: {file_path}\n")

    # Check if file exists
    if not os.path.exists(file_path):
        print(f"❌ ERROR: File not found: {file_path}")
        print("Usage: python 04_multi_agent_crew.py <file_path>")
        return

    # Run the analysis
    analyze_file(file_path)


if __name__ == "__main__":
    main()
