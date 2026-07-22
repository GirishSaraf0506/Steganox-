"""Example: Extract a hidden message from a stego-image."""

from steganox.core.steganography import SteganoxEngine

engine = SteganoxEngine()

message = engine.extract(
    image_path="output.png",
    password="<your-password>"
)
print(f"🔓 Extracted message: {message}")
