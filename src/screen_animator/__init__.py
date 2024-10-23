import importlib.resources
import shutil
from functools import partial
import argparse
from pathlib import Path
import logging
from collections.abc import Iterable

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


def _set_display_size(display_size: tuple[float, float] | None = None) -> pg.Surface:
    if display_size is None:
        return pg.display.set_mode((0, 0), pg.FULLSCREEN)

    return pg.display.set_mode(display_size)


def _create_settings_manager(settings_file: str | Path) -> SettingsManager:
    settings_manager = SettingsManager(settings_file)
    settings_manager.setup_settings()

    return settings_manager


def _create_event_manager(event_types: Iterable[tuple[int, int] | int], listeners: Iterable[Listener]) -> EventManager:
    event_manager = EventManager()
    for event_type, listener in zip(event_types, listeners):
        event_manager.register_listener(listener, event_type)

    return event_manager


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
    screen_animator = Controller(settings_manager.settings, model)
    listeners = [quit_event := QuitEvent([screen_animator]), quit_event, view]
    event_manager = _create_event_manager(event_types, listeners)

    screen_animator.run(event_manager)


if __name__ == "__main__":
    main()
