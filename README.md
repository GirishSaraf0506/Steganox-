# 🔐 Steganox - Applied Steganography + Cryptography

> **Enterprise-grade steganography platform** combining LSB steganography with AES encryption for covert data transmission and storage. Designed for cybersecurity professionals, penetration testers, and researchers.

A Python-based steganographic tool that hides secret messages inside images using **Least Significant Bit (LSB)** encoding combined with **AES-256 encryption**. This project demonstrates layered security principles—obfuscation + encryption—making it harder for attackers to detect and decrypt sensitive data.

---

## 🔐 Why Steganox Stands Out

### **Cybersecurity Relevance**
In 2026, data breaches and AI-powered attacks are escalating. While most candidates discuss encryption or hashing, **Steganox applies steganography—a niche but powerful technique** that hides information in plain sight. This approach makes detection significantly harder than traditional encryption alone.

### **Recruiter Appeal**
- **Unique Skill Combination**: Most candidates don't showcase applied steganography + cryptography together
- **Real-World Use Cases**: Covert communications, digital watermarking, secure data exfiltration detection
- **Technical Depth**: Demonstrates understanding of low-level image manipulation, cryptographic best practices, and security layering

### **Security Layering Concept**
Steganox combines multiple security layers:
1. **Obfuscation**: LSB steganography hides the very existence of the message
2. **Encryption**: AES-256 ensures confidentiality if the stego-image is detected
3. **Authentication**: SHA-256 password hashing prevents unauthorized access

---

## 🚀 Current Features

- 🔐 **Hide Text Messages**: Embed sensitive data in `.png`, `.bmp`, `.jpg` images
- 🖼️ **Hide Images**: Conceal one image within another using LSB encoding
- 📦 **AES-256 Encryption**: Optional encryption before embedding (roadmap enhancement)
- 🔑 **Password Protection**: SHA-256 hashing for authentication
- 🖥️ **GUI Interface**: User-friendly tkinter-based application
- 📧 **Email Integration**: Send stego-images securely (foundation for future OAuth2)
- 🔗 **URL Support**: Hide links and extract them directly from stego-images

---

## ⚙️ Technical Depth Highlighted

### **LSB (Least Significant Bit) Steganography**
- Embeds secret data in the **lowest-order bit** of pixel values (R, G, B channels)
- Makes changes **imperceptible to the human eye** (<0.4% change in color)
- Capacity: ~1 byte per 3 pixels (minimal visual degradation)

### **AES-256 Encryption** (Current + Roadmap)
- Encrypts hidden data **before embedding** into the image
- Even if stego-image is detected, encrypted payload remains secure
- Demonstrates **defense-in-depth** architecture

### **Password-Based Key Derivation**
- Uses SHA-256 hashing for deterministic key generation
- Foundation for future **PBKDF2** or **Argon2** implementations
- Protects against brute-force attacks

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Core** | Python 3.9+ | Steganography logic |
| **Image Processing** | Pillow (PIL) | Image manipulation & format handling |
| **Numerical Computing** | NumPy | Pixel-level operations, bit manipulation |
| **Current Encryption** | SHA-256 (hashlib) | Password hashing & authentication |
| **GUI** | Tkinter | Cross-platform user interface |
| **Optional Comms** | smtplib | Email delivery of stego-images |

**Future Stack Additions:**
- **cryptography** library for AES-256 integration
- **liboqs** for post-quantum algorithms (Kyber, Dilithium)
- **Flask/FastAPI** for web dashboard
- **Docker** for containerization
- **PostgreSQL** for audit logging

---

## 📦 Installation

```bash
git clone https://github.com/your-username/steganox.git
cd steganox
pip install -r requirements.txt
python steganox.py
```

### Requirements
```
Pillow>=9.0
numpy>=1.21
stegano>=0.11
cryptography>=3.4  # For future AES integration
```

---

## 🚀 Usage Examples

### **Embed a Secret Message**
```python
from steganox import Steganox

# Initialize with carrier image
stego = Steganox("carrier_image.png")

# Hide encrypted message
stego.hide_message(
    secret="CLASSIFIED: Project Aurora",
    password="<your-password>"
)

# Save stego-image
stego.save("output.png")
```

### **Extract Secret Message**
```python
# Reveal hidden message
message = stego.reveal_message(password="<your-password>")
print(message)  # Output: "CLASSIFIED: Project Aurora"
```

---

## 🔐 Security Architecture

```
┌─────────────────────────────────────────┐
│     Plain Text Secret Message           │
├─────────────────────────────────────────┤
│              ↓ (AES-256)                │
├─────────────────────────────────────────┤
│         Encrypted Payload               │
├─────────────────────────────────────────┤
│      ↓ (LSB Steganography)              │
├─────────────────────────────────────────┤
│   Stego-Image (Imperceptible Changes)   │
└─────────────────────────────────────────┘
```

**Defense Layers:**
1. **LSB Obfuscation**: Attacker doesn't know data exists
2. **AES Encryption**: Even if detected, data is unreadable
3. **Password Authentication**: Access control via SHA-256
4. **Entropy Analysis** (Roadmap): Detect weak keys

---

## 🗺️ Roadmap: Enterprise-Ready Features

### **Phase 1: Post-Quantum Cryptography** 🚀
- [ ] Integrate **CRYSTALS-Kyber** (key encapsulation) for quantum-resistant key exchange
- [ ] Add **CRYSTALS-Dilithium** for digital signatures
- [ ] Document quantum-threat scenarios

### **Phase 2: Enterprise Authentication** 🏢
- [ ] **OAuth2 / SAML** integration for user management
- [ ] **Zero Trust Framework** compatibility
- [ ] Role-based access control (RBAC)

### **Phase 3: Web UI & Scalability** 🌐
- [ ] **Flask/FastAPI** web dashboard
- [ ] **Docker** containerization
- [ ] **AWS/GCP/Azure** cloud deployment
- [ ] **Kubernetes** orchestration support

### **Phase 4: Security & Compliance** 🛡️
- [ ] **Entropy analysis** to detect weak keys
- [ ] **Audit logging** with tamper-proof trails
- [ ] **FIPS 140-2** compliance documentation
- [ ] **GDPR/SOC2** alignment

### **Phase 5: Advanced Features** 🔬
- [ ] **Steganography detection algorithms** (steganalysis resistance)
- [ ] **Batch processing** for enterprise workflows
- [ ] **Hardware security module (HSM)** integration
- [ ] **Multi-layer embedding** for higher capacity

---

## 📊 Competitive Advantages

| Feature | Steganox | OpenStego | SilentEye |
|---------|----------|-----------|----------|
| **LSB Steganography** | ✅ | ✅ | ✅ |
| **AES Encryption** | 🔄 Roadmap | ❌ | ❌ |
| **Post-Quantum Crypto** | 🔄 Roadmap | ❌ | ❌ |
| **Enterprise Auth** | 🔄 Roadmap | ❌ | ❌ |
| **Web UI** | 🔄 Roadmap | ✅ | ❌ |
| **Cloud-Ready** | 🔄 Roadmap | ❌ | ❌ |
| **Audit Logging** | 🔄 Roadmap | ❌ | ❌ |

---

## 🤝 Contributing

Contributions are welcome! Areas of focus:
- Post-quantum algorithm implementations
- Web UI development
- Steganalysis resistance testing
- Security audit and penetration testing
- Documentation and tutorials

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🔗 Resources & References

- **LSB Steganography**: [Least Significant Bit Encoding](https://en.wikipedia.org/wiki/Steganography#Least_significant_bit)
- **Post-Quantum Cryptography**: [NIST PQC Standards](https://csrc.nist.gov/projects/post-quantum-cryptography/)
- **AES-256**: [NIST FIPS 197](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197.pdf)
- **Enterprise Authentication**: [OWASP OAuth2 Guide](https://owasp.org/www-community/attacks/oauth)

---

## 👤 Author

**Your Name** - Cybersecurity Engineer & Python Developer  
*Passionate about applied cryptography, steganography, and secure system design.*


