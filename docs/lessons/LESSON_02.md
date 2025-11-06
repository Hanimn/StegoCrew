# Lesson 2: Development Environment Setup

**Duration:** 1-2 hours
**Prerequisites:** Lesson 1 completed

---

## Setup Overview

This part is tedious but necessary. Get it right once and you're set for the entire project.

We'll install:
- Python 3.10+ and virtual environment
- CrewAI framework
- Steganography tools (steghide, binwalk, exiftool)
- API key configuration

---

## Python Environment

**Check your Python version:**

```bash
python3 --version
```

Need Python 3.10 or higher. If not:
- Ubuntu/Debian: `sudo apt install python3.10 python3.10-venv`
- Mac: `brew install python@3.10`
- Windows: Download from python.org or use WSL2

**Create project and virtual environment:**

```bash
mkdir ctf-stego-solver
cd ctf-stego-solver

python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

You should see `(venv)` in your prompt. If not, the activation didn't work.

**Upgrade pip:**

```bash
pip install --upgrade pip
```

---

## Install CrewAI and Dependencies

Create `requirements.txt`:

```txt
# Core framework
crewai>=0.28.0
crewai-tools>=0.1.0

# LLM providers
langchain-anthropic>=0.1.0
python-dotenv>=1.0.0

# Optional: image processing
Pillow>=10.0.0
```

Install everything:

```bash
pip install -r requirements.txt
```

This takes a few minutes. CrewAI pulls in many dependencies.

**Verify installation:**

```bash
python -c "import crewai; print(crewai.__version__)"
```

Should print version number without errors.

---

## Install Steganography Tools

These are system tools, not Python packages.

**Linux (Ubuntu/Debian):**

```bash
sudo apt update
sudo apt install -y steghide binwalk exiftool foremost hexedit
```

**For zsteg (Ruby-based):**

```bash
sudo apt install -y ruby-full
sudo gem install zsteg
```

**macOS:**

```bash
brew install steghide binwalk exiftool foremost
gem install zsteg
```

**Windows:**

Use WSL2. Seriously. Native Windows installation for these tools is painful.

1. Install WSL2: https://learn.microsoft.com/en-us/windows/wsl/install
2. Follow Linux instructions above

**Verify tools work:**

```bash
steghide --version
binwalk --help
exiftool -ver
zsteg --version
```

Each should respond without "command not found" errors.

---

## Troubleshooting: Steghide Issues (Common)

**Problem:** steghide installs but gives linking errors when running.

This happened to me on Ubuntu 22.04. steghide has old dependencies.

**Fix:**

```bash
sudo apt install -y libjpeg62 libmhash2
```

If that doesn't work, try installing from source or use Docker (covered later).

**Problem:** zsteg not found after `gem install`

Ruby gems install to user directory, may not be in PATH.

**Fix:**

```bash
# Find where it installed
gem environment

# Add to PATH (in ~/.bashrc or ~/.zshrc)
export PATH="$HOME/.local/share/gem/ruby/3.0.0/bin:$PATH"

# Reload shell
source ~/.bashrc
```

---

## API Key Configuration

You need an LLM for agents to "think." Anthropic Claude is recommended.

**Get Claude API key:**

1. Go to https://console.anthropic.com/
2. Sign up (free tier available)
3. Navigate to API Keys
4. Create new key
5. Copy it

**Pricing:** Claude Sonnet costs ~$3 per million input tokens. For learning/testing, you'll spend a few dollars max.

Alternative: OpenAI GPT-4 works too, but costs more.

**Create `.env` file:**

```bash
# In project root
cat > .env << 'EOF'
ANTHROPIC_API_KEY=your_actual_key_here
DEFAULT_MODEL=claude-3-5-sonnet-20241022
VERBOSE=True
EOF
```

Replace `your_actual_key_here` with your real key.

**Secure it:**

```bash
cat > .gitignore << 'EOF'
.env
*.env
venv/
__pycache__/
*.pyc
.vscode/
.idea/
*.log
*.extracted
EOF
```

**Critical:** Never commit `.env` to git. Your API key = your money.

---

## Troubleshooting: API Key Issues

**Problem:** "Invalid API key" error even though key is correct.

Check for hidden spaces:
```bash
# Wrong (space after =)
ANTHROPIC_API_KEY= sk-ant-xxxxx

# Right (no space)
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

Also verify the key starts with `sk-ant-` for Anthropic.

**Problem:** python-dotenv not loading `.env`

Make sure `.env` is in the same directory where you run python, or use absolute path:

```python
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
```

---

## Project Structure

Create directories:

```bash
mkdir -p src/{agents,tools,tasks,utils}
mkdir -p tests examples outputs

touch src/__init__.py
touch src/agents/__init__.py
touch src/tools/__init__.py
touch src/tasks/__init__.py
touch src/utils/__init__.py
```

Final structure:

```
ctf-stego-solver/
├── venv/
├── src/
│   ├── agents/
│   ├── tools/
│   ├── tasks/
│   └── utils/
├── tests/
├── examples/
├── outputs/
├── .env
├── .gitignore
└── requirements.txt
```

---

## Verify Everything Works

Create `test_setup.py`:

```python
#!/usr/bin/env python3
import sys
import subprocess
from pathlib import Path

def check_tool(name):
    try:
        subprocess.run([name, '--version'], capture_output=True, timeout=5)
        print(f"✓ {name}")
        return True
    except FileNotFoundError:
        print(f"✗ {name} not found")
        return False

def main():
    print("Checking setup...\n")

    results = []

    # Python packages
    print("Python packages:")
    for pkg in ['crewai', 'anthropic', 'dotenv']:
        try:
            __import__(pkg)
            print(f"✓ {pkg}")
            results.append(True)
        except ImportError:
            print(f"✗ {pkg}")
            results.append(False)

    # System tools
    print("\nSystem tools:")
    for tool in ['steghide', 'binwalk', 'exiftool']:
        results.append(check_tool(tool))

    # Config
    print("\nConfiguration:")
    if Path('.env').exists():
        print("✓ .env file")
        results.append(True)
    else:
        print("✗ .env file missing")
        results.append(False)

    print(f"\n{sum(results)}/{len(results)} checks passed")

    if all(results):
        print("Ready to proceed!")
        return 0
    else:
        print("Fix issues above before continuing")
        return 1

if __name__ == '__main__':
    sys.exit(main())
```

Run it:

```bash
chmod +x test_setup.py
python test_setup.py
```

Should see all checkmarks.

---

## Test LLM Connection

Create `test_llm.py`:

```python
#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

load_dotenv()

api_key = os.getenv('ANTHROPIC_API_KEY')

if not api_key or api_key == 'your_actual_key_here':
    print("Set your API key in .env first")
    exit(1)

try:
    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        anthropic_api_key=api_key
    )

    response = llm.invoke("Say 'Hello' and nothing else.")
    print(f"Response: {response.content}")
    print("\nLLM connection works!")

except Exception as e:
    print(f"Error: {e}")
    exit(1)
```

Run it:

```bash
chmod +x test_llm.py
python test_llm.py
```

Should get response from Claude.

---

## Common Setup Mistakes

**Mistake 1: Not activating virtual environment**

Symptom: `crewai` works in one terminal, not another.

Cause: Forgot to run `source venv/bin/activate`.

Always activate before working. I add this to my shell prompt to remind me.

**Mistake 2: Running Python 3.9 or older**

Symptom: Import errors with typing or other weird errors.

Cause: CrewAI needs 3.10+.

Check: `python --version` inside activated venv should show 3.10+.

**Mistake 3: Installing tools globally instead of in venv**

Symptom: Works on your machine, breaks when someone else tries it.

Cause: Installed crewai with `sudo pip install` (don't do this).

Always use venv, never sudo pip for project dependencies.

**Mistake 4: API key in code**

Don't do this:
```python
llm = ChatAnthropic(api_key="sk-ant-hardcoded-key")  # WRONG
```

Do this:
```python
api_key = os.getenv('ANTHROPIC_API_KEY')  # RIGHT
llm = ChatAnthropic(api_key=api_key)
```

---

## Quick Reference

**Activate venv:**
```bash
source venv/bin/activate
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Verify setup:**
```bash
python test_setup.py
python test_llm.py
```

**Deactivate:**
```bash
deactivate
```

---

## Next Steps

Setup complete. Now the fun part - writing actual agent code.

[Continue to Lesson 3: Your First Agent →](./LESSON_03.md)

---

*Note: If you hit issues not covered here, check tool versions. steghide in particular has compatibility issues on newer systems. Docker setup in Lesson 8 addresses this.*
