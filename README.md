<div align="center">
  <img src="assets/logo.png" alt="StegoCrew Logo" width="400"/>

  # StegoCrew

  ### Multi-Agent CTF Steganography Solver

  > Learn CrewAI by building a real-world CTF challenge solver

  [![GitHub](https://img.shields.io/badge/GitHub-StegoCrew-blue?logo=github)](https://github.com/Hanimn/StegoCrew)
  [![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
  [![CrewAI](https://img.shields.io/badge/CrewAI-Powered-orange)](https://crewai.com)
  [![License](https://img.shields.io/badge/License-Educational-green)](LICENSE)
</div>

---

## Why This Project Exists

I got tired of manually running steghide, binwalk, exiftool, and strings on every CTF challenge. After spending an hour on a challenge that turned out to be basic LSB steganography, I realized this workflow could be automated.

But instead of writing a bash script, I used this as an opportunity to learn CrewAI and multi-agent systems. This project is both a functional CTF solver and a complete learning resource for anyone wanting to understand how AI agents work together.

If you're new to CrewAI or multi-agent systems, this is a practical way to learn. If you're a CTF player, you'll get a tool that actually works.

---

## What You're Building

A 5-agent system that automatically analyzes suspicious files and extracts hidden data:

```
Suspicious File → [AI Agent Team] → Solution + Flag
```

**Agent Team:**
- **Reconnaissance Agent** - File analysis and metadata extraction
- **Steganography Expert** - Runs steghide, binwalk, zsteg, etc.
- **Pattern Hunter** - Detects encodings, patterns, anomalies
- **Decoder Agent** - Base64, hex, ROT13, XOR decoding
- **Orchestrator** - Coordinates results and generates reports

Each agent specializes in one aspect of the challenge, then shares findings with the team. Sequential workflow ensures agents build on each other's discoveries.

---

## Course Structure

8 lessons taking you from zero to a complete working system:

| Lesson | Topic | Time | Status |
|--------|-------|------|--------|
| [Lesson 1](./docs/lessons/LESSON_01.md) | Multi-Agent Systems Concepts | 1-2h | Ready |
| [Lesson 2](./docs/lessons/LESSON_02.md) | Environment Setup | 1-2h | Ready |
| [Lesson 3](./docs/lessons/LESSON_03.md) | Your First Agent | 2-3h | Ready |
| [Lesson 4](./docs/lessons/LESSON_04.md) | Custom Tools | 2-3h | Ready |
| [Lesson 5](./docs/lessons/LESSON_05.md) | Multi-Agent Coordination | 3-4h | Ready |
| [Lesson 6](./docs/lessons/LESSON_06.md) | Steganography Tools Integration | 3-4h | Ready |
| [Lesson 7](./docs/lessons/LESSON_07.md) | Complete MVP Build | 4-6h | Ready |
| [Lesson 8](./docs/lessons/LESSON_08.md) | Testing & Deployment | 2-3h | Ready |

**Total time:** 2-3 weeks part-time, 1 week full-time

Start here: **[LEARNING_GUIDE.md](./LEARNING_GUIDE.md)**

---

## Prerequisites

**You need:**
- Basic Python (functions, classes, imports)
- Command line basics
- Text editor or IDE

**You don't need:**
- ML/AI experience
- Advanced Python
- Prior CrewAI knowledge
- CTF expertise

If you can write a Python function, you're ready.

---

## Tech Stack & Tool Choices

**Why CrewAI?**

I evaluated AutoGPT, LangGraph, and CrewAI. CrewAI won because:
- Clean API for defining agents and tasks
- Built-in context sharing between agents
- Good tool integration patterns
- Active development and community

LangGraph offers more control but has a steeper learning curve. AutoGPT felt too opinionated for this use case.

**Why Claude over GPT-4?**

After testing both extensively:
- Claude handles tool-calling more reliably (in my experience)
- Better at following complex instructions
- Cheaper for development/testing

GPT-4 is faster but I hit more tool-calling errors. Your results may vary - the code works with both.

**Steganography Tools:**
- steghide - Password-protected embedding
- binwalk - File carving and analysis
- exiftool - Metadata extraction
- zsteg - PNG/BMP LSB analysis
- strings - Basic text extraction

All wrapped as CrewAI tools with proper error handling.

---

## Project Structure

```
StegoCrew/
├── README.md                    ← You are here
├── LEARNING_GUIDE.md           ← Start here
├── requirements.txt            ← Dependencies
│
├── docs/
│   ├── GLOSSARY.md             ← Terms explained
│   └── lessons/
│       ├── LESSON_01.md        ← Concepts
│       ├── LESSON_02.md        ← Setup
│       └── ...                 ← More lessons
│
├── examples/
│   ├── 01_first_agent.py       ← Hello World agent
│   ├── 02_first_tool.py        ← Custom tools
│   ├── ...
│   └── 06_complete_stegocrew.py ← Full system
│
├── tests/
│   ├── test_challenges.py      ← Challenge tests
│   └── benchmark.py            ← Performance tests
│
└── src/                        ← Production structure
    ├── agents/
    ├── tools/
    ├── tasks/
    └── main.py
```

---

## Quick Start

1. Clone the repo
2. Read [LEARNING_GUIDE.md](./LEARNING_GUIDE.md)
3. Start with [Lesson 1](./docs/lessons/LESSON_01.md)
4. Work through each lesson sequentially
5. Run the examples
6. Build the complete system

Each lesson has:
- Concepts explained
- Working code examples
- Practice exercises
- Troubleshooting tips

---

## What You'll Learn

**Multi-Agent Systems:**
- How agents communicate and share context
- Task delegation and workflow design
- Tool integration patterns
- Error handling across agents

**CrewAI Specifics:**
- Agent configuration (role, goal, backstory)
- Tool wrapping and @tool decorator
- Task creation and context chains
- Sequential vs. hierarchical workflows

**Practical Skills:**
- Integrating system tools with AI agents
- Building modular, maintainable agent systems
- Testing and debugging multi-agent workflows
- Real-world CTF steganography techniques

---

## Success Rate & Limitations

**What this solves well:**
- Basic steganography (LSB, file embedding, metadata)
- Common CTF challenge formats
- Standard encoding schemes
- Password-protected steghide (with wordlist)

**What it struggles with:**
- Advanced cryptography (that's not the goal)
- Custom/exotic steganography methods
- Challenges requiring domain-specific knowledge
- Highly obfuscated data

Expected success rate on beginner-intermediate CTF stego challenges: 60-80%

---

## After This Course

Once you complete the project, you can:

**Extend StegoCrew:**
- Add audio steganography (LSB in WAV files)
- Implement password brute-forcing
- Add machine learning for anomaly detection
- Build a web interface

**Build Other Systems:**
- Research assistants
- Code review agents
- Content creation pipelines
- Data analysis teams

The patterns you learn here transfer to any multi-agent system.

---

## Getting Help

**Documentation:**
- [LEARNING_GUIDE.md](./LEARNING_GUIDE.md) - Course roadmap
- [GLOSSARY.md](./docs/GLOSSARY.md) - Term definitions
- Lesson files - Step-by-step guides
- Code examples - Reference implementations

**Troubleshooting:**
- Check the glossary first
- Review previous lessons
- Run provided examples to verify setup
- Lesson 2 has common setup issues covered

---

## Contributing

Found a bug? Have an improvement? Contributions welcome.

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

Common contributions:
- New steganography tool integrations
- Additional test challenges
- Documentation improvements
- Bug fixes

---

## License & Responsible Use

Educational project licensed under MIT. See [LICENSE](./LICENSE).

Use this for:
- Learning CTF techniques
- Authorized CTF competitions
- Educational demonstrations
- Personal skill development

Don't use for unauthorized access to systems or malicious purposes.

---

## Credits

- CrewAI team for the framework
- CTF community for technique documentation
- Steganography tool developers

---

**Ready to start?** → [LEARNING_GUIDE.md](./LEARNING_GUIDE.md)

*Last Updated: 2025-11-06*
