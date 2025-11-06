# Contributing to StegoCrew

Thanks for considering contributing. This project is meant to be educational, so contributions that help people learn are especially valuable.

---

## How to Contribute

**Report bugs:**
- Open an issue with steps to reproduce
- Include Python version, OS, and error messages
- Check if it's already reported

**Fix documentation:**
- Typos, unclear explanations, broken links
- Better code examples
- Troubleshooting tips you discovered

**Add tools:**
- Wrap new steganography tools (e.g., outguess, stegpy)
- Follow the @tool decorator pattern
- Include error handling and docstrings

**Share challenges:**
- Add test CTF challenges to `test_files/`
- Document the solution
- Include difficulty level

**Improve performance:**
- Caching, parallel execution, faster tools
- Profile before optimizing
- Benchmark the improvement

---

## Setup

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/StegoCrew.git
cd StegoCrew

# Set up environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create branch
git checkout -b feature/your-feature
```

---

## Code Style

**Python:**
- Follow PEP 8 (mostly)
- Descriptive variable names
- Docstrings for tools and functions
- Type hints where helpful

**Example tool:**
```python
@tool
def analyze_something(file_path: str, option: bool = False) -> str:
    """
    Brief description of what this tool does.

    Args:
        file_path: Path to the file
        option: What this option does

    Returns:
        Result as formatted string
    """
    # Implementation
    if not os.path.exists(file_path):
        return f"Error: File not found - {file_path}"

    try:
        # Do the thing
        result = do_analysis(file_path)
        return f"Success: {result}"
    except Exception as e:
        return f"Error: {str(e)}"
```

**Key points:**
- Clear docstrings (agents read these!)
- Error handling
- Return strings, not exceptions
- Validate inputs

---

## Commit Messages

Keep them simple and descriptive:

```
add support for outguess tool
fix steghide error handling
update lesson 3 with better examples
```

Not:
```
Add comprehensive support for the outguess steganography detection tool with full error handling
```

---

## Pull Requests

1. **One feature per PR**
   - Don't bundle multiple unrelated changes
   - Easier to review and merge

2. **Test your changes**
   - Run examples that use your code
   - Add tests if you're adding tools
   - Make sure nothing breaks

3. **Update docs if needed**
   - New tool? Document it
   - Changed behavior? Update relevant lesson
   - Breaking change? Update examples

4. **Write a clear PR description**
   ```
   ## What
   Added support for outguess steganography tool

   ## Why
   Common CTF tool that wasn't supported

   ## Testing
   Tested on 5 sample files, found hidden data in 3
   ```

---

## Good First Issues

Starting points:

- **Add a new tool wrapper:** Pick any stego tool not yet supported
- **Improve error messages:** Make them more helpful
- **Add test challenges:** Create sample CTF files
- **Fix documentation:** Typos, unclear sections, missing examples
- **Add code comments:** Explain complex sections

---

## Areas That Need Help

**Tool integration:**
- Audio steganography (LSB in WAV, SSTV)
- Video steganography
- More image formats (GIF, WebP)

**Testing:**
- More test challenges
- Benchmark suite
- Real CTF challenge validation

**Performance:**
- Caching mechanisms
- Parallel tool execution
- Faster file analysis

**Documentation:**
- Video tutorials
- More examples
- Better troubleshooting guides

---

## Code of Conduct

Be respectful. Help people learn. We're all here to get better at this stuff.

If you see inappropriate behavior, report it via GitHub issues.

---

## Questions?

- Open an issue for questions about contributing
- Check existing issues and PRs first
- Don't hesitate to ask for clarification

---

## License

By contributing, you agree your code will be licensed under the MIT License.
