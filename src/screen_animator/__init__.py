import logging
import importlib.resources
import shutil
from functools import partial

import example
from .screen_animator import ScreenAnimator
from .item_groups import (
    ItemGroup,
    TimedItemGroup,
    LeftScrollingTextItemGroup,
    ColorChangeItemGroup,
    RandomImagesItemGroup,
    FpsCounterItemGroup,
)
from .image_loading import ImageLoader, SvgTypeImageLoader

log = logging.getLogger(__name__)


def copy_examples() -> None:
    """Copies example files to working directory."""
    for file in example_files:
        example_path = importlib.resources.path(example, file)
        with example_path as path:
            shutil.copy2(path, path.name)


ImageLoader.register_loader(".svg", SvgTypeImageLoader)

item_groups = [
    partial(TimedItemGroup, wrapped_group=ColorChangeItemGroup),
    partial(TimedItemGroup, wrapped_group=RandomImagesItemGroup),
    LeftScrollingTextItemGroup,
]
for item_group in item_groups:
    ScreenAnimator.register_item_group(item_group)

example_files = ["inputs.toml", "script.py"]
