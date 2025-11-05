#!/usr/bin/env python3
"""
StegoCrew Logo Generator

Generates the StegoCrew logo programmatically using Python PIL/Pillow.
Creates multiple versions: primary, icon, dark mode, etc.
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

# Configuration
OUTPUT_DIR = "assets/logo"
SIZE = 1000

# Color Palette
COLORS = {
    'deep_blue': (44, 62, 80),
    'bright_cyan': (0, 217, 255),
    'dark_bg': (26, 26, 26),
    'light_text': (255, 255, 255),
    'flag_red': (239, 68, 68),
}


def create_primary_logo(size=SIZE):
    """Create the main StegoCrew logo."""

    # Create image with dark background
    img = Image.new('RGBA', (size, size), COLORS['dark_bg'] + (255,))
    draw = ImageDraw.Draw(img)

    center = size // 2
    agent_radius = int(size * 0.30)  # Agents arranged in circle

    # Draw 5 agents in pentagon formation
    for i in range(5):
        # Calculate position
        angle = (i * 2 * math.pi / 5) - (math.pi / 2)  # Start from top
        x = center + agent_radius * math.cos(angle)
        y = center + agent_radius * math.sin(angle)

        # Draw agent figure
        agent_size = size // 20

        # Head (circle)
        head_radius = agent_size // 2
        draw.ellipse(
            [x - head_radius, y - head_radius * 3,
             x + head_radius, y - head_radius],
            fill=COLORS['deep_blue']
        )

        # Body (rectangle)
        body_width = agent_size // 1.5
        body_height = agent_size * 1.5
        draw.rectangle(
            [x - body_width, y - head_radius,
             x + body_width, y + body_height],
            fill=COLORS['deep_blue']
        )

        # Arms (lines)
        arm_length = agent_size
        draw.line(
            [x - body_width, y, x - body_width - arm_length, y + arm_length // 2],
            fill=COLORS['deep_blue'], width=3
        )
        draw.line(
            [x + body_width, y, x + body_width + arm_length, y + arm_length // 2],
            fill=COLORS['deep_blue'], width=3
        )

    # Draw magnifying glass in center
    glass_radius = size // 8
    handle_length = glass_radius // 2

    # Lens (circle outline)
    draw.ellipse(
        [center - glass_radius, center - glass_radius,
         center + glass_radius, center + glass_radius],
        outline=COLORS['bright_cyan'], width=8
    )

    # Handle (line)
    handle_angle = math.pi / 4  # 45 degrees
    handle_start_x = center + glass_radius * math.cos(handle_angle)
    handle_start_y = center + glass_radius * math.sin(handle_angle)
    handle_end_x = handle_start_x + handle_length * math.cos(handle_angle)
    handle_end_y = handle_start_y + handle_length * math.sin(handle_angle)

    draw.line(
        [handle_start_x, handle_start_y, handle_end_x, handle_end_y],
        fill=COLORS['bright_cyan'], width=8
    )

    # Flag symbol inside magnifying glass
    flag_size = glass_radius // 2
    flag_x = center
    flag_y = center

    # Flag pole
    draw.line(
        [flag_x, flag_y - flag_size, flag_x, flag_y + flag_size],
        fill=COLORS['flag_red'], width=3
    )

    # Flag triangle
    draw.polygon(
        [
            (flag_x, flag_y - flag_size),
            (flag_x + flag_size, flag_y - flag_size // 2),
            (flag_x, flag_y)
        ],
        fill=COLORS['flag_red']
    )

    # Add binary pattern background (subtle)
    try:
        # Try to load monospace font
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 24)
    except:
        # Fallback to default
        font = ImageFont.load_default()

    binary_text = "01010101"
    for y in range(0, size, 60):
        for x in range(0, size, 120):
            # Very low opacity for background pattern
            draw.text(
                (x, y),
                binary_text,
                fill=COLORS['light_text'] + (20,),  # 20 = very low opacity
                font=font
            )

    return img


def create_icon_version(primary_logo, size=512):
    """Create simplified icon version (just magnifying glass + flag)."""

    img = Image.new('RGBA', (size, size), COLORS['dark_bg'] + (255,))
    draw = ImageDraw.Draw(img)

    center = size // 2
    glass_radius = size // 3
    handle_length = glass_radius // 2

    # Magnifying glass
    draw.ellipse(
        [center - glass_radius, center - glass_radius,
         center + glass_radius, center + glass_radius],
        outline=COLORS['bright_cyan'], width=int(size * 0.02)
    )

    # Handle
    handle_angle = math.pi / 4
    handle_start_x = center + glass_radius * math.cos(handle_angle)
    handle_start_y = center + glass_radius * math.sin(handle_angle)
    handle_end_x = handle_start_x + handle_length * math.cos(handle_angle)
    handle_end_y = handle_start_y + handle_length * math.sin(handle_angle)

    draw.line(
        [handle_start_x, handle_start_y, handle_end_x, handle_end_y],
        fill=COLORS['bright_cyan'], width=int(size * 0.02)
    )

    # Flag
    flag_size = glass_radius // 2
    flag_x = center
    flag_y = center

    draw.line(
        [flag_x, flag_y - flag_size, flag_x, flag_y + flag_size],
        fill=COLORS['flag_red'], width=int(size * 0.01)
    )

    draw.polygon(
        [
            (flag_x, flag_y - flag_size),
            (flag_x + flag_size, flag_y - flag_size // 2),
            (flag_x, flag_y)
        ],
        fill=COLORS['flag_red']
    )

    return img


def create_light_mode_version(primary_logo):
    """Create version for light backgrounds."""

    img = Image.new('RGBA', primary_logo.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # Redraw with adjusted colors for light background
    size = primary_logo.size[0]
    center = size // 2
    agent_radius = int(size * 0.30)

    # Draw agents in darker blue (more visible on light)
    for i in range(5):
        angle = (i * 2 * math.pi / 5) - (math.pi / 2)
        x = center + agent_radius * math.cos(angle)
        y = center + agent_radius * math.sin(angle)

        agent_size = size // 20
        head_radius = agent_size // 2

        draw.ellipse(
            [x - head_radius, y - head_radius * 3,
             x + head_radius, y - head_radius],
            fill=COLORS['deep_blue']
        )

        body_width = agent_size // 1.5
        body_height = agent_size * 1.5
        draw.rectangle(
            [x - body_width, y - head_radius,
             x + body_width, y + body_height],
            fill=COLORS['deep_blue']
        )

    # Magnifying glass and flag (same as dark mode)
    glass_radius = size // 8
    handle_length = glass_radius // 2

    draw.ellipse(
        [center - glass_radius, center - glass_radius,
         center + glass_radius, center + glass_radius],
        outline=COLORS['bright_cyan'], width=8
    )

    handle_angle = math.pi / 4
    handle_start_x = center + glass_radius * math.cos(handle_angle)
    handle_start_y = center + glass_radius * math.sin(handle_angle)
    handle_end_x = handle_start_x + handle_length * math.cos(handle_angle)
    handle_end_y = handle_start_y + handle_length * math.sin(handle_angle)

    draw.line(
        [handle_start_x, handle_start_y, handle_end_x, handle_end_y],
        fill=COLORS['bright_cyan'], width=8
    )

    flag_size = glass_radius // 2
    flag_x = center
    flag_y = center

    draw.line(
        [flag_x, flag_y - flag_size, flag_x, flag_y + flag_size],
        fill=COLORS['flag_red'], width=3
    )

    draw.polygon(
        [
            (flag_x, flag_y - flag_size),
            (flag_x + flag_size, flag_y - flag_size // 2),
            (flag_x, flag_y)
        ],
        fill=COLORS['flag_red']
    )

    return img


def main():
    """Generate all logo variations."""

    print("🎨 StegoCrew Logo Generator")
    print("=" * 50)

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(f"{OUTPUT_DIR}/social", exist_ok=True)

    # Generate primary logo
    print("\n📐 Generating primary logo (1000x1000)...")
    primary = create_primary_logo(1000)
    primary.save(f"{OUTPUT_DIR}/stegocrew-logo-primary.png")
    print("✅ Saved: stegocrew-logo-primary.png")

    # Generate icon versions
    for size in [512, 256, 128, 64, 32, 16]:
        print(f"📐 Generating icon ({size}x{size})...")
        icon = create_icon_version(primary, size)
        icon.save(f"{OUTPUT_DIR}/stegocrew-icon-{size}.png")
        print(f"✅ Saved: stegocrew-icon-{size}.png")

    # Generate light mode version
    print("\n📐 Generating light mode version...")
    light = create_light_mode_version(primary)
    light.save(f"{OUTPUT_DIR}/stegocrew-logo-light.png")
    print("✅ Saved: stegocrew-logo-light.png")

    # Generate social media versions
    print("\n📐 Generating social media versions...")
    for size, name in [(400, 'linkedin'), (400, 'twitter'), (512, 'github')]:
        social = create_icon_version(primary, size)
        social.save(f"{OUTPUT_DIR}/social/{name}-profile.png")
        print(f"✅ Saved: social/{name}-profile.png")

    # Generate favicon
    print("\n📐 Generating favicon...")
    favicon = create_icon_version(primary, 32)
    favicon.save(f"{OUTPUT_DIR}/favicon.ico", format='ICO', sizes=[(32, 32), (16, 16)])
    print("✅ Saved: favicon.ico")

    print("\n" + "=" * 50)
    print("🎉 Logo generation complete!")
    print(f"\n📁 All files saved to: {OUTPUT_DIR}/")
    print("\nGenerated files:")
    print("  - Primary logo (1000x1000)")
    print("  - Icons (512, 256, 128, 64, 32, 16 px)")
    print("  - Light mode version")
    print("  - Social media profiles (LinkedIn, Twitter, GitHub)")
    print("  - Favicon (.ico)")
    print("\n💡 Use these files in your project!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Make sure you have Pillow installed:")
        print("   pip install pillow")
