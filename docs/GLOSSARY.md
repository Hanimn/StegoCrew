# 📖 Glossary - AI Agent & CTF Terms

This glossary explains all the technical terms you'll encounter in this project.

---

## AI & Agent Terms

### Agent
An AI-powered entity that can:
- **Reason** about problems
- **Use tools** to accomplish tasks
- **Make decisions** based on context
- **Communicate** with other agents

**Simple analogy:** Like a virtual employee with a specific job role.

### Multi-Agent System
Multiple agents working together, each with specialized roles.

**Example:** A hospital has doctors, nurses, and technicians working together - each with expertise.

### CrewAI
A Python framework for building multi-agent systems. Handles:
- Agent creation
- Tool integration
- Task coordination
- Communication between agents

**Website:** https://www.crewai.com/

### LLM (Large Language Model)
The "brain" that powers each agent. Examples:
- Claude (Anthropic) ← Recommended for this project
- GPT-4 (OpenAI)
- Llama (Meta)

### Tool
A capability an agent can use. Examples:
- Running shell commands
- Reading files
- Calling APIs
- Executing Python functions

**Code example:**
```python
from crewai_tools import tool

@tool
def calculate_sum(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b
```

### Task
A goal assigned to an agent. Example:
- "Analyze this image for hidden data"
- "Extract all metadata from the file"
- "Decode this Base64 string"

### Crew
A team of agents working together on related tasks.

**Structure:**
```
Crew = Agents + Tasks + Process
```

### Process
How the crew coordinates work:
- **Sequential:** One agent at a time (A → B → C)
- **Hierarchical:** Manager assigns tasks
- **Parallel:** Multiple agents work simultaneously

### Prompt Engineering
Crafting instructions for AI agents. Good prompts are:
- **Clear:** Specific about what to do
- **Contextual:** Provide background information
- **Actionable:** Define concrete steps

### Context
Information shared between agents. Includes:
- Previous agent findings
- Original input data
- Intermediate results

---

## Steganography Terms

### Steganography (Stego)
The practice of hiding data inside other data.

**Example:** Hiding a text message inside an image file.

**Etymology:** Greek - "steganos" (covered) + "graphein" (writing)

### LSB (Least Significant Bit)
A common steganography technique hiding data in image pixels.

**How it works:**
```
Original pixel: RGB(255, 128, 64)
Binary:         11111111, 10000000, 01000000
                       ↑        ↑        ↑
Change last bit:    11111110, 10000001, 01000001
New pixel:      RGB(254, 129, 65) ← Looks identical!
```

### Metadata
Information about a file (not the file content itself):
- Creator name
- Creation date
- GPS coordinates (photos)
- Software used
- Comments/descriptions

**Tool to extract:** `exiftool`

### Entropy
A measure of randomness/complexity in data:
- **Low entropy:** Predictable patterns (text files)
- **High entropy:** Random-looking (encrypted/compressed)

**Why it matters:** Hidden data often increases entropy.

### File Carving
Extracting embedded files from within other files.

**Example:** A ZIP file hidden inside a PNG image.

**Tools:** binwalk, foremost

### Steghide
A popular tool for hiding data in images/audio with password protection.

**Usage:**
```bash
# Hide data
steghide embed -cf image.jpg -ef secret.txt -p password

# Extract data
steghide extract -sf image.jpg -p password
```

### Bit Plane
Images are made of bit layers. Higher bits = more visual importance.

**Example (8-bit image):**
```
Bit 7 (MSB): Major visual information
Bit 6:       Visual details
...
Bit 1:       Subtle details
Bit 0 (LSB): Invisible changes ← Great for hiding data!
```

### Spectrogram
Visual representation of audio frequencies over time. Data can be hidden as visual patterns.

**Famous example:** Aphex Twin's face hidden in song spectrogram.

---

## CTF Terms

### CTF (Capture The Flag)
A cybersecurity competition where participants solve challenges to find "flags."

**Types:**
- **Jeopardy:** Individual challenges in categories
- **Attack-Defense:** Teams defend servers while attacking others
- **Mixed:** Combination of both

### Flag
The target string to find, usually in format:
- `CTF{...}`
- `flag{...}`
- `HTB{...}` (HackTheBox)

**Example:** `CTF{h1dd3n_1n_pl41n_s1ght}`

### Challenge Categories
- **Stego:** Hidden data (our focus!)
- **Crypto:** Encryption/decoding
- **Forensics:** File analysis
- **Web:** Website vulnerabilities
- **Pwn:** Binary exploitation
- **Reversing:** Reverse engineering

### Writeup
A detailed explanation of how a challenge was solved.

**Purpose:** Learning and sharing knowledge.

---

## Python & Development Terms

### Virtual Environment (venv)
An isolated Python environment for a project.

**Why use it:**
- Prevents dependency conflicts
- Easy to recreate on another machine
- Keeps global Python clean

**Commands:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Dependency
An external library your project needs.

**Example:** `crewai`, `Pillow`, `numpy`

**Managed by:** `requirements.txt` or `pyproject.toml`

### API (Application Programming Interface)
A way for programs to communicate.

**In our project:** Agents use LLM APIs (Claude, OpenAI) to think and reason.

### Environment Variable
A configuration value stored outside code.

**Example:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

**Why:** Keeps secrets out of code (security!)

### Wrapper
Code that simplifies using a complex tool.

**Example:**
```python
# Instead of this:
subprocess.run(['steghide', 'extract', '-sf', 'image.jpg'])

# We create a wrapper:
def extract_steghide(image_path):
    """Simple wrapper for steghide extraction"""
    # Handle errors, parse output, return clean results
```

---

## File Format Terms

### PNG (Portable Network Graphics)
Lossless image format supporting transparency.

**Stego relevance:** Predictable structure makes analysis easier.

### JPEG (Joint Photographic Experts Group)
Lossy image compression format.

**Stego relevance:** Can hide data in DCT coefficients.

### WAV (Waveform Audio File Format)
Uncompressed audio format.

**Stego relevance:** Can hide data in LSBs or as spectrograms.

### ZIP Archive
Compressed file container.

**Stego trick:** Can be appended to images (polyglot files).

---

## Command Line Tools

### exiftool
Swiss-army knife for metadata extraction.

**Usage:** `exiftool suspicious.jpg`

### binwalk
Analyzes and extracts embedded files.

**Usage:** `binwalk suspicious.png`

### strings
Extracts human-readable text from binary files.

**Usage:** `strings suspicious.jpg | grep flag`

### file
Identifies file types.

**Usage:** `file suspicious.png`

### hexdump / xxd
Views file contents in hexadecimal.

**Usage:** `xxd suspicious.png | head`

---

## Terms to Remember

| Term | Simple Definition |
|------|-------------------|
| **Agent** | AI worker with a specific role |
| **Tool** | Capability an agent can use |
| **Crew** | Team of agents working together |
| **Stego** | Hiding data inside other data |
| **LSB** | Hiding data in image pixels |
| **Flag** | The target string to find |
| **Metadata** | Information about a file |
| **Wrapper** | Simplified interface for complex tool |

---

**💡 Pro tip:** Bookmark this page and refer back whenever you encounter unfamiliar terms!

*[Back to Learning Guide](../LEARNING_GUIDE.md)*
