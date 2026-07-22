"""Shared pytest fixtures."""

import os
import tempfile

import numpy as np
import pytest
from PIL import Image


@pytest.fixture
def test_image_path():
    """Create a 256x256 random RGB PNG for testing."""
    arr = np.random.randint(0, 256, (256, 256, 3), dtype=np.uint8)
    img = Image.fromarray(arr)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        img.save(f.name)
        yield f.name
    os.unlink(f.name)


@pytest.fixture
def tmp_output(tmp_path):
    return str(tmp_path / "stego_output.png")
