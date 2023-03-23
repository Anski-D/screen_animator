import logging
from pathlib import Path
import importlib.resources
import shutil

import pygame as pg

from .item_groups import (
    ItemGroup,
    LeftScrollingTextGroup,
    ColorChangeGroup,
    TimedRandomImagesGroup,
    FpsCounterGroup,
)
from .settings import SettingsManager, SettingsImporter
from .model import Model
from .controller import Controller
import example
from .image_loading import ImageLoader, load_svg_image

log = logging.getLogger(__name__)

ImageLoader.register_loader(".svg", load_svg_image)
item_groups = [ColorChangeGroup, TimedRandomImagesGroup, LeftScrollingTextGroup]
example_files = ["inputs.toml", "script.py"]


class ScreenAnimator:
    """
    Bring together models of `screen_animator` and run.

    Methods
    -------
    run
        Run `screen_animator`.
    """

    _item_groups: list[type[ItemGroup]] = item_groups

    def __init__(
        self,
        input_file: str | Path = "inputs.toml",
        display_size: tuple[int, int] = None,
        flipped: bool = False,
        fps_on: bool = False,
        debug: bool = False,
    ) -> None:
        """
        Perform setup of `screen_animator`.

        Parameters
        ----------
        input_file
            File with user settings, default is `inputs.toml` in working directory.
        display_size : optional
            User-defined screen size (default is None, full-screen).
        flipped : optional
            Flip display across the horizontal axis (default is False).
        fps_on
            FPS counter is on (default is False).
        debug
            Turns on debug model (default is False).
        """
        self._settings_file = input_file
        self._display_size = display_size
        log.info(
            "Display size set to: %s",
            "fullscreen" if self._display_size is None else self._display_size,
        )
        self._flipped = flipped
        log.info("Output will be flipped vertically: %s", self._flipped)
        self._is_fps_on = fps_on
        if self._is_fps_on:
            self._fps_on()
        self._debug = debug
        if self._debug:
            self._debug_setup()
        log.info("Creating %s", self)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self._settings_file}, {self._display_size}, {self._flipped}, {self._is_fps_on}, {self._debug})"

    def run(self) -> None:
        """Run `screen_animator`."""
        log.info("Creating key components of %s", type(self).__name__)
        pg.init()
        settings_manager = SettingsManager(SettingsImporter(), self._settings_file)
        model = Model(settings_manager, self._item_groups)
        controller = Controller(
            settings_manager, model, self._display_size, self._flipped
        )
        controller.init()
        log.info("Setting %s to run", type(self).__name__)
        controller.run()
        log.info("Run method complete, %s stopping", type(self).__name__)

    def _debug_setup(self) -> None:
        log.info("Debug mode enabled")
        self._display_size = (800, 480)
        log.info("Display size changed to: %s", self._display_size)
        self._fps_on()

    def _fps_on(self) -> None:
        log.info("FPS will be displayed")
        if FpsCounterGroup not in self._item_groups:
            self._item_groups.append(FpsCounterGroup)


def copy_examples() -> None:
    """Copies example files to working directory."""
    for file in example_files:
        example_path = importlib.resources.path(example, file)
        with example_path as path:
            shutil.copy2(path, path.name)
