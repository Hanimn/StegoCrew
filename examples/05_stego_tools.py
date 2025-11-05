#!/usr/bin/env python3
"""
Lesson 6: Real Steganography Tools Example
Demonstrates professional tool wrapping for CTF challenges.
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


def get_install_command(tool_name: str) -> str:
    """Get installation command for a tool."""
    install_commands = {
        'steghide': 'sudo apt install steghide',
        'binwalk': 'sudo apt install binwalk',
        'exiftool': 'sudo apt install libimage-exiftool-perl',
        'zsteg': 'gem install zsteg',
        'foremost': 'sudo apt install foremost',
        'strings': 'sudo apt install binutils',
        'file': 'sudo apt install file'
    }
    return install_commands.get(tool_name, f'Install {tool_name} manually')


# ==================== STEGANOGRAPHY TOOLS ====================

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
    # Check if steghide is installed
    if not check_tool_installed('steghide'):
        return f"❌ ERROR: steghide not installed\nInstall: {get_install_command('steghide')}"

    # Check file exists
    if not os.path.exists(file_path):
        return f"❌ ERROR: File not found - {file_path}"

    try:
        # Output file path
        output_file = file_path + ".extracted"

        # Build command
        cmd = ['steghide', 'extract', '-sf', file_path, '-xf', output_file, '-f']
        if password:
            cmd.extend(['-p', password])
        else:
            cmd.extend(['-p', ''])  # Try empty password

        # Run with timeout
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )

        # Check result
        if result.returncode == 0 and os.path.exists(output_file):
            # Try to read extracted data
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    data = f.read()

                # Clean up
                os.remove(output_file)

                # Look for flags
                if 'CTF{' in data or 'FLAG{' in data or 'flag{' in data:
                    return f"🚩 FLAG FOUND!\n✅ Extracted data:\n{data}"
                else:
                    return f"✅ Data extracted successfully:\n{data[:500]}"

            except UnicodeDecodeError:
                # Binary data
                size = os.path.getsize(output_file)
                os.remove(output_file)
                return f"✅ Binary data extracted ({size} bytes) - check file manually"

            except Exception as e:
                return f"✅ Data extracted but couldn't read: {str(e)}"

        elif "could not extract" in result.stderr.lower():
            if password:
                return "❌ No embedded data found or wrong password"
            else:
                return "❌ No embedded data found (try with password?)"

        else:
            return f"⚠️ Extraction failed: {result.stderr.strip()}"

    except subprocess.TimeoutExpired:
        return "❌ ERROR: steghide timed out (30 seconds)"

    except Exception as e:
        return f"❌ ERROR: {type(e).__name__}: {str(e)}"


@tool
def analyze_with_binwalk(file_path: str, extract: bool = False) -> str:
    """
    Scan for embedded files using binwalk.

    Args:
        file_path: Path to file to analyze
        extract: Whether to extract found files (default: False)

    Returns:
        Report of embedded files found
    """
    # Check if binwalk is installed
    if not check_tool_installed('binwalk'):
        return f"❌ ERROR: binwalk not installed\nInstall: {get_install_command('binwalk')}"

    # Check file exists
    if not os.path.exists(file_path):
        return f"❌ ERROR: File not found - {file_path}"

    try:
        cmd = ['binwalk', file_path]
        if extract:
            cmd.append('-e')  # Extract files

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )

        # Parse output
        lines = result.stdout.split('\n')
        findings = []

        for line in lines:
            # Skip header and empty lines
            if line.strip() and not line.startswith('DECIMAL'):
                findings.append(line.strip())

        if findings:
            report = f"🔍 Binwalk found {len(findings)} embedded items:\n\n"
            report += "\n".join(findings[:20])  # Limit to first 20

            if len(findings) > 20:
                report += f"\n... and {len(findings) - 20} more items"

            if extract:
                extract_dir = "_" + os.path.basename(file_path) + ".extracted"
                report += f"\n\n✅ Files extracted to: {extract_dir}/"

            return report
        else:
            return "✓ No embedded files detected"

    except subprocess.TimeoutExpired:
        return "❌ ERROR: binwalk timed out (60 seconds)"

    except Exception as e:
        return f"❌ ERROR: {str(e)}"


@tool
def extract_metadata(file_path: str) -> str:
    """
    Extract metadata using exiftool.

    Args:
        file_path: Path to file

    Returns:
        Formatted metadata or error message
    """
    # Check if exiftool is installed
    if not check_tool_installed('exiftool'):
        return f"❌ ERROR: exiftool not installed\nInstall: {get_install_command('exiftool')}"

    # Check file exists
    if not os.path.exists(file_path):
        return f"❌ ERROR: File not found - {file_path}"

    try:
        result = subprocess.run(
            ['exiftool', file_path],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            return f"⚠️ Exiftool failed: {result.stderr}"

        # Parse metadata
        lines = result.stdout.split('\n')
        metadata = {}
        interesting = []

        for line in lines:
            if ': ' in line:
                key, value = line.split(': ', 1)
                key = key.strip()
                value = value.strip()
                metadata[key] = value

                # Look for interesting fields
                if any(keyword in key.lower() for keyword in ['comment', 'description', 'copyright', 'author']):
                    interesting.append(f"⭐ {key}: {value}")

                # Look for flags in any field
                if 'CTF{' in value or 'FLAG{' in value or 'flag{' in value:
                    interesting.append(f"🚩 FLAG IN METADATA! {key}: {value}")

        # Build report
        report = f"📋 Metadata Analysis ({len(metadata)} fields):\n\n"

        if interesting:
            report += "🔍 Interesting Findings:\n"
            report += "\n".join(interesting) + "\n\n"

        # Show all metadata (limited)
        report += "All Metadata:\n"
        for key, value in list(metadata.items())[:15]:
            report += f"  {key}: {value}\n"

        if len(metadata) > 15:
            report += f"  ... and {len(metadata) - 15} more fields"

        return report

    except subprocess.TimeoutExpired:
        return "❌ ERROR: exiftool timed out (30 seconds)"

    except Exception as e:
        return f"❌ ERROR: {str(e)}"


@tool
def extract_strings(file_path: str, min_length: int = 6) -> str:
    """
    Extract printable strings from file.

    Args:
        file_path: Path to file
        min_length: Minimum string length to extract (default: 6)

    Returns:
        Interesting strings found
    """
    # Check if strings is installed
    if not check_tool_installed('strings'):
        return f"❌ ERROR: strings not installed\nInstall: {get_install_command('strings')}"

    # Check file exists
    if not os.path.exists(file_path):
        return f"❌ ERROR: File not found - {file_path}"

    try:
        result = subprocess.run(
            ['strings', '-n', str(min_length), file_path],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            return f"⚠️ strings command failed: {result.stderr}"

        lines = result.stdout.split('\n')

        # Look for interesting strings
        flags = []
        interesting = []
        base64_like = []

        for line in lines:
            line = line.strip()

            # Check for flags
            if 'CTF{' in line or 'FLAG{' in line or 'flag{' in line:
                flags.append(f"🚩 {line}")

            # Check for other keywords
            elif any(keyword in line.lower() for keyword in ['password', 'secret', 'key', 'hidden']):
                interesting.append(f"⭐ {line}")

            # Check for base64-like strings (long alphanumeric)
            elif len(line) > 40 and line.isalnum():
                base64_like.append(f"📝 Possible encoded: {line[:60]}...")

        # Build report
        report = f"🔤 Strings Analysis (min length: {min_length}):\n\n"

        if flags:
            report += "🚩 FLAGS FOUND:\n" + "\n".join(flags[:5]) + "\n\n"

        if interesting:
            report += "⭐ Interesting strings:\n" + "\n".join(interesting[:10]) + "\n\n"

        if base64_like:
            report += "📝 Possible encoded data:\n" + "\n".join(base64_like[:5]) + "\n\n"

        if not flags and not interesting and not base64_like:
            report += f"Found {len(lines)} strings, but none particularly interesting\n"
            report += "First few strings:\n"
            report += "\n".join(f"  {s}" for s in lines[:10] if s.strip())

        return report

    except subprocess.TimeoutExpired:
        return "❌ ERROR: strings timed out (30 seconds)"

    except Exception as e:
        return f"❌ ERROR: {str(e)}"


@tool
def get_file_type(file_path: str) -> str:
    """
    Get detailed file type information.

    Args:
        file_path: Path to file

    Returns:
        File type description
    """
    # Check if file command is installed
    if not check_tool_installed('file'):
        return f"❌ ERROR: file command not installed\nInstall: {get_install_command('file')}"

    # Check file exists
    if not os.path.exists(file_path):
        return f"❌ ERROR: File not found - {file_path}"

    try:
        result = subprocess.run(
            ['file', '-b', file_path],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            file_type = result.stdout.strip()

            # Add file size
            size = os.path.getsize(file_path)
            size_readable = f"{size / 1024:.2f} KB" if size > 1024 else f"{size} bytes"

            return f"📄 File Type: {file_type}\n📊 Size: {size_readable} ({size} bytes)"
        else:
            return f"⚠️ file command failed: {result.stderr}"

    except subprocess.TimeoutExpired:
        return "❌ ERROR: file command timed out"

    except Exception as e:
        return f"❌ ERROR: {str(e)}"


# ==================== AGENT ====================

stego_analyst = Agent(
    role="CTF Steganography Specialist",
    goal="Analyze files systematically using all available steganography tools to find hidden data and flags",
    backstory="""You are an expert CTF competitor with years of experience in steganography
    challenges. You systematically apply tools in the right order, starting with basic file
    analysis, then metadata extraction, then steganography-specific tools. You look for patterns
    like embedded files, hidden messages, and encoded data. You always check for flags in the
    format CTF{...} or FLAG{...}.""",
    tools=[
        get_file_type,
        extract_metadata,
        extract_strings,
        extract_with_steghide,
        analyze_with_binwalk
    ],
    llm=llm,
    verbose=True
)


# ==================== TASK ====================

analysis_task = Task(
    description="""
    Perform a comprehensive steganography analysis of the file: {file_path}

    Use your tools in this order:
    1. Identify the file type and size
    2. Extract and examine all metadata
    3. Extract strings and look for interesting patterns
    4. Try steghide extraction (with empty password first)
    5. Use binwalk to check for embedded files

    Pay special attention to:
    - CTF flags in format: CTF{{...}}, FLAG{{...}}, flag{{...}}
    - Base64-encoded data
    - Unusual metadata fields
    - Embedded files or archives
    - Suspicious strings

    Provide a comprehensive report with all findings.
    """,
    expected_output="Complete steganography analysis report with all findings and any flags discovered",
    agent=stego_analyst
)


# ==================== MAIN ====================

def analyze_file(file_path: str):
    """Analyze a file for steganography challenges."""

    print("="*70)
    print("🔍 STEGOCREW: REAL STEGANOGRAPHY TOOLS DEMONSTRATION")
    print("="*70)
    print(f"\n📁 Analyzing file: {file_path}\n")
    print("🛠️  Available Tools:")
    print("   • file      - File type identification")
    print("   • exiftool  - Metadata extraction")
    print("   • strings   - String extraction")
    print("   • steghide  - Steganography extraction")
    print("   • binwalk   - Embedded file detection")
    print("\n" + "="*70 + "\n")

    # Check which tools are installed
    print("🔧 Tool Status Check:")
    tools = ['file', 'exiftool', 'strings', 'steghide', 'binwalk']
    for tool in tools:
        status = "✅ Installed" if check_tool_installed(tool) else "❌ Not installed"
        print(f"   {tool:12} {status}")

    print("\n" + "="*70 + "\n")

    # Create and run crew
    crew = Crew(
        agents=[stego_analyst],
        tasks=[analysis_task],
        verbose=True
    )

    result = crew.kickoff(inputs={"file_path": file_path})

    # Display final result
    print("\n" + "="*70)
    print("✅ ANALYSIS COMPLETE - FINAL REPORT")
    print("="*70)
    print(result)
    print("="*70)

    return result


def main():
    import sys

    # Get file path from command line
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        # Use README as default test file
        file_path = "../README.md"
        print(f"No file specified, using default: {file_path}\n")

    # Check if file exists
    if not os.path.exists(file_path):
        print(f"❌ ERROR: File not found: {file_path}")
        print("\nUsage: python 05_stego_tools.py <file_path>")
        print("\nExample:")
        print("  python 05_stego_tools.py ../test_files/challenge.jpg")
        return

    # Run analysis
    analyze_file(file_path)


if __name__ == "__main__":
    main()
