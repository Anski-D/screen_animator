from io import BytesIO
from pathlib import Path
import logging

import cairosvg
import pygame as pg
from svgutils import transform as sg

log = logging.getLogger(__name__)


def load_raster_image(image_loc: str, width: int) -> pg.Surface:
    try:
        image = pg.image.load(image_loc)

        if width > 0:
            width_old, height_old = image.get_size()
            return pg.transform.scale(image, (width, width / (width_old / height_old)))
        else:
            return image

    except FileNotFoundError:
        log.exception("%s not found", image_loc)


def load_svg_image(image_loc: str, width: int) -> pg.Surface:
    try:
        image = sg.fromfile(str(image_loc))
        view_box = image.root.attrib["viewBox"]
        width_old, height_old = tuple(
            int(number)
            for number
            in view_box.split(" ")[2:]
        )
        image.set_size((str(width), str(int(width / (width_old / height_old)))))
        image_str = image.to_str()

        return pg.image.load(BytesIO(cairosvg.svg2png(image_str)))

    except FileNotFoundError:
        log.exception("%s not found", image_loc)


class ImageLoader:
    _loaders = {}

    @classmethod
    def register_loader(cls, image_format, loader):
        cls._loaders[image_format] = loader

    def load_image(self, image_loc: str, width: int) -> pg.Surface:
        loader = self._loaders.get(Path(image_loc).suffix, load_raster_image)
        return loader(image_loc, width)


ImageLoader.register_loader(".svg", load_svg_image)
