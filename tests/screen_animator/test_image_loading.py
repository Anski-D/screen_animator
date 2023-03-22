import pytest

from screen_animator.image_loading import load_raster_image, load_svg_image


def test_load_raster_image_file_not_found() -> None:
    """`FileNotFoundError` not raised further when image files are not found."""
    try:
        load_raster_image("test1.bmp", -1)
    except FileNotFoundError as error:
        assert False, f"{error}"


def test_load_svg_image_file_not_found() -> None:
    """`FileNotFoundError` not raised further when image files are not found."""
    try:
        load_svg_image("test1.svg", -1)
    except FileNotFoundError as error:
        assert False, f"{error}"
