"""
Tests for image utilities.
"""

import pytest
import io
from PIL import Image
import os

from gyvatukas.utils.image import (
    convert_to_base64,
    get_image_cropped_to_context,
    get_optimized_image_as_jpeg,
    get_image_info,
)


@pytest.fixture(params=["jpg", "png", "webp"])
def test_image_bytes(request):
    """Fixture that provides test image bytes in different formats."""
    format_name = request.param
    test_image_path = f"tests/assets/test_image.{format_name}"

    if not os.path.exists(test_image_path):
        pytest.skip(f"Test image not found at {test_image_path}")

    with open(test_image_path, "rb") as f:
        return f.read(), format_name


def create_test_image(
    width: int = 100, height: int = 100, color: str = "white"
) -> bytes:
    """Create a test image and return its bytes."""
    image = Image.new("RGB", (width, height), color=color)
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="JPEG")
    return image_bytes.getvalue()


def create_complex_test_image(width: int = 100, height: int = 100) -> bytes:
    """Create a test image with complex content that shows quality differences."""
    image = Image.new("RGB", (width, height), color="white")

    # Add gradients and patterns that will show quality differences
    for x in range(width):
        for y in range(height):
            # Create a gradient pattern
            r = int((x / width) * 255)
            g = int((y / height) * 255)
            b = int(((x + y) / (width + height)) * 255)

            # Add some noise for more complexity
            if (x + y) % 10 == 0:
                r = min(255, r + 50)
                g = min(255, g + 30)
                b = min(255, b + 40)

            image.putpixel((x, y), (r, g, b))

    image_bytes = io.BytesIO()
    image.save(image_bytes, format="JPEG")
    return image_bytes.getvalue()


def create_content_image() -> bytes:
    """Create a test image with content in the center."""
    image = Image.new("RGB", (200, 200), color="white")
    # Draw a black rectangle in the center
    for x in range(50, 150):
        for y in range(50, 150):
            image.putpixel((x, y), (0, 0, 0))
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="JPEG")
    return image_bytes.getvalue()


def test_convert_to_base64(test_image_bytes):
    """Test base64 conversion."""
    image_bytes, format_name = test_image_bytes
    result = convert_to_base64(image_bytes, format_name)

    assert result.startswith(f"data:image/{format_name};base64,")
    assert len(result) > 100  # Should have substantial base64 content

    # Test with different extensions
    result_png = convert_to_base64(image_bytes, ".png")
    assert result_png.startswith("data:image/png;base64,")


def test_get_image_cropped_to_context(test_image_bytes):
    """Test image cropping to content."""
    image_bytes, format_name = test_image_bytes

    # Test with real image
    result = get_image_cropped_to_context(image_bytes)
    assert len(result) > 0

    # Test with padding parameter
    result_with_padding = get_image_cropped_to_context(image_bytes, padding=20)
    assert len(result_with_padding) > 0


def test_get_optimized_image_as_jpeg(test_image_bytes):
    """Test image optimization."""
    image_bytes, format_name = test_image_bytes

    # Test basic optimization
    result = get_optimized_image_as_jpeg(image_bytes)
    assert result != image_bytes  # Should be optimized
    assert len(result) > 0

    # Test with different quality levels
    result_high_quality = get_optimized_image_as_jpeg(image_bytes, quality=95)
    result_low_quality = get_optimized_image_as_jpeg(image_bytes, quality=50)

    # Higher quality should be larger
    assert len(result_high_quality) > len(result_low_quality)


def test_get_image_info(test_image_bytes):
    """Test getting image information."""
    image_bytes, format_name = test_image_bytes
    info = get_image_info(image_bytes)

    assert info["width"] > 0
    assert info["height"] > 0
    assert info["format"] in ["JPEG", "PNG", "WEBP"]
    assert info["size_bytes"] == len(image_bytes)


def test_rgba_conversion():
    """Test RGBA to RGB conversion."""
    # Create RGBA image
    rgba_image = Image.new("RGBA", (50, 50), color=(255, 0, 0, 128))
    rgba_bytes = io.BytesIO()
    rgba_image.save(rgba_bytes, format="PNG")
    rgba_bytes = rgba_bytes.getvalue()

    # Test that RGBA images are handled correctly
    result = get_optimized_image_as_jpeg(rgba_bytes)
    result_image = Image.open(io.BytesIO(result))

    assert result_image.mode == "RGB"
    assert len(result) > 0


def test_empty_image_handling():
    """Test handling of edge cases."""
    # Test with very small image
    small_image = Image.new("RGB", (1, 1), color="red")
    small_bytes = io.BytesIO()
    small_image.save(small_bytes, format="JPEG")
    small_bytes = small_bytes.getvalue()

    # All functions should handle small images gracefully
    result = get_optimized_image_as_jpeg(small_bytes)
    assert len(result) > 0

    info = get_image_info(small_bytes)
    assert info["width"] == 1
    assert info["height"] == 1
