# StegoCrew Testing Suite

Testing utilities for the StegoCrew multi-agent CTF solver.

## 🧪 Test Files

### test_challenges.py

**Run CTF Challenge Tests:**

```bash
cd tests
python test_challenges.py
```

**What it does:**
- Tests StegoCrew with predefined CTF challenges
- Verifies flags are correctly found
- Generates success rate statistics

**Test Challenges:**
1. **Metadata Flag** (Easy) - Flag in EXIF data
2. **Steghide No Password** (Easy) - Steghide extraction
3. **Embedded Archive** (Medium) - Binwalk detection
4. **Simple Strings** (Beginner) - Flag in plaintext

**Prerequisites:**
- Create test challenges first: `cd ../test_files && python create_test_challenges.py`

### benchmark.py

**Run Performance Benchmarks:**

```bash
cd tests
python benchmark.py
```

**What it measures:**
- File analysis speed
- String extraction performance
- Metadata extraction timing
- Average operation times

**Use for:**
- Identifying performance bottlenecks
- Comparing before/after optimizations
- Setting performance baselines

## 📊 Expected Results

### Test Success Criteria

**Passing Tests:**
```
✅ SUCCESS: Found flag CTF{...}
```

**Test Summary:**
```
📊 TEST SUMMARY
Total Challenges: 4
✅ Passed: 4
❌ Failed: 0
⚠️  Skipped: 0

🎯 Success Rate: 100.0%
```

### Benchmark Baselines

**Typical Performance (may vary):**
- File analysis: ~0.01-0.05s
- String extraction: ~0.001-0.01s
- Metadata extraction: ~0.1-0.5s

## 🔧 Troubleshooting

### Tests Skipped

**Problem:** Tests show as "SKIP: File not found"

**Solution:**
```bash
cd ../test_files
python create_test_challenges.py
cd ../tests
python test_challenges.py
```

### Tests Failing

**Problem:** Expected flag not found

**Debugging steps:**
1. Run the challenge manually:
   ```bash
   cd ../examples
   python 06_complete_stegocrew.py ../test_files/challenge_metadata.jpg
   ```

2. Check if tools are installed:
   ```bash
   which steghide binwalk exiftool
   ```

3. Verify challenge file exists and is valid:
   ```bash
   file ../test_files/challenge_metadata.jpg
   exiftool ../test_files/challenge_metadata.jpg | grep CTF
   ```

### Slow Performance

**If benchmarks show slow performance:**

1. Check system resources (CPU, memory)
2. Reduce concurrent operations
3. Use more specific task descriptions
4. Consider caching repeated operations

## 🎯 Adding New Tests

### Add a Challenge Test

Edit `test_challenges.py` and add to the `CHALLENGES` list:

```python
{
    "name": "Your Challenge Name",
    "file": "test_files/your_challenge.jpg",
    "expected_flag": "CTF{your_flag}",
    "difficulty": "Medium",
    "description": "What this challenge tests"
}
```

### Add a Benchmark

Edit `benchmark.py` and add a new function:

```python
def benchmark_your_operation():
    """Benchmark your operation."""
    print("📊 Benchmarking: Your Operation")

    iterations = 5
    times = []

    for i in range(iterations):
        start = time.time()
        # Your operation here
        duration = time.time() - start
        times.append(duration)
        print(f"   Run {i+1}: {duration:.4f}s")

    avg_time = sum(times) / len(times)
    print(f"   Average: {avg_time:.4f}s\n")
```

Then call it in `main()`.

## 📝 Testing Best Practices

1. **Run tests regularly** - After any code changes
2. **Create challenge files first** - Before running tests
3. **Check tool availability** - Ensure system tools are installed
4. **Monitor performance** - Track benchmark changes over time
5. **Add new tests** - For new features or bug fixes

## 🚀 CI/CD Integration

### GitHub Actions Example

```yaml
name: Test StegoCrew

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        sudo apt-get update
        sudo apt-get install -y steghide binwalk exiftool

    - name: Create test challenges
      run: |
        cd test_files
        python create_test_challenges.py

    - name: Run tests
      run: |
        cd tests
        python test_challenges.py

    - name: Run benchmarks
      run: |
        cd tests
        python benchmark.py
```

---

**Happy Testing! 🧪**
