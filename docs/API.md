# Steganox API Reference

## SteganoxEngine

### `embed(image_path, message, password) -> PIL.Image`
Encrypts `message` with AES-256-GCM (PBKDF2 key) and embeds it into the carrier image via LSB steganography.

- `image_path` — path to carrier PNG/BMP/JPEG
- `message` — plaintext secret string
- `password` — encryption password (12+ chars recommended)
- Raises `ValueError` if message is too large for the image

### `extract(image_path, password) -> str`
Extracts and decrypts the hidden message from a stego-image.

- `image_path` — path to stego-image
- `password` — decryption password
- Raises `ValueError` on wrong password or no hidden message

---

## encrypt_message / decrypt_message

```python
from steganox.core.encryption import encrypt_message, decrypt_message

ciphertext = encrypt_message(message: str, password: str) -> bytes
plaintext  = decrypt_message(data: bytes, password: str) -> str
```

Format: `salt(16) + iv(12) + ciphertext(n) + tag(16)`

---

## validate_image / validate_password_strength

```python
from steganox.core.validation import validate_image, validate_password_strength

ok, msg  = validate_image(image_path: str) -> (bool, str)
ok, info = validate_password_strength(password: str) -> (bool, dict)
```

---

## AuditLogger

```python
from steganox.logging.audit import AuditLogger

logger = AuditLogger("audit.log")
logger.log(action="embed", image_hash="abc123", status="success")
logger.verify_integrity() -> bool
```

---

## CLI

```bash
steganox embed -i carrier.png -o output.png -m "secret message"
steganox extract -i output.png
```

---

## Web API

| Method | Endpoint | Body (multipart) | Response |
|--------|----------|-----------------|----------|
| POST | `/api/embed` | `image`, `message`, `password` | stego PNG file download |
| POST | `/api/extract` | `image`, `password` | `{"success": true, "message": "..."}` |
