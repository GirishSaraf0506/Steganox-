"""
AES-256-GCM encryption with PBKDF2 key derivation.
"""

import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


def _derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return kdf.derive(password.encode())


def encrypt_message(message: str, password: str) -> bytes:
    """Encrypt message with AES-256-GCM. Returns salt + iv + ciphertext + tag."""
    salt = os.urandom(16)
    key = _derive_key(password, salt)
    iv = os.urandom(12)
    encryptor = Cipher(algorithms.AES(key), modes.GCM(iv)).encryptor()
    ciphertext = encryptor.update(message.encode()) + encryptor.finalize()
    return salt + iv + ciphertext + encryptor.tag


def decrypt_message(encrypted_data: bytes, password: str) -> str:
    """Decrypt AES-256-GCM encrypted message."""
    salt = encrypted_data[:16]
    iv = encrypted_data[16:28]
    tag = encrypted_data[-16:]
    ciphertext = encrypted_data[28:-16]
    key = _derive_key(password, salt)
    decryptor = Cipher(algorithms.AES(key), modes.GCM(iv, tag)).decryptor()
    return (decryptor.update(ciphertext) + decryptor.finalize()).decode()
