from pathlib import Path
import pygame as pg
from .item_groups import LeftScrollingTextGroup, ColorChangeGroup, TimedRandomImagesGroup
from .settings import SettingsManager, SettingsImporter
from .model import Model
from .controller import Controller

__version__ = "0.1.0"

item_groups = [LeftScrollingTextGroup, ColorChangeGroup, TimedRandomImagesGroup]


class ScreenAnimator:
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
        model = Model(settings_manager, item_groups)
        controller = Controller(settings_manager, model, self._display_size)
        controller.init()
        controller.run()

    def _debug_setup(self) -> None:
        self._display_size = (800, 600)
