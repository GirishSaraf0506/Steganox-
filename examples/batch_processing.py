"""Example: Batch embed the same message into multiple carrier images."""

import os
from steganox.core.steganography import SteganoxEngine

engine = SteganoxEngine()

carriers = ["image1.png", "image2.png", "image3.png"]
message = "Batch embedded secret"
password = "<your-password>"
output_dir = "batch_output"

os.makedirs(output_dir, exist_ok=True)

for carrier in carriers:
    if not os.path.exists(carrier):
        print(f"⚠️  Skipping {carrier} (not found)")
        continue
    try:
        result = engine.embed(carrier, message, password)
        out_path = os.path.join(output_dir, f"stego_{carrier}")
        result.save(out_path)
        print(f"✅ {carrier} → {out_path}")
    except ValueError as e:
        print(f"❌ {carrier}: {e}")
