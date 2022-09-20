import numpy as np
from PIL import Image

g_scale = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "


class Converter:
    def __init__(self, image_file: str) -> None:
        pass

    def calculate_lum(self, image: Image) -> float:
        im = np.array(image)
        return np.average(im)
