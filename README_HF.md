---
title: Steganox
emoji: 🔐
colorFrom: cyan
colorTo: blue
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
short_description: LSB Steganography + AES-256 Encryption
---

# 🔐 Steganox - Applied Steganography + Cryptography

Hide secret messages inside images using **LSB steganography** + **AES-256-GCM encryption**.

## How it works
1. **Embed** — message is encrypted with AES-256, then hidden in pixel LSBs
2. **Extract** — LSBs are read and decrypted using your password

## Security
- AES-256-GCM encryption with PBKDF2-HMAC-SHA256 key derivation (100k iterations)
- Changes are imperceptible to the human eye (<0.4% pixel change)

[GitHub Repository](https://github.com/GirishSaraf0506/Steganox-)
