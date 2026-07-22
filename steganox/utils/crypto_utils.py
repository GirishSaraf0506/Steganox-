"""Cryptographic utility helpers."""

import hashlib
import os
import secrets


def generate_salt(length: int = 16) -> bytes:
    return os.urandom(length)


def generate_token(length: int = 32) -> str:
    return secrets.token_hex(length)


def sha256_hex(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()


def sha256_bytes(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()
