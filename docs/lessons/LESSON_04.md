# Lesson 4: Custom Tools Deep Dive

**Duration:** 2-3 hours
**Prerequisites:** Lesson 3 completed
**Goal:** Master creating complex, production-ready tools for agents

---

## 🎯 What You'll Learn

By the end of this lesson, you'll have:
1. ✅ Created tools with multiple parameters
2. ✅ Implemented proper error handling
3. ✅ Wrapped system commands (steghide, binwalk, exiftool)
4. ✅ Returned structured data from tools
5. ✅ Built reusable tool patterns
6. ✅ Understood tool best practices

---

## 📚 Lesson Overview

```
Part 1: Advanced Tool Parameters
Part 2: Error Handling Patterns
Part 3: Wrapping System Commands
Part 4: Structured Data Returns
Part 5: Real Steganography Tools
Part 6: Tool Testing & Debugging
Part 7: Best Practices
```

---

## Part 1: Tools with Multiple Parameters

In Lesson 3, we created simple tools with one parameter. Real-world tools need more!

### Basic Multi-Parameter Tool

```python
from crewai_tools import tool

@tool
def search_text_in_file(file_path: str, search_term: str, case_sensitive: bool = False) -> str:
    """
    Search for a specific term in a file.

    Args:
        file_path: Path to the file to search
        search_term: The text to search for
        case_sensitive: Whether search should be case-sensitive (default: False)

    Returns:
        Lines containing the search term with line numbers
    """
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()

        results = []
        for i, line in enumerate(lines, 1):
            # Apply case sensitivity
            line_to_check = line if case_sensitive else line.lower()
            term_to_check = search_term if case_sensitive else search_term.lower()

            if term_to_check in line_to_check:
                results.append(f"Line {i}: {line.strip()}")

        if results:
            return "\n".join(results)
        else:
            return f"No matches found for '{search_term}'"

    except FileNotFoundError:
        return f"Error: File not found - {file_path}"
    except Exception as e:
        return f"Error reading file: {str(e)}"
```

**Key points:**
- Multiple typed parameters
- Default values (case_sensitive=False)
- Clear docstring explaining each parameter
- Error handling for different scenarios

---

## Part 2: Error Handling Patterns

Good tools handle errors gracefully!

### Pattern 1: Try-Except with Specific Errors

```python
@tool
def read_file_safely(file_path: str, max_size_mb: int = 10) -> str:
    """
    Safely read a file with size limits and error handling.

    Args:
        file_path: Path to file
        max_size_mb: Maximum file size in MB (default: 10)

    Returns:
        File contents or error message
    """
    import os

    try:
        # Check if file exists
        if not os.path.exists(file_path):
            return f"ERROR: File does not exist: {file_path}"

        # Check file size
        file_size = os.path.getsize(file_path)
        max_size_bytes = max_size_mb * 1024 * 1024

        if file_size > max_size_bytes:
            return f"ERROR: File too large ({file_size / 1024 / 1024:.2f} MB). Max: {max_size_mb} MB"

        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return f"Successfully read {len(content)} characters from {file_path}"

    except PermissionError:
        return f"ERROR: Permission denied for file: {file_path}"
    except UnicodeDecodeError:
        return f"ERROR: File is not a text file or has encoding issues"
    except Exception as e:
        return f"ERROR: Unexpected error - {type(e).__name__}: {str(e)}"
```

**Error handling best practices:**
1. Check preconditions (file exists, size limits)
2. Catch specific exceptions first
3. Provide clear error messages
4. Always return a string (never raise exceptions in tools)

---

## Part 3: Wrapping System Commands

This is crucial for our CTF solver! Let's wrap real steganography tools.

### Pattern: Subprocess Wrapper

```python
import subprocess
from crewai_tools import tool

@tool
def run_exiftool(file_path: str) -> str:
    """
    Extract metadata from a file using exiftool.

    Args:
        file_path: Path to the file to analyze

    Returns:
        Metadata information or error message
    """
    try:
        # Run exiftool command
        result = subprocess.run(
            ['exiftool', file_path],
            capture_output=True,
            text=True,
            timeout=30  # 30 second timeout
        )

        # Check if command succeeded
        if result.returncode == 0:
            return f"Metadata for {file_path}:\n{result.stdout}"
        else:
            return f"Error running exiftool: {result.stderr}"

    except FileNotFoundError:
        return "ERROR: exiftool not installed. Install with: sudo apt install exiftool"
    except subprocess.TimeoutExpired:
        return "ERROR: exiftool timed out (file too large or hung)"
    except Exception as e:
        return f"ERROR: {type(e).__name__}: {str(e)}"
```

### Pattern: Command with Options

```python
@tool
def run_binwalk(file_path: str, extract: bool = False) -> str:
    """
    Analyze file for embedded files and data using binwalk.

    Args:
        file_path: Path to file to analyze
        extract: Whether to extract found files (default: False)

    Returns:
        Binwalk analysis results
    """
    try:
        # Build command
        cmd = ['binwalk']

        if extract:
            cmd.append('-e')  # Extract files

        cmd.append(file_path)

        # Run command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            output = result.stdout

            if "DECIMAL" in output:
                # Binwalk found something!
                return f"Binwalk found embedded data:\n{output}"
            else:
                return f"Binwalk found nothing suspicious in {file_path}"
        else:
            return f"Binwalk error: {result.stderr}"

    except FileNotFoundError:
        return "ERROR: binwalk not installed. Install with: sudo apt install binwalk"
    except subprocess.TimeoutExpired:
        return "ERROR: binwalk timed out"
    except Exception as e:
        return f"ERROR: {str(e)}"
```

---

## Part 4: Structured Data Returns

Sometimes you need to return complex data, not just strings.

### Pattern: JSON Returns

```python
import json
from crewai_tools import tool

@tool
def analyze_image_metadata(image_path: str) -> str:
    """
    Analyze image metadata and return structured information.

    Args:
        image_path: Path to image file

    Returns:
        JSON string with structured metadata
    """
    from PIL import Image
    import os

    try:
        # Open image
        img = Image.open(image_path)

        # Collect metadata
        metadata = {
            "file_name": os.path.basename(image_path),
            "file_size_bytes": os.path.getsize(image_path),
            "format": img.format,
            "mode": img.mode,
            "width": img.width,
            "height": img.height,
            "total_pixels": img.width * img.height,
            "has_exif": hasattr(img, '_getexif') and img._getexif() is not None
        }

        # Return as formatted JSON
        return json.dumps(metadata, indent=2)

    except Exception as e:
        error_data = {
            "error": str(e),
            "error_type": type(e).__name__
        }
        return json.dumps(error_data, indent=2)
```

**Note:** Return JSON as a string! Agents can parse it.

---

## Part 5: Real Steganography Tools

Let's create actual tools for our CTF solver!

### Tool 1: Steghide Wrapper

```python
@tool
def check_steghide(file_path: str, password: str = "") -> str:
    """
    Try to extract hidden data from an image using steghide.

    Args:
        file_path: Path to image file (JPG or BMP)
        password: Password to try (default: empty string)

    Returns:
        Extraction result or error message
    """
    import subprocess
    import os

    try:
        # Create temp output file
        output_file = f"/tmp/steghide_output_{os.getpid()}.txt"

        # Build command
        cmd = ['steghide', 'extract', '-sf', file_path, '-xf', output_file]

        if password:
            cmd.extend(['-p', password])
        else:
            cmd.extend(['-p', ''])  # Empty password

        # Run steghide
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )

        # Check if extraction succeeded
        if result.returncode == 0:
            # Read extracted data
            if os.path.exists(output_file):
                with open(output_file, 'r') as f:
                    data = f.read()
                os.remove(output_file)  # Clean up
                return f"Steghide extraction successful!\nExtracted data:\n{data}"
            else:
                return "Steghide succeeded but no output file created"
        else:
            if "could not extract" in result.stderr.lower():
                return "No steghide data found or wrong password"
            else:
                return f"Steghide error: {result.stderr}"

    except FileNotFoundError:
        return "ERROR: steghide not installed. Install with: sudo apt install steghide"
    except subprocess.TimeoutExpired:
        return "ERROR: steghide timed out"
    except Exception as e:
        return f"ERROR: {str(e)}"
```

### Tool 2: String Extractor

```python
@tool
def extract_strings(file_path: str, min_length: int = 4) -> str:
    """
    Extract printable strings from a binary file.

    Args:
        file_path: Path to file
        min_length: Minimum string length (default: 4)

    Returns:
        Found strings
    """
    import subprocess

    try:
        # Run strings command
        result = subprocess.run(
            ['strings', '-n', str(min_length), file_path],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            strings = result.stdout.strip().split('\n')

            # Filter interesting strings (potential flags, URLs, etc.)
            interesting = []
            for s in strings:
                s = s.strip()
                if len(s) >= min_length:
                    # Check for flag formats
                    if 'CTF{' in s or 'FLAG{' in s or 'flag{' in s:
                        interesting.insert(0, f"⭐ POTENTIAL FLAG: {s}")
                    # Check for URLs
                    elif 'http://' in s or 'https://' in s:
                        interesting.append(f"🔗 URL: {s}")
                    # Check for base64-like
                    elif len(s) > 20 and s.replace('=', '').isalnum():
                        interesting.append(f"🔤 BASE64?: {s}")

            if interesting:
                return "Interesting strings found:\n" + "\n".join(interesting[:20])
            else:
                return f"No particularly interesting strings found (found {len(strings)} total strings)"

        else:
            return f"Strings command error: {result.stderr}"

    except FileNotFoundError:
        return "ERROR: 'strings' command not found"
    except Exception as e:
        return f"ERROR: {str(e)}"
```

### Tool 3: File Entropy Calculator

```python
@tool
def calculate_entropy(file_path: str) -> str:
    """
    Calculate Shannon entropy of a file (measure of randomness).
    High entropy suggests encryption or compression.

    Args:
        file_path: Path to file

    Returns:
        Entropy value and interpretation
    """
    import math
    from collections import Counter

    try:
        # Read file as bytes
        with open(file_path, 'rb') as f:
            data = f.read()

        if len(data) == 0:
            return "ERROR: File is empty"

        # Count byte frequencies
        byte_counts = Counter(data)

        # Calculate Shannon entropy
        entropy = 0
        for count in byte_counts.values():
            probability = count / len(data)
            entropy -= probability * math.log2(probability)

        # Interpret entropy
        interpretation = ""
        if entropy < 3:
            interpretation = "Very low (likely plain text or simple data)"
        elif entropy < 5:
            interpretation = "Low to medium (normal files)"
        elif entropy < 7:
            interpretation = "Medium to high (compressed or mixed data)"
        else:
            interpretation = "Very high (encrypted or random data)"

        return f"""
Entropy Analysis for {file_path}:
- Shannon Entropy: {entropy:.4f} bits per byte
- Maximum possible: 8.0 bits per byte
- Interpretation: {interpretation}
- File size: {len(data)} bytes

⚠️  High entropy (>7.5) may indicate:
- Encrypted data
- Compressed archives
- Random data
- Steganography payload
"""

    except Exception as e:
        return f"ERROR: {str(e)}"
```

---

## Part 6: Tool Testing & Debugging

How to test your tools before giving them to agents.

### Testing Pattern

```python
def test_tool():
    """Test a tool manually before using with agents."""

    print("Testing extract_strings tool...")

    # Test 1: Normal file
    result = extract_strings("/etc/hosts")
    print("Test 1 - Normal file:")
    print(result)
    print()

    # Test 2: Non-existent file
    result = extract_strings("/nonexistent/file.txt")
    print("Test 2 - Non-existent file:")
    print(result)
    print()

    # Test 3: Binary file
    result = extract_strings("/bin/ls")
    print("Test 3 - Binary file:")
    print(result)
    print()

if __name__ == "__main__":
    test_tool()
```

---

## Part 7: Tool Best Practices

### ✅ DO's

1. **Clear Docstrings**
   ```python
   @tool
   def my_tool(param: str) -> str:
       """
       Clear one-line summary.

       Detailed explanation of what the tool does.

       Args:
           param: What this parameter is for

       Returns:
           What the tool returns
       """
   ```

2. **Type Hints**
   ```python
   def my_tool(file_path: str, count: int = 5) -> str:
   ```

3. **Error Handling**
   ```python
   try:
       # do something
   except SpecificError:
       return "Clear error message"
   ```

4. **Return Strings**
   ```python
   return "Success: result here"  # ✅
   return {"data": "value"}       # ❌ Return JSON string instead
   ```

5. **Timeouts for External Commands**
   ```python
   subprocess.run(cmd, timeout=30)
   ```

### ❌ DON'Ts

1. **Don't Raise Exceptions**
   ```python
   # BAD
   raise ValueError("Error!")

   # GOOD
   return "ERROR: Invalid value"
   ```

2. **Don't Return Complex Objects**
   ```python
   # BAD
   return {"key": "value"}

   # GOOD
   return json.dumps({"key": "value"})
   ```

3. **Don't Forget Error Cases**
   ```python
   # BAD - no error handling
   with open(file) as f:
       return f.read()

   # GOOD
   try:
       with open(file) as f:
           return f.read()
   except FileNotFoundError:
       return "ERROR: File not found"
   ```

---

## 🧪 Practice Exercises

### Exercise 1: Password List Tool

Create a tool that tries steghide with multiple passwords from a list.

**Requirements:**
- Accept file path and list of passwords
- Try each password
- Return which password worked (if any)
- Handle errors gracefully

<details>
<summary>Click for solution</summary>

```python
@tool
def try_steghide_passwords(file_path: str, passwords: list) -> str:
    """
    Try multiple passwords with steghide.

    Args:
        file_path: Path to image
        passwords: List of passwords to try

    Returns:
        Result of password attempts
    """
    import subprocess

    # Note: Can't pass list directly to agents easily
    # Better approach: pass comma-separated string
    if isinstance(passwords, str):
        password_list = [p.strip() for p in passwords.split(',')]
    else:
        password_list = passwords

    for password in password_list:
        try:
            result = subprocess.run(
                ['steghide', 'extract', '-sf', file_path, '-p', password, '-xf', '/tmp/test'],
                capture_output=True,
                timeout=10
            )

            if result.returncode == 0:
                return f"SUCCESS! Password found: '{password}'"
        except:
            continue

    return f"No valid password found in list of {len(password_list)} passwords"
```
</details>

### Exercise 2: File Type Identifier

Create a tool that identifies the true file type (even if extension is wrong).

**Requirements:**
- Check file signature (magic bytes)
- Compare with file extension
- Return true type vs claimed type

---

## 🎓 Summary

You now know how to create:

✅ **Multi-parameter tools** with defaults
✅ **Error handling** that never crashes
✅ **System command wrappers** for external tools
✅ **Structured data returns** using JSON
✅ **Real steganography tools** for CTF solving
✅ **Tool testing** patterns
✅ **Best practices** for production tools

---

## 🚀 What's Next?

**Next lesson: [Lesson 5 - Multi-Agent Coordination](./LESSON_05.md)**

We'll learn:
- Running multiple agents together
- Agent communication and context sharing
- Sequential vs parallel workflows
- Building your first multi-agent crew

---

## 📝 Homework

Before Lesson 5, create these tools:

1. **zsteg wrapper** - Tool for PNG/BMP analysis
2. **Base64 decoder** - Detect and decode Base64 strings
3. **File comparator** - Compare two files for differences

---

**🎉 Congratulations! You can now create professional-grade tools for AI agents!**

*Previous: [Lesson 3 - Your First Agent](./LESSON_03.md)*
*Next: [Lesson 5 - Multi-Agent Coordination](./LESSON_05.md)*
