#!/usr/bin/env python3
"""
Performance Benchmarks for StegoCrew
Lesson 8 - Performance Testing
"""

import os
import sys
import time

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def benchmark_file_analysis():
    """Benchmark file analysis performance."""
    from examples.my_first_tool import count_lines_by_type

    print("📊 Benchmarking: count_lines_by_type")

    file_path = "../README.md"
    iterations = 5

    times = []
    for i in range(iterations):
        start = time.time()
        result = count_lines_by_type(file_path, "all")
        duration = time.time() - start
        times.append(duration)
        print(f"   Run {i+1}: {duration:.4f}s")

    avg_time = sum(times) / len(times)
    print(f"   Average: {avg_time:.4f}s\n")


def benchmark_string_extraction():
    """Benchmark string extraction."""
    print("📊 Benchmarking: String extraction")

    # Simulate extracting strings from file
    file_path = "README.md"

    if not os.path.exists(file_path):
        print("   ⚠️  README.md not found, skipping\n")
        return

    iterations = 3

    times = []
    for i in range(iterations):
        start = time.time()

        # Read and process file
        with open(file_path, 'r') as f:
            content = f.read()
            lines = content.split('\n')
            # Simulate processing
            words = [word for line in lines for word in line.split()]

        duration = time.time() - start
        times.append(duration)
        print(f"   Run {i+1}: {duration:.4f}s (processed {len(words)} words)")

    avg_time = sum(times) / len(times)
    print(f"   Average: {avg_time:.4f}s\n")


def benchmark_metadata_extraction():
    """Benchmark metadata extraction simulation."""
    import subprocess

    print("📊 Benchmarking: Metadata extraction (if exiftool available)")

    file_path = "README.md"

    if not os.path.exists(file_path):
        print("   ⚠️  File not found, skipping\n")
        return

    try:
        iterations = 3
        times = []

        for i in range(iterations):
            start = time.time()
            result = subprocess.run(
                ['file', file_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            duration = time.time() - start
            times.append(duration)
            print(f"   Run {i+1}: {duration:.4f}s")

        avg_time = sum(times) / len(times)
        print(f"   Average: {avg_time:.4f}s\n")

    except Exception as e:
        print(f"   ⚠️  Benchmark failed: {str(e)}\n")


def main():
    """Run all benchmarks."""

    print("="*70)
    print("⏱️  STEGOCREW PERFORMANCE BENCHMARKS")
    print("="*70)
    print()

    # Change to project root
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    print(f"Working directory: {os.getcwd()}\n")

    benchmark_file_analysis()
    benchmark_string_extraction()
    benchmark_metadata_extraction()

    print("="*70)
    print("✅ Benchmarks Complete")
    print("="*70)
    print()
    print("💡 Tips for optimization:")
    print("   - Cache repeated file operations")
    print("   - Use specific task descriptions to reduce LLM calls")
    print("   - Consider parallel tool execution")
    print("="*70)


if __name__ == "__main__":
    main()
