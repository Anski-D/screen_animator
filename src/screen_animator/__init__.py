from pathlib import Path
import pygame as pg
import importlib.resources
import shutil
from .item_groups import (
    LeftScrollingTextGroup,
    ColorChangeGroup,
    TimedRandomImagesGroup,
    FpsCounterGroup,
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
        flipped=False,
        fps_on=False,
        debug=False,
    ) -> None:
        self._settings_file = input_file
        self._display_size = display_size
        self._flipped = flipped
        if fps_on:
            self._fps_on()
        if debug:
            self._debug_setup()

    def run(self) -> None:
        pg.init()
        settings_manager = SettingsManager(SettingsImporter(), self._settings_file)
        model = Model(settings_manager, self._item_groups)
        controller = Controller(
            settings_manager, model, self._display_size, self._flipped
        )
        controller.init()
        controller.run()

    def _debug_setup(self) -> None:
        self._display_size = (800, 480)
        self._fps_on()

    def _fps_on(self) -> None:
        if FpsCounterGroup not in self._item_groups:
            self._item_groups.append(FpsCounterGroup)


def copy_examples():
    for file in example_files:
        path = importlib.resources.path(example, file)
        with path as p:
            shutil.copy2(p, p.name)
