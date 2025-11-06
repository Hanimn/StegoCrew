# Lesson 6: Steganography Tools Integration

**Duration:** 3-4 hours
**Prerequisites:** Lessons 3-5 completed

---

## Integrating Real Stego Tools

Now we wrap actual steganography tools: steghide, binwalk, exiftool, zsteg.

Reference the complete implementation in `examples/05_stego_tools.py`.

---

## Tool Patterns

All stego tools follow this pattern:

```python
from crewai_tools import tool
import subprocess
import os

@tool
def tool_name(file_path: str, optional_param: str = "") -> str:
    """Clear description of what this does."""

    # 1. Check tool installed
    # 2. Validate file exists
    # 3. Run command with timeout
    # 4. Parse/format output
    # 5. Return result string
```

---

## Key Tools

See `examples/05_stego_tools.py` for complete implementations of:

- `extract_with_steghide` - Extract password-protected data
- `analyze_with_binwalk` - Find embedded files
- `extract_metadata` - Get EXIF/metadata
- `extract_strings` - Pull printable text
- `get_file_type` - Identify file format

Practice file: `examples/my_stego_analyzer.py` has TODO markers for you to complete.

---

## Next Steps

You have working stego tools. Next: building the complete 5-agent system.

[Continue to Lesson 7: Complete MVP →](./LESSON_07.md)
