# Steganox Architecture Document

## System Design Overview

Steganox is designed as a **modular, layered security platform** combining obfuscation, encryption, and authentication to provide enterprise-grade steganography capabilities.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Presentation Layer                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  GUI (Tkinter) │ Web Dashboard (Flask) │ CLI (Future) │  │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Business Logic Layer                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Steganography Engine  │  Encryption Manager        │   │
│  │  ─────────────────────   ─────────────────────      │   │
│  │  • LSB Embedding       • AES-256                     │   │
│  │  • LSB Extraction      • PBKDF2 (Future)            │   │
│  │  • Image Validation    • Kyber (Roadmap)            │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Data/Security Layer                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Password Hashing (SHA-256)                          │   │
│  │  Entropy Analysis & Validation                       │   │
│  │  Audit Logging & Compliance                          │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Media Layer                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Image Formats (PNG, BMP, JPG)                       │   │
│  │  Pixel Manipulation (Pillow + NumPy)                 │   │
│  │  LSB Bitwise Operations                              │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Module Structure

### Current Implementation (v1.0)

```
steganox/
├── steganox.py              # Main GUI application (Tkinter)
├── requirements.txt         # Project dependencies
└── README.md               # Documentation
```

### Proposed Modular Structure (v2.0+)

```
steganox/
├── steganox/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── steganography.py      # LSB embedding/extraction
│   │   ├── encryption.py         # AES-256, Kyber integration
│   │   └── validation.py         # Image validation, entropy checks
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── password_hash.py      # SHA-256, PBKDF2, Argon2
│   │   └── oauth2.py             # OAuth2/SAML (Future)
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── gui/
│   │   │   ├── __init__.py
│   │   │   └── tkinter_app.py    # Current Tkinter GUI
│   │   └── web/
│   │       ├── __init__.py
│   │       ├── app.py            # Flask application
│   │       └── routes.py         # Web endpoints
│   ├── cli/
│   │   ├── __init__.py
│   │   └── commands.py           # Command-line interface
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── image_utils.py        # Image I/O, format detection
│   │   └── crypto_utils.py       # Cryptographic utilities
│   └── logging/
│       ├── __init__.py
│       └── audit.py              # Audit trails, compliance logs
├── tests/
│   ├── __init__.py
│   ├── test_steganography.py
│   ├── test_encryption.py
│   └── test_validation.py
├── docs/
│   ├── ARCHITECTURE.md           # This file
│   ├── ROADMAP.md                # Implementation timeline
│   ├── SECURITY.md               # Security considerations
│   └── API.md                    # API documentation
├── docker/
│   ├── Dockerfile                # Container image
│   └── docker-compose.yml        # Orchestration
├── examples/
│   ├── basic_embed.py
│   ├── basic_extract.py
│   └── batch_processing.py
├── setup.py                      # Package setup
├── requirements.txt              # Dependencies
├── README.md                     # Project overview
└── LICENSE                       # MIT License
```

---

## Security Data Flow

### Message Embedding Flow

```
┌──────────────────────────────────────────────────────────┐
│ User Input:                                              │
│ • Secret Message: "CLASSIFIED: Project Aurora"          │
│ • Password: "<your-password>"                           │
│ • Carrier Image: carrier.png                            │
└──────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────┐
│ Step 1: Password Hashing (SHA-256)                       │
│ Hash = SHA256("<your-password>")                         │
│ → Output: "a7f5k9x2m1b8..." (64 hex chars)              │
└──────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────┐
│ Step 2: Encryption (AES-256) - FUTURE                   │
│ Encrypted_Payload = AES256(Message, Hash)               │
│ → Output: Binary encrypted data                          │
└──────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────┐
│ Step 3: LSB Embedding                                    │
│ • Load carrier image pixels (RGB values)                │
│ • Replace LSB of each pixel with encrypted bits         │
│ • 1 byte = 3 pixels (R[0], G[0], B[0])                 │
└──────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────┐
│ Step 4: Validation                                       │
│ • Verify stego-image integrity                          │
│ • Check capacity constraints                            │
│ • Entropy analysis (detect weak passwords)              │
└──────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────┐
│ Output: Stego-Image (output.png)                         │
│ • Visually indistinguishable from carrier               │
│ • Contains encrypted message in LSB layer               │
└──────────────────────────────────────────────────────────┘
```

### Message Extraction Flow

```
Stego-Image (input.png) + Password
              ↓
    Extract LSB Layer
              ↓
    Decode Binary Data
              ↓
    Hash Password (SHA-256)
              ↓
    Decrypt with AES-256 (using hash as key)
              ↓
    Validate Message Format
              ↓
    Output: Secret Message
```

---

## Cryptographic Stack

### Current (v1.0)
- **Password Hashing**: SHA-256
- **Obfuscation**: LSB Steganography
- **Authentication**: Password-based

### Planned Enhancements

#### Phase 1: Robust Encryption (v1.5)
```python
# Before: Simple SHA-256 hashing
password_hash = hashlib.sha256(password.encode()).hexdigest()

# After: PBKDF2 key derivation
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2

key = PBKDF2(
    algorithm=hashes.SHA256(),
    length=32,
    salt=os.urandom(16),
    iterations=100000,
).derive(password.encode())

# AES-256 encryption
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

cipher = Cipher(
    algorithms.AES(key),
    modes.GCM(os.urandom(12))
).encryptor()
```

#### Phase 2: Post-Quantum (v2.0)
```python
# CRYSTALS-Kyber: Quantum-resistant key encapsulation
from liboqs import KeyEncapsulation

kem = KeyEncapsulation("Kyber512")
public_key = kem.generate_keypair()
shared_secret, ciphertext = kem.encaps(public_key)

# Use shared_secret as AES key for encryption
# CRYSTALS-Dilithium: Digital signatures
from liboqs import Signature

sig = Signature("Dilithium3")
signer_key = sig.generate_keypair()
signature = sig.sign(message, signer_key)
```

---

## Performance Considerations

### LSB Embedding Complexity

| Image Size | Capacity (bytes) | Embedding Time | Notes |
|-----------|-----------------|-----------------|-------|
| 256×256   | ~21 KB          | 50-100 ms       | Small images, quick ops |
| 512×512   | ~85 KB          | 200-300 ms      | Medium images |
| 1024×1024 | ~340 KB         | 800-1000 ms     | Large images |
| 4K        | ~1.3 MB         | 3-5 sec         | High capacity |

### Encryption Overhead

| Algorithm | Key Size | Speed | Quantum-Safe |
|-----------|----------|-------|-------------|
| SHA-256   | 256-bit  | ~10μs/KB | ❌ |
| AES-256   | 256-bit  | ~1-2μs/KB | ❌ |
| PBKDF2    | 256-bit  | ~100ms (100k iter) | ❌ |
| Kyber512  | 2.4 KB   | ~100μs | ✅ |
| Dilithium3 | 2.95 KB | ~500μs | ✅ |

---

## Integration Points for Future Phases

### OAuth2 / Enterprise Auth (Phase 2)
```python
# Proposed integration with OAuth2 provider
@app.route('/oauth/callback')
def oauth_callback():
    # Exchange auth code for token
    # Verify user identity
    # Create session with audit logging
    pass
```

### Cloud Deployment (Phase 3)
```dockerfile
# Containerized Steganox
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "-m", "steganox.ui.web.app"]
```

### Audit Logging (Phase 4)
```python
# Compliance-grade audit trail
@dataclass
class AuditLog:
    timestamp: datetime
    user_id: str
    action: str  # "embed", "extract", "delete"
    image_hash: str
    status: str  # "success", "failure"
    ip_address: str
```

---

## Development Roadmap

See [ROADMAP.md](./ROADMAP.md) for detailed timeline and implementation steps.

## Security Considerations

See [SECURITY.md](./SECURITY.md) for threat models and security practices.
