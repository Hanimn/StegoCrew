#!/usr/bin/env python3
"""
Test Challenge Generator for StegoCrew
Creates sample CTF steganography challenges for practice.
"""

import os
import subprocess
import sys

def check_tool(tool_name):
    """Check if a tool is installed."""
    try:
        subprocess.run(
            [tool_name, '--version'],
            capture_output=True,
            timeout=5,
            stderr=subprocess.DEVNULL
        )
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False
    except Exception:
        return False


def create_sample_text_file():
    """Create a simple text file with strings."""
    print("📝 Creating sample text file...")

    content = """
Welcome to StegoCrew Practice!

This is a sample file with some interesting strings:
- username: admin
- password: P@ssw0rd123
- secret_key: aGVsbG93b3JsZA==
- flag: CTF{this_was_easy}

Some base64-encoded data:
VGhpcyBpcyBhIHNlY3JldCBtZXNzYWdlIQ==

Good luck finding all the secrets!
"""

    with open('sample_with_metadata.txt', 'w') as f:
        f.write(content)

    print("   ✅ Created: sample_with_metadata.txt")


def create_steghide_challenge():
    """Create a steghide challenge (requires steghide and convert)."""
    if not check_tool('steghide'):
        print("   ⏭️  Skipped: steghide not installed")
        return

    if not check_tool('convert'):  # ImageMagick
        print("   ⏭️  Skipped: ImageMagick (convert) not installed")
        return

    print("🖼️  Creating steghide challenge...")

    try:
        # Create secret message
        with open('secret.txt', 'w') as f:
            f.write("Congratulations! You found the hidden message!\n\n")
            f.write("CTF{steghide_beginner_challenge}\n\n")
            f.write("This data was embedded using steghide with no password.\n")

        # Create a simple image
        subprocess.run(
            ['convert', '-size', '600x400', 'xc:blue', 'base_image.jpg'],
            capture_output=True,
            timeout=10
        )

        # Embed secret with steghide (no password)
        result = subprocess.run(
            ['steghide', 'embed', '-cf', 'base_image.jpg', '-ef', 'secret.txt', '-p', '', '-f'],
            capture_output=True,
            timeout=30
        )

        if result.returncode == 0:
            # Rename to final name
            os.rename('base_image.jpg', 'challenge_steghide.jpg')
            print("   ✅ Created: challenge_steghide.jpg")
            print("      🔑 Password: (empty)")
            print("      🚩 Contains: CTF{steghide_beginner_challenge}")
        else:
            print(f"   ❌ Failed: {result.stderr.decode()}")

        # Cleanup
        if os.path.exists('secret.txt'):
            os.remove('secret.txt')

    except Exception as e:
        print(f"   ❌ Error: {str(e)}")


def create_steghide_with_password():
    """Create a steghide challenge with password."""
    if not check_tool('steghide'):
        print("   ⏭️  Skipped: steghide not installed")
        return

    if not check_tool('convert'):
        print("   ⏭️  Skipped: ImageMagick (convert) not installed")
        return

    print("🔐 Creating steghide challenge with password...")

    try:
        # Create secret message
        with open('secret_password.txt', 'w') as f:
            f.write("Great job cracking the password!\n\n")
            f.write("CTF{password_was_stego123}\n\n")
            f.write("Password hint: Common stego password\n")

        # Create image
        subprocess.run(
            ['convert', '-size', '700x500', 'xc:green', 'base_image_pw.jpg'],
            capture_output=True,
            timeout=10
        )

        # Embed with password
        result = subprocess.run(
            ['steghide', 'embed', '-cf', 'base_image_pw.jpg', '-ef', 'secret_password.txt', '-p', 'stego123', '-f'],
            capture_output=True,
            timeout=30
        )

        if result.returncode == 0:
            os.rename('base_image_pw.jpg', 'challenge_steghide_password.jpg')
            print("   ✅ Created: challenge_steghide_password.jpg")
            print("      🔑 Password: stego123")
            print("      🚩 Contains: CTF{password_was_stego123}")
        else:
            print(f"   ❌ Failed: {result.stderr.decode()}")

        # Cleanup
        if os.path.exists('secret_password.txt'):
            os.remove('secret_password.txt')

    except Exception as e:
        print(f"   ❌ Error: {str(e)}")


def create_embedded_archive():
    """Create file with embedded ZIP archive."""
    if not check_tool('convert'):
        print("   ⏭️  Skipped: ImageMagick (convert) not installed")
        return

    print("📦 Creating embedded archive challenge...")

    try:
        # Create flag file
        with open('hidden_flag.txt', 'w') as f:
            f.write("CTF{binwalk_extraction_master}\n\n")
            f.write("You successfully used binwalk to find and extract this hidden archive!\n")

        # Create ZIP
        subprocess.run(
            ['zip', '-q', 'hidden.zip', 'hidden_flag.txt'],
            capture_output=True,
            timeout=10
        )

        # Create base image
        subprocess.run(
            ['convert', '-size', '800x600', 'xc:red', 'base_archive.jpg'],
            capture_output=True,
            timeout=10
        )

        # Combine image and ZIP
        with open('challenge_embedded_archive.jpg', 'wb') as outfile:
            with open('base_archive.jpg', 'rb') as img:
                outfile.write(img.read())
            with open('hidden.zip', 'rb') as zip_file:
                outfile.write(zip_file.read())

        print("   ✅ Created: challenge_embedded_archive.jpg")
        print("      🚩 Contains: CTF{binwalk_extraction_master}")
        print("      💡 Hint: Use binwalk -e to extract")

        # Cleanup
        for f in ['hidden_flag.txt', 'hidden.zip', 'base_archive.jpg']:
            if os.path.exists(f):
                os.remove(f)

    except Exception as e:
        print(f"   ❌ Error: {str(e)}")


def create_metadata_challenge():
    """Create challenge with flag in metadata."""
    if not check_tool('exiftool'):
        print("   ⏭️  Skipped: exiftool not installed")
        return

    if not check_tool('convert'):
        print("   ⏭️  Skipped: ImageMagick (convert) not installed")
        return

    print("📋 Creating metadata challenge...")

    try:
        # Create image
        subprocess.run(
            ['convert', '-size', '500x500', 'xc:yellow', 'challenge_metadata.jpg'],
            capture_output=True,
            timeout=10
        )

        # Add metadata with flag
        subprocess.run(
            ['exiftool', '-Comment=CTF{check_the_exif_data}', '-overwrite_original', 'challenge_metadata.jpg'],
            capture_output=True,
            timeout=10
        )

        subprocess.run(
            ['exiftool', '-Artist=John Stego', '-overwrite_original', 'challenge_metadata.jpg'],
            capture_output=True,
            timeout=10
        )

        subprocess.run(
            ['exiftool', '-Copyright=Hint: The answer is in the comment field', '-overwrite_original', 'challenge_metadata.jpg'],
            capture_output=True,
            timeout=10
        )

        print("   ✅ Created: challenge_metadata.jpg")
        print("      🚩 Contains: CTF{check_the_exif_data}")
        print("      💡 Hint: Check the Comment field")

    except Exception as e:
        print(f"   ❌ Error: {str(e)}")


def create_readme():
    """Create README for challenges."""
    print("📖 Creating challenge guide...")

    content = """# Generated CTF Challenges

This directory contains auto-generated steganography challenges for practice.

## 🎯 Challenges

### 1. sample_with_metadata.txt
**Difficulty:** Beginner
**Tools needed:** strings, grep
**Flag:** CTF{this_was_easy}
**Solution:** `strings sample_with_metadata.txt | grep CTF`

### 2. challenge_steghide.jpg
**Difficulty:** Beginner
**Tools needed:** steghide
**Password:** (empty)
**Flag:** CTF{steghide_beginner_challenge}
**Solution:**
```bash
steghide extract -sf challenge_steghide.jpg -p ""
cat challenge_steghide.jpg.extracted
```

### 3. challenge_steghide_password.jpg
**Difficulty:** Intermediate
**Tools needed:** steghide
**Password:** stego123
**Flag:** CTF{password_was_stego123}
**Solution:**
```bash
steghide extract -sf challenge_steghide_password.jpg -p "stego123"
```

### 4. challenge_embedded_archive.jpg
**Difficulty:** Intermediate
**Tools needed:** binwalk
**Flag:** CTF{binwalk_extraction_master}
**Solution:**
```bash
binwalk -e challenge_embedded_archive.jpg
cat _challenge_embedded_archive.jpg.extracted/hidden_flag.txt
```

### 5. challenge_metadata.jpg
**Difficulty:** Beginner
**Tools needed:** exiftool
**Flag:** CTF{check_the_exif_data}
**Solution:**
```bash
exiftool challenge_metadata.jpg | grep CTF
```

## 🧪 Test with StegoCrew

```bash
# Analyze a challenge with the complete example
cd ../examples
python3 05_stego_tools.py ../test_files/challenge_steghide.jpg

# Or use your practice analyzer
python3 my_stego_analyzer.py ../test_files/challenge_metadata.jpg
```

## 🎓 Learning Path

1. Start with **sample_with_metadata.txt** - practice strings
2. Try **challenge_metadata.jpg** - practice exiftool
3. Move to **challenge_steghide.jpg** - learn steghide
4. Challenge yourself with **challenge_steghide_password.jpg** - password brute-force
5. Master **challenge_embedded_archive.jpg** - practice binwalk

## 💡 Tips

- Always start with basic file analysis (`file`, `exiftool`)
- Use `strings` to look for obvious flags
- Try steghide with empty password first
- Use binwalk to detect embedded files
- Check all metadata fields carefully

Good luck! 🚀
"""

    with open('CHALLENGE_GUIDE.md', 'w') as f:
        f.write(content)

    print("   ✅ Created: CHALLENGE_GUIDE.md")


def main():
    print("="*70)
    print("🎯 STEGOCREW TEST CHALLENGE GENERATOR")
    print("="*70)
    print()

    # Check available tools
    print("🔧 Checking available tools...")
    tools = {
        'steghide': check_tool('steghide'),
        'binwalk': check_tool('binwalk'),
        'exiftool': check_tool('exiftool'),
        'convert': check_tool('convert'),
        'zip': check_tool('zip')
    }

    for tool, available in tools.items():
        status = "✅" if available else "❌"
        print(f"   {status} {tool}")

    print()
    print("="*70)
    print("Creating challenges...")
    print("="*70)
    print()

    # Create all challenges
    create_sample_text_file()
    create_metadata_challenge()
    create_steghide_challenge()
    create_steghide_with_password()
    create_embedded_archive()
    create_readme()

    print()
    print("="*70)
    print("✅ DONE! Check CHALLENGE_GUIDE.md for solutions")
    print("="*70)
    print()
    print("💡 Test with:")
    print("   cd ../examples")
    print("   python3 05_stego_tools.py ../test_files/challenge_steghide.jpg")
    print()

    # Count created files
    files = [f for f in os.listdir('.') if f.startswith('challenge_') or f == 'sample_with_metadata.txt']
    print(f"📊 Created {len(files)} challenge files")
    print()


if __name__ == "__main__":
    main()
