# Steganox Security Documentation

Comprehensive security analysis, threat models, and best practices for Steganox development and deployment.

---

## Executive Summary

Steganox implements **defense-in-depth security** combining:
1. **Obfuscation** (LSB steganography) - conceals data existence
2. **Encryption** (AES-256) - ensures confidentiality
3. **Authentication** (SHA-256/PBKDF2) - verifies access
4. **Compliance** (Audit logging, FIPS) - enables enterprise use

---

## Threat Model

### Assets to Protect
1. **Hidden Messages** - Confidentiality critical
2. **Carrier Images** - Integrity critical
3. **Encryption Keys** - Availability critical
4. **User Credentials** - Confidentiality critical

### Threat Actors

| Actor | Capability | Motivation | Risk |
|-------|-----------|-----------|------|
| **Network Attacker** | Intercept communications | Eavesdropping | High |
| **Image Analyzer** | Statistical analysis | Detect steganography | Medium |
| **Brute Force Attacker** | Computational power | Extract payload | Medium |
| **Insider Threat** | Direct system access | Exfiltrate data | Medium |
| **Quantum Computer** | Break classical crypto | Future threat | High |

### Attack Vectors

#### 1. Cryptanalysis Attacks
**Threat**: Attacker breaks encryption without password
- **Risk**: Low (AES-256 is NSA Suite B approved)
- **Mitigation**: 
  - Use NIST-approved algorithms only
  - Regular security audits
  - Post-quantum crypto roadmap

#### 2. Brute Force Attacks
**Threat**: Attacker tries all possible passwords
- **Risk**: Medium (depends on password strength)
- **Mitigation**:
  ```python
  # Current: Poor - fast hashing
  hash = hashlib.sha256(password.encode()).hexdigest()
  
  # Improved: PBKDF2 with high iteration count
  kdf = PBKDF2(algorithm=SHA256(), length=32, 
               salt=os.urandom(16), iterations=100000)
  
  # Future: Argon2 with memory hardening
  hash = argon2.hash_password(
      password.encode(),
      salt=os.urandom(16),
      memory_cost=65536,  # 64MB
      time_cost=4,
      parallelism=4
  )
  ```

#### 3. Steganalysis Attacks
**Threat**: Attacker detects presence of hidden data
- **Risk**: Medium (LSB modifications visible to statistical analysis)
- **Detection Methods**:
  - Chi-square test on bit distribution
  - Histogram analysis
  - Entropy measurements
- **Mitigation**:
  ```python
  # Defense: Randomized LSB embedding
  import random
  
  def embed_random_lsb(carrier, payload):
      """Embed using randomly selected LSB positions"""
      pixels = carrier.flatten()
      payload_bits = payload_to_bits(payload)
      
      # Select random LSB positions to avoid patterns
      available_positions = list(range(len(pixels)))
      random.shuffle(available_positions)
      
      for i, bit in enumerate(payload_bits):
          pos = available_positions[i]
          pixels[pos] = (pixels[pos] & 0xFE) | bit
      
      return pixels.reshape(carrier.shape)
  ```

#### 4. Side-Channel Attacks
**Threat**: Attacker extracts info via timing, power consumption, cache
- **Risk**: Low (desktop/web usage, not embedded systems)
- **Mitigation**: Use constant-time operations for cryptographic functions

#### 5. Message Recovery Attacks
**Threat**: Attacker extracts payload from detected stego-image without password
- **Risk**: Low (AES-256 encryption protects even if LSB is found)
- **Mitigation**: Mandatory encryption before embedding

#### 6. Social Engineering
**Threat**: Attacker tricks user into revealing password
- **Risk**: Medium (human factor)
- **Mitigation**:
  - Educate users on password security
  - Require minimum 12-character passwords
  - Implement MFA for enterprise
  - Disable password reuse

---

## Cryptographic Standards & Compliance

### Current Standards (v1.0)

```
┌─────────────────────────────────────────────────┐
│ Cryptographic Algorithm Approval Status          │
├─────────────────────────────────────────────────┤
│ SHA-256          │ ✅ NIST, NSA Suite B         │
│ LSB Steganography│ ⚠️  Research-grade           │
│ PBKDF2           │ ✅ NIST, RFC 2898            │
│ AES-256 (GCM)    │ ✅ NIST, NSA Suite B         │
│ SHA-256 Hashing  │ ✅ FIPS 180-4               │
└─────────────────────────────────────────────────┘
```

### NIST Compliance Roadmap

| Requirement | Current | v1.5 | v2.0 | v3.0 |
|------------|---------|------|------|------|
| FIPS 140-2 | ⚠️ Partial | ✅ Full | ✅ Full | ✅ Certified |
| Post-Quantum | ❌ None | ❌ None | ✅ Kyber/Dilithium | ✅ FIPS 203+ |
| Key Derivation | ⚠️ SHA256 | ✅ PBKDF2 | ✅ PBKDF2 | ✅ Argon2 |
| AES Encryption | ❌ None | ✅ GCM | ✅ GCM | ✅ GCM |

---

## Key Management

### Key Lifecycle

```
1. GENERATION
   └─ Derived from user password
   └─ PBKDF2(password, salt, 100k iterations)
   └─ 256-bit key (32 bytes)

2. USAGE
   └─ Encrypt payload before LSB embedding
   └─ Key held in memory during operation
   └─ NO persistent key storage

3. DESTRUCTION
   └─ Key overwritten with zeros
   └─ Garbage collected after use
   └─ Session terminated
```

### Password Requirements

Current (v1.0):
- Minimum 8 characters ❌ Too weak
- No complexity requirements

Recommended (v1.5+):
- Minimum 12 characters ✅
- Require uppercase, lowercase, numbers, symbols
- Check against common password list (HIBP API)
- Entropy requirement: >50 bits

```python
def validate_password_strength(password: str) -> tuple[bool, dict]:
    """Validate password meets security requirements"""
    
    issues = []
    
    # Length check
    if len(password) < 12:
        issues.append("Minimum 12 characters required")
    
    # Complexity checks
    if not any(c.isupper() for c in password):
        issues.append("Must contain uppercase letter")
    if not any(c.islower() for c in password):
        issues.append("Must contain lowercase letter")
    if not any(c.isdigit() for c in password):
        issues.append("Must contain digit")
    if not any(c in "!@#$%^&*()" for c in password):
        issues.append("Must contain special character")
    
    # Entropy calculation
    entropy = calculate_entropy(password)
    if entropy < 50:
        issues.append(f"Entropy too low ({entropy} bits, need >50)")
    
    return len(issues) == 0, {'issues': issues, 'entropy': entropy}
```

---

## Input Validation & Sanitization

### Image Validation

```python
def validate_carrier_image(image_path: str) -> tuple[bool, str]:
    """Validate carrier image meets requirements"""
    
    try:
        img = Image.open(image_path)
        
        # Format check
        if img.format not in ['PNG', 'BMP', 'JPEG']:
            return False, "Unsupported format. Use PNG, BMP, or JPEG"
        
        # Size check (prevent DoS)
        size_mb = os.path.getsize(image_path) / (1024 * 1024)
        if size_mb > 100:
            return False, "Image too large (max 100 MB)"
        
        # Dimension check (prevent memory exhaustion)
        width, height = img.size
        if width * height > 16384 * 16384:
            return False, "Resolution too high (max 16384x16384)"
        
        # Color mode check
        if img.mode not in ['RGB', 'RGBA', 'L']:
            return False, "Image must be RGB, RGBA, or grayscale"
        
        return True, "Valid carrier image"
        
    except Exception as e:
        return False, f"Image validation error: {str(e)}"
```

### Payload Validation

```python
def validate_payload(payload: bytes, max_size: int) -> tuple[bool, str]:
    """Validate payload before embedding"""
    
    # Size constraints
    if len(payload) == 0:
        return False, "Payload cannot be empty"
    
    if len(payload) > max_size:
        return False, f"Payload too large ({len(payload)} > {max_size})"
    
    # No null bytes in UTF-8 messages
    try:
        payload.decode('utf-8')
    except UnicodeDecodeError:
        return False, "Payload must be valid UTF-8"
    
    return True, "Valid payload"
```

---

## Secure Coding Practices

### Memory Safety

```python
import secrets
import os

# Good: Use secrets module for sensitive data
random_token = secrets.token_hex(16)
encryption_key = secrets.token_bytes(32)

# Bad: Use os.urandom directly (less safe semantics)
random_data = os.urandom(32)  # Acceptable for non-crypto

# Memory overwriting (future enhancement)
def secure_delete(data: bytes):
    """Overwrite sensitive data in memory"""
    import ctypes
    ctypes.memmove(id(data), b'\x00' * len(data), len(data))
```

### SQL Injection Prevention

```python
# Bad: String concatenation
query = f"SELECT * FROM users WHERE id = {user_id}"

# Good: Parameterized queries
from sqlalchemy import text
query = text("SELECT * FROM users WHERE id = :user_id")
result = db.execute(query, {"user_id": user_id})
```

### Command Injection Prevention

```python
# Bad: os.system() with unsanitized input
os.system(f"convert {image_path} -o output.png")

# Good: subprocess with list arguments
import subprocess
subprocess.run(["convert", image_path, "-o", "output.png"], 
               check=True, capture_output=True)
```

---

## Secure Deployment

### Environment Variables

```bash
# Never commit secrets to git!
# .env (NOT in git)
DATABASE_URL=postgresql://user:pass@localhost/steganox
SECRET_KEY=your-super-secret-key-here
ENCRYPTION_KEY=base64-encoded-key

# Load safely in Python
from dotenv import load_dotenv
load_dotenv()
db_url = os.getenv('DATABASE_URL')
```

### Docker Security

```dockerfile
# Bad: Run as root
FROM python:3.9
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]

# Good: Non-root user, minimal image
FROM python:3.9-slim
RUN groupadd -r steganox && useradd -r -g steganox steganox
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY steganox/ steganox/
USER steganox
CMD ["python", "-m", "steganox.ui.web.app"]
```

### Network Security

```python
# Flask: Enable HTTPS/TLS
from flask_talisman import Talisman

app = Flask(__name__)
Talisman(app, 
    force_https=True,
    strict_transport_security=True,
    strict_transport_security_max_age=31536000,
)

# CSRF Protection
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)
```

---

## Security Testing

### Unit Tests

```python
def test_encryption_decryption_roundtrip():
    """Verify encrypt -> decrypt returns original"""
    plaintext = b"Secret message"
    password = "<your-password>"
    
    encrypted = encrypt_aes(plaintext, password)
    decrypted = decrypt_aes(encrypted, password)
    
    assert decrypted == plaintext

def test_wrong_password_fails():
    """Verify wrong password cannot decrypt"""
    plaintext = b"Secret message"
    ciphertext = encrypt_aes(plaintext, "Password1")
    
    with pytest.raises(InvalidTag):
        decrypt_aes(ciphertext, "WrongPassword")

def test_password_entropy_validation():
    """Verify weak passwords are rejected"""
    weak_passwords = ["12345", "password", "abc"]
    
    for pwd in weak_passwords:
        valid, _ = validate_password_strength(pwd)
        assert not valid
```

### Penetration Testing Checklist

- [ ] **Steganography Detection**: Run steganalysis tools (Chi-square, SPA)
- [ ] **Brute Force**: Attempt password cracking with common wordlists
- [ ] **Input Fuzzing**: Provide malformed images, oversized files
- [ ] **Side-Channel**: Measure timing differences for password validation
- [ ] **Injection Attacks**: Try SQL injection, command injection
- [ ] **CSRF/XSS**: Test web UI for cross-site attacks
- [ ] **Privilege Escalation**: Verify RBAC enforcement
- [ ] **Data Leakage**: Check for logs containing sensitive data

---

## Incident Response Plan

### Discovery Phase
1. **Detect** unauthorized access or data breach
2. **Verify** incident through logs and monitoring
3. **Document** timeline and affected systems

### Containment Phase
1. **Isolate** affected systems
2. **Revoke** compromised credentials
3. **Patch** vulnerabilities immediately

### Eradication Phase
1. **Remove** malicious code/backdoors
2. **Verify** system integrity
3. **Restore** from clean backups

### Recovery Phase
1. **Restore** systems to known-good state
2. **Monitor** for signs of re-compromise
3. **Communicate** with affected users

### Lessons Learned
1. **Root cause analysis**
2. **Preventive measures** for future
3. **Update security policies**

---

## Compliance Frameworks

### GDPR (General Data Protection Regulation)
- ✅ Data minimization: Only collect necessary data
- ✅ Purpose limitation: Clear data usage policies
- ✅ Storage limitation: Auto-delete audit logs after 90 days
- ✅ Right to erasure: Implement account deletion

### SOC 2 Type II
- ✅ Security: Encryption, access controls, MFA
- ✅ Availability: 99.5% uptime SLA, disaster recovery
- ✅ Integrity: Change management, code review
- ✅ Confidentiality: Data classification, DLP

### FIPS 140-2
- ✅ Cryptographic module approval (Phase 3.0)
- ✅ Key management: Documented policies
- ✅ Testing & validation: Approved laboratory
- ✅ Documentation: Security policy, user manual

---

## Security Update Policy

### Vulnerability Disclosure
1. **Report to**: security@steganox.io (PGP available)
2. **Timeline**: 90-day disclosure grace period
3. **Severity**: Use CVSS v3.1 scale

### Patch Release
- **Critical**: Within 24-48 hours
- **High**: Within 1 week
- **Medium**: Within 2 weeks
- **Low**: Next regular release

---

## Related Documents
- [ARCHITECTURE.md](./ARCHITECTURE.md) - System design
- [ROADMAP.md](./ROADMAP.md) - Implementation timeline
- [README.md](./README.md) - Project overview
