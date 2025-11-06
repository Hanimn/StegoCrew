# Lesson 8: Testing & Deployment

**Duration:** 2-3 hours
**Prerequisites:** Lessons 1-7 completed

---

## Testing

**Test suite location:** `tests/`

- `test_challenges.py` - Run against known challenges
- `benchmark.py` - Performance testing
- `create_test_challenges.py` - Generate test CTF files

Run tests:
```bash
cd tests
python test_challenges.py
```

---

## Deployment

**Local use:**
Just run the Python scripts.

**Docker:**
```bash
docker build -t stegocrew .
docker run -v $(pwd)/challenges:/challenges stegocrew /challenges/file.jpg
```

**Web API:**
See NEXT_STEPS.md for Flask example.

---

## Performance

Current bottlenecks:
- LLM API calls (2-5s each)
- Sequential processing
- Large file analysis

Optimization ideas in NEXT_STEPS.md.

---

## Course Complete

You've built a complete multi-agent CTF solver.

**What you learned:**
- Multi-agent coordination
- Tool integration patterns
- Context sharing
- Production architecture

**Apply these patterns to:**
- Research assistants
- Code review systems
- Content creation
- Data analysis

See NEXT_STEPS.md for where to go from here.

---

**Now go solve some CTFs.**
