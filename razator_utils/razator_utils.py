"""Main module."""
import subprocess
import shutil
import re


def batchify(iterable, n=1):
    iter_len = len(iterable)
    for ndx in range(0, iter_len, n):
        yield iterable[ndx:min(ndx + n, iter_len)]


def camel_to_snake(camel_str):
    import re
    snake_str = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_str)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', snake_str).lower()


def flatten_dict(d, parent_key='', sep='_'):
    items = {}
    for key, val in d.items():
        new_key = (parent_key + sep + key) if parent_key else key
        if isinstance(val, dict):
            items = {**items, **flatten_dict(val, parent_key=new_key, sep=sep)}
        else:
            items[new_key] = val
    return items


def get_chrome_major_version():
    """
    Detects the major version of Google Chrome installed.
    Returns:
        int: The major version number (e.g., 120), or None if not found.
    """
    # Common executable names for Chrome/Chromium
    chrome_names = [
        "google-chrome",
        "chrome",
        "chromium",
        "chromium-browser",
        "google-chrome-stable",
    ]

    binary = None
    for name in chrome_names:
        binary = shutil.which(name)
        if binary:
            break

    if not binary:
        # Fallback for Windows if not in PATH (common locations)
        # This is a basic check, could be expanded if needed
        import platform
        if platform.system() == "Windows":
            possible_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            ]
            for path in possible_paths:
                if shutil.which(path):
                    binary = path
                    break

    if not binary:
        return None

    try:
        # Run the '--version' command and capture output
        output = subprocess.check_output([binary, "--version"]).decode("utf-8")
        # Extract the major version (e.g., '120' from 'Google Chrome 120.0.xxxx')
        match = re.search(r"(\d+)\.", output)
        if match:
            return int(match.group(1))
    except Exception as e:
        print(f"Could not detect Chrome version: {e}")

    return None
