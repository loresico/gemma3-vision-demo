"""
Pytest configuration and shared fixtures.

This file contains pytest configuration and fixtures that are available
to all test modules.
"""
import pytest
from PIL import Image


@pytest.fixture
def sample_red_image():
    """Create a sample red 100x100 image."""
    return Image.new('RGB', (100, 100), color='red')


@pytest.fixture
def sample_green_image():
    """Create a sample green 100x100 image."""
    return Image.new('RGB', (100, 100), color='green')


@pytest.fixture
def sample_blue_image():
    """Create a sample blue 100x100 image."""
    return Image.new('RGB', (100, 100), color='blue')


@pytest.fixture
def large_image():
    """Create a large 1920x1080 image."""
    return Image.new('RGB', (1920, 1080), color='white')


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests (deselect with '-m \"not integration\"')"
    )
