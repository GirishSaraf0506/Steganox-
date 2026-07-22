"""
Core steganography engine for LSB embedding and extraction.
"""

import struct
from PIL import Image
import numpy as np

from steganox.core.encryption import encrypt_message, decrypt_message


class SteganoxEngine:
    """LSB steganography engine with AES-256 encryption."""

    def embed(self, image_path: str, message: str, password: str) -> Image.Image:
        """
        Encrypt and embed message into carrier image using LSB steganography.

        Args:
            image_path: Path to carrier image
            message: Secret message to hide
            password: Password for AES-256 encryption

        Returns:
            PIL Image with embedded message

        Raises:
            ValueError: If message is too large for the carrier image
        """
        carrier = Image.open(image_path).convert('RGB')
        carrier_array = np.array(carrier, dtype=np.uint8)

        payload = encrypt_message(message, password)
        # Prepend 4-byte length header so extraction knows when to stop
        payload = struct.pack('>I', len(payload)) + payload

        payload_bits = self._bytes_to_bits(payload)

        if len(payload_bits) > carrier_array.size:
            raise ValueError(
                f"Message too large. Capacity: {carrier_array.size // 8} bytes, "
                f"Required: {len(payload_bits) // 8} bytes"
            )

        flat = carrier_array.flatten()
        for i, bit in enumerate(payload_bits):
            flat[i] = (flat[i] & 0xFE) | bit

        return Image.fromarray(flat.reshape(carrier_array.shape))

    def extract(self, image_path: str, password: str) -> str:
        """
        Extract and decrypt hidden message from stego-image.

        Args:
            image_path: Path to stego-image
            password: Password for AES-256 decryption

        Returns:
            Decrypted secret message

        Raises:
            ValueError: If decryption fails (wrong password or no hidden message)
        """
        stego = Image.open(image_path).convert('RGB')
        flat = np.array(stego, dtype=np.uint8).flatten()
        lsb_bits = (flat & 0x01).tolist()

        # Read 4-byte length header first (32 bits)
        header_bytes = self._bits_to_bytes(lsb_bits[:32])
        payload_len = struct.unpack('>I', header_bytes)[0]

        total_bits = 32 + payload_len * 8
        if total_bits > len(lsb_bits):
            raise ValueError("No valid hidden message found in this image.")

        payload_bytes = self._bits_to_bytes(lsb_bits[32:total_bits])

        try:
            return decrypt_message(payload_bytes, password)
        except Exception as e:
            raise ValueError(f"Decryption failed — wrong password or corrupted data: {e}")

    @staticmethod
    def _bytes_to_bits(data: bytes) -> list:
        bits = []
        for byte in data:
            for i in range(7, -1, -1):
                bits.append((byte >> i) & 1)
        return bits

    @staticmethod
    def _bits_to_bytes(bits: list) -> bytes:
        result = []
        for i in range(0, len(bits) - 7, 8):
            byte = 0
            for j in range(8):
                byte = (byte << 1) | bits[i + j]
            result.append(byte)
        return bytes(result)
