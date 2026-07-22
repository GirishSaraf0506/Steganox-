"""Image and payload validation."""

import os
import math
from typing import Tuple
from PIL import Image


def validate_image(image_path: str) -> Tuple[bool, str]:
    """Validate carrier image meets requirements."""
    try:
        img = Image.open(image_path)

        if img.format not in ['PNG', 'BMP', 'JPEG']:
            return False, "Unsupported format. Use PNG, BMP, or JPEG."

        size_mb = os.path.getsize(image_path) / (1024 * 1024)
        if size_mb > 100:
            return False, "Image too large (max 100 MB)."

        if img.size[0] * img.size[1] > 16384 * 16384:
            return False, "Resolution too high (max 16384×16384)."

        if img.mode not in ['RGB', 'RGBA', 'L']:
            return False, "Image must be RGB, RGBA, or grayscale."

        return True, "Valid"
    except Exception as e:
        return False, f"Image validation error: {e}"


def validate_message(message: str, max_bytes: int) -> Tuple[bool, str]:
    """Validate message before embedding."""
    if not message:
        return False, "Message cannot be empty."
    encoded = message.encode()
    if len(encoded) > max_bytes:
        return False, f"Message too large ({len(encoded)} bytes, max {max_bytes})."
    return True, "Valid"


def calculate_entropy(password: str) -> float:
    """Calculate Shannon entropy of a password string."""
    if not password:
        return 0.0
    entropy = 0.0
    for char in set(password):
        p = password.count(char) / len(password)
        entropy -= p * math.log2(p)
    return entropy * len(password)


def validate_password_strength(password: str) -> Tuple[bool, dict]:
    """Validate password meets minimum security requirements."""
    issues = []
    if len(password) < 12:
        issues.append("Minimum 12 characters required.")
    if not any(c.isupper() for c in password):
        issues.append("Must contain an uppercase letter.")
    if not any(c.islower() for c in password):
        issues.append("Must contain a lowercase letter.")
    if not any(c.isdigit() for c in password):
        issues.append("Must contain a digit.")
    if not any(c in "!@#$%^&*()" for c in password):
        issues.append("Must contain a special character (!@#$%^&*()).")
    entropy = calculate_entropy(password)
    if entropy < 50:
        issues.append(f"Entropy too low ({entropy:.1f} bits, need >50).")
    return len(issues) == 0, {"issues": issues, "entropy_bits": entropy}
