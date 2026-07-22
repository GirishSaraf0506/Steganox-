# Steganox Enhancement Guide

Quick-reference implementation guide for core enhancements from the roadmap. Use this to implement features systematically.

---

## Enhancement 1: AES-256 Encryption Integration

**Priority**: HIGH | **Effort**: 20 hours | **Timeline**: v1.5

### Current State
```python
# Current: Weak password hashing
import hashlib

password = "<your-password>"
password_hash = hashlib.sha256(password.encode()).hexdigest()
message_with_hash = f"{password_hash}:{message}"
secret = lsb.hide(filename, message_with_hash)
```

**Issues**: 
- ❌ SHA-256 is too fast for password hashing (vulnerable to brute force)
- ❌ No encryption layer (message visible if LSB is detected)

### Target State
```python
# Future: Strong encryption
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.primitives import hashes
import os

def encrypt_message(message: str, password: str) -> bytes:
    # Derive 256-bit key from password
    salt = os.urandom(16)
    kdf = PBKDF2(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,  # 100k iterations = ~100ms
    )
    key = kdf.derive(password.encode())
    
    # Encrypt with AES-256-GCM
    iv = os.urandom(12)
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv)).encryptor()
    ciphertext = cipher.update(message.encode()) + cipher.finalize()
    
    # Return: salt + iv + ciphertext + tag
    return salt + iv + ciphertext + cipher.tag

def decrypt_message(encrypted_data: bytes, password: str) -> str:
    # Extract components
    salt = encrypted_data[:16]
    iv = encrypted_data[16:28]
    ciphertext = encrypted_data[28:-16]
    tag = encrypted_data[-16:]
    
    # Derive same key from password
    kdf = PBKDF2(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = kdf.derive(password.encode())
    
    # Decrypt
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag)).decryptor()
    message = cipher.update(ciphertext) + cipher.finalize()
    
    return message.decode()
```

### Implementation Checklist
- [ ] Install `cryptography` library: `pip install cryptography>=41.0`
- [ ] Create `steganox/core/encryption.py` module
- [ ] Implement `encrypt_message()` function
- [ ] Implement `decrypt_message()` function
- [ ] Create unit tests in `tests/test_encryption.py`
- [ ] Update GUI to use new encryption
- [ ] Update README with encryption details
- [ ] Security audit of implementation

### Code Location
- Create: `steganox/core/encryption.py`
- Update: `steganox.py` (GUI integration)
- Add tests: `tests/test_encryption.py`

---

## Enhancement 2: Web Dashboard (Flask)

**Priority**: HIGH | **Effort**: 25 hours | **Timeline**: v1.5

### Project Structure
```
steganox/ui/web/
├── __init__.py
├── app.py              # Flask application
├── routes.py           # URL endpoints
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
└── templates/
    ├── base.html       # Base template
    ├── index.html      # Dashboard home
    ├── embed.html      # Embed message
    └── extract.html    # Extract message
```

### Core Implementation

**app.py**:
```python
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from steganox.core.steganography import SteganoxEngine

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB limit
app.config['UPLOAD_FOLDER'] = 'uploads'

engine = SteganoxEngine()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/embed', methods=['POST'])
def embed():
    try:
        image = request.files['image']
        message = request.form.get('message')
        password = request.form.get('password')
        
        # Validate inputs
        if not image or not message or not password:
            return jsonify({'error': 'Missing fields'}), 400
        
        filename = secure_filename(image.filename)
        image.save(f'uploads/{filename}')
        
        # Embed message
        result = engine.embed(
            image_path=f'uploads/{filename}',
            message=message,
            password=password
        )
        
        # Save result
        output_path = f'uploads/stego_{filename}'
        result.save(output_path)
        
        return jsonify({
            'success': True,
            'output_file': output_path,
            'message': 'Message embedded successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/extract', methods=['POST'])
def extract():
    try:
        image = request.files['image']
        password = request.form.get('password')
        
        if not image or not password:
            return jsonify({'error': 'Missing fields'}), 400
        
        filename = secure_filename(image.filename)
        image.save(f'uploads/{filename}')
        
        # Extract message
        message = engine.extract(
            image_path=f'uploads/{filename}',
            password=password
        )
        
        return jsonify({
            'success': True,
            'message': message
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=False, host='0.0.0.0', port=5000)
```

**templates/index.html**:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Steganox - Steganography Tool</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <div class="container">
        <h1>🔐 Steganox</h1>
        
        <div class="tabs">
            <button class="tab-button active" onclick="switchTab('embed')">Embed Message</button>
            <button class="tab-button" onclick="switchTab('extract')">Extract Message</button>
        </div>
        
        <div id="embed" class="tab-content active">
            <form id="embedForm">
                <input type="file" id="embedImage" accept="image/*" required>
                <textarea id="embedMessage" placeholder="Enter secret message" required></textarea>
                <input type="password" id="embedPassword" placeholder="Enter password" required>
                <button type="submit">Embed Message</button>
            </form>
            <div id="embedResult"></div>
        </div>
        
        <div id="extract" class="tab-content">
            <form id="extractForm">
                <input type="file" id="extractImage" accept="image/*" required>
                <input type="password" id="extractPassword" placeholder="Enter password" required>
                <button type="submit">Extract Message</button>
            </form>
            <div id="extractResult"></div>
        </div>
    </div>
    
    <script src="{{ url_for('static', filename='js/app.js') }}"></script>
</body>
</html>
```

### Implementation Checklist
- [ ] Install Flask: `pip install Flask>=2.3`
- [ ] Create `steganox/ui/web/app.py`
- [ ] Create `steganox/ui/web/routes.py`
- [ ] Create HTML templates
- [ ] Create CSS styling
- [ ] Implement file upload handling
- [ ] Add input validation
- [ ] Security headers (CSP, X-Frame-Options)
- [ ] Error handling & logging
- [ ] Unit tests for routes
- [ ] Load testing

---

## Enhancement 3: Docker Containerization

**Priority**: MEDIUM | **Effort**: 8 hours | **Timeline**: v1.5

### Dockerfile

```dockerfile
# Multi-stage build for smaller image
FROM python:3.9-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.9-slim

# Security: Create non-root user
RUN groupadd -r steganox && useradd -r -g steganox steganox

WORKDIR /app

# Copy only necessary files
COPY --from=builder /root/.local /home/steganox/.local
COPY steganox/ steganox/
COPY README.md .
COPY LICENSE .

# Set environment
ENV PATH=/home/steganox/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# Security: Change ownership
RUN chown -R steganox:steganox /app

USER steganox

EXPOSE 5000

CMD ["python", "-m", "steganox.ui.web.app"]
```

### docker-compose.yml

```yaml
version: '3.9'

services:
  steganox:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    volumes:
      - ./uploads:/app/uploads
    environment:
      - FLASK_ENV=production
      - FLASK_DEBUG=0
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true
```

### Build & Run

```bash
# Build image
docker build -t steganox:latest .

# Run container
docker run -p 5000:5000 steganox:latest

# Or use docker-compose
docker-compose up -d

# View logs
docker logs -f <container_id>
```

### Implementation Checklist
- [ ] Create Dockerfile
- [ ] Create docker-compose.yml
- [ ] Test image builds successfully
- [ ] Test container runs correctly
- [ ] Add security scanning (.hadolint)
- [ ] Document build process
- [ ] Add .dockerignore file

---

## Enhancement 4: Core Module Refactoring

**Priority**: HIGH | **Effort**: 15 hours | **Timeline**: v1.5

### Create `steganox/core/steganography.py`

```python
"""
Core steganography engine for LSB embedding and extraction.
"""

from PIL import Image
import numpy as np
from typing import Tuple
import os

class SteganoxEngine:
    """Main steganography engine"""
    
    def __init__(self):
        self.max_message_size = None
    
    def embed(self, image_path: str, message: str, password: str) -> Image.Image:
        """
        Embed encrypted message into image using LSB steganography.
        
        Args:
            image_path: Path to carrier image
            message: Secret message to hide
            password: Password for encryption
            
        Returns:
            PIL Image with embedded message
            
        Raises:
            ValueError: If message too large for image
            IOError: If image cannot be read
        """
        # Load image
        carrier = Image.open(image_path).convert('RGB')
        carrier_array = np.array(carrier)
        
        # Encrypt message
        from steganox.core.encryption import encrypt_message
        encrypted_payload = encrypt_message(message, password)
        
        # Convert bytes to bits
        payload_bits = self._bytes_to_bits(encrypted_payload)
        
        # Check capacity
        max_bits = carrier_array.size
        if len(payload_bits) > max_bits:
            raise ValueError(
                f"Message too large. Max: {max_bits // 8} bytes, "
                f"Got: {len(encrypted_payload)} bytes"
            )
        
        # Embed LSBs
        carrier_flat = carrier_array.flatten()
        for i, bit in enumerate(payload_bits):
            carrier_flat[i] = (carrier_flat[i] & 0xFE) | int(bit)
        
        # Reshape and create image
        result_array = carrier_flat.reshape(carrier_array.shape)
        result_image = Image.fromarray(result_array.astype('uint8'))
        
        return result_image
    
    def extract(self, image_path: str, password: str) -> str:
        """
        Extract and decrypt hidden message from image.
        
        Args:
            image_path: Path to stego-image
            password: Password for decryption
            
        Returns:
            Decrypted secret message
            
        Raises:
            ValueError: If password incorrect
            IOError: If image cannot be read
        """
        # Load image
        stego = Image.open(image_path).convert('RGB')
        stego_array = np.array(stego)
        
        # Extract LSBs (raw bits)
        stego_flat = stego_array.flatten()
        lsb_bits = stego_flat & 0x01
        
        # Convert bits to bytes
        encrypted_payload = self._bits_to_bytes(lsb_bits)
        
        # Decrypt message
        from steganox.core.encryption import decrypt_message
        try:
            message = decrypt_message(encrypted_payload, password)
            return message
        except Exception as e:
            raise ValueError(f"Decryption failed (wrong password?): {str(e)}")
    
    @staticmethod
    def _bytes_to_bits(data: bytes) -> list:
        """Convert bytes to list of bits"""
        bits = []
        for byte in data:
            for i in range(8):
                bits.append((byte >> i) & 1)
        return bits
    
    @staticmethod
    def _bits_to_bytes(bits: np.ndarray) -> bytes:
        """Convert array of bits to bytes"""
        # Pad to multiple of 8
        if len(bits) % 8 != 0:
            bits = np.pad(bits, (0, 8 - len(bits) % 8))
        
        # Convert to bytes
        bytes_array = []
        for i in range(0, len(bits), 8):
            byte = 0
            for j in range(8):
                byte |= (bits[i + j] << j)
            bytes_array.append(byte)
        
        return bytes(bytes_array)
```

### Create `steganox/core/validation.py`

```python
"""Image and payload validation"""

from PIL import Image
import os

def validate_image(image_path: str) -> Tuple[bool, str]:
    """Validate image meets requirements"""
    try:
        img = Image.open(image_path)
        
        # Format check
        if img.format not in ['PNG', 'BMP', 'JPEG']:
            return False, "Unsupported format"
        
        # Size check
        size_mb = os.path.getsize(image_path) / (1024 * 1024)
        if size_mb > 100:
            return False, "Image too large (>100MB)"
        
        # Dimensions check
        if img.size[0] * img.size[1] > 16384 * 16384:
            return False, "Resolution too high"
        
        return True, "Valid"
    except Exception as e:
        return False, str(e)

def validate_message(message: str, max_size: int) -> Tuple[bool, str]:
    """Validate message before embedding"""
    if not message:
        return False, "Message cannot be empty"
    if len(message.encode()) > max_size:
        return False, "Message too large"
    return True, "Valid"
```

### Implementation Checklist
- [ ] Create `steganox/core/` directory
- [ ] Create `steganox/core/__init__.py`
- [ ] Create `steganox/core/steganography.py`
- [ ] Create `steganox/core/encryption.py`
- [ ] Create `steganox/core/validation.py`
- [ ] Create comprehensive docstrings
- [ ] Add type hints throughout
- [ ] Create unit tests
- [ ] Update imports in main app

---

## Enhancement 5: Unit Testing

**Priority**: HIGH | **Effort**: 20 hours | **Timeline**: v1.5

### Create `tests/test_steganography.py`

```python
import pytest
import numpy as np
from PIL import Image
import tempfile
import os

from steganox.core.steganography import SteganoxEngine

@pytest.fixture
def engine():
    return SteganoxEngine()

@pytest.fixture
def test_image():
    """Create a test image"""
    arr = np.random.randint(0, 256, (256, 256, 3), dtype=np.uint8)
    img = Image.fromarray(arr)
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        img.save(f.name)
        yield f.name
    os.unlink(f.name)

def test_embed_and_extract(engine, test_image):
    """Test message roundtrip"""
    message = "Test message"
    password = "<your-password>"
    
    # Embed
    stego = engine.embed(test_image, message, password)
    
    # Save temporarily
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        stego.save(f.name)
        stego_path = f.name
    
    try:
        # Extract
        extracted = engine.extract(stego_path, password)
        assert extracted == message
    finally:
        os.unlink(stego_path)

def test_wrong_password_fails(engine, test_image):
    """Test extraction with wrong password"""
    message = "Secret"
    password = "<your-password>"
    wrong_password = "<wrong-password>"
    
    stego = engine.embed(test_image, message, password)
    
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        stego.save(f.name)
        stego_path = f.name
    
    try:
        with pytest.raises(ValueError):
            engine.extract(stego_path, wrong_password)
    finally:
        os.unlink(stego_path)
```

### Running Tests

```bash
# Install pytest
pip install pytest pytest-cov

# Run tests
pytest tests/ -v

# With coverage report
pytest tests/ --cov=steganox --cov-report=html
```

### Implementation Checklist
- [ ] Create `tests/` directory
- [ ] Create `tests/__init__.py`
- [ ] Create `tests/conftest.py` (fixtures)
- [ ] Create `tests/test_steganography.py`
- [ ] Create `tests/test_encryption.py`
- [ ] Create `tests/test_validation.py`
- [ ] Achieve >80% code coverage
- [ ] Set up GitHub Actions CI/CD
- [ ] Add coverage badges to README

---

## Enhancement 6: Post-Quantum Crypto Roadmap (Future)

**Priority**: MEDIUM | **Effort**: 30 hours | **Timeline**: v2.0

### Kyber Key Encapsulation

```python
from liboqs import KeyEncapsulation
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

class HybridKeyExchange:
    """Combine classical (ECDH) + post-quantum (Kyber) for hybrid security"""
    
    def __init__(self):
        self.kyber = KeyEncapsulation("Kyber512")
    
    def generate_hybrid_key(self, password: str) -> bytes:
        """Generate hybrid encryption key"""
        # Generate Kyber keypair
        kyber_public = self.kyber.generate_keypair()
        kyber_secret, kyber_cipher = self.kyber.encaps(kyber_public)
        
        # Combine with password-derived key
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'steganox-hybrid',
        )
        
        # Derive final key from kyber secret + password
        final_key = hkdf.derive(kyber_secret + password.encode())
        return final_key
```

### Implementation Checklist (for v2.0)
- [ ] Install liboqs: `pip install liboqs-python`
- [ ] Create `steganox/crypto/pqc.py`
- [ ] Implement Kyber key exchange
- [ ] Implement Dilithium signing
- [ ] Create hybrid encryption mode
- [ ] Write comprehensive tests
- [ ] Backward compatibility checks
- [ ] Security audit

---

## Implementation Priority & Timeline

```
WEEK 1-2  │ Enhancement 2 (Web Dashboard)
          │ Enhancement 1 (AES Encryption)
────────┤
WEEK 3-4  │ Enhancement 4 (Core Refactoring)
          │ Enhancement 3 (Docker)
────────┤
WEEK 5-6  │ Enhancement 5 (Testing)
          │ Documentation
────────┤
WEEK 7-8  │ Code review, security audit
          │ Release v1.5
```

---

## Quick Start

1. **Pick an enhancement** from above
2. **Follow the implementation checklist**
3. **Create tests** as you code
4. **Commit frequently** with clear messages
5. **Get code review** before merging

---

## Reference Links

- [Cryptography Library Docs](https://cryptography.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [NIST Cryptography Standards](https://csrc.nist.gov/)
- [liboqs Documentation](https://liboqs-python.readthedocs.io/)
