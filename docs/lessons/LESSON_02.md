# Lesson 2: Development Environment Setup

**Duration:** 1-2 hours
**Prerequisites:** Lesson 1 completed
**Goal:** Set up a complete working environment for building our CTF solver

---

## 🎯 What You'll Learn

By the end of this lesson, you'll have:
1. ✅ Python virtual environment configured
2. ✅ CrewAI and dependencies installed
3. ✅ System steganography tools installed
4. ✅ API keys configured
5. ✅ Project structure created
6. ✅ Test environment verified working

---

## 📋 Installation Checklist

```
[ ] Python 3.10+ installed
[ ] Virtual environment created
[ ] CrewAI installed
[ ] Python dependencies installed
[ ] System tools installed (steghide, binwalk, etc.)
[ ] API key configured
[ ] Project structure created
[ ] Test run successful
```

---

## Part 1: Python Environment Setup

### Step 1: Check Python Version

First, verify you have Python 3.10 or higher:

```bash
python --version
# or
python3 --version
```

**Expected output:** `Python 3.10.x` or higher

**If you don't have Python 3.10+:**
- **Ubuntu/Debian:** `sudo apt install python3.10 python3.10-venv`
- **Mac:** `brew install python@3.10`
- **Windows:** Download from https://python.org

---

### Step 2: Create Project Directory

```bash
# Navigate to where you want to create the project
cd ~/projects  # or wherever you keep projects

# Create project directory
mkdir ctf-stego-solver
cd ctf-stego-solver
```

---

### Step 3: Create Virtual Environment

A virtual environment isolates your project dependencies:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

**You should see `(venv)` at the start of your command prompt.**

**Why use a virtual environment?**
- Prevents conflicts between project dependencies
- Keeps your global Python clean
- Easy to reproduce on other machines
- Easy to delete and start fresh if needed

---

### Step 4: Upgrade pip

Always upgrade pip first:

```bash
pip install --upgrade pip
```

---

## Part 2: Install CrewAI and Python Dependencies

### Step 1: Install CrewAI

```bash
pip install crewai crewai-tools
```

This installs:
- `crewai` - The core framework
- `crewai-tools` - Pre-built tools for agents

**This might take a few minutes...**

---

### Step 2: Install Additional Python Libraries

Create a file called `requirements.txt`:

```bash
# Create requirements file
cat > requirements.txt << 'EOF'
# Core framework
crewai==0.41.1
crewai-tools==0.8.3

# LLM providers
anthropic==0.34.0
openai==1.40.0

# Image processing
Pillow==10.4.0
opencv-python==4.10.0.84
numpy==1.26.4

# Cryptography
pycryptodome==3.20.0

# File analysis
python-magic==0.4.27

# Audio processing (for future use)
pydub==0.25.1

# Utilities
requests==2.32.3
python-dotenv==1.0.1

# CLI improvements
rich==13.7.1
click==8.1.7
EOF
```

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

### Step 3: Verify Installation

Test that CrewAI is installed correctly:

```bash
python -c "import crewai; print(f'CrewAI version: {crewai.__version__}')"
```

**Expected output:** `CrewAI version: 0.41.1` (or similar)

---

## Part 3: Install System Steganography Tools

These are command-line tools that our agents will use.

### Linux (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install essential stego tools
sudo apt install -y \
    steghide \
    binwalk \
    exiftool \
    foremost \
    hexedit \
    xxd \
    file

# Install zsteg (Ruby gem)
sudo apt install -y ruby-full
sudo gem install zsteg
```

---

### macOS

```bash
# Install Homebrew if you don't have it
# /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install stego tools
brew install steghide
brew install binwalk
brew install exiftool
brew install foremost

# Install zsteg
gem install zsteg
```

---

### Windows

**Option 1: Use WSL2 (Recommended)**
1. Install WSL2: https://learn.microsoft.com/en-us/windows/wsl/install
2. Follow Linux instructions above

**Option 2: Native Windows**
- Download tools manually:
  - Steghide: http://steghide.sourceforge.net/
  - ExifTool: https://exiftool.org/
  - Binwalk: https://github.com/ReFirmLabs/binwalk

*Note: WSL2 is much easier for this project!*

---

### Verify Tool Installation

Test that tools are accessible:

```bash
# Test each tool
steghide --version
binwalk --help
exiftool -ver
foremost -V
zsteg --version
```

**Each should show version information without errors.**

---

## Part 4: API Key Configuration

Our agents need an LLM to "think." We'll use Anthropic Claude (recommended).

### Step 1: Get an API Key

**Anthropic Claude (Recommended):**
1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to "API Keys"
4. Create a new key
5. Copy it (keep it secret!)

**Pricing:** Claude Sonnet costs ~$3 per million input tokens (very affordable for learning)

**Alternative - OpenAI:**
1. Go to https://platform.openai.com/
2. Create API key
3. Note: GPT-4 is more expensive

---

### Step 2: Create .env File

Create a `.env` file in your project root:

```bash
cat > .env << 'EOF'
# Anthropic Claude API Key
ANTHROPIC_API_KEY=your_key_here

# Alternative: OpenAI
# OPENAI_API_KEY=your_key_here

# Model selection
DEFAULT_MODEL=claude-3-5-sonnet-20241022

# Project settings
PROJECT_NAME=CTF-Stego-Solver
VERBOSE=True
EOF
```

**Replace `your_key_here` with your actual API key!**

---

### Step 3: Secure Your .env File

**Important:** Never commit API keys to git!

```bash
# Create .gitignore
cat > .gitignore << 'EOF'
# Environment files
.env
*.env

# Virtual environment
venv/
.venv/

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# IDE
.vscode/
.idea/
*.swp

# Outputs
*.log
outputs/
test_files/
*.png
*.jpg
*.wav

# OS
.DS_Store
Thumbs.db
EOF
```

---

## Part 5: Create Project Structure

Let's create the directory structure for our project:

```bash
# Create directory structure
mkdir -p src/{agents,tools,tasks,crew,utils}
mkdir -p tests/sample_challenges
mkdir -p outputs
mkdir -p docs/notes

# Create __init__.py files for Python packages
touch src/__init__.py
touch src/agents/__init__.py
touch src/tools/__init__.py
touch src/tasks/__init__.py
touch src/crew/__init__.py
touch src/utils/__init__.py
```

**Your structure should now look like:**

```
ctf-stego-solver/
├── venv/                    # Virtual environment
├── src/
│   ├── __init__.py
│   ├── agents/             # Agent definitions
│   │   └── __init__.py
│   ├── tools/              # Custom tools
│   │   └── __init__.py
│   ├── tasks/              # Task definitions
│   │   └── __init__.py
│   ├── crew/               # Crew configuration
│   │   └── __init__.py
│   └── utils/              # Helper functions
│       └── __init__.py
├── tests/
│   └── sample_challenges/  # Test CTF files
├── outputs/                # Generated reports
├── docs/
│   └── notes/              # Your learning notes
├── .env                    # API keys (secret!)
├── .gitignore              # Git ignore rules
└── requirements.txt        # Python dependencies
```

---

## Part 6: Verify Everything Works

Let's create a simple test script to verify your setup:

```bash
cat > test_setup.py << 'EOF'
#!/usr/bin/env python3
"""
Setup verification script.
Tests that all dependencies and tools are properly installed.
"""

import sys
import subprocess
from pathlib import Path

def test_python_version():
    """Check Python version."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print("✅ Python version:", f"{version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print("❌ Python 3.10+ required")
        return False

def test_import(module_name):
    """Test if a Python module can be imported."""
    try:
        __import__(module_name)
        print(f"✅ {module_name} imported successfully")
        return True
    except ImportError:
        print(f"❌ {module_name} not found")
        return False

def test_system_tool(tool_name):
    """Test if a system tool is available."""
    try:
        result = subprocess.run(
            [tool_name, '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✅ {tool_name} is available")
            return True
        else:
            print(f"⚠️  {tool_name} found but returned error")
            return False
    except FileNotFoundError:
        print(f"❌ {tool_name} not found")
        return False
    except subprocess.TimeoutExpired:
        print(f"⚠️  {tool_name} timeout")
        return False
    except Exception as e:
        print(f"❌ {tool_name} error: {e}")
        return False

def test_env_file():
    """Check if .env file exists."""
    if Path('.env').exists():
        print("✅ .env file found")
        return True
    else:
        print("❌ .env file not found")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing CTF Stego Solver Setup\n")
    print("=" * 50)

    results = []

    # Test Python
    print("\n📦 Python Environment:")
    results.append(test_python_version())

    # Test Python packages
    print("\n📚 Python Packages:")
    packages = ['crewai', 'anthropic', 'PIL', 'numpy', 'dotenv']
    for package in packages:
        results.append(test_import(package))

    # Test system tools
    print("\n🔧 System Tools:")
    tools = ['steghide', 'binwalk', 'exiftool']
    for tool in tools:
        results.append(test_system_tool(tool))

    # Test config
    print("\n⚙️  Configuration:")
    results.append(test_env_file())

    # Summary
    print("\n" + "=" * 50)
    passed = sum(results)
    total = len(results)

    if passed == total:
        print(f"✅ All tests passed! ({passed}/{total})")
        print("\n🎉 You're ready to start building!")
        return 0
    else:
        print(f"⚠️  Some tests failed ({passed}/{total} passed)")
        print("\n📝 Please fix the issues above and try again.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
EOF

# Make it executable
chmod +x test_setup.py
```

---

### Run the Test

```bash
python test_setup.py
```

**Expected output:**

```
🧪 Testing CTF Stego Solver Setup

==================================================

📦 Python Environment:
✅ Python version: 3.10.12

📚 Python Packages:
✅ crewai imported successfully
✅ anthropic imported successfully
✅ PIL imported successfully
✅ numpy imported successfully
✅ dotenv imported successfully

🔧 System Tools:
✅ steghide is available
✅ binwalk is available
✅ exiftool is available

⚙️  Configuration:
✅ .env file found

==================================================
✅ All tests passed! (10/10)

🎉 You're ready to start building!
```

**If you see all ✅ checkmarks, you're ready to proceed!**

---

## Part 7: Create a Simple Test

Let's verify that CrewAI can actually connect to the LLM:

```bash
cat > test_llm.py << 'EOF'
#!/usr/bin/env python3
"""
Test LLM connection.
Verifies that the API key works and we can communicate with Claude.
"""

import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

# Load environment variables
load_dotenv()

def test_claude_connection():
    """Test connection to Claude API."""

    # Get API key
    api_key = os.getenv('ANTHROPIC_API_KEY')

    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found in .env file")
        return False

    if api_key == 'your_key_here':
        print("❌ Please replace 'your_key_here' with your actual API key in .env")
        return False

    print("🧪 Testing connection to Claude...\n")

    try:
        # Initialize Claude
        llm = ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            anthropic_api_key=api_key,
            temperature=0
        )

        # Send test message
        response = llm.invoke("Say 'Hello! I'm ready to help with CTF challenges!' and nothing else.")

        print("✅ Connection successful!")
        print(f"\n📝 Response from Claude:\n{response.content}\n")

        return True

    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == '__main__':
    success = test_claude_connection()

    if success:
        print("🎉 LLM connection verified! You're all set!")
        exit(0)
    else:
        print("\n📝 Please check your API key and try again.")
        exit(1)
EOF

chmod +x test_llm.py
```

Run the LLM test:

```bash
python test_llm.py
```

**Expected output:**

```
🧪 Testing connection to Claude...

✅ Connection successful!

📝 Response from Claude:
Hello! I'm ready to help with CTF challenges!

🎉 LLM connection verified! You're all set!
```

---

## Part 8: Optional - Create Development Helpers

### Helper Script: Activate Environment

```bash
cat > activate.sh << 'EOF'
#!/bin/bash
# Quick activation script
source venv/bin/activate
echo "✅ Virtual environment activated"
echo "📁 Project: $(pwd)"
echo "🐍 Python: $(python --version)"
EOF

chmod +x activate.sh
```

Usage: `source activate.sh`

---

### Helper Script: Run Tests

```bash
cat > run_tests.sh << 'EOF'
#!/bin/bash
# Run all verification tests
set -e

echo "🧪 Running setup verification..."
python test_setup.py

echo ""
echo "🧪 Testing LLM connection..."
python test_llm.py

echo ""
echo "✅ All tests passed!"
EOF

chmod +x run_tests.sh
```

---

## 🎓 Summary: What You've Accomplished

Congratulations! Your development environment is now fully configured:

✅ **Python Environment**
- Virtual environment created and activated
- All Python dependencies installed
- CrewAI framework ready to use

✅ **System Tools**
- Steganography tools installed
- Command-line utilities available
- Tools verified and working

✅ **Configuration**
- API key configured
- Environment variables set
- Security measures in place (.gitignore)

✅ **Project Structure**
- Clean directory organization
- Python packages initialized
- Ready for development

✅ **Verification**
- All dependencies tested
- LLM connection confirmed
- Ready to build!

---

## 🚀 What's Next?

Now that your environment is set up, you're ready to **build your first agent!**

**Next lesson:** [Lesson 3: Your First CrewAI Agent (Hello World)](./LESSON_03.md)

In the next lesson, we'll:
1. Create a simple agent from scratch
2. Give it a basic tool to use
3. Run your first agent task
4. Understand how it all works

---

## 🐛 Troubleshooting

### Common Issues

**Issue: `pip install crewai` fails**
- Solution: Upgrade pip: `pip install --upgrade pip`
- Try: `pip install crewai --no-cache-dir`

**Issue: `steghide: command not found`**
- Solution: Reinstall: `sudo apt install steghide`
- Check PATH: `which steghide`

**Issue: API key not working**
- Verify key is correct in `.env`
- Check you're using the right variable name: `ANTHROPIC_API_KEY`
- Ensure no extra spaces: `ANTHROPIC_API_KEY=sk-ant-...` (no spaces around =)

**Issue: Import errors**
- Verify venv is activated: `which python` should show path with `venv`
- Reinstall in venv: `pip install -r requirements.txt`

**Issue: Python version too old**
- Install Python 3.10+
- Create venv with: `python3.10 -m venv venv`

---

## 📝 Quick Reference

### Activate Virtual Environment
```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Verify Setup
```bash
python test_setup.py
python test_llm.py
```

### Deactivate Virtual Environment
```bash
deactivate
```

---

**🎉 Great job completing Lesson 2!**

Your environment is now ready. Take a break, then dive into Lesson 3 where we'll write actual agent code!

---

*Questions? Review the [GLOSSARY](../GLOSSARY.md) or ask your mentor!*

*Previous: [Lesson 1 - Understanding Multi-Agent Systems](./LESSON_01.md)*
*Next: [Lesson 3 - Your First Agent](./LESSON_03.md)*
