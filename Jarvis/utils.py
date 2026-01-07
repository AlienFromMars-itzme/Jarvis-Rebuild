"""Utility functions for Jarvis AI Assistant."""

import os
import json
import datetime
import re
from typing import Dict, List, Any, Optional


def get_greeting() -> str:
    """Get appropriate greeting based on time of day."""
    hour = datetime.datetime.now().hour
    if 4 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 16:
        return "Good afternoon"
    elif 16 <= hour < 24:
        return "Good evening"
    else:
        return "Good night"


def format_time(fmt: str = "12h") -> str:
    """Format current time."""
    if fmt == "12h":
        return datetime.datetime.now().strftime("%I:%M:%S %p")
    else:
        return datetime.datetime.now().strftime("%H:%M:%S")


def format_date() -> str:
    """Format current date."""
    now = datetime.datetime.now()
    return f"{now.day} {now.strftime('%B')} {now.year}"


def extract_number(text: str) -> Optional[int]:
    """Extract a number from text."""
    match = re.search(r'\d+', text)
    return int(match.group()) if match else None


def extract_percentage(text: str) -> Optional[int]:
    """Extract percentage from text."""
    match = re.search(r'(\d+)\s*%', text)
    if match:
        return int(match.group(1))
    return extract_number(text)


def sanitize_filename(filename: str) -> str:
    """Sanitize filename by removing invalid characters."""
    return re.sub(r'[<>:"/\\|?*]', '', filename)


def load_json(filepath: str, default: Any = None) -> Any:
    """Load JSON data from file."""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return default if default is not None else {}
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return default if default is not None else {}


def save_json(filepath: str, data: Any) -> bool:
    """Save JSON data to file."""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving {filepath}: {e}")
        return False


def format_bytes(bytes_val: int) -> str:
    """Format bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.2f} PB"


def parse_duration(text: str) -> Optional[int]:
    """Parse duration from text (e.g., '5 minutes', '2 hours')."""
    text = text.lower()
    match = re.search(r'(\d+)\s*(second|minute|hour|day)s?', text)
    if match:
        value = int(match.group(1))
        unit = match.group(2)
        if unit == 'second':
            return value
        elif unit == 'minute':
            return value * 60
        elif unit == 'hour':
            return value * 3600
        elif unit == 'day':
            return value * 86400
    return None


def is_valid_url(url: str) -> bool:
    """Check if a string is a valid URL."""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to maximum length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def get_platform() -> str:
    """Get the current platform."""
    import platform
    return platform.system().lower()


def is_windows() -> bool:
    """Check if running on Windows."""
    return get_platform() == "windows"


def is_linux() -> bool:
    """Check if running on Linux."""
    return get_platform() == "linux"


def is_mac() -> bool:
    """Check if running on macOS."""
    return get_platform() == "darwin"


class ColorText:
    """ANSI color codes for terminal output."""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    
    @staticmethod
    def print_colored(text: str, color: str):
        """Print colored text."""
        print(f"{color}{text}{ColorText.END}")
    
    @staticmethod
    def success(text: str):
        """Print success message."""
        print(f"✓ {ColorText.GREEN}{text}{ColorText.END}")
    
    @staticmethod
    def error(text: str):
        """Print error message."""
        print(f"✗ {ColorText.RED}{text}{ColorText.END}")
    
    @staticmethod
    def info(text: str):
        """Print info message."""
        print(f"ℹ {ColorText.BLUE}{text}{ColorText.END}")
    
    @staticmethod
    def warning(text: str):
        """Print warning message."""
        print(f"⚠ {ColorText.YELLOW}{text}{ColorText.END}")
