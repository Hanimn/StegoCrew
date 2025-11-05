#!/usr/bin/env python3
"""
Your First Multi-Agent Crew - Practice from Lesson 5

Build a simple 2-agent system to understand coordination.
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import tool
from langchain_anthropic import ChatAnthropic

load_dotenv()
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)

# ==================== TOOLS FOR AGENT 1 ====================

@tool
def count_words_in_file(file_path: str) -> str:
    """Count total words in a text file."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        words = content.split()
        return f"Total words in file: {len(words)}"

    except Exception as e:
        return f"ERROR: {str(e)}"


@tool
def find_longest_word(file_path: str) -> str:
    """Find the longest word in a file."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        words = content.split()
        if not words:
            return "No words found in file"

        # Remove punctuation and find longest
        cleaned_words = [word.strip('.,!?;:"()[]{}') for word in words]
        longest = max(cleaned_words, key=len)

        return f"Longest word: '{longest}' ({len(longest)} characters)"

    except Exception as e:
        return f"ERROR: {str(e)}"


# ==================== TOOLS FOR AGENT 2 ====================

@tool
def calculate_average_word_length(total_words: int, total_chars: int) -> str:
    """Calculate average word length from statistics."""
    try:
        if total_words == 0:
            return "Cannot calculate average - no words"

        avg = total_chars / total_words
        return f"Average word length: {avg:.2f} characters"

    except Exception as e:
        return f"ERROR: {str(e)}"


@tool
def categorize_document(word_count: int) -> str:
    """Categorize document size based on word count."""
    if word_count < 100:
        return "CATEGORY: Very Short (< 100 words)"
    elif word_count < 500:
        return "CATEGORY: Short (100-500 words)"
    elif word_count < 1000:
        return "CATEGORY: Medium (500-1000 words)"
    elif word_count < 5000:
        return "CATEGORY: Long (1000-5000 words)"
    else:
        return "CATEGORY: Very Long (5000+ words)"


# ==================== AGENT 1: ANALYZER ====================

analyzer_agent = Agent(
    role="Document Analyzer",

    goal="Analyze text documents and gather basic statistics",

    backstory="""You are a document analysis expert who carefully
    examines text files. You count words, find patterns, and gather
    statistics that help others understand the document.""",

    tools=[count_words_in_file, find_longest_word],

    llm=llm,
    verbose=True
)


# ==================== AGENT 2: SUMMARIZER ====================

summarizer_agent = Agent(
    role="Document Summarizer",

    goal="Create summaries based on document analysis",

    backstory="""You are a summary specialist who takes statistical
    data about documents and creates clear, concise reports. You
    interpret numbers and categorize documents.""",

    tools=[categorize_document],  # Different tools than Agent 1!

    llm=llm,
    verbose=True
)


# ==================== TASK 1: ANALYZE ====================

analyze_task = Task(
    description="""
    Analyze the file: {file_path}

    Use your tools to:
    1. Count the total number of words
    2. Find the longest word in the document

    Provide a clear report of your findings.
    """,

    expected_output="Document analysis with word count and longest word",

    agent=analyzer_agent
)


# ==================== TASK 2: SUMMARIZE ====================

summarize_task = Task(
    description="""
    Based on the analysis from the document analyzer, create a summary.

    Use the word count they found to:
    1. Categorize the document size
    2. Provide an overall assessment

    Create a brief, informative summary.
    """,

    expected_output="Document summary and categorization",

    agent=summarizer_agent,

    context=[analyze_task]  # ← CRITICAL! Summarizer sees analyzer's work
)


# ==================== CREATE THE CREW ====================

def analyze_document(file_path: str):
    """Analyze a document with our 2-agent crew."""

    print("="*70)
    print("📄 TWO-AGENT DOCUMENT ANALYSIS SYSTEM")
    print("="*70)
    print(f"\n📁 Analyzing: {file_path}\n")
    print("👥 Agent Team:")
    print("   1. 📊 Document Analyzer  (gathers statistics)")
    print("   2. 📝 Document Summarizer (creates summary)")
    print("\n" + "="*70 + "\n")

    # Create crew
    crew = Crew(
        agents=[analyzer_agent, summarizer_agent],
        tasks=[analyze_task, summarize_task],
        process=Process.sequential,  # One at a time, in order
        verbose=True
    )

    # Run analysis
    result = crew.kickoff(inputs={"file_path": file_path})

    print("\n" + "="*70)
    print("✅ ANALYSIS COMPLETE - FINAL SUMMARY")
    print("="*70)
    print(result)
    print("="*70)

    return result


# ==================== MAIN ====================

if __name__ == "__main__":
    import sys

    # Get file from command line or use default
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = "../README.md"
        print(f"No file specified, using: {file_path}\n")

    # Check file exists
    if not os.path.exists(file_path):
        print(f"❌ ERROR: File not found: {file_path}")
        print("Usage: python my_first_crew.py <file_path>")
    else:
        analyze_document(file_path)
