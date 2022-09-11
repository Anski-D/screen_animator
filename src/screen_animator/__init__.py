from pathlib import Path
import pygame as pg
import importlib.resources
import shutil
from .item_groups import (
    LeftScrollingTextGroup,
    ColorChangeGroup,
    TimedRandomImagesGroup,
)
from .settings import SettingsManager, SettingsImporter
from .model import Model
from .controller import Controller
import example

__version__ = "0.1.0"

item_groups = [ColorChangeGroup, TimedRandomImagesGroup, LeftScrollingTextGroup]
example_files = ["inputs.toml", "script.py"]


class ScreenAnimator:
    _item_groups = item_groups

    def __init__(
        self,
        input_file: str | Path = "inputs.toml",
        display_size: tuple[int, int] = None,
        debug=False,
    ) -> None:
        self._settings_file = input_file
        self._display_size = display_size
        if debug:
            self._debug_setup()

    def run(self) -> None:
        pg.init()
        settings_manager = SettingsManager(SettingsImporter(), self._settings_file)
        model = Model(settings_manager, self._item_groups)
        controller = Controller(settings_manager, model, self._display_size)
        controller.init()
        controller.run()

    def _debug_setup(self) -> None:
        self._display_size = (800, 480)


def copy_examples():
    for file in example_files:
        path = importlib.resources.path(example, file)
        with path as p:
            shutil.copy2(p, p.name)
