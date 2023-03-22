import pytest

import screen_animator.image_loading
from screen_animator.image_loading import ImageLoader, load_raster_image, load_svg_image


class TestImageLoader:
    @pytest.mark.parametrize(
        "input_file, output",
        [
            ("test1.bmp", "raster"),
            ("test2.png", "raster"),
            ("test3.svg", "svg"),
            ("test4.svg", "svg"),
        ],
    )
    @pytest.mark.xfail
    def test_load_image_file_type(
        self, input_file: str, output: str, monkeypatch
    ) -> None:
        """Correct loader function is used for loading images."""
        monkeypatch.setattr(
            screen_animator.image_loading, "load_raster_image", lambda x, y: "raster"
        )
        monkeypatch.setattr(
            screen_animator.image_loading, "load_svg_image", lambda x, y: "svg"
        )
        image_loader = ImageLoader()
        image = image_loader.load_image(input_file, -1)

        assert image == output


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
