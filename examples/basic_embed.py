"""Example: Embed a secret message into an image."""

from steganox.core.steganography import SteganoxEngine

engine = SteganoxEngine()

result = engine.embed(
    image_path="carrier.png",
    message="CLASSIFIED: Project Aurora",
    password="<your-password>"
)
result.save("output.png")
print("✅ Message embedded into output.png")
