#!/usr/bin/env python3
"""
Test StegoCrew with real CTF challenges
Lesson 8 - Testing Suite
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from examples.my_stego_analyzer import analyze_file

# Define test challenges
CHALLENGES = [
    {
        "name": "Metadata Flag",
        "file": "test_files/challenge_metadata.jpg",
        "expected_flag": "CTF{check_the_exif_data}",
        "difficulty": "Easy",
        "description": "Flag hidden in EXIF metadata"
    },
    {
        "name": "Steghide No Password",
        "file": "test_files/challenge_steghide.jpg",
        "expected_flag": "CTF{steghide_beginner_challenge}",
        "difficulty": "Easy",
        "description": "Data embedded with steghide (no password)"
    },
    {
        "name": "Embedded Archive",
        "file": "test_files/challenge_embedded_archive.jpg",
        "expected_flag": "CTF{binwalk_extraction_master}",
        "difficulty": "Medium",
        "description": "ZIP archive appended to image"
    },
    {
        "name": "Simple Strings",
        "file": "test_files/sample_with_metadata.txt",
        "expected_flag": "CTF{this_was_easy}",
        "difficulty": "Beginner",
        "description": "Flag visible in strings"
    }
]


def test_challenge(challenge):
    """Test a single challenge."""

    print(f"\n{'='*70}")
    print(f"📝 Challenge: {challenge['name']}")
    print(f"🎯 Difficulty: {challenge['difficulty']}")
    print(f"📄 Description: {challenge['description']}")
    print(f"📁 File: {challenge['file']}")
    print('='*70)

    # Check if file exists
    if not os.path.exists(challenge['file']):
        print(f"⚠️  SKIP: File not found")
        print("    💡 Run: cd test_files && python create_test_challenges.py")
        return None

    try:
        # Run StegoCrew
        print("\n🚀 Running analysis...")
        result = analyze_file(challenge['file'])

        # Check for flag
        if challenge['expected_flag'] in str(result):
            print(f"\n✅ SUCCESS: Found flag {challenge['expected_flag']}")
            return True
        else:
            print(f"\n❌ FAILED: Expected flag not found")
            print(f"   Expected: {challenge['expected_flag']}")
            print(f"   Result preview: {str(result)[:200]}...")
            return False

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        return False


def main():
    """Run all challenge tests."""

    print("="*70)
    print("🧪 STEGOCREW CTF CHALLENGE TEST SUITE")
    print("="*70)
    print()

    passed = 0
    failed = 0
    skipped = 0

    for i, challenge in enumerate(CHALLENGES, 1):
        print(f"\n[Test {i}/{len(CHALLENGES)}]")
        result = test_challenge(challenge)

        if result is None:
            skipped += 1
        elif result:
            passed += 1
        else:
            failed += 1

    # Summary
    print(f"\n{'='*70}")
    print("📊 TEST SUMMARY")
    print(f"{'='*70}")
    print(f"Total Challenges: {len(CHALLENGES)}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"⚠️  Skipped: {skipped}")

    if len(CHALLENGES) > skipped:
        success_rate = (passed / (len(CHALLENGES) - skipped)) * 100
        print(f"\n🎯 Success Rate: {success_rate:.1f}%")

    print("="*70)

    # Exit code
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
