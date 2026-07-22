"""Tests for SteganoxEngine (LSB embed/extract)."""

import pytest
from steganox.core.steganography import SteganoxEngine


@pytest.fixture
def engine():
    return SteganoxEngine()


def test_embed_and_extract_roundtrip(engine, test_image_path, tmp_output):
    message = "Hello, Steganox!"
    password = "T3stP@ssw0rd!XY"

    result = engine.embed(test_image_path, message, password)
    result.save(tmp_output)

    extracted = engine.extract(tmp_output, password)
    assert extracted == message


def test_wrong_password_raises(engine, test_image_path, tmp_output):
    engine.embed(test_image_path, "secret", "CorrectP@ss1!").save(tmp_output)
    with pytest.raises(ValueError):
        engine.extract(tmp_output, "WrongP@ss1!")


def test_message_too_large_raises(engine, test_image_path):
    huge_message = "A" * 100_000
    with pytest.raises(ValueError, match="too large"):
        engine.embed(test_image_path, huge_message, "P@ssw0rd!123")


def test_unicode_message(engine, test_image_path, tmp_output):
    message = "Héllo Wörld 🔐 日本語"
    password = "Unic0de!P@ss#1"
    engine.embed(test_image_path, message, password).save(tmp_output)
    assert engine.extract(tmp_output, password) == message
