"""
Password hashing utilities.
Current: SHA-256 (v1.0)
Planned: PBKDF2 / Argon2 (v1.5+)
"""

import hashlib
import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def hash_password_sha256(password: str) -> str:
    """SHA-256 password hash (v1.0 — fast, use PBKDF2 for production)."""
    return hashlib.sha256(password.encode()).hexdigest()


def derive_key_pbkdf2(password: str, salt: bytes | None = None) -> tuple[bytes, bytes]:
    """
    Derive a 256-bit key using PBKDF2-HMAC-SHA256 (v1.5+).

    Returns:
        (key, salt) tuple
    """
    if salt is None:
        salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return kdf.derive(password.encode()), salt


def verify_password(password: str, stored_hash: str) -> bool:
    """Verify password against stored SHA-256 hash."""
    return hash_password_sha256(password) == stored_hash
