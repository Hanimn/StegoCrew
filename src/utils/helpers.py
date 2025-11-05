"""
Helper utilities for StegoCrew
"""

import subprocess


def check_tool_installed(tool_name: str) -> bool:
    """Check if a system tool is installed."""
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


def get_install_command(tool_name: str) -> str:
    """Get installation command for a tool."""
    install_commands = {
        'steghide': 'sudo apt install steghide',
        'binwalk': 'sudo apt install binwalk',
        'exiftool': 'sudo apt install libimage-exiftool-perl',
        'zsteg': 'gem install zsteg',
        'foremost': 'sudo apt install foremost',
        'strings': 'sudo apt install binutils',
        'file': 'sudo apt install file'
    }
    return install_commands.get(tool_name, f'Install {tool_name} manually')
