from pathlib import Path
import importlib.resources
import shutil
import pygame as pg
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

    _item_groups = item_groups

    def __init__(
        self,
        input_file: str | Path = "inputs.toml",
        display_size: tuple[int, int] = None,
        flipped=False,
        fps_on=False,
        debug=False,
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
        self._flipped = flipped
        if fps_on:
            self._fps_on()
        if debug:
            self._debug_setup()

    def run(self) -> None:
        """Run `screen_animator`."""
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


def copy_examples() -> None:
    """Copies example files to working directory."""
    for file in example_files:
        example_path = importlib.resources.path(example, file)
        with example_path as path:
            shutil.copy2(path, path.name)
