"""
Read a practice user from the .env file.

Each account is one pair, written as username / password:

    VALID=user@premiumbank.com / Bank@123

    username, password = get_user("valid")
    username, password = get_user("invalid")
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# This file lives in helper/, so the project root is one folder up.
# Load that .env even when pytest is started from another directory.
ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(ENV_FILE)

# The separator between username and password in .env. Spaces keep an
# email or a password that contains "/" from being split in the wrong place.
PAIR_SEPARATOR = " / "


def get_user(name: str) -> tuple[str, str]:
    """Return (username, password) for a user named in .env."""
    key = name.strip().upper()
    pair = os.getenv(key)

    if not pair or PAIR_SEPARATOR not in pair:
        raise KeyError(f"Add {key}=username / password to {ENV_FILE}")

    username, password = pair.split(PAIR_SEPARATOR, 1)
    return username.strip(), password.strip()
