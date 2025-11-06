# Lesson 4: Custom Tools

**Duration:** 2-3 hours
**Prerequisites:** Lesson 3 completed

---

## Building Production-Ready Tools

Lesson 3 showed basic tools. Now we'll build tools that wrap real system commands and handle errors properly.

---

## Multi-Parameter Tools

Real tools need multiple parameters and defaults:

```python
from crewai_tools import tool

@tool
def search_in_file(file_path: str, term: str, case_sensitive: bool = False) -> str:
    """
    Search for text in a file.

    Args:
        file_path: File to search
        term: Text to find
        case_sensitive: Match case (default: False)

    Returns:
        Lines containing the term with line numbers
    """
    try:
        with open(file_path) as f:
            lines = f.readlines()

        results = []
        for i, line in enumerate(lines, 1):
            check_line = line if case_sensitive else line.lower()
            check_term = term if case_sensitive else term.lower()

            if check_term in check_line:
                results.append(f"Line {i}: {line.strip()}")

        return "\n".join(results) if results else f"No matches for '{term}'"

    except FileNotFoundError:
        return f"File not found: {file_path}"
    except Exception as e:
        return f"Error: {str(e)}"
```

**Key points:**
- Type hints help agents understand parameters
- Default values for optional params
- Specific error handling
- Always return strings (never raise exceptions)

---

## Error Handling Patterns

**Pattern 1: Check before acting**

```python
@tool
def process_file(file_path: str) -> str:
    """Process a file safely."""
    # Validate first
    if not os.path.exists(file_path):
        return f"File not found: {file_path}"

    if not os.path.isfile(file_path):
        return f"Not a file: {file_path}"

    if os.path.getsize(file_path) > 10_000_000:  # 10MB limit
        return "File too large (max 10MB)"

    # Then process
    try:
        with open(file_path) as f:
            content = f.read()
        return f"Processed {len(content)} bytes"
    except Exception as e:
        return f"Error: {str(e)}"
```

**Pattern 2: Subprocess with timeout**

```python
import subprocess

@tool
def run_system_command(command: str, timeout_sec: int = 30) -> str:
    """Run system command with timeout."""
    try:
        result = subprocess.run(
            command.split(),
            capture_output=True,
            text=True,
            timeout=timeout_sec
        )

        if result.returncode == 0:
            return result.stdout
        else:
            return f"Command failed: {result.stderr}"

    except subprocess.TimeoutExpired:
        return f"Command timed out after {timeout_sec}s"
    except FileNotFoundError:
        return f"Command not found: {command.split()[0]}"
    except Exception as e:
        return f"Error: {str(e)}"
```

---

## Wrapping Steganography Tools

Real example: wrapping steghide

```python
import subprocess
import os

@tool
def extract_with_steghide(file_path: str, password: str = "") -> str:
    """
    Extract hidden data using steghide.

    Args:
        file_path: Image file to analyze
        password: Steghide password (default: empty)

    Returns:
        Extracted data or error message
    """
    # Check steghide is installed
    try:
        subprocess.run(['steghide', '--version'], capture_output=True, timeout=5)
    except FileNotFoundError:
        return "steghide not installed. Run: sudo apt install steghide"

    # Check file exists
    if not os.path.exists(file_path):
        return f"File not found: {file_path}"

    # Run steghide
    output_file = f"{file_path}.extracted"

    try:
        cmd = [
            'steghide', 'extract',
            '-sf', file_path,        # source file
            '-xf', output_file,      # extract to
            '-p', password,          # password
            '-f'                     # force overwrite
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if result.returncode == 0 and os.path.exists(output_file):
            # Read extracted data
            with open(output_file) as f:
                data = f.read()

            # Clean up
            os.remove(output_file)

            # Check for flag
            if 'CTF{' in data or 'FLAG{' in data:
                return f"FLAG FOUND!\n{data}"

            return f"Extracted data:\n{data[:500]}"  # Limit output

        return "No embedded data found"

    except subprocess.TimeoutExpired:
        return "steghide timed out (30s)"
    except Exception as e:
        return f"Error: {str(e)}"
```

**Why this pattern works:**
- Checks tool is installed first
- Validates inputs
- Uses timeout to prevent hanging
- Captures both stdout and stderr
- Cleans up temp files
- Limits output length
- Highlights flags

---

## Helper Function Pattern

Don't repeat yourself. Create helpers:

```python
def check_tool_installed(tool_name: str) -> bool:
    """Check if a system tool is available."""
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


@tool
def use_binwalk(file_path: str) -> str:
    """Analyze file for embedded data using binwalk."""
    if not check_tool_installed('binwalk'):
        return "binwalk not installed"

    if not os.path.exists(file_path):
        return f"File not found: {file_path}"

    try:
        result = subprocess.run(
            ['binwalk', file_path],
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return f"Error: {str(e)}"
```

---

## Structured Output

Sometimes you want to format results consistently:

```python
@tool
def analyze_image_metadata(file_path: str) -> str:
    """Extract image metadata using exiftool."""
    if not check_tool_installed('exiftool'):
        return "exiftool not installed"

    if not os.path.exists(file_path):
        return f"File not found: {file_path}"

    try:
        result = subprocess.run(
            ['exiftool', file_path],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            return f"exiftool failed: {result.stderr}"

        # Parse output into structured format
        metadata = {}
        for line in result.stdout.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()

        # Format for readability
        output = ["=== METADATA ==="]
        for key, value in metadata.items():
            output.append(f"{key}: {value}")

        return "\n".join(output)

    except Exception as e:
        return f"Error: {str(e)}"
```

---

## Tool Testing

Test your tools independently before giving them to agents:

```python
if __name__ == '__main__':
    # Test the tool directly
    print("Testing steghide tool...")

    result = extract_with_steghide("test_image.jpg", password="")
    print(result)

    result = extract_with_steghide("test_image.jpg", password="secret")
    print(result)

    result = extract_with_steghide("nonexistent.jpg")
    print(result)
```

---

## Common Issues

**Tool doesn't execute:**

Agent doesn't call your tool. Usually means:
- Docstring is unclear
- Tool name is confusing
- Task description doesn't hint at tool usage

Fix: Make docstring very explicit about what the tool does.

**Tool returns None:**

Breaks agent execution. Always return a string:
```python
# Bad
@tool
def bad_tool(x):
    if x:
        return "ok"
    # Returns None if x is False!

# Good
@tool
def good_tool(x):
    if x:
        return "ok"
    return "Input was false"  # Always return something
```

**Tool hangs:**

Always use timeouts on subprocess calls:
```python
subprocess.run(cmd, timeout=30)  # 30 second max
```

**Large output breaks context:**

LLMs have token limits. Truncate long outputs:
```python
output = long_string[:1000] + "..." if len(long_string) > 1000 else long_string
return output
```

---

## Best Practices

1. **Clear docstrings** - Agents read these to decide which tool to use
2. **Type hints** - Help agents understand parameters
3. **Error handling** - Never raise exceptions, return error strings
4. **Timeouts** - Prevent tools from hanging forever
5. **Validate inputs** - Check files exist, parameters are valid
6. **Limit output** - Don't return megabytes of text
7. **Clean up** - Remove temp files
8. **Test independently** - Run tools standalone first
9. **Check dependencies** - Verify system tools are installed
10. **Return strings** - Always, even for errors

---

## Practice Exercise

Create `examples/my_first_tool.py` that wraps the `strings` command:

```python
@tool
def extract_strings(file_path: str, min_length: int = 4) -> str:
    """
    Extract printable strings from a file.

    Args:
        file_path: File to analyze
        min_length: Minimum string length (default: 4)

    Returns:
        Printable strings found in the file
    """
    # Your implementation here
    pass
```

**Requirements:**
- Check if `strings` command is available
- Validate file exists
- Use subprocess with timeout
- Return first 50 strings max
- Handle errors

**Test it on:** `/bin/ls` or any binary file

---

## Key Takeaways

**Good tool structure:**
```python
@tool
def tool_name(param: type, param2: type = default) -> str:
    """Clear description.

    Args:
        param: What it is
        param2: What it is

    Returns:
        What you get back
    """
    # 1. Validate inputs
    # 2. Try operation with timeout
    # 3. Handle errors
    # 4. Return formatted string
```

**Error handling priority:**
1. Check dependencies (tool installed?)
2. Validate inputs (file exists?)
3. Try operation with timeout
4. Catch specific exceptions
5. Always return helpful error message

---

## Next Steps

You can now wrap any system command as a tool. Next lesson: multi-agent coordination.

[Continue to Lesson 5: Multi-Agent Systems →](./LESSON_05.md)

---

*Tip: When wrapping commands, run them manually in terminal first to understand their output format. This helps you parse the results correctly.*
