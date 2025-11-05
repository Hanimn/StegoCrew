#!/usr/bin/env python3
"""
Your Steganography Analyzer - Practice from Lesson 6

Build your own stego analysis system with real tools!
Complete the TODOs to create a working CTF challenge solver.
"""

import os
import subprocess
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import tool
from langchain_anthropic import ChatAnthropic

load_dotenv()
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)

# ==================== HELPER FUNCTIONS ====================

def check_tool_installed(tool_name: str) -> bool:
    """Check if a system tool is installed."""
    try:
        subprocess.run(
            [tool_name, '--version'],
            capture_output=True,
            timeout=5,
            stderr=subprocess.DEVNULL
        )
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False
    except Exception:
        return False


# ==================== YOUR TOOLS ====================

@tool
def extract_with_steghide(file_path: str, password: str = "") -> str:
    """
    Extract hidden data from image/audio using steghide.

    Args:
        file_path: Path to file (JPEG, BMP, WAV, AU)
        password: Passphrase (empty string tries no password)

    Returns:
        Extracted data or status message
    """
    # TODO: Check if steghide is installed
    if not check_tool_installed('steghide'):
        return "❌ ERROR: steghide not installed\nInstall: sudo apt install steghide"

    # TODO: Check if file exists
    if not os.path.exists(file_path):
        return f"❌ ERROR: File not found - {file_path}"

    try:
        # TODO: Create output file path
        output_file = file_path + ".extracted"

        # TODO: Build steghide command
        # Hint: ['steghide', 'extract', '-sf', file_path, '-xf', output_file, '-f', '-p', password]
        cmd = ['steghide', 'extract', '-sf', file_path, '-xf', output_file, '-f']

        if password:
            cmd.extend(['-p', password])
        else:
            cmd.extend(['-p', ''])  # Empty password

        # TODO: Run command with timeout
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )

        # TODO: Check if extraction succeeded
        if result.returncode == 0 and os.path.exists(output_file):
            try:
                # Try to read as text
                with open(output_file, 'r', encoding='utf-8') as f:
                    data = f.read()

                # Clean up
                os.remove(output_file)

                # Look for flags!
                if 'CTF{' in data or 'FLAG{' in data:
                    return f"🚩 FLAG FOUND!\n{data}"
                else:
                    return f"✅ Extracted:\n{data}"

            except UnicodeDecodeError:
                os.remove(output_file)
                return "✅ Binary data extracted (check manually)"

        else:
            return "❌ No embedded data found"

    except subprocess.TimeoutExpired:
        return "❌ ERROR: steghide timed out"

    except Exception as e:
        return f"❌ ERROR: {str(e)}"


@tool
def analyze_with_binwalk(file_path: str) -> str:
    """
    Scan for embedded files using binwalk.

    Args:
        file_path: Path to file to analyze

    Returns:
        Report of embedded files found
    """
    # TODO: Check if binwalk is installed
    if not check_tool_installed('binwalk'):
        return "❌ ERROR: binwalk not installed\nInstall: sudo apt install binwalk"

    # TODO: Check if file exists
    if not os.path.exists(file_path):
        return f"❌ ERROR: File not found - {file_path}"

    try:
        # TODO: Run binwalk command
        result = subprocess.run(
            ['binwalk', file_path],
            capture_output=True,
            text=True,
            timeout=60
        )

        # TODO: Parse output and look for findings
        lines = result.stdout.split('\n')
        findings = []

        for line in lines:
            if line.strip() and not line.startswith('DECIMAL'):
                findings.append(line.strip())

        if findings:
            report = f"🔍 Binwalk found {len(findings)} embedded items:\n\n"
            report += "\n".join(findings[:10])  # First 10
            return report
        else:
            return "✓ No embedded files detected"

    except subprocess.TimeoutExpired:
        return "❌ ERROR: binwalk timed out"

    except Exception as e:
        return f"❌ ERROR: {str(e)}"


@tool
def extract_metadata(file_path: str) -> str:
    """
    Extract metadata using exiftool.

    Args:
        file_path: Path to file

    Returns:
        Formatted metadata
    """
    # TODO: Check if exiftool is installed
    if not check_tool_installed('exiftool'):
        return "❌ ERROR: exiftool not installed\nInstall: sudo apt install libimage-exiftool-perl"

    # TODO: Check if file exists
    if not os.path.exists(file_path):
        return f"❌ ERROR: File not found - {file_path}"

    try:
        # TODO: Run exiftool
        result = subprocess.run(
            ['exiftool', file_path],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            return f"⚠️ Exiftool failed: {result.stderr}"

        # TODO: Parse and format metadata
        lines = result.stdout.split('\n')
        interesting = []

        for line in lines:
            if ': ' in line:
                # Look for flags or interesting fields
                if 'CTF{' in line or 'FLAG{' in line:
                    interesting.append(f"🚩 {line}")
                elif any(keyword in line.lower() for keyword in ['comment', 'description']):
                    interesting.append(f"⭐ {line}")

        if interesting:
            return "📋 Interesting Metadata:\n" + "\n".join(interesting)
        else:
            # Show first 10 lines
            return "📋 Metadata:\n" + "\n".join(lines[:10])

    except subprocess.TimeoutExpired:
        return "❌ ERROR: exiftool timed out"

    except Exception as e:
        return f"❌ ERROR: {str(e)}"


@tool
def extract_strings(file_path: str, min_length: int = 6) -> str:
    """
    Extract printable strings from file.

    Args:
        file_path: Path to file
        min_length: Minimum string length (default: 6)

    Returns:
        Interesting strings found
    """
    # TODO: Check if strings is installed
    if not check_tool_installed('strings'):
        return "❌ ERROR: strings not installed\nInstall: sudo apt install binutils"

    # TODO: Check if file exists
    if not os.path.exists(file_path):
        return f"❌ ERROR: File not found - {file_path}"

    try:
        # TODO: Run strings command
        result = subprocess.run(
            ['strings', '-n', str(min_length), file_path],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            return f"⚠️ strings failed: {result.stderr}"

        # TODO: Look for interesting patterns
        lines = result.stdout.split('\n')
        flags = []
        interesting = []

        for line in lines:
            line = line.strip()

            # Check for flags
            if 'CTF{' in line or 'FLAG{' in line:
                flags.append(f"🚩 {line}")

            # Check for keywords
            elif any(keyword in line.lower() for keyword in ['password', 'secret', 'key']):
                interesting.append(f"⭐ {line}")

        # Build report
        report = f"🔤 Strings Analysis:\n\n"

        if flags:
            report += "FLAGS FOUND:\n" + "\n".join(flags) + "\n\n"

        if interesting:
            report += "Interesting:\n" + "\n".join(interesting[:5])
        else:
            report += f"Found {len(lines)} strings (none particularly interesting)"

        return report

    except subprocess.TimeoutExpired:
        return "❌ ERROR: strings timed out"

    except Exception as e:
        return f"❌ ERROR: {str(e)}"


# ==================== YOUR AGENT ====================

stego_analyst = Agent(
    role="Steganography Analysis Expert",

    # TODO: Write a good goal for your agent
    goal="Thoroughly analyze files for hidden data using all available steganography techniques",

    # TODO: Write a backstory that explains your agent's expertise
    backstory="""You are a CTF steganography specialist with years of experience.
    You systematically apply tools to uncover hidden flags. You check metadata first,
    then use specialized tools like steghide and binwalk.""",

    # TODO: Assign your tools to the agent
    tools=[extract_metadata, extract_strings, extract_with_steghide, analyze_with_binwalk],

    llm=llm,
    verbose=True
)


# ==================== YOUR TASK ====================

analysis_task = Task(
    # TODO: Write a clear task description
    description="""
    Analyze the file: {file_path}

    Use your tools systematically:
    1. Extract and examine metadata (look for hidden clues)
    2. Extract strings and search for flags or encoded data
    3. Try steghide extraction (with empty password first)
    4. Use binwalk to check for embedded files

    Look for CTF flags in format: CTF{{...}} or FLAG{{...}}

    Provide a complete analysis report with all findings.
    """,

    # TODO: Write expected output description
    expected_output="Comprehensive steganography analysis report with all findings and any flags discovered",

    agent=stego_analyst
)


# ==================== MAIN ====================

def analyze_file(file_path: str):
    """Analyze a file for steganography."""

    print("="*70)
    print("🔍 YOUR STEGO ANALYZER")
    print("="*70)
    print(f"\n📁 Analyzing: {file_path}\n")

    # Check which tools are available
    print("🔧 Tool Status:")
    tools = ['exiftool', 'strings', 'steghide', 'binwalk']
    for tool in tools:
        status = "✅" if check_tool_installed(tool) else "❌"
        print(f"   {status} {tool}")

    print("\n" + "="*70 + "\n")

    # Create and run crew
    crew = Crew(
        agents=[stego_analyst],
        tasks=[analysis_task],
        verbose=True
    )

    result = crew.kickoff(inputs={"file_path": file_path})

    print("\n" + "="*70)
    print("✅ ANALYSIS COMPLETE")
    print("="*70)
    print(result)
    print("="*70)

    return result


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
        print("Usage: python my_stego_analyzer.py <file_path>")
    else:
        analyze_file(file_path)


# ==================== EXTENSION CHALLENGES ====================

"""
🎯 CHALLENGES TO EXTEND THIS ANALYZER:

1. PASSWORD BRUTE-FORCING
   Add a tool that tries common passwords with steghide:
   - Try empty password
   - Try common passwords: "password", "admin", "ctf", etc.
   - Try passwords from a wordlist file

2. LSB ANALYSIS
   Add zsteg for PNG files:
   - Install: gem install zsteg
   - Run: zsteg -a image.png
   - Look for hidden data in LSB channels

3. MULTI-AGENT UPGRADE
   Convert to 3-agent system:
   - Agent 1: Metadata Extractor (exiftool only)
   - Agent 2: Stego Hunter (steghide, binwalk, zsteg)
   - Agent 3: Report Generator (no tools, summarizes findings)

4. AUTO-EXTRACT
   When binwalk finds embedded files:
   - Automatically extract them with binwalk -e
   - Recursively analyze extracted files
   - Create a full extraction tree

5. ENCODING DETECTION
   Add encoding detection for found strings:
   - Detect Base64
   - Detect Hex
   - Automatically try decoding

Good luck! 🚀
"""
