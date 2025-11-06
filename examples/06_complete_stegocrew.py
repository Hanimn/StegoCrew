#!/usr/bin/env python3
"""
Lesson 7: Complete StegoCrew MVP
Full 5-agent system for solving CTF steganography challenges

This is a single-file demo. In Lesson 7, we'll reorganize this into
a modular structure (src/ directory).
"""

import os
import subprocess
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
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


# ==================== RECONNAISSANCE TOOLS ====================

@tool
def get_file_type(file_path: str) -> str:
    """Get detailed file type information."""
    if not check_tool_installed('file'):
        return "❌ file command not installed"

    if not os.path.exists(file_path):
        return f"❌ File not found: {file_path}"

    try:
        result = subprocess.run(
            ['file', '-b', file_path],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            file_type = result.stdout.strip()
            size = os.path.getsize(file_path)
            size_readable = f"{size / 1024:.2f} KB" if size > 1024 else f"{size} bytes"

            return f"📄 File Type: {file_type}\n📊 Size: {size_readable} ({size} bytes)"
        else:
            return f"⚠️ file command failed"

    except Exception as e:
        return f"❌ ERROR: {str(e)}"


@tool
def extract_metadata(file_path: str) -> str:
    """Extract metadata using exiftool."""
    if not check_tool_installed('exiftool'):
        return "❌ exiftool not installed"

    if not os.path.exists(file_path):
        return f"❌ File not found: {file_path}"

    try:
        result = subprocess.run(
            ['exiftool', file_path],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            return "⚠️ Exiftool failed"

        lines = result.stdout.split('\n')
        interesting = []

        for line in lines:
            if ': ' in line:
                # Look for flags or interesting fields
                if 'CTF{' in line or 'FLAG{' in line or 'flag{' in line:
                    interesting.append(f"🚩 FLAG IN METADATA! {line}")
                elif any(keyword in line.lower() for keyword in ['comment', 'description', 'copyright', 'author']):
                    interesting.append(f"⭐ {line}")

        report = f"📋 Metadata Analysis ({len(lines)} fields):\n\n"

        if interesting:
            report += "🔍 Interesting Findings:\n" + "\n".join(interesting[:10])
        else:
            report += "First 10 fields:\n" + "\n".join(lines[:10])

        return report

    except Exception as e:
        return f"❌ ERROR: {str(e)}"


@tool
def calculate_entropy(file_path: str) -> str:
    """Calculate file entropy (measure of randomness/encryption)."""
    import math
    from collections import Counter

    try:
        if not os.path.exists(file_path):
            return f"❌ File not found: {file_path}"

        with open(file_path, 'rb') as f:
            data = f.read()

        if len(data) == 0:
            return "❌ Empty file"

        byte_counts = Counter(data)
        entropy = 0

        for count in byte_counts.values():
            p = count / len(data)
            entropy -= p * math.log2(p)

        if entropy > 7.5:
            assessment = "VERY HIGH - likely encrypted/compressed"
        elif entropy > 7.0:
            assessment = "HIGH - possible encryption/compression"
        elif entropy > 6.0:
            assessment = "MODERATE - normal for images"
        else:
            assessment = "LOW - text or simple data"

        return f"📊 Entropy: {entropy:.4f}/8.0\n💡 Assessment: {assessment}"

    except Exception as e:
        return f"❌ ERROR: {str(e)}"


# ==================== STEGANOGRAPHY TOOLS ====================

@tool
def extract_with_steghide(file_path: str, password: str = "") -> str:
    """Extract hidden data using steghide."""
    if not check_tool_installed('steghide'):
        return "❌ steghide not installed (optional tool)"

    if not os.path.exists(file_path):
        return f"❌ File not found: {file_path}"

    try:
        output_file = file_path + ".extracted"

        cmd = ['steghide', 'extract', '-sf', file_path, '-xf', output_file, '-f']
        cmd.extend(['-p', password if password else ''])

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if result.returncode == 0 and os.path.exists(output_file):
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    data = f.read()
                os.remove(output_file)

                if 'CTF{' in data or 'FLAG{' in data or 'flag{' in data:
                    return f"🚩 FLAG FOUND!\n✅ Extracted data:\n{data[:500]}"
                else:
                    return f"✅ Data extracted successfully:\n{data[:500]}"

            except UnicodeDecodeError:
                os.remove(output_file)
                return "✅ Binary data extracted (check manually)"

        elif "could not extract" in result.stderr.lower():
            return "ℹ️ No steghide data found"
        else:
            return "ℹ️ Steghide extraction unsuccessful"

    except Exception as e:
        return f"ℹ️ Steghide check complete: {str(e)}"


@tool
def analyze_with_binwalk(file_path: str) -> str:
    """Scan for embedded files using binwalk."""
    if not check_tool_installed('binwalk'):
        return "❌ binwalk not installed (optional tool)"

    if not os.path.exists(file_path):
        return f"❌ File not found: {file_path}"

    try:
        result = subprocess.run(
            ['binwalk', file_path],
            capture_output=True,
            text=True,
            timeout=60
        )

        lines = result.stdout.split('\n')
        findings = []

        for line in lines:
            if line.strip() and not line.startswith('DECIMAL'):
                findings.append(line.strip())

        if findings:
            report = f"🔍 Binwalk found {len(findings)} embedded items:\n\n"
            report += "\n".join(findings[:15])
            report += "\n\n💡 Hint: Run 'binwalk -e' to extract files"
            return report
        else:
            return "✓ No embedded files detected"

    except Exception as e:
        return f"ℹ️ Binwalk check complete"


# ==================== PATTERN TOOLS ====================

@tool
def extract_strings(file_path: str, min_length: int = 6) -> str:
    """Extract printable strings from file."""
    if not check_tool_installed('strings'):
        return "❌ strings not installed"

    if not os.path.exists(file_path):
        return f"❌ File not found: {file_path}"

    try:
        result = subprocess.run(
            ['strings', '-n', str(min_length), file_path],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            return "⚠️ strings command failed"

        lines = result.stdout.split('\n')
        flags = []
        interesting = []
        base64_like = []

        for line in lines:
            line = line.strip()

            if 'CTF{' in line or 'FLAG{' in line or 'flag{' in line:
                flags.append(f"🚩 {line}")
            elif any(keyword in line.lower() for keyword in ['password', 'secret', 'key', 'hidden']):
                interesting.append(f"⭐ {line}")
            elif len(line) > 40 and all(c.isalnum() or c in '+/=' for c in line):
                base64_like.append(f"📝 Possible encoded: {line[:60]}...")

        report = f"🔤 Strings Analysis:\n\n"

        if flags:
            report += "🚩 FLAGS FOUND:\n" + "\n".join(flags[:5]) + "\n\n"

        if interesting:
            report += "⭐ Interesting:\n" + "\n".join(interesting[:10]) + "\n\n"

        if base64_like:
            report += "📝 Possible encoded data:\n" + "\n".join(base64_like[:5])

        if not flags and not interesting and not base64_like:
            report += f"Found {len(lines)} strings (none particularly interesting)"

        return report

    except Exception as e:
        return f"❌ ERROR: {str(e)}"


@tool
def detect_encoding_type(text: str) -> str:
    """Identify the encoding type of text."""
    import re

    # Base64 pattern
    if re.match(r'^[A-Za-z0-9+/]*={0,2}$', text) and len(text) % 4 == 0 and len(text) > 10:
        return "🔍 LIKELY BASE64: Contains Base64 character set and proper padding"

    # Hex pattern
    if re.match(r'^[0-9A-Fa-f]+$', text) and len(text) % 2 == 0 and len(text) > 10:
        return "🔍 LIKELY HEXADECIMAL: Contains only hex characters"

    # Binary pattern
    if re.match(r'^[01]+$', text) and len(text) > 10:
        return "🔍 LIKELY BINARY: Contains only 0s and 1s"

    # Check for URL encoding
    if '%' in text and re.search(r'%[0-9A-Fa-f]{2}', text):
        return "🔍 LIKELY URL ENCODED: Contains %XX patterns"

    # Plain text
    if all(32 <= ord(c) <= 126 or c in '\n\r\t' for c in text):
        return "🔍 PLAIN TEXT: All printable ASCII characters"

    return "🔍 UNKNOWN ENCODING: Unable to identify clear pattern"


# ==================== DECODER TOOLS ====================

@tool
def decode_base64(text: str) -> str:
    """Attempt to decode Base64 encoded text."""
    import base64

    try:
        # Clean whitespace
        text = text.strip()

        # Try to decode
        decoded_bytes = base64.b64decode(text)
        decoded = decoded_bytes.decode('utf-8')

        # Check for flag
        if 'CTF{' in decoded or 'FLAG{' in decoded or 'flag{' in decoded:
            return f"🚩 FLAG FOUND AFTER DECODING!\n✅ Decoded: {decoded}"
        else:
            return f"✅ Base64 decoded successfully:\n{decoded}"

    except Exception as e:
        return f"❌ Not valid Base64 or decoding failed: {str(e)}"


@tool
def decode_hex(text: str) -> str:
    """Attempt to decode hexadecimal encoded text."""
    try:
        # Remove common prefixes
        text = text.replace('0x', '').replace('\\x', '').strip()

        # Remove spaces
        text = text.replace(' ', '')

        # Decode
        decoded_bytes = bytes.fromhex(text)
        decoded = decoded_bytes.decode('utf-8')

        # Check for flag
        if 'CTF{' in decoded or 'FLAG{' in decoded or 'flag{' in decoded:
            return f"🚩 FLAG FOUND AFTER DECODING!\n✅ Decoded: {decoded}"
        else:
            return f"✅ Hex decoded successfully:\n{decoded}"

    except Exception as e:
        return f"❌ Not valid hex or decoding failed: {str(e)}"


@tool
def try_common_decodings(text: str) -> str:
    """Try multiple common encoding schemes."""
    import base64

    results = []

    # Try Base64
    try:
        decoded = base64.b64decode(text).decode('utf-8')
        results.append(f"✅ Base64: {decoded[:100]}")
        if 'CTF{' in decoded or 'FLAG{' in decoded:
            results.append("🚩 FLAG FOUND IN BASE64!")
    except:
        results.append("❌ Base64: Failed")

    # Try Hex
    try:
        text_clean = text.replace('0x', '').replace('\\x', '').replace(' ', '')
        decoded = bytes.fromhex(text_clean).decode('utf-8')
        results.append(f"✅ Hex: {decoded[:100]}")
        if 'CTF{' in decoded or 'FLAG{' in decoded:
            results.append("🚩 FLAG FOUND IN HEX!")
    except:
        results.append("❌ Hex: Failed")

    # Try ROT13
    try:
        import codecs
        decoded = codecs.decode(text, 'rot_13')
        results.append(f"✅ ROT13: {decoded[:100]}")
        if 'CTF{' in decoded or 'FLAG{' in decoded:
            results.append("🚩 FLAG FOUND IN ROT13!")
    except:
        results.append("❌ ROT13: Failed")

    return "🔄 Trying multiple decodings:\n\n" + "\n".join(results)


# ==================== AGENT 1: RECONNAISSANCE SPECIALIST ====================

recon_agent = Agent(
    role="File Reconnaissance Specialist",

    goal="Perform thorough initial file analysis to identify characteristics and anomalies",

    backstory="""You're the team's file detective. Check file signatures, metadata, entropy -
    the basics that everyone else skips. Weird metadata usually means hidden data.""",

    tools=[
        get_file_type,
        extract_metadata,
        calculate_entropy
    ],

    llm=llm,
    verbose=True
)


# ==================== AGENT 2: STEGANOGRAPHY EXPERT ====================

stego_agent = Agent(
    role="Steganography Extraction Expert",

    goal="Extract hidden data using specialized steganography tools and techniques",

    backstory="""You've been running stego tools since 2015. steghide, binwalk, zsteg - you know their
    quirks and failure modes. Start with the obvious, then try the weird stuff.""",

    tools=[
        extract_with_steghide,
        analyze_with_binwalk
    ],

    llm=llm,
    verbose=True
)


# ==================== AGENT 3: PATTERN HUNTER ====================

pattern_agent = Agent(
    role="Pattern Detection Specialist",

    goal="Identify encoded data, suspicious patterns, and potential flags in all findings",

    backstory="""Pattern recognition is your thing. base64 ends with '=', hex is all 0-9A-F, binary patterns
    stand out. You've seen enough encoded data to spot it immediately.""",

    tools=[
        extract_strings,
        detect_encoding_type
    ],

    llm=llm,
    verbose=True
)


# ==================== AGENT 4: DECODER SPECIALIST ====================

decoder_agent = Agent(
    role="Decoding and Decryption Specialist",

    goal="Decode encoded messages and decrypt data to reveal flags",

    backstory="""Decoding is straightforward: try base64, then hex, then ROT13. If none work, it's probably
    XOR or a multi-layer encoding. Work through them methodically.""",

    tools=[
        decode_base64,
        decode_hex,
        try_common_decodings
    ],

    llm=llm,
    verbose=True
)


# ==================== AGENT 5: ORCHESTRATOR ====================

orchestrator_agent = Agent(
    role="Analysis Coordinator and Report Generator",

    goal="Synthesize all findings into comprehensive report and identify all flags",

    backstory="""You compile what the team found into something readable. Highlight the flag if found,
    show the solution path, note what didn't work. Keep it concise.""",

    tools=[],  # No tools - synthesizes information

    llm=llm,
    verbose=True
)


# ==================== TASK DEFINITIONS ====================

def create_tasks(file_path: str):
    """Create all tasks with proper context chain."""

    # Task 1: Reconnaissance
    recon_task = Task(
        description=f"""
        Perform initial reconnaissance on: {file_path}

        Use your tools to:
        1. Identify file type and size
        2. Extract all metadata
        3. Calculate entropy to detect anomalies

        Provide a clear summary of file characteristics and any unusual findings.
        """,

        expected_output="Initial reconnaissance report with file characteristics and anomalies",

        agent=recon_agent
    )

    # Task 2: Steganography Analysis
    stego_task = Task(
        description="""
        Based on the reconnaissance findings, extract hidden data.

        Use your tools to:
        1. Try steghide extraction (with empty password first)
        2. Scan with binwalk for embedded files

        Report all findings, extracted data, and embedded files discovered.
        """,

        expected_output="Steganography analysis with extracted data and embedded files",

        agent=stego_agent,
        context=[recon_task]  # ← Sees reconnaissance findings
    )

    # Task 3: Pattern Detection
    pattern_task = Task(
        description="""
        Analyze all data found by reconnaissance and steganography teams.

        Use your tools to:
        1. Extract strings from the original file
        2. Examine any data extracted by steganography expert
        3. Identify encoding patterns (base64, hex, etc.)
        4. Look for CTF flag formats

        Report all suspicious patterns and potential encoded data.
        """,

        expected_output="Pattern analysis with encoding detection and flag candidates",

        agent=pattern_agent,
        context=[recon_task, stego_task]  # ← Sees both previous findings
    )

    # Task 4: Decoding
    decoder_task = Task(
        description="""
        Decode all encoded data identified by the pattern hunter.

        Use your tools to:
        1. Decode any base64 strings found
        2. Decode any hex data found
        3. Try other common encodings
        4. Search for flags in all decoded output

        Report all successfully decoded messages and flags found.
        """,

        expected_output="Decoded messages and all flags discovered",

        agent=decoder_agent,
        context=[pattern_task]  # ← Sees pattern findings
    )

    # Task 5: Final Report
    orchestrator_task = Task(
        description="""
        Create a comprehensive final report of the complete analysis.

        Your report should include:
        1. Summary of findings from all agents
        2. Key discoveries highlighted
        3. ALL flags found (if any) clearly listed
        4. The solution path that led to the flags
        5. Any recommendations for further investigation

        Format the report professionally with clear sections.
        """,

        expected_output="Comprehensive final analysis report with all flags and solution path",

        agent=orchestrator_agent,
        context=[recon_task, stego_task, pattern_task, decoder_task]  # ← Sees ALL
    )

    return [recon_task, stego_task, pattern_task, decoder_task, orchestrator_task]


# ==================== MAIN FUNCTION ====================

def analyze_file(file_path: str):
    """Analyze a file using the complete 5-agent StegoCrew."""

    print("="*70)
    print("🔍 STEGOCREW: COMPLETE 5-AGENT CTF SOLVER")
    print("="*70)
    print(f"\n📁 Target File: {file_path}\n")
    print("👥 Agent Team:")
    print("   1. 🔍 Reconnaissance Specialist  (file analysis & metadata)")
    print("   2. 🛠️  Steganography Expert      (hidden data extraction)")
    print("   3. 🧩 Pattern Hunter             (encoding detection)")
    print("   4. 🔐 Decoder Specialist         (decode & decrypt)")
    print("   5. 📊 Orchestrator               (final report)")
    print("\n" + "="*70 + "\n")

    # Check file exists
    if not os.path.exists(file_path):
        print(f"❌ ERROR: File not found - {file_path}")
        return

    # Check tool availability
    print("🔧 Tool Status Check:")
    tools = ['file', 'exiftool', 'strings', 'steghide', 'binwalk']
    for tool in tools:
        status = "✅ Ready" if check_tool_installed(tool) else "⚠️ Not installed (optional)"
        print(f"   {tool:12} {status}")

    print("\n" + "="*70 + "\n")

    # Create tasks
    tasks = create_tasks(file_path)

    # Create crew
    crew = Crew(
        agents=[
            recon_agent,
            stego_agent,
            pattern_agent,
            decoder_agent,
            orchestrator_agent
        ],
        tasks=tasks,
        process=Process.sequential,  # One agent at a time, in order
        verbose=True
    )

    # Execute analysis
    print("🚀 Starting analysis...\n")
    result = crew.kickoff()

    # Display final result
    print("\n" + "="*70)
    print("✅ STEGOCREW ANALYSIS COMPLETE - FINAL REPORT")
    print("="*70)
    print(result)
    print("="*70)

    return result


# ==================== MAIN ====================

def main():
    import sys

    # Get file from command line
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        # Use sample test file
        file_path = "../test_files/sample_with_metadata.txt"
        print(f"No file specified, using default: {file_path}\n")

    # Check file exists
    if not os.path.exists(file_path):
        print(f"❌ ERROR: File not found: {file_path}")
        print("\nUsage: python 06_complete_stegocrew.py <file_path>")
        print("\nExample:")
        print("  python 06_complete_stegocrew.py ../test_files/challenge_metadata.jpg")
        return

    # Run analysis
    analyze_file(file_path)


if __name__ == "__main__":
    main()
