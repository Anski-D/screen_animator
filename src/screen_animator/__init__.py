import importlib.resources
import shutil
from functools import partial
import argparse
from pathlib import Path
import logging
from collections.abc import Sequence, Iterable, Iterator

import pygame as pg

from screen_animator.listener import Listener
from screen_animator.log_setup import setup_logging
from screen_animator.controller import Controller, EventManager, QuitEvent
from screen_animator.item_groups import (
    ItemGroup,
    TimedItemGroup,
    LeftScrollingTextItemGroup,
    ColorChangeItemGroup,
    RandomImagesItemGroup,
    FpsCounterItemGroup,
)
from screen_animator.image_loading import ImageLoader, SvgTypeImageLoader
from screen_animator.model import Model
from screen_animator.settings import SettingsManager
from screen_animator.view import View

log = logging.getLogger(__name__)

DEBUG_DISPLAY_SIZE = 800, 400
ITEM_GROUP_TYPES = [
    partial(TimedItemGroup, wrapped_group=ColorChangeItemGroup),
    partial(TimedItemGroup, wrapped_group=RandomImagesItemGroup),
    LeftScrollingTextItemGroup,
]
EVENT_TYPES = [pg.QUIT, (pg.KEYDOWN, pg.K_q)]


def copy_examples() -> None:
    """Copies `example` files to working directory."""
    for file_path in importlib.resources.files(example).iterdir():
        shutil.copy2(str(file_path), file_path.name)


def _parse_args() -> argparse.Namespace:
    """Processes the command line arguments provided."""
    parser = argparse.ArgumentParser(
        prog="ScreenAnimator",
        description="A Python app to generate animated messages and images on a screen, with a focus on the Raspberry Pi.",
    )
    parser.add_argument(
        "-i",
        "--input",
        default="inputs.toml",
        help="path to TOML file with inputs (optional, falls back to `inputs.toml` by default)",
    )
    parser.add_argument(
        "-r",
        "--rotate",
        action="store_true",
        help="rotate rendered output by 180 degrees (optional, disabled by default)",
    )
    parser.add_argument(
        "-f",
        "--fps",
        action="store_true",
        help="turn on FPS counter (optional, off by default, forced on if debug mode used)",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="turns on debug mode which limits output to windowed mode and renders FPS counter (optional, off by default)",
    )
    parser.add_argument(
        "-l",
        "--logging",
        default="",
        help="activates logging and sets logging level (off by default, writes to log file when on)",
    )

    args = parser.parse_args()
    args.fps = args.debug if args.debug else args.fps

    return args


def _set_display_size(display_size: Sequence[float] | None = None) -> pg.Surface:
    if display_size is None:
        return pg.display.set_mode((0, 0), pg.FULLSCREEN)

    return pg.display.set_mode(display_size)


def _create_settings_manager(settings_file: str | Path) -> SettingsManager:
    settings_manager = SettingsManager(settings_file)
    settings_manager.setup_settings()

    return settings_manager


def _create_event_manager(event_types: Sequence[tuple[int, int] | int], listeners: Sequence[Listener]) -> EventManager:
    event_manager = EventManager()
    for event_type, listener in zip(event_types, listeners):
        event_manager.register_listener(listener, event_type)

    return event_manager


class ScreenAnimator:
    """
    Bring together models of `screen_animator` and run.

    Methods
    -------
    register_item_group
        Add `ItemGroup` to class list.
    run
        Run `screen_animator`.
    """

    _item_groups: list[type[ItemGroup]] = []

    def __init__(
        self,
        input_file: str | Path = "inputs.toml",
        display_size: tuple[int, int] | None = None,
        rotated: bool = False,
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
        rotated : optional
            Rotate display 180 degrees (default is False).
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
        self.rotated = rotated
        log.info("Output will be rotated 180 degrees: %s", self.rotated)
        self._is_fps_on = fps_on
        if self._is_fps_on:
            self._fps_on()
        self._debug = debug
        if self._debug:
            self._debug_setup()
        log.info("Creating %s", self)

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"{self._settings_file},"
            f" {self._display_size},"
            f" {self.rotated},"
            f" {self._is_fps_on},"
            f" {self._debug})"
        )

    @classmethod
    def register_item_group(cls, item_group: type[ItemGroup]) -> None:
        """Add `ItemGroup` to class list."""
        cls._item_groups.append(item_group)

    def run(self) -> None:
        """Run `screen_animator`."""
        log.info("Creating key components of %s", type(self).__name__)
        pg.init()  # pylint: disable=no-member
        settings_manager = SettingsManager(self._settings_file)
        settings_manager.setup_settings()
        model = Model(settings_manager, self._item_groups)
        controller = Controller(settings_manager, model, self.rotated)
        controller.init(self._display_size)
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
        if FpsCounterItemGroup not in self._item_groups:
            self._item_groups.append(FpsCounterItemGroup)


def main() -> None:
    """Main app function to run."""
    pg.init()
    args = _parse_args()
    setup_logging(args.logging)

    ImageLoader.register_loader(".svg", SvgTypeImageLoader)

    item_group_types = ITEM_GROUP_TYPES + [FpsCounterItemGroup] if args.fps else ITEM_GROUP_TYPES

    display = _set_display_size(DEBUG_DISPLAY_SIZE if args.debug else None)
    settings_manager = _create_settings_manager(args.input)
    model = Model(settings_manager, item_group_types, display.get_rect())
    view = View(model, display, settings_manager.settings, args.rotate)

    event_types = EVENT_TYPES + [model.update_event_type]
    listeners = [quit_event := QuitEvent(), quit_event, view]
    event_manager = _create_event_manager(event_types, listeners)

    screen_animator = Controller(settings_manager, model, args.rotate)

    screen_animator.run()


if __name__ == "__main__":
    main()
