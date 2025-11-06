# Lesson 7: Complete MVP Build

**Duration:** 4-6 hours
**Prerequisites:** Lessons 1-6 completed

---

## Building the Complete System

Complete working implementation: `examples/06_complete_stegocrew.py`

---

## Architecture

5 agents working sequentially:

```
Recon Agent → Stego Agent → Pattern Agent → Decoder Agent → Orchestrator
```

Each agent:
- Has specialized tools
- Receives context from previous agents
- Produces focused output for next agent

---

## Running It

```bash
python examples/06_complete_stegocrew.py test_file.jpg
```

---

## Production Structure

For larger projects, organize into `src/`:

```
src/
├── tools/      # Tool definitions
├── agents/     # Agent configurations
├── tasks/      # Task definitions
└── main.py     # Entry point
```

See `src/README.md` for details.

---

## Next Steps

You have a complete working system. Next: testing and deployment.

[Continue to Lesson 8: Testing & Deployment →](./LESSON_08.md)
