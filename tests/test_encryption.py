"""Tests for AES-256-GCM encryption/decryption."""

import pytest

from steganox.core.encryption import decrypt_message, encrypt_message


def test_roundtrip():
    msg = "Top secret payload"
    pwd = "Str0ng!P@ssw0rd#"
    assert decrypt_message(encrypt_message(msg, pwd), pwd) == msg


def test_wrong_password_raises():
    encrypted = encrypt_message("secret", "CorrectP@ss1!")
    with pytest.raises(Exception):
        decrypt_message(encrypted, "WrongP@ss1!")


def test_different_encryptions_differ():
    msg, pwd = "same message", "S@meP@ss1!XYZ"
    assert encrypt_message(msg, pwd) != encrypt_message(msg, pwd)


def test_empty_message():
    pwd = "EmptyMsg!P@ss1"
    assert decrypt_message(encrypt_message("", pwd), pwd) == ""
