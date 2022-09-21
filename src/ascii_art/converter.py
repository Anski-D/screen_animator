import numpy as np
from PIL import Image

g_scale = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "


class Converter:
    def __init__(self, image_file: str, cols: int = 150, scale: float = 0.5) -> None:
        self._image = Image.open(image_file).convert("L")
        self._cols = cols
        self._scale = scale
        self._calc_sizes()
        self._ascii_image = [""]

    def convert_to_ascii(self) -> list[str]:
        ascii_image = []

        for row_idx in range(self._rows):
            y_1 = int(row_idx * self._tile_height)
            y_2 = int((row_idx + 1) * self._tile_height)
            ascii_image.append("")

            for col_idx in range(self._cols):
                x_1 = int(col_idx * self._tile_width)
                x_2 = int((col_idx + 1) * self._tile_width)

                tile_image = self._image.crop((x_1, y_1, x_2, y_2))
                lum = self._calculate_lum(tile_image)
                g_scale_idx = int(lum / 255 * (len(g_scale) - 1))
                ascii_image[row_idx] += g_scale[g_scale_idx]

        self._ascii_image = ascii_image

        return self._ascii_image

    def print_ascii_image(self) -> None:
        for line in self._ascii_image:
            print(line)

    def _calc_sizes(self) -> None:
        self._image_width, self._image_height = self._image.size
        self._tile_width = self._image_width / self._cols
        self._tile_height = self._tile_width / self._scale
        self._rows = int(self._image_height / self._tile_height)

    def _calculate_lum(self, image: Image) -> float:
        im = np.array(image)
        return np.average(im)
