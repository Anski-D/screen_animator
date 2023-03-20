from io import BytesIO
from pathlib import Path
import logging

import cairosvg
import pygame as pg
from svgutils import transform as sg

log = logging.getLogger(__name__)


def load_raster_image(image_loc: str, width: int) -> pg.Surface:
    """
    Loads raster images (e.g., BMP, JPG, PNG) for use in `pygame`.

    Parameters
    ----------
    image_loc
        Location of image file.
    width
        Required width in pixels of image when loaded.

    Returns
    -------
    pg.Surface
        Image loaded for use in `pygame`.
    """
    try:
        log.info("Loading %s...", image_loc)
        image = pg.image.load(image_loc)

        if width > 0:
            width_old, height_old = image.get_size()
            height = width / (width_old / height_old)
            log.info("Scaling image from (%s,%s) to (%s,%s)", width_old, height_old, width, height)
            return pg.transform.scale(image, (width, height))

        log.info("No scaling required")
        return image

    except FileNotFoundError:
        log.exception("%s not found", image_loc)


def load_svg_image(image_loc: str, width: int) -> pg.Surface:
    """
    Loads SVG images for use in `pygame`.

    Parameters
    ----------
    image_loc
        Location of image file.
    width
        Required width in pixels of image when loaded.

    Returns
    -------
    pg.Surface
        Image loaded for use in `pygame`.
    """
    try:
        log.info("Loading %s...", image_loc)
        image = sg.fromfile(str(image_loc))
        view_box = image.root.attrib["viewBox"]
        width_old, height_old = tuple(int(float(number)) for number in view_box.split(" ")[2:])
        height = int(width / (width_old / height_old))
        log.info("Scaling image from (%s,%s) to (%s,%s)", width_old, height_old, width, height)
        image.set_size((str(width), str(height)))
        image_str = image.to_str()

        return pg.image.load(BytesIO(cairosvg.svg2png(image_str)))

    except FileNotFoundError:
        log.exception("%s not found", image_loc)


class ImageLoader:
    """
    Loads images for use in `pygame`.

    Methods
    -------
    register_loader
        Add reference to class dictionary to image loading function.
    load_image
        Return a loaded image as a `pygame` Surface.
    """

    _loaders: dict = {}

    @classmethod
    def register_loader(cls, image_format, loader) -> None:
        """Add image loader to class dictionary."""
        cls._loaders[image_format] = loader

    def load_image(self, image_loc: str, width: int) -> pg.Surface:
        """
        Load the image from location at specified width, dependent on file type.

        Returns
        -------
        pg.Surface
            Image loaded as `pygame` Surface.
        """
        loader = self._loaders.get(Path(image_loc).suffix, load_raster_image)

        return loader(image_loc, width)


ImageLoader.register_loader(".svg", load_svg_image)
