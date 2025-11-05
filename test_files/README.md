# Test Files for Steganography Practice

This directory contains sample files for testing your steganography tools and agents.

## 📁 What's Here

### Sample Files

- **sample_with_metadata.txt** - Text file with interesting strings
- **create_test_challenges.py** - Script to generate CTF challenge files

## 🛠️ Creating Your Own Test Files

### Method 1: Use the Generator Script

```bash
cd test_files
python3 create_test_challenges.py
```

This will create:
- Images with hidden data (using steghide)
- Files with embedded archives (using cat)
- Files with interesting metadata (using exiftool)

### Method 2: Manual Creation

#### Create File with Steghide

```bash
# 1. Create secret message
echo "CTF{stego_master_2024}" > secret.txt

# 2. Get a JPEG image (or create one)
# Download any JPEG or use convert to create one:
convert -size 800x600 xc:blue test_image.jpg

# 3. Embed secret with steghide
steghide embed -cf test_image.jpg -ef secret.txt -p "mypassword"

# 4. Clean up
rm secret.txt
```

#### Create File with Embedded Archive

```bash
# 1. Create a flag file
echo "CTF{hidden_in_archive}" > flag.txt

# 2. Create a ZIP
zip hidden.zip flag.txt

# 3. Get a JPEG image
convert -size 800x600 xc:red base_image.jpg

# 4. Append ZIP to JPEG (both formats work!)
cat base_image.jpg hidden.zip > combined.jpg

# 5. Test with binwalk
binwalk combined.jpg  # Should show embedded ZIP

# 6. Clean up
rm flag.txt hidden.zip base_image.jpg
```

#### Add Metadata with Exiftool

```bash
# Add flag to image metadata
exiftool -Comment="CTF{check_the_metadata}" image.jpg

# Add to multiple fields
exiftool -Artist="CTF{hidden_artist}" -Copyright="Super Secret" image.jpg
```

#### Create LSB Stego (PNG)

For PNG files with LSB steganography, you can use online tools or:

```bash
# Using zsteg to check LSB
zsteg -a image.png  # Analyze all LSB channels

# Create LSB stego (requires specialized tools)
# Many CTF challenges use custom scripts or tools like:
# - stegano (Python library)
# - OpenStego
# - StegPy
```

## 📥 Download Practice CTF Challenges

### From Public Repositories

```bash
# Clone stego toolkit examples
git clone https://github.com/DominicBreuker/stego-toolkit.git
cd stego-toolkit/examples/

# Or download specific challenges from CTF archives
# https://github.com/ctfs/write-ups
```

### Sample CTF Sites for Practice

- **PicoCTF** - https://play.picoctf.org/ (many stego challenges)
- **CTFTime** - https://ctftime.org/ (find past CTF challenges)
- **247CTF** - https://247ctf.com/ (ongoing challenges)

## 🧪 Testing Your Tools

### Quick Test with README

```bash
# Test basic tools with the repository README
cd examples
python3 05_stego_tools.py ../README.md
```

### Test with Custom Challenge

```bash
# Create a challenge
cd test_files
python3 create_test_challenges.py

# Analyze it
cd ../examples
python3 05_stego_tools.py ../test_files/challenge_steghide.jpg
```

### Test Your Practice Analyzer

```bash
cd examples
python3 my_stego_analyzer.py ../test_files/challenge_steghide.jpg
```

## 🎯 Challenge Difficulty Levels

### Beginner

1. **Metadata Only** - Flag hidden in EXIF data
2. **Strings** - Flag visible in strings output
3. **Steghide No Password** - Data embedded without password

### Intermediate

4. **Steghide with Password** - Password provided separately
5. **Embedded ZIP** - ZIP appended to image
6. **LSB Basic** - Simple LSB in PNG

### Advanced

7. **Multi-Layer** - Metadata → password → steghide → flag
8. **Corrupted Headers** - File type misidentified
9. **Multiple Files** - ZIP containing multiple images with parts of flag
10. **Custom Encoding** - Base64 → Hex → ROT13 → Flag

## 📊 Tool Requirements

To create all types of test files:

```bash
# Install steganography tools
sudo apt update
sudo apt install -y steghide binwalk exiftool imagemagick

# For PNG LSB (optional)
gem install zsteg

# For Python-based creation (optional)
pip install stegano pillow
```

## 🔐 Sample Flags

Use these formats for CTF flags in your test files:

- `CTF{test_flag_12345}`
- `FLAG{hidden_message}`
- `flag{simple_stego}`
- `STEGO{solved_challenge}`

## 🚨 Important Notes

1. **Don't commit large files** - Keep test images small (<1MB)
2. **Document passwords** - If using steghide with password, note it in filename or README
3. **Verify before testing** - Make sure challenges are solvable before using them
4. **Safe to share** - These are practice files, not real secrets

## 📖 Examples

### Example 1: Simple Metadata Challenge

```bash
# Create image
convert -size 400x300 xc:green metadata_challenge.jpg

# Add flag to metadata
exiftool -Comment="CTF{metadata_master}" metadata_challenge.jpg

# Test
exiftool metadata_challenge.jpg | grep CTF
```

### Example 2: Steghide Challenge

```bash
# Create secret
echo "Congratulations! CTF{you_found_the_stego}" > secret.txt

# Create image
convert -size 600x400 xc:purple stego_challenge.jpg

# Embed (no password for beginners)
steghide embed -cf stego_challenge.jpg -ef secret.txt -p ""

# Test
steghide extract -sf stego_challenge.jpg -p ""
```

### Example 3: Embedded Archive

```bash
# Create flag file
echo "CTF{binwalk_expert}" > flag.txt
zip flag.zip flag.txt

# Create base image
convert -size 500x500 xc:cyan archive_challenge.jpg

# Combine
cat archive_challenge.jpg flag.zip > archive_challenge_final.jpg

# Test
binwalk archive_challenge_final.jpg
binwalk -e archive_challenge_final.jpg  # Extract
```

---

Happy Stego Hunting! 🔍🚩
