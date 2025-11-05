# Lesson 6: Building Real Steganography Tools 🔐🛠️

**Duration:** 3-4 hours
**Prerequisite:** Lessons 1-5 completed
**Goal:** Build production-ready tools that wrap real steganography utilities for CTF challenges

---

## 📚 What You'll Learn

By the end of this lesson, you will:

1. ✅ Understand common steganography techniques used in CTFs
2. ✅ Build tools that wrap real stego utilities (`steghide`, `binwalk`, `exiftool`, etc.)
3. ✅ Handle missing dependencies gracefully
4. ✅ Parse and interpret output from various tools
5. ✅ Create a reusable steganography tool library
6. ✅ Test tools with real CTF challenge files

---

## Part 1: Understanding CTF Steganography Techniques

### Common Hiding Techniques

**1. LSB (Least Significant Bit) Steganography**
- Data hidden in the least significant bits of image pixels
- Minimal visual impact
- Tools: `zsteg` (PNG/BMP), `stegsolve`
- Example: Hidden flag in last bit of each RGB value

**2. File Embedding**
- Complete files hidden inside other files
- Uses file format structures (headers, metadata)
- Tools: `binwalk`, `foremost`, `steghide`
- Example: ZIP file appended to end of JPEG

**3. Metadata Hiding**
- Data in EXIF, comments, or other metadata fields
- Tools: `exiftool`, `strings`
- Example: Flag in JPEG comment field

**4. Password-Protected Steganography**
- Encrypted data requiring passphrase
- Tools: `steghide` with password
- Example: Data hidden with steghide requiring password from another clue

**5. Audio/Video Steganography**
- Similar techniques for multimedia files
- Tools: `sonic-visualizer`, `audacity`, `ffmpeg`
- Example: Hidden image in audio spectrogram

### CTF-Specific Patterns

CTF challenges often combine multiple techniques:
```
Initial file → Metadata reveals password → Password unlocks steghide →
Reveals ZIP → ZIP contains image → Image has LSB data → Flag!
```

---

## Part 2: Essential Steganography Tools

### Tool Overview

| Tool | Purpose | Installation |
|------|---------|-------------|
| **steghide** | Embed/extract from JPEG/BMP/WAV/AU | `sudo apt install steghide` |
| **binwalk** | Find embedded files | `sudo apt install binwalk` |
| **exiftool** | Read/write metadata | `sudo apt install libimage-exiftool-perl` |
| **zsteg** | PNG/BMP LSB analysis | `gem install zsteg` |
| **strings** | Extract text strings | Built-in (usually) |
| **file** | Identify file type | Built-in |
| **foremost** | Carve embedded files | `sudo apt install foremost` |

### Why Wrap These Tools?

Instead of running commands manually, we create Python tools because:

1. **Consistent Interface:** All tools return structured data
2. **Error Handling:** Gracefully handle missing tools or failures
3. **Output Parsing:** Convert raw output to actionable information
4. **Agent-Friendly:** AI agents can use them reliably
5. **Automation:** Chain multiple tools together automatically

---

## Part 3: Building Your First Stego Tool

### Example: Steghide Wrapper

```python
import subprocess
from crewai_tools import tool

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
    try:
        # Build command
        cmd = ['steghide', 'extract', '-sf', file_path, '-f']
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

        # Check if extraction succeeded
        if result.returncode == 0:
            # Read extracted file (steghide writes to file)
            output_file = file_path + ".out"
            try:
                with open(output_file, 'r') as f:
                    data = f.read()
                return f"✅ Data extracted successfully:\n{data}"
            except:
                return "✅ Data extracted to file (binary data)"

        elif "could not extract" in result.stderr.lower():
            return "❌ No steghide data found or wrong password"

        else:
            return f"⚠️ Extraction failed: {result.stderr}"

    except FileNotFoundError:
        return "❌ ERROR: steghide not installed. Run: sudo apt install steghide"

    except subprocess.TimeoutExpired:
        return "❌ ERROR: steghide timed out (30 seconds)"

    except Exception as e:
        return f"❌ ERROR: {type(e).__name__}: {str(e)}"
```

### Key Patterns Demonstrated

1. **Command Building:** Construct subprocess command with arguments
2. **Empty Password Handling:** Try extraction without password first
3. **Output Files:** Steghide writes to file, we need to read it
4. **Tool Detection:** Catch `FileNotFoundError` for missing tools
5. **Timeout Protection:** Prevent hanging on malicious files
6. **User-Friendly Messages:** Emoji and clear status indicators

---

## Part 4: Advanced Tool Wrapping

### Example: Binwalk with Parsing

```python
@tool
def analyze_with_binwalk(file_path: str, extract: bool = False) -> str:
    """
    Scan for embedded files using binwalk.

    Args:
        file_path: Path to file to analyze
        extract: Whether to extract found files

    Returns:
        Report of embedded files found
    """
    try:
        cmd = ['binwalk', file_path]
        if extract:
            cmd.append('-e')  # Extract files

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

        if result.returncode != 0:
            return f"⚠️ Binwalk failed: {result.stderr}"

        # Parse output
        lines = result.stdout.split('\n')
        findings = []

        for line in lines:
            # Binwalk output format: "DECIMAL   HEX   DESCRIPTION"
            if line.strip() and not line.startswith('DECIMAL'):
                findings.append(line.strip())

        if findings:
            report = f"🔍 Found {len(findings)} embedded items:\n"
            report += "\n".join(findings[:20])  # Limit output

            if extract:
                report += "\n\n✅ Files extracted to: _" + file_path + ".extracted/"

            return report
        else:
            return "✓ No embedded files detected"

    except FileNotFoundError:
        return "❌ ERROR: binwalk not installed. Run: sudo apt install binwalk"

    except Exception as e:
        return f"❌ ERROR: {str(e)}"
```

### Parsing Strategy

The key is understanding each tool's output format:

- **binwalk:** Tab-separated columns with headers
- **exiftool:** "Tag Name: Value" pairs
- **strings:** Raw text lines
- **file:** "filename: file type description"

Example parsing for exiftool:
```python
lines = output.split('\n')
metadata = {}
for line in lines:
    if ': ' in line:
        key, value = line.split(': ', 1)
        metadata[key.strip()] = value.strip()
```

---

## Part 5: Creating a Tool Library

### Organizing Your Tools

Create a reusable module: `stego_tools.py`

```python
"""
StegoCrew Tool Library
Reusable steganography tools for CTF challenges
"""

import subprocess
import os
from crewai_tools import tool

# ==================== FILE ANALYSIS TOOLS ====================

@tool
def get_file_type(file_path: str) -> str:
    """Get detailed file type information."""
    # Implementation...

@tool
def extract_metadata(file_path: str) -> str:
    """Extract all metadata using exiftool."""
    # Implementation...

# ==================== STEGANOGRAPHY TOOLS ====================

@tool
def extract_with_steghide(file_path: str, password: str = "") -> str:
    """Extract hidden data with steghide."""
    # Implementation...

@tool
def analyze_with_binwalk(file_path: str, extract: bool = False) -> str:
    """Find embedded files with binwalk."""
    # Implementation...

@tool
def extract_strings(file_path: str, min_length: int = 4) -> str:
    """Extract printable strings."""
    # Implementation...

@tool
def analyze_lsb(file_path: str) -> str:
    """Analyze LSB steganography (PNG/BMP) with zsteg."""
    # Implementation...

# ==================== HELPER FUNCTIONS ====================

def check_tool_installed(tool_name: str) -> bool:
    """Check if a system tool is installed."""
    try:
        subprocess.run([tool_name, '--version'],
                      capture_output=True, timeout=5)
        return True
    except FileNotFoundError:
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
        'foremost': 'sudo apt install foremost'
    }
    return install_commands.get(tool_name, f'Install {tool_name} manually')
```

---

## Part 6: Error Handling Best Practices

### Handling Missing Tools

**Pattern 1: Tool Check Before Use**

```python
@tool
def safe_tool_wrapper(file_path: str) -> str:
    """Wrapper with tool availability check."""

    # Check if tool exists
    if not check_tool_installed('steghide'):
        return (
            "❌ ERROR: steghide not installed\n"
            "Install with: sudo apt install steghide\n"
            "Then retry this task."
        )

    # Proceed with tool usage...
```

**Pattern 2: Try Multiple Tools**

```python
@tool
def extract_with_fallback(file_path: str) -> str:
    """Try multiple extraction methods."""

    results = []

    # Try steghide
    if check_tool_installed('steghide'):
        result = try_steghide(file_path)
        results.append(('steghide', result))

    # Try zsteg
    if check_tool_installed('zsteg'):
        result = try_zsteg(file_path)
        results.append(('zsteg', result))

    # Try binwalk
    if check_tool_installed('binwalk'):
        result = try_binwalk(file_path)
        results.append(('binwalk', result))

    # Compile results
    report = "Attempted multiple extraction methods:\n\n"
    for tool, result in results:
        report += f"[{tool}] {result}\n\n"

    return report
```

### Timeout Protection

```python
# Always use timeout to prevent hanging
result = subprocess.run(
    command,
    capture_output=True,
    text=True,
    timeout=30  # ← CRITICAL for potentially slow tools
)
```

---

## Part 7: Testing Your Tools

### Creating Test Files

**Method 1: Create Simple Test File**

```bash
# Create image with hidden data using steghide
echo "CTF{test_flag_12345}" > secret.txt
steghide embed -cf test_image.jpg -ef secret.txt -p "mypassword"
```

**Method 2: Use Sample CTF Challenges**

Download from:
- https://github.com/DominicBreuker/stego-toolkit/tree/master/examples
- Practice CTFs on https://ctftime.org/
- Create your own test files

### Unit Testing Pattern

```python
def test_steghide_tool():
    """Test steghide wrapper."""

    print("Testing steghide extraction...")

    # Test 1: File with embedded data
    result = extract_with_steghide("test_files/hidden.jpg", "password123")
    print(f"Test 1: {result}")
    assert "CTF{" in result, "Should find flag"

    # Test 2: File without embedded data
    result = extract_with_steghide("test_files/clean.jpg", "")
    print(f"Test 2: {result}")
    assert "No steghide data" in result

    # Test 3: Wrong password
    result = extract_with_steghide("test_files/hidden.jpg", "wrong")
    print(f"Test 3: {result}")
    assert "wrong password" in result.lower()

    print("✅ All tests passed!")

if __name__ == "__main__":
    test_steghide_tool()
```

---

## Part 8: Building the Complete Example

See `examples/05_stego_tools.py` for a complete working example that demonstrates:

1. ✅ Multiple steganography tools (steghide, binwalk, exiftool, strings)
2. ✅ Proper error handling and tool detection
3. ✅ Output parsing and formatting
4. ✅ Agent integration with specialized stego agent
5. ✅ Real CTF challenge workflow

---

## Part 9: Practice Exercise

### 🎯 Challenge: Build Your Stego Analyzer

Create `my_stego_analyzer.py` that:

1. Creates a **Stego Analyst Agent** with these tools:
   - `extract_with_steghide` (with password support)
   - `analyze_with_binwalk` (with extraction option)
   - `extract_metadata` (using exiftool)
   - `extract_strings` (with configurable min length)

2. Processes a CTF challenge file through all tools

3. Generates a comprehensive report with findings

**Starter Template:**

```python
#!/usr/bin/env python3
"""
Your Steganography Analyzer
Practice building a complete stego analysis system.
"""

from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import tool
from langchain_anthropic import ChatAnthropic
import subprocess

load_dotenv()
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)

# ==================== YOUR TOOLS ====================

@tool
def extract_with_steghide(file_path: str, password: str = "") -> str:
    """Extract hidden data from image/audio using steghide."""
    # TODO: Implement steghide wrapper
    pass

@tool
def analyze_with_binwalk(file_path: str) -> str:
    """Scan for embedded files using binwalk."""
    # TODO: Implement binwalk wrapper
    pass

@tool
def extract_metadata(file_path: str) -> str:
    """Extract metadata using exiftool."""
    # TODO: Implement exiftool wrapper
    pass

# ==================== YOUR AGENT ====================

stego_analyst = Agent(
    role="Steganography Analysis Expert",
    goal="Thoroughly analyze files for hidden data using all available techniques",
    backstory="""You are a CTF steganography specialist with years of experience.
    You systematically apply tools to uncover hidden flags.""",
    tools=[extract_with_steghide, analyze_with_binwalk, extract_metadata],
    llm=llm,
    verbose=True
)

# ==================== YOUR TASK ====================

analysis_task = Task(
    description="""
    Analyze the file: {file_path}

    Use all your tools to:
    1. Extract metadata
    2. Check for steghide data
    3. Scan for embedded files

    Look for CTF flags in format: CTF{...} or FLAG{...}
    Provide a complete analysis report.
    """,
    expected_output="Comprehensive steganography analysis report",
    agent=stego_analyst
)

# ==================== MAIN ====================

def analyze_file(file_path: str):
    """Analyze a file for steganography."""
    crew = Crew(
        agents=[stego_analyst],
        tasks=[analysis_task],
        verbose=True
    )

    result = crew.kickoff(inputs={"file_path": file_path})
    print(f"\n{'='*70}\n{result}\n{'='*70}")
    return result

if __name__ == "__main__":
    import sys
    file_path = sys.argv[1] if len(sys.argv) > 1 else "test_file.jpg"
    analyze_file(file_path)
```

### Extension Challenge

After completing the basic analyzer:

1. Add **password brute-forcing** for steghide (try common passwords)
2. Add **LSB analysis** using zsteg for PNG files
3. Create a **multi-agent system** with separate agents for:
   - Metadata extraction
   - Steganography detection
   - Data decoding
   - Report generation

---

## Part 10: Common Pitfalls and Solutions

### Pitfall 1: Not Checking Tool Installation

**Problem:** Agent crashes when tool missing

**Solution:** Always check tool availability first

```python
if not check_tool_installed('steghide'):
    return "Install steghide first: sudo apt install steghide"
```

### Pitfall 2: Not Handling Binary Output

**Problem:** Tool returns binary data that can't be displayed

**Solution:** Detect and handle binary data

```python
try:
    data.decode('utf-8')  # Try to decode
    return f"Extracted text: {data}"
except UnicodeDecodeError:
    return f"Extracted binary data ({len(data)} bytes) - saved to file"
```

### Pitfall 3: Ignoring Exit Codes

**Problem:** Tool fails but you don't detect it

**Solution:** Check `returncode`

```python
if result.returncode != 0:
    return f"Tool failed: {result.stderr}"
```

### Pitfall 4: Not Sanitizing File Paths

**Problem:** Command injection vulnerability

**Solution:** Validate file paths

```python
import os

def safe_file_path(file_path: str) -> bool:
    """Check if file path is safe."""
    # Check file exists
    if not os.path.exists(file_path):
        return False

    # Check it's actually a file
    if not os.path.isfile(file_path):
        return False

    # Resolve to absolute path (prevents path traversal)
    abs_path = os.path.abspath(file_path)

    return True
```

---

## 📊 Progress Check

You should now be able to:

- ✅ Explain common CTF steganography techniques
- ✅ Build tools that wrap system utilities
- ✅ Handle missing dependencies gracefully
- ✅ Parse output from various stego tools
- ✅ Create a reusable tool library
- ✅ Test tools with real challenge files

---

## 🎯 Next Steps

1. **Complete the practice exercise** (`my_stego_analyzer.py`)
2. **Test with real CTF challenges** from past competitions
3. **Move to Lesson 7** where we build the complete multi-agent StegoCrew system!

---

## 📚 Additional Resources

- **Steghide Manual:** http://steghide.sourceforge.net/documentation/manpage.php
- **Binwalk Wiki:** https://github.com/ReFirmLabs/binwalk/wiki
- **CTF Stego Challenges:** https://github.com/topics/ctf-steganography
- **Stego Toolkit:** https://github.com/DominicBreuker/stego-toolkit

---

**Ready to build real CTF-solving agents?** 🚀

The tools you built in this lesson will power the complete StegoCrew system in Lesson 7!
