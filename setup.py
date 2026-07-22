from setuptools import setup, find_packages

setup(
    name="steganox",
    version="1.0.0",
    description="Applied Steganography + Cryptography Platform",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "Pillow>=9.0",
        "numpy>=1.21",
        "cryptography>=41.0",
        "Flask>=2.3",
        "Werkzeug>=2.3",
    ],
    entry_points={
        "console_scripts": [
            "steganox=steganox.cli.commands:main",
        ],
    },
)
