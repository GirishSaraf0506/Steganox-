"""Tests for image and password validation."""

import pytest

from steganox.core.validation import (validate_message,
                                      validate_password_strength)


def test_strong_password_passes():
    valid, info = validate_password_strength("Str0ng!P@ssw0rd#")
    assert valid
    assert info["issues"] == []


@pytest.mark.parametrize(
    "pwd", ["short", "alllowercase1!", "ALLUPPERCASE1!", "NoSpecial123"]
)
def test_weak_passwords_fail(pwd):
    valid, _ = validate_password_strength(pwd)
    assert not valid


def test_validate_message_empty():
    valid, msg = validate_message("", 1000)
    assert not valid


def test_validate_message_too_large():
    valid, msg = validate_message("A" * 100, 10)
    assert not valid


def test_validate_message_ok():
    valid, msg = validate_message("Hello", 1000)
    assert valid
