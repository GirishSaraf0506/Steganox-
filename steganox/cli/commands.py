"""
Steganox CLI — embed and extract messages from the command line.

Usage:
    python -m steganox.cli.commands embed -i carrier.png -o output.png -m "secret"
    python -m steganox.cli.commands extract -i output.png
"""

import argparse
import getpass
import sys

from steganox.core.steganography import SteganoxEngine
from steganox.core.validation import validate_image, validate_password_strength


def cmd_embed(args):
    password = getpass.getpass("Password: ")
    valid_pwd, info = validate_password_strength(password)
    if not valid_pwd:
        print("⚠️  Weak password:")
        for issue in info["issues"]:
            print(f"   - {issue}")

    valid_img, msg = validate_image(args.input)
    if not valid_img:
        print(f"❌ {msg}")
        sys.exit(1)

    engine = SteganoxEngine()
    try:
        result = engine.embed(args.input, args.message, password)
        result.save(args.output)
        print(f"✅ Stego-image saved to: {args.output}")
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)


def cmd_extract(args):
    password = getpass.getpass("Password: ")
    engine = SteganoxEngine()
    try:
        message = engine.extract(args.input, password)
        print(f"\n🔓 Extracted message:\n{message}")
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        prog="steganox",
        description="🔐 Steganox — LSB Steganography + AES-256 Encryption",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    embed_p = sub.add_parser("embed", help="Hide a message in an image")
    embed_p.add_argument("-i", "--input", required=True, help="Carrier image path")
    embed_p.add_argument(
        "-o", "--output", required=True, help="Output stego-image path"
    )
    embed_p.add_argument(
        "-m", "--message", required=True, help="Secret message to hide"
    )
    embed_p.set_defaults(func=cmd_embed)

    extract_p = sub.add_parser("extract", help="Extract a hidden message from an image")
    extract_p.add_argument("-i", "--input", required=True, help="Stego-image path")
    extract_p.set_defaults(func=cmd_extract)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
