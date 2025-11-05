# Contributing to StegoCrew 🤝

Thank you for your interest in contributing to StegoCrew! This project aims to teach multi-agent systems through a practical CTF steganography solver.

---

## 🌟 Ways to Contribute

### 1. **Report Issues**
- Found a bug? [Open an issue](../../issues/new)
- Unclear documentation? Let us know
- Tool not working? Report it

### 2. **Improve Documentation**
- Fix typos or unclear explanations
- Add examples or clarifications
- Translate lessons (future)
- Improve code comments

### 3. **Add Steganography Tools**
- Implement new tool wrappers
- Add support for new file types
- Improve existing tools
- Add error handling

### 4. **Share CTF Challenges**
- Add test cases to `test_files/`
- Share challenge solutions
- Document interesting techniques
- Create practice challenges

### 5. **Extend Examples**
- Create new lesson materials
- Build additional examples
- Add practice exercises
- Create video tutorials

### 6. **Build New Features**
- Web interface improvements
- Performance optimizations
- New agent types
- Integration with other tools

---

## 🚀 Getting Started

### Step 1: Fork & Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/StegoCrew.git
cd StegoCrew
```

### Step 2: Set Up Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install system tools (optional)
sudo apt install steghide binwalk exiftool
```

### Step 3: Create a Branch

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Or a bugfix branch
git checkout -b fix/bug-description
```

### Step 4: Make Your Changes

- Write clear, documented code
- Follow existing code style
- Add tests if applicable
- Update documentation

### Step 5: Test Your Changes

```bash
# Test the examples
cd examples
python 01_first_agent.py
python 06_complete_stegocrew.py

# Run the test suite
cd ../tests
python test_challenges.py
python benchmark.py
```

### Step 6: Commit & Push

```bash
# Commit with clear message
git add .
git commit -m "Add feature: description of what you did"

# Push to your fork
git push origin feature/your-feature-name
```

### Step 7: Create Pull Request

1. Go to your fork on GitHub
2. Click "Pull Request"
3. Describe your changes
4. Submit!

---

## 📝 Contribution Guidelines

### Code Style

**Python:**
- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to all functions
- Include type hints where helpful

**Example:**
```python
from crewai_tools import tool

@tool
def my_new_tool(file_path: str, option: bool = False) -> str:
    """
    Brief description of what this tool does.

    Args:
        file_path: Path to the file to analyze
        option: Enable special processing (default: False)

    Returns:
        Analysis result as formatted string
    """
    try:
        # Implementation
        return "✅ Success"
    except Exception as e:
        return f"❌ Error: {str(e)}"
```

**Documentation:**
- Clear and concise
- Include examples
- Use proper markdown
- Check for typos

### Commit Messages

**Good commit messages:**
```
✅ Add zsteg tool for PNG LSB analysis
✅ Fix: Handle empty files in metadata extraction
✅ Docs: Clarify installation steps in Lesson 2
✅ Test: Add benchmark for string extraction
```

**Less helpful:**
```
❌ Update stuff
❌ Fix bug
❌ Changes
```

### Pull Request Guidelines

**Include in your PR:**
- Clear description of changes
- Reason for the change
- Testing performed
- Screenshots/demos (if UI changes)
- Reference to related issues

**PR Template:**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
Describe how you tested your changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests pass
- [ ] No breaking changes
```

---

## 🧪 Testing

### Run All Tests

```bash
# Create test challenges
cd test_files
python create_test_challenges.py

# Run challenge tests
cd ../tests
python test_challenges.py

# Run benchmarks
python benchmark.py
```

### Add New Tests

If adding new tools or features, add tests:

```python
# In tests/test_challenges.py
CHALLENGES.append({
    "name": "Your New Challenge",
    "file": "test_files/your_challenge.jpg",
    "expected_flag": "CTF{your_flag}",
    "difficulty": "Medium",
    "description": "Tests your new feature"
})
```

---

## 🎯 Good First Issues

New to the project? Start with these:

### Documentation
- Fix typos in lessons
- Improve code comments
- Add more examples to NEXT_STEPS.md

### Easy Enhancements
- Add new test challenges
- Improve error messages
- Add progress indicators

### Tool Additions
- Wrap new stego tools (zsteg, foremost, etc.)
- Add encoding decoders (ROT13, XOR, etc.)
- Improve existing tool output

---

## 🐛 Reporting Bugs

### Before Reporting

1. Check if issue already exists
2. Try with latest version
3. Test with minimal example

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Run command '...'
2. With file '...'
3. See error

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: Ubuntu 22.04
- Python: 3.10.5
- CrewAI: 0.28.0

**Error Message**
```
Paste full error here
```

**Additional Context**
Any other relevant information
```

---

## 💡 Feature Requests

Have an idea? We'd love to hear it!

### Feature Request Template

```markdown
**Problem**
What problem does this solve?

**Proposed Solution**
How would you implement it?

**Alternatives**
Any alternative approaches?

**Use Case**
Example of how this would be used
```

---

## 🏆 Recognition

Contributors will be:
- Added to CONTRIBUTORS.md (if we create one)
- Mentioned in release notes
- Credited in relevant documentation

---

## 📚 Resources

### Project Resources
- [README.md](README.md) - Project overview
- [LEARNING_GUIDE.md](LEARNING_GUIDE.md) - Course structure
- [NEXT_STEPS.md](NEXT_STEPS.md) - Future development ideas

### External Resources
- [CrewAI Documentation](https://docs.crewai.com/)
- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Git Commit Messages](https://chris.beams.io/posts/git-commit/)

---

## ❓ Questions?

- Open a [Discussion](../../discussions) for general questions
- Open an [Issue](../../issues) for bugs/features
- Check [existing issues](../../issues) first

---

## 🤝 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all.

### Our Standards

**Positive behavior:**
- Being respectful and inclusive
- Accepting constructive criticism
- Focusing on what's best for the community
- Showing empathy towards others

**Unacceptable behavior:**
- Harassment or discriminatory language
- Trolling or insulting comments
- Public or private harassment
- Publishing others' private information

### Enforcement

Report unacceptable behavior by opening an issue or contacting maintainers.

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).

---

**Thank you for contributing to StegoCrew! Together we can build something amazing! 🚀**
